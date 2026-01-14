#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from datetime import datetime

from telebot import TeleBot
from telebot.types import Message, CallbackQuery

from config import *
from database import Database
from language_manager import LanguageManager
from payments import PaymentHandler
from ui_components import UIComponents
from transcription import TranscriptionService

# Setup Logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Initialize components
bot = TeleBot(BOT_TOKEN, parse_mode='Markdown')
db = Database(DATABASE_NAME)
lang_manager = LanguageManager()
payments = PaymentHandler(bot, db)
ui = UIComponents()
transcription_service = TranscriptionService(bot)


# ================== Command Handlers ==================

@bot.message_handler(commands=['start'])
def start_command(message: Message):
    """Start command handler"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    language_code = message.from_user.language_code
    
    referral_code = None
    if len(message.text.split()) > 1:
        referral_code = message.text.split()[1]
    
    db.add_user(user_id, username, first_name, last_name, language_code, referral_code)
    
    settings = db.get_user_settings(user_id)
    user_lang = settings.get('interface_lang', 'ar')
    
    welcome_text = lang_manager.get(
        'welcome_message',
        user_lang,
        name=first_name or username or 'المستخدم'
    )
    
    bot.send_message(
        message.chat.id,
        welcome_text,
        reply_markup=ui.create_main_keyboard(user_lang)
    )
    
    logger.info(f"User {user_id} started the bot")


@bot.message_handler(func=lambda m: m.text in ['🎙️ تفريغ صوتي', '🎙️ Transcribe'])
def transcribe_button(message: Message):
    """Transcribe button"""
    user_id = message.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    text = lang_manager.get('send_audio', lang)
    bot.send_message(message.chat.id, text)


@bot.message_handler(func=lambda m: m.text in ['📊 إحصائياتي', '📊 My Stats'])
def stats_button(message: Message):
    """Stats button"""
    user_id = message.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    quota = db.get_user_quota(user_id)
    stats = db.get_user_statistics(user_id)
    plan = quota['plan_type']
    badge = PLAN_CONFIG[plan]['badge']
    
    if quota['minutes_limit'] == -1:
        remaining = '∞'
    else:
        remaining = f"{(quota['minutes_limit'] + quota['bonus_minutes'] - quota['minutes_used']):.1f}"
    
    progress_bar = ui.create_progress_bar(
        quota['minutes_used'],
        quota['minutes_limit'] if quota['minutes_limit'] != -1 else 100
    )
    
    stats_text = lang_manager.get(
        'stats_content',
        lang,
        plan=plan,
        badge=badge,
        progress_bar=progress_bar,
        used=quota['minutes_used'],
        remaining=remaining,
        total_requests=stats.get('total_requests', 0),
        total_minutes=stats.get('total_minutes', 0) or 0,
        total_chars=stats.get('total_characters', 0) or 0,
        member_since=stats.get('member_since', '')[:10]
    )
    
    bot.send_message(message.chat.id, lang_manager.get('stats_title', lang, badge=badge) + '\n\n' + stats_text)


@bot.message_handler(func=lambda m: m.text in ['⚙️ الإعدادات', '⚙️ Settings'])
def settings_button(message: Message):
    """Settings button"""
    user_id = message.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    settings_text = lang_manager.get(
        'settings_content',
        lang,
        interface_lang=lang_manager.get_language_name(settings['interface_lang']),
        transcribe_lang=lang_manager.get_language_name(settings['transcribe_lang']),
        task_type=lang_manager.get('task_' + settings['task_type'], lang),
        export_format=settings['export_format'].upper()
    )
    
    bot.send_message(
        message.chat.id,
        lang_manager.get('settings_title', lang) + '\n\n' + settings_text,
        reply_markup=ui.create_settings_keyboard(lang)
    )


@bot.message_handler(func=lambda m: m.text in ['ℹ️ المساعدة', 'ℹ️ Help'])
def help_button(message: Message):
    """Help button"""
    user_id = message.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    help_text = lang_manager.get('help_content', lang)
    bot.send_message(message.chat.id, lang_manager.get('help_title', lang) + '\n\n' + help_text)


@bot.message_handler(func=lambda m: m.text in ['🌐 تغيير اللغة', '🌐 Change Language'])
def language_button(message: Message):
    """Language button"""
    user_id = message.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    text = lang_manager.get('select_interface_lang', lang)
    bot.send_message(
        message.chat.id,
        text,
        reply_markup=ui.create_language_selection_keyboard(lang)
    )


# ================== Callback Handlers ==================

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_selection(call: CallbackQuery):
    """Language selection"""
    new_lang = call.data.split('_')[1]
    user_id = call.from_user.id
    
    db.update_setting(user_id, 'interface_lang', new_lang)
    
    bot.answer_callback_query(call.id, lang_manager.get('lang_updated', new_lang))
    
    bot.send_message(
        call.message.chat.id,
        lang_manager.get('language_changed', new_lang),
        reply_markup=ui.create_main_keyboard(new_lang)
    )
    
    bot.delete_message(call.message.chat.id, call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == 'set_transcribe_lang')
def set_transcribe_lang(call: CallbackQuery):
    """Set transcription language"""
    user_id = call.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    text = lang_manager.get('select_transcribe_lang', lang)
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=ui.create_transcribe_lang_keyboard(lang)
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith('tlang_'))
def handle_transcribe_lang(call: CallbackQuery):
    """Handle transcription language"""
    new_lang = call.data.split('_')[1]
    user_id = call.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    db.update_setting(user_id, 'transcribe_lang', new_lang)
    
    bot.answer_callback_query(call.id, lang_manager.get('lang_updated', lang))
    bot.delete_message(call.message.chat.id, call.message.message_id)


# ================== Media Handlers ==================

@bot.message_handler(content_types=['voice', 'audio', 'video'])
def handle_media(message: Message):
    """Handle media files"""
    user_id = message.from_user.id
    settings = db.get_user_settings(user_id)
    lang = settings.get('interface_lang', 'ar')
    
    try:
        if message.content_type == 'voice':
            file_id = message.voice.file_id
            file_extension = 'ogg'
        elif message.content_type == 'audio':
            file_id = message.audio.file_id
            file_extension = 'mp3'
        elif message.content_type == 'video':
            file_id = message.video.file_id
            file_extension = 'mp4'
        
        processing_msg = bot.send_message(
            message.chat.id,
            lang_manager.get('processing', lang)
        )
        
        file_path, file_size = transcription_service.download_file(file_id, file_extension)
        
        if file_size > MAX_FILE_SIZE:
            bot.edit_message_text(
                lang_manager.get('file_too_large', lang),
                message.chat.id,
                processing_msg.message_id
            )
            transcription_service.cleanup_file(file_path)
            return
        
        duration = transcription_service.get_audio_duration(file_path)
        duration_minutes = duration / 60
        
        can_use, msg = db.can_use_service(user_id, duration_minutes)
        if not can_use:
            quota = db.get_user_quota(user_id)
            bot.edit_message_text(
                lang_manager.get('quota_exceeded', lang, used=quota['minutes_used'], limit=quota['minutes_limit']),
                message.chat.id,
                processing_msg.message_id
            )
            transcription_service.cleanup_file(file_path)
            return
        
        bot.edit_message_text(
            lang_manager.get('transcribing', lang),
            message.chat.id,
            processing_msg.message_id
        )
        
        quota = db.get_user_quota(user_id)
        plan = quota['plan_type']
        model = PLAN_CONFIG[plan]['model']
        
        transcribe_lang = settings['transcribe_lang'] if settings['transcribe_lang'] != 'auto' else 'auto'
        task_type = settings['task_type']
        
        result = transcription_service.transcribe_audio(
            file_path,
            language=transcribe_lang,
            task=task_type,
            model=model
        )
        
        db.update_usage(user_id, duration_minutes)
        
        db.add_usage_stat(
            user_id,
            file_type=message.content_type,
            file_size=file_size,
            duration_seconds=duration,
            processing_time=result['processing_time'],
            language=result['language'],
            task_type=task_type,
            characters_count=len(result['text']),
            words_count=len(result['text'].split())
        )
        
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
        quota = db.get_user_quota(user_id)
        remaining = '∞' if quota['minutes_limit'] == -1 else f"{(quota['minutes_limit'] + quota['bonus_minutes'] - quota['minutes_used']):.1f} دقيقة"
        
        result_text = f"{lang_manager.get('transcription_complete' if task_type == 'transcribe' else 'translation_complete', lang)}\n\n"
        result_text += f"**النص:**\n{result['text'][:1000]}\n\n"
        result_text += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        result_text += lang_manager.get(
            'result_info',
            lang,
            duration=f"{duration/60:.1f}",
            language=lang_manager.get_language_name(result['language']),
            chars=len(result['text']),
            processing_time=f"{result['processing_time']:.1f}",
            used=f"{duration_minutes:.1f}",
            remaining=remaining
        )
        
        if len(result_text) <= 4000:
            bot.send_message(message.chat.id, result_text, reply_to_message_id=message.message_id)
        else:
            txt_file = transcription_service.export_as_txt(result['text'])
            with open(txt_file, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=lang_manager.get('transcription_complete', lang))
            transcription_service.cleanup_file(txt_file)
        
        transcription_service.cleanup_file(file_path)
        
        logger.info(f"Transcription completed for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error handling media: {e}")
        bot.send_message(
            message.chat.id,
            lang_manager.get('error_occurred', lang, error=str(e))
        )


# ================== Run Bot ==================

def main():
    """Main function"""
    logger.info("Bot started successfully!")
    logger.info(f"Bot username: @{BOT_USERNAME}")
    
    bot.infinity_polling(timeout=60, long_polling_timeout=60)


if __name__ == '__main__':
    main()
