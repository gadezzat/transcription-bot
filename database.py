import sqlite3
import logging
from datetime import datetime, timedelta
from contextlib import contextmanager
import secrets
from config import DATABASE_NAME, PLAN_CONFIG, REFERRAL_BONUS_MINUTES

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_name=DATABASE_NAME):
        self.db_name = db_name
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    language_code TEXT,
                    referral_code TEXT UNIQUE,
                    referred_by INTEGER,
                    total_referrals INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    interface_lang TEXT DEFAULT 'ar',
                    transcribe_lang TEXT DEFAULT 'auto',
                    task_type TEXT DEFAULT 'transcribe',
                    export_format TEXT DEFAULT 'txt',
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_quota (
                    user_id INTEGER PRIMARY KEY,
                    plan_type TEXT DEFAULT 'free',
                    minutes_used REAL DEFAULT 0,
                    minutes_limit INTEGER DEFAULT 5,
                    bonus_minutes REAL DEFAULT 0,
                    last_reset TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    subscription_start TIMESTAMP,
                    subscription_end TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    file_type TEXT,
                    file_size INTEGER,
                    duration_seconds REAL,
                    processing_time REAL,
                    language TEXT,
                    task_type TEXT,
                    characters_count INTEGER,
                    words_count INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    plan_type TEXT,
                    amount REAL,
                    currency TEXT,
                    status TEXT DEFAULT 'pending',
                    payment_method TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    verified_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')
            
            logger.info("Database initialized successfully")
    
    def add_user(self, user_id, username, first_name, last_name, language_code, referral_code=None):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE users SET last_active = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (user_id,))
                return False
            
            user_referral_code = secrets.token_urlsafe(8)
            referred_by_id = None
            
            if referral_code:
                cursor.execute('SELECT user_id FROM users WHERE referral_code = ?', (referral_code,))
                referrer = cursor.fetchone()
                if referrer:
                    referred_by_id = referrer['user_id']
                    cursor.execute('''
                        UPDATE users SET total_referrals = total_referrals + 1
                        WHERE user_id = ?
                    ''', (referred_by_id,))
                    cursor.execute('''
                        UPDATE user_quota SET bonus_minutes = bonus_minutes + ?
                        WHERE user_id = ?
                    ''', (REFERRAL_BONUS_MINUTES, referred_by_id))
            
            cursor.execute('''
                INSERT INTO users (user_id, username, first_name, last_name, language_code, referral_code, referred_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, language_code, user_referral_code, referred_by_id))
            
            cursor.execute('''
                INSERT INTO user_settings (user_id, interface_lang)
                VALUES (?, ?)
            ''', (user_id, 'ar' if language_code == 'ar' else 'en'))
            
            cursor.execute('''
                INSERT INTO user_quota (user_id, plan_type, minutes_limit)
                VALUES (?, 'free', 5)
            ''', (user_id,))
            
            logger.info(f"New user added: {user_id}")
            return True
    
    def get_user_settings(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_settings WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                return dict(result)
            return {
                'interface_lang': 'ar',
                'transcribe_lang': 'auto',
                'task_type': 'transcribe',
                'export_format': 'txt'
            }
    
    def update_setting(self, user_id, setting_name, value):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''
                UPDATE user_settings SET {setting_name} = ?
                WHERE user_id = ?
            ''', (value, user_id))
    
    def get_user_quota(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM user_quota WHERE user_id = ?', (user_id,))
            result = cursor.fetchone()
            if result:
                quota = dict(result)
                plan_config = PLAN_CONFIG[quota['plan_type']]
                if plan_config['is_daily']:
                    last_reset = datetime.fromisoformat(quota['last_reset'])
                    if datetime.now().date() > last_reset.date():
                        self.reset_daily_quota(user_id)
                        quota['minutes_used'] = 0
                return quota
            return None
    
    def reset_daily_quota(self, user_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_quota 
                SET minutes_used = 0, last_reset = CURRENT_TIMESTAMP
                WHERE user_id = ?
            ''', (user_id,))
    
    def can_use_service(self, user_id, duration_minutes):
        quota = self.get_user_quota(user_id)
        if not quota:
            return False, "No quota found"
        
        if quota['minutes_limit'] == -1:
            return True, "Unlimited"
        
        total_available = quota['minutes_limit'] + quota['bonus_minutes']
        if quota['minutes_used'] + duration_minutes <= total_available:
            return True, "OK"
        
        return False, "Quota exceeded"
    
    def update_usage(self, user_id, duration_minutes):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE user_quota 
                SET minutes_used = minutes_used + ?
                WHERE user_id = ?
            ''', (duration_minutes, user_id))
    
    def add_usage_stat(self, user_id, file_type, file_size, duration_seconds, 
                      processing_time, language, task_type, characters_count, words_count):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usage_stats 
                (user_id, file_type, file_size, duration_seconds, processing_time, 
                 language, task_
