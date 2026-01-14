
import os
from dotenv import load_dotenv

load_dotenv()

# Bot Settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
ADMIN_IDS = [int(id.strip()) for id in os.getenv('ADMIN_IDS', '').split(',') if id.strip()]

# Database
DATABASE_NAME = 'transcription_bot.db'

# File Settings
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
TEMP_FOLDER = 'temp_files'

# Whisper Models
WHISPER_MODELS = {
    'free': 'base',
    'basic': 'medium',
    'pro': 'large-v2',
    'business': 'large-v3'
}

# Plan Configuration
PLAN_CONFIG = {
    'free': {
        'minutes_limit': 5,
        'is_daily': True,
        'model': 'base',
        'export_formats': ['txt', 'srt'],
        'badge': '🆓',
        'priority': 0
    },
    'basic': {
        'minutes_limit': 180,
        'is_daily': False,
        'model': 'medium',
        'export_formats': ['txt', 'srt'],
        'badge': '⭐',
        'priority': 1
    },
    'pro': {
        'minutes_limit': 600,
        'is_daily': False,
        'model': 'large-v2',
        'export_formats': ['txt', 'srt', 'pdf', 'docx'],
        'badge': '💎',
        'priority': 2
    },
    'business': {
        'minutes_limit': -1,
        'is_daily': False,
        'model': 'large-v3',
        'export_formats': ['txt', 'srt', 'pdf', 'docx', 'vtt'],
        'badge': '👑',
        'priority': 3
    }
}

# Bank Details
BANK_DETAILS = {
    'bank_name_ar': 'البنك الأهلي المصري',
    'bank_name_en': 'National Bank of Egypt',
    'account_name': os.getenv('BANK_ACCOUNT_NAME', 'اسمك الكامل'),
    'account_number': os.getenv('BANK_ACCOUNT_NUMBER', '1234567890123456'),
    'iban': os.getenv('BANK_IBAN', 'EG380002000112345678901234567890'),
    'swift_code': 'NBEGEGCX',
    'branch_ar': 'فرع المعادي - القاهرة',
    'branch_en': 'Maadi Branch - Cairo',
    'whatsapp': os.getenv('WHATSAPP_NUMBER', '+201234567890'),
}

# Exchange Rate
EXCHANGE_RATE = float(os.getenv('EXCHANGE_RATE', '31.2'))

# Bot Username
BOT_USERNAME = os.getenv('BOT_USERNAME', 'YourBotUsername')

# Other Settings
REFERRAL_BONUS_MINUTES = 30
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
