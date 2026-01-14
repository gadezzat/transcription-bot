import os
import tempfile
from config import TEMP_FOLDER
import logging

logger = logging.getLogger(__name__)

os.makedirs(TEMP_FOLDER, exist_ok=True)

class TranscriptionService:
    """Transcription Service"""
    
    def __init__(self, bot):
        self.bot = bot
    
    def download_file(self, file_id, file_extension='mp3'):
        """Download file from Telegram"""
        try:
            file_info = self.bot.get_file(file_id)
            downloaded_file = self.bot.download_file(file_info.file_path)
            
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f'.{file_extension}',
                dir=TEMP_FOLDER
            )
            temp_file.write(downloaded_file)
            temp_file.close()
            
            file_size = os.path.getsize(temp_file.name)
            
            return temp_file.name, file_size
        except Exception as e:
            logger.error(f'Error downloading file: {e}')
            raise
    
    def transcribe_audio(self, file_path, language='auto', task='transcribe', model='base'):
        """Transcribe audio using Whisper"""
        try:
            import whisper
            import time
            
            start_time = time.time()
            
            whisper_model = whisper.load_model(model)
            
            transcribe_options = {
                'task': task,
                'verbose': False
            }
            
            if language != 'auto':
                transcribe_options['language'] = language
            
            result = whisper_model.transcribe(file_path, **transcribe_options)
            
            processing_time = time.time() - start_time
            
            return {
                'text': result['text'].strip(),
                'language': result.get('language', language),
                'segments': result.get('segments', []),
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f'Error transcribing audio: {e}')
            raise
    
    def get_audio_duration(self, file_path):
        """Get audio file duration"""
        try:
            import whisper
            audio = whisper.load_audio(file_path)
            duration = len(audio) / whisper.audio.SAMPLE_RATE
            return duration
        except Exception as e:
            logger.error(f'Error getting audio duration: {e}')
            return 0
    
    def export_as_txt(self, text):
        """Export as TXT file"""
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            suffix='.txt',
            delete=False,
            dir=TEMP_FOLDER
        )
        temp_file.write(text)
        temp_file.close()
        return temp_file.name
    
    def export_as_srt(self, segments):
        """Export as SRT file"""
        def format_timestamp(seconds):
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = int(seconds % 60)
            millis = int((seconds % 1) * 1000)
            return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
        
        srt_content = ""
        for i, segment in enumerate(segments, 1):
            start = format_timestamp(segment['start'])
            end = format_timestamp(segment['end'])
            text = segment['text'].strip()
            
            srt_content += f"{i}\n{start} --> {end}\n{text}\n\n"
        
        temp_file = tempfile.NamedTemporaryFile(
            mode='w',
            encoding='utf-8',
            suffix='.srt',
            delete=False,
            dir=TEMP_FOLDER
        )
        temp_file.write(srt_content)
        temp_file.close()
        return temp_file.name
    
    def cleanup_file(self, file_path):
        """Delete temporary file"""
        try:
            if os.path.exists(file_path):
                os.unlink(file_path)
        except Exception as e:
            logger.error(f'Error cleaning up file: {e}')
