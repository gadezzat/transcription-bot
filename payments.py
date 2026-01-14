from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BANK_DETAILS, EXCHANGE_RATE, BOT_USERNAME
import logging

logger = logging.getLogger(__name__)

class PaymentHandler:
    """Payment Handler"""
    
    def __init__(self, bot, db):
        self.bot = bot
        self.db = db
        
        self.plans = {
            'basic': {
                'name_ar': '⭐ الخطة الأساسية',
                'name_en': '⭐ Basic Plan',
                'price_usd': 4.99,
                'duration_days': 30,
                'minutes': 180,
            },
            'pro': {
                'name_ar': '💎 الخطة الاحترافية',
                'name_en': '💎 Pro Plan',
                'price_usd': 12.99,
                'duration_days': 30,
                'minutes': 600,
            },
            'business': {
                'name_ar': '👑 خطة الأعمال',
                'name_en': '👑 Business Plan',
                'price_usd': 29.99,
                'duration_days': 30,
                'minutes': -1,
            }
        }
    
    def get_price_egp(self, price_usd):
        """Calculate price in EGP"""
        return round(price_usd * EXCHANGE_RATE, 2)
    
    def get_currency_keyboard(self, plan_id, lang='ar'):
        """Currency selection keyboard"""
        plan = self.plans[plan_id]
        markup = InlineKeyboardMarkup(row_width=1)
        
        price_egp = self.get_price_egp(plan['price_usd'])
        
        if lang == 'ar':
            markup.add(
                InlineKeyboardButton(
                    f'💵 {price_egp} جنيه مصري',
                    callback_data=f'pay_{plan_id}_EGP'
                ),
                InlineKeyboardButton(
                    f'💵 ${plan["price_usd"]} دولار',
                    callback_data=f'pay_{plan_id}_USD'
                ),
                InlineKeyboardButton('🔙 رجوع', callback_data='pricing')
            )
        else:
            markup.add(
                InlineKeyboardButton(
                    f'💵 {price_egp} EGP',
                    callback_data=f'pay_{plan_id}_EGP'
                ),
                InlineKeyboardButton(
                    f'💵 ${plan["price_usd"]} USD',
                    callback_data=f'pay_{plan_id}_USD'
                ),
                InlineKeyboardButton('🔙 Back', callback_data='pricing')
            )
        
        return markup
    
    def get_payment_instructions(self, plan_id, currency, user_id, username, lang='ar'):
        """Payment instructions"""
        plan = self.plans[plan_id]
        amount = self.get_price_egp(plan['price_usd']) if currency == 'EGP' else plan['price_usd']
        plan_name = plan['name_ar'] if lang == 'ar' else plan['name_en']
        user_name = username or str(user_id)
        
        if lang == 'ar':
            instructions = f'''💳 **بيانات الحساب البنكي**

🏦 البنك: {BANK_DETAILS['bank_name_ar']}
👤 المستفيد: {BANK_DETAILS['account_name']}
💳 رقم الحساب: `{BANK_DETAILS['account_number']}`
🌍 IBAN: `{BANK_DETAILS['iban']}`

💰 المبلغ: {amount} {currency}
📋 الخطة: {plan_name}

📱 للتأكيد، تواصل عبر:
{BANK_DETAILS['whatsapp']}'''
        else:
            instructions = f'''💳 **Bank Account Details**

🏦 Bank: {BANK_DETAILS['bank_name_en']}
👤 Name: {BANK_DETAILS['account_name']}
💳 Account: `{BANK_DETAILS['account_number']}`
🌍 IBAN: `{BANK_DETAILS['iban']}`

💰 Amount: {amount} {currency}
📋 Plan: {plan_name}

📱 For confirmation, contact:
{BANK_DETAILS['whatsapp']}'''
        
        return instructions
