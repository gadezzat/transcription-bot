class LanguageManager:
    """Language management - Arabic and English"""
    
    def __init__(self):
        self.translations = {
            'ar': {
                'welcome_message': '''🎉 **مرحباً بك {name}!**

🎙️ أنا بوت التفريغ الصوتي الاحترافي

✨ **ماذا أستطيع أن أفعل؟**
• 🌍 تفريغ صوتي ل 98+ لغة
• ⚡ معالجة سريعة ودقيقة
• 📝 تصدير بصيغ متعددة
• 🌐 ترجمة تلقائية

🚀 **ابدأ الآن!**
أرسل لي تسجيل صوتي أو فيديو''',
                
                'btn_transcribe': '🎙️ تفريغ صوتي',
                'btn_my_stats': '📊 إحصائياتي',
                'btn_settings': '⚙️ الإعدادات',
                'btn_pricing': '💎 الاشتراكات',
                'btn_help': 'ℹ️ المساعدة',
                'btn_refer': '🎁 إحالة صديق',
                'btn_language': '🌐 تغيير اللغة',
                'btn_back': '🔙 رجوع',
                
                'settings_title': '⚙️ **الإعدادات الحالية**',
                'settings_content': '''🌍 لغة الواجهة: {interface_lang}
🎯 لغة التفريغ: {transcribe_lang}
📝 نوع المهمة: {task_type}
📄 صيغة التصدير: {export_format}''',
                
                'select_interface_lang': 'اختر لغة الواجهة:',
                'select_transcribe_lang': 'اختر لغة التفريغ:',
                'lang_updated': '✅ تم تحديث اللغة بنجاح',
                'auto_detect': '🌐 كشف تلقائي',
                
                'task_transcribe': '✍️ تفريغ صوتي',
                'task_translate': '🌐 ترجمة للإنجليزية',
                'task_updated': '✅ تم تحديث نوع المهمة',
                
                'format_txt': '📄 TXT - نص عادي',
                'format_srt': '🎬 SRT - ترجمة',
                'format_pdf': '📕 PDF - ملف PDF',
                'format_docx': '📘 DOCX - Word',
                'format_updated': '✅ تم تحديث صيغة التصدير',
                
                'pricing_title': '💎 **خطط الاشتراك**',
                'current_plan': '📌 خطتك: **{plan}** {badge}',
                
                'plan_free': '🆓 مجانية',
                'plan_basic': '⭐ أساسية',
                'plan_pro': '💎 احترافية',
                'plan_business': '👑 أعمال',
                
                'processing': '⏳ جاري المعالجة...',
                'downloading': '📥 جاري التحميل...',
                'transcribing': '🎯 جاري التفريغ الصوتي...',
                
                'transcription_complete': '✅ **اكتمل التفريغ!**',
                'translation_complete': '✅ **اكتملت الترجمة!**',
                
                'result_info': '''📊 **معلومات الملف:**
• المدة: {duration} دقيقة
• اللغة: {language}
• الأحرف: {chars:,}
• وقت المعالجة: {processing_time}ث

💎 استخدمت: {used} دقيقة
✨ متبقي: {remaining}''',
                
                'file_too_large': '❌ الملف كبير جداً! الحد الأقصى: 25MB',
                'invalid_file': '❌ صيغة ملف غير مدعومة',
                'quota_exceeded': '''⚠️ **نفذت حصتك!**

📊 استخدمت: {used} دقيقة
💎 الحد: {limit} دقيقة

🚀 ترقية خطتك للحصول على المزيد''',
                'error_occurred': '❌ حدث خطأ: {error}',
                
                'stats_title': '📊 **إحصائياتك** {badge}',
                'stats_content': '''**💎 الخطة: {plan}**

📈 **حصتك:**
{progress_bar}
📝 استخدمت: **{used:.1f}** دقيقة
✨ متبقي: **{remaining}** دقيقة

📊 **الإجمالي:**
🎯 الطلبات: **{total_requests}**
⏱️ الدقائق: **{total_minutes:.1f}**
📄 الأحرف: **{total_chars:,}**

📅 عضو منذ: {member_since}''',
                
                'help_title': '📖 **دليل الاستخدام**',
                'help_content': '''🎯 **كيفية الاستخدام:**

1️⃣ أرسل رسالة صوتية أو ملف
2️⃣ انتظر المعالجة
3️⃣ احصل على النص

🎬 **الملفات المدعومة:**
• صوت: MP3, WAV, OGG
• فيديو: MP4, MKV

📊 **صيغ التصدير:**
• TXT, SRT (مجاني)
• PDF, DOCX (احترافية+)''',
                
                'referral_title': '🎁 **برنامج الإحالة**',
                'referral_content': '''💰 **اربح دقائق مجانية!**

🎉 احصل على **30 دقيقة** لكل صديق!

**🔗 رابطك:**
`{link}`

**📊 إحصائياتك:**
• الإحالات: **{count}**
• المكتسب: **{bonus}** دقيقة''',
                
                'send_audio': '🎙️ أرسل ملف صوتي للتفريغ!',
                'language_changed': '✅ تم تغيير اللغة',
            },
            
            'en': {
                'welcome_message': '''🎉 **Welcome {name}!**

🎙️ Professional AI Transcription Bot

✨ **What can I do?**
• 🌍 Transcribe 98+ languages
• ⚡ Fast and accurate
• 📝 Multiple export formats
• 🌐 Auto-translate

🚀 **Get Started!**
Send me audio or video''',
                
                'btn_transcribe': '🎙️ Transcribe',
                'btn_my_stats': '📊 My Stats',
                'btn_settings': '⚙️ Settings',
                'btn_pricing': '💎 Pricing',
                'btn_help': 'ℹ️ Help',
                'btn_refer': '🎁 Refer Friend',
                'btn_language': '🌐 Language',
                'btn_back': '🔙 Back',
                
                'settings_title': '⚙️ **Settings**',
                'settings_content': '''🌍 Interface: {interface_lang}
🎯 Transcription: {transcribe_lang}
📝 Task: {task_type}
📄 Export: {export_format}''',
                
                'select_interface_lang': 'Choose interface language:',
                'select_transcribe_lang': 'Choose transcription language:',
                'lang_updated': '✅ Language updated',
                'auto_detect': '🌐 Auto Detect',
                
                'task_transcribe': '✍️ Transcription',
                'task_translate': '🌐 Translate to English',
                'task_updated': '✅ Task updated',
                
                'format_txt': '📄 TXT',
                'format_srt': '🎬 SRT',
                'format_pdf': '📕 PDF',
                'format_docx': '📘 DOCX',
                'format_updated': '✅ Format updated',
                
                'pricing_title': '💎 **Subscription Plans**',
                'current_plan': '📌 Your Plan: **{plan}** {badge}',
                
                'plan_free': '🆓 Free',
                'plan_basic': '⭐ Basic',
                'plan_pro': '💎 Pro',
                'plan_business': '👑 Business',
                
                'processing': '⏳ Processing...',
                'downloading': '📥 Downloading...',
                'transcribing': '🎯 Transcribing...',
                
                'transcription_complete': '✅ **Transcription Complete!**',
                'translation_complete': '✅ **Translation Complete!**',
                
                'result_info': '''📊 **File Info:**
• Duration: {duration} min
• Language: {language}
• Characters: {chars:,}
• Processing: {processing_time}s

💎 Used: {used} min
✨ Remaining: {remaining}''',
                
                'file_too_large': '❌ File too large! Max: 25MB',
                'invalid_file': '❌ Unsupported file format',
                'quota_exceeded': '''⚠️ **Quota Exceeded!**

📊 Used: {used} min
💎 Limit: {limit} min

🚀 Upgrade for more''',
                'error_occurred': '❌ Error: {error}',
                
                'stats_title': '📊 **Your Stats** {badge}',
                'stats_content': '''**💎 Plan: {plan}**

📈 **Quota:**
{progress_bar}
📝 Used: **{used:.1f}** min
✨ Remaining: **{remaining}** min

📊 **Total:**
🎯 Requests: **{total_requests}**
⏱️ Minutes: **{total_minutes:.1f}**
📄 Characters: **{total_chars:,}**

📅 Member since: {member_since}''',
                
                'help_title': '📖 **User Guide**',
                'help_content': '''🎯 **How to use:**

1️⃣ Send audio/video file
2️⃣ Wait for processing
3️⃣ Get transcription

🎬 **Supported:**
• Audio: MP3, WAV, OGG
• Video: MP4, MKV

📊 **Export:**
• TXT, SRT (free)
• PDF, DOCX (pro+)''',
                
                'referral_title': '🎁 **Referral Program**',
                'referral_content': '''💰 **Earn free minutes!**

🎉 Get **30 minutes** per friend!

**🔗 Your link:**
`{link}`

**📊 Your stats:**
• Referrals: **{count}**
• Earned: **{bonus}** min''',
                
                'send_audio': '🎙️ Send audio file to transcribe!',
                'language_changed': '✅ Language changed',
            }
        }
    
    def get(self, key, lang='ar', **kwargs):
        text = self.translations.get(lang, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text
        return text
    
    def get_language_name(self, code):
        languages = {
            'ar': '🇸🇦 العربية',
            'en': '🇺🇸 English',
            'es': '🇪🇸 Español',
            'fr': '🇫🇷 Français',
            'de': '🇩🇪 Deutsch',
            'auto': '🌐'
        }
        return languages.get(code, code)
