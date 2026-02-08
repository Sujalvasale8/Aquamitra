"""Translation service using Google Gemini API for multilingual support.

Supports translation between English and Indian languages:
Hindi, Marathi, Bengali, Tamil, Telugu, Gujarati
"""

import os
import time
import logging
from typing import Dict, Optional
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()

logger = logging.getLogger(__name__)

# Language mappings
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi', 
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'gu': 'Gujarati'
}

class TranslationService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        # Configure Gemini
        genai.configure(api_key=self.api_key)
        self.model = "gemini-1.5-flash"
        
        # Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1.0  # 1 second between requests to avoid rate limits
    
    def _wait_for_rate_limit(self):
        """Ensure we don't exceed rate limits"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()
    
    def translate_to_english(self, text: str, source_language: str) -> str:
        """Translate text from source language to English"""
        if source_language == 'en':
            return text
        try:
            # New SDK syntax: client.models.generate_content
            response = self.client.models.generate_content(
                model=self.model_id, 
                contents=f"Translate this to English: {text}"
            )
            return response.text.strip()
        except Exception as e:
            return text # Safe fallback
        
        source_lang_name = SUPPORTED_LANGUAGES.get(source_language, source_language)
        
        prompt = f"""
Translate the following {source_lang_name} text to English. 
Keep the translation accurate and natural. If it's a question about groundwater, water resources, or geographic locations, preserve technical terms and place names correctly.

{source_lang_name} text: {text}

English translation:"""
        
        try:
            self._wait_for_rate_limit()
            response = self.model.generate_content(prompt)
            translation = response.text.strip()
            
            logger.info(f"Translated from {source_lang_name} to English: {text[:50]}... -> {translation[:50]}...")
            return translation
            
        except Exception as e:
            logger.error(f"Translation error ({source_lang_name} to English): {e}")
            # Fallback to original text if translation fails
            return text
    
    def translate_from_english(self, text: str, target_language: str) -> str:
        """Translate text from English to target language"""
        if target_language == 'en':
            return text
            
        target_lang_name = SUPPORTED_LANGUAGES.get(target_language, target_language)
        
        prompt = f"""
Translate the following English text to {target_lang_name}.
Keep the translation natural and accurate. Preserve numbers, technical terms, and proper nouns when appropriate.
If translating groundwater/water resource information, maintain technical accuracy.

English text: {text}

{target_lang_name} translation:"""
        
        try:
            self._wait_for_rate_limit()
            response = self.model.generate_content(prompt)
            translation = response.text.strip()
            
            logger.info(f"Translated from English to {target_lang_name}: {text[:50]}... -> {translation[:50]}...")
            return translation
            
        except Exception as e:
            logger.error(f"Translation error (English to {target_lang_name}): {e}")
            # Fallback to original text if translation fails
            return text
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        prompt = f"""
Detect the language of the following text and respond with only the language code:
- en for English
- hi for Hindi  
- mr for Marathi
- bn for Bengali
- ta for Tamil
- te for Telugu
- gu for Gujarati

If the language is not one of these, respond with 'en'.

Text: {text}

Language code:"""
        
        try:
            self._wait_for_rate_limit()
            response = self.model.generate_content(prompt)
            detected_lang = response.text.strip().lower()
            
            # Validate the response
            if detected_lang in SUPPORTED_LANGUAGES:
                return detected_lang
            else:
                logger.warning(f"Unknown language detected: {detected_lang}, defaulting to English")
                return 'en'
                
        except Exception as e:
            logger.error(f"Language detection error: {e}")
            return 'en'  # Default to English if detection fails

# Global instance
_translation_service = None

def get_translation_service() -> TranslationService:
    """Get or create the global translation service instance"""
    global _translation_service
    if _translation_service is None:
        _translation_service = TranslationService()
    return _translation_service

def translate_query_to_english(query: str, source_language: str = 'auto') -> str:
    """Convenience function to translate query to English"""
    service = get_translation_service()
    
    if source_language == 'auto':
        source_language = service.detect_language(query)
    
    return service.translate_to_english(query, source_language)

def translate_response_to_language(response: str, target_language: str) -> str:
    """Convenience function to translate response to target language"""
    service = get_translation_service()
    return service.translate_from_english(response, target_language)
