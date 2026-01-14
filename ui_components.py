from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

class UIComponents:
    """UI Components - Keyboards and Buttons"""
    
    @staticmethod
    def create_main_keyboard(lang='ar'):
        """Main keyboard"""
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        
        if lang == 'ar':
            markup.add(
                KeyboardButton('🎙️ تفريغ صوتي'),
                KeyboardButton('📊 إحصائياتي'),
                KeyboardButton('⚙️ الإعدادات'),
                KeyboardButton('💎 الاشتراكات'),
                KeyboardButton('ℹ️ المساعدة'),
                KeyboardButton('🎁 إحالة صديق'),
                KeyboardButton('🌐 تغيير اللغة')
            )
        else:
            markup.add(
                KeyboardButton('🎙️ Transcribe'),
                KeyboardButton('📊 My Stats'),
                KeyboardButton('⚙️ Settings'),
                KeyboardButton('💎 Pricing'),
                KeyboardButton('ℹ️ Help'),
                KeyboardButton('🎁 Refer Friend'),
                KeyboardButton('🌐 Change Language')
            )
        
        return markup
    
    @staticmethod
    def create_settings_keyboard(lang='ar'):
        """Settings keyboard"""
        markup = InlineKeyboardMarkup(row_width=1)
        
        if lang == 'ar':
            markup.add(
                InlineKeyboardButton('🌍 تغيير لغة الواجهة', callback_data='set_interface_lang'),
                InlineKeyboardButton('🎯 تغيير لغة التفريغ', callback_data='set_transcribe_lang'),
                InlineKeyboardButton('📝 تغيير نوع المهمة', callback_data='set_task_type'),
                InlineKeyboardButton('📄 تغيير صيغة التصدير', callback_data='set_export_format'),
                InlineKeyboardButton('🔙 رجوع', callback_data='main_menu')
            )
        else:
            markup.add(
                InlineKeyboardButton('🌍 Change Interface Language', callback_data='set_interface_lang'),
                InlineKeyboardButton('🎯 Change Transcription Language', callback_data='set_transcribe_lang'),
                InlineKeyboardButton('📝 Change Task Type', callback_data='set_task_type'),
                InlineKeyboardButton('📄 Change Export Format', callback_data='set_export_format'),
                InlineKeyboardButton('🔙 Back', callback_data='main_menu')
            )
        
        return markup
    
    @staticmethod
    def create_language_selection_keyboard(current_lang='ar'):
        """Language selection keyboard"""
        markup = InlineKeyboardMarkup(row_width=2)
        
        markup.add(
            InlineKeyboardButton('🇸🇦 العربية', callback_data='lang_ar'),
            InlineKeyboardButton('🇺🇸 English', callback_data='lang_en')
        )
        
        back_text = '🔙 رجوع' if current_lang == 'ar' else '🔙 Back'
        markup.add(InlineKeyboardButton(back_text, callback_data='settings'))
        
        return markup
    
    @staticmethod
    def create_transcribe_lang_keyboard(lang='ar'):
        """Transcription language selection keyboard"""
        markup = InlineKeyboardMarkup(row_width=2)
        
        auto_text = '🌐 كشف تلقائي' if lang == 'ar' else '🌐 Auto Detect'
        markup.add(InlineKeyboardButton(auto_text, callback_data='tlang_auto'))
        
        markup.add(
            InlineKeyboardButton('🇸🇦 العربية', callback_data='tlang_ar'),
            InlineKeyboardButton('🇺🇸 English', callback_data='tlang_en'),
            InlineKeyboardButton('🇪🇸 Español', callback_data='tlang_es'),
            InlineKeyboardButton('🇫🇷 Français', callback_data='tlang_fr'),
            InlineKeyboardButton('🇩🇪 Deutsch', callback_data='tlang_de'),
            InlineKeyboardButton('🇮🇹 Italiano', callback_data='tlang_it'),
            InlineKeyboardButton('🇷🇺 Русский', callback_data='tlang_ru'),
            InlineKeyboardButton('🇨🇳 中文', callback_data='tlang_zh')
        )
        
        back_text = '🔙 رجوع' if lang == 'ar' else '🔙 Back'
        markup.add(InlineKeyboardButton(back_text, callback_data='settings'))
        
        return markup
    
    @staticmethod
    def create_progress_bar(current, total, length=10):
        """Create progress bar"""
        if total == -1:
            return '∞ غير محدود'
        
        if total == 0:
            return '░' * length + ' 0%'
        
        percentage = min(current / total, 1.0)
        filled = int(percentage * length)
        empty = length - filled
        
        bar = '█' * filled + '░' * empty
        return f'{bar} {percentage*100:.0f}%'
    
    @staticmethod
    def format_duration(seconds):
        """Format duration"""
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f'{minutes}:{secs:02d}'
