import os
import hashlib
import subprocess
from gtts import gTTS
from pathlib import Path

# Import configuration
from configs.config import get_static_config, get_api_base_path

# Get configuration
static_config = get_static_config()
STATIC_FOLDER = static_config['folder']
AUDIO_SUBFOLDER = static_config['audio_subfolder']
STATIC_URL_PATH = static_config['url_path']
API_BASE_PATH = get_api_base_path()

class NumberService:
    def __init__(self):
        self.audio_dir = os.path.join(STATIC_FOLDER, AUDIO_SUBFOLDER)
        # Ensure audio directory exists
        os.makedirs(self.audio_dir, exist_ok=True)

    def number_to_french_words(self, number):
        """Convert number to French words"""
        if number == 0:
            return "zéro"
        
        units = ["", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf"]
        teens = ["dix", "onze", "douze", "treize", "quatorze", "quinze", "seize", "dix-sept", "dix-huit", "dix-neuf"]
        tens = ["", "", "vingt", "trente", "quarante", "cinquante", "soixante", "soixante-dix", "quatre-vingt", "quatre-vingt-dix"]
        
        if number < 20:
            if number < 10:
                return units[number]
            else:
                return teens[number - 10]
        
        elif number < 100:
            if number < 70:
                if number % 10 == 0:
                    return tens[number // 10]
                elif number % 10 == 1 and number // 10 != 8:
                    return tens[number // 10] + " et un"
                else:
                    return tens[number // 10] + ("-" + units[number % 10] if number % 10 > 0 else "")
            elif number < 80:
                remainder = number - 60
                if remainder < 10:
                    return "soixante-" + teens[remainder]
                else:
                    return "soixante-" + teens[remainder - 10]
            else:
                if number == 80:
                    return "quatre-vingts"
                elif number < 90:
                    return "quatre-vingt-" + units[number - 80]
                else:
                    remainder = number - 80
                    if remainder == 10:
                        return "quatre-vingt-dix"
                    else:
                        return "quatre-vingt-" + teens[remainder - 10]
        
        elif number < 1000:
            if number == 100:
                return "cent"
            elif number < 200:
                return "cent " + self.number_to_french_words(number - 100)
            else:
                hundreds = number // 100
                remainder = number % 100
                if remainder == 0:
                    return units[hundreds] + " cents"
                else:
                    return units[hundreds] + " cent " + self.number_to_french_words(remainder)
        
        elif number < 10000:
            if number == 1000:
                return "mille"
            elif number < 2000:
                return "mille " + self.number_to_french_words(number - 1000)
            else:
                thousands = number // 1000
                remainder = number % 1000
                if remainder == 0:
                    return units[thousands] + " mille"
                else:
                    return units[thousands] + " mille " + self.number_to_french_words(remainder)
        
        else:
            return "dix mille"  # For 10000

    def _generate_audio_file(self, text, output_path):
        """Generate audio file using gTTS"""
        try:
            tts = gTTS(text=text, lang='fr', slow=False)
            tts.save(output_path)
            return True
        except Exception as e:
            print(f"Error generating audio: {e}")
            return False

    def get_audio_url(self, number):
        """Get or generate audio URL for a number"""
        if number < 0 or number > 10000:
            return None
            
        french_text = self.number_to_french_words(number)
        text_hash = hashlib.sha256(french_text.encode('utf-8')).hexdigest()
        audio_filename = f"audio_{text_hash}.mp3"
        audio_path = os.path.join(self.audio_dir, audio_filename)
        
        # If file doesn't exist, generate it
        if not os.path.exists(audio_path):
            if not self._generate_audio_file(french_text, audio_path):
                return None
        
        path = f"{STATIC_URL_PATH}/{audio_filename}" if STATIC_URL_PATH else f"{API_BASE_PATH}/audio/{audio_filename}"
        return path
    
    def get_number_info(self, number):
        """Get number information including French text and audio URL"""
        if number < 0 or number > 10000:
            return None
            
        french_text = self.number_to_french_words(number)
        audio_url = self.get_audio_url(number)
        
        if not audio_url:
            return None
            
        return {
            "number": number,
            "french_text": french_text,
            "audio_url": audio_url
        }
