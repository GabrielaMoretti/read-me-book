"""
Text-to-Speech Engine Module
Handles audio conversion using pyttsx3 (default) or Coqui TTS (optional, natural voice)
"""
import pyttsx3
from typing import Callable, Optional

# Check if Coqui TTS is available
try:
    from coqui_tts_engine import CoquiTTSEngine, COQUI_AVAILABLE
except ImportError:
    COQUI_AVAILABLE = False


class TTSEngine:
    def __init__(self):
        """
        Initialize TTS engine with best available technology
        Automatically uses Coqui TTS if available, otherwise pyttsx3
        """
        self.engine = None
        self.coqui_engine = None
        self.is_reading = False
        self.paused = False
        
        # Try Coqui TTS first for natural voice quality
        if COQUI_AVAILABLE:
            try:
                self.coqui_engine = CoquiTTSEngine()
                print("Using Coqui TTS for natural voice generation")
            except Exception as e:
                print(f"Note: Coqui TTS unavailable, using pyttsx3: {e}")
                self._init_pyttsx3()
        else:
            self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 engine as fallback"""
        self.engine = pyttsx3.init()
        self._setup_voice()
        print("Using pyttsx3 for text-to-speech")
        
    def _setup_voice(self):
        """Configure voice settings (pyttsx3 only)"""
        if not self.engine:
            return
            
        voices = self.engine.getProperty('voices')
        # Set to first available voice (can be customized)
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 150)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute) - pyttsx3 only"""
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0) - pyttsx3 only"""
        if self.engine:
            self.engine.setProperty('volume', volume)
    
    def list_voices(self):
        """Get available voices from current TTS engine"""
        if self.coqui_engine:
            return self.coqui_engine.list_speakers()
        elif self.engine:
            return self.engine.getProperty('voices')
        return []
    
    def set_voice(self, voice_id: str):
        """Set voice by ID - pyttsx3 only"""
        if self.engine:
            self.engine.setProperty('voice', voice_id)
    
    def speak(self, text: str, on_word: Callable = None):
        """Speak the given text using available TTS engine"""
        if self.coqui_engine:
            print("Note: Coqui TTS generates audio files. Use save_to_file() method instead.")
            return
        
        if self.engine:
            if on_word:
                self.engine.connect('started-word', on_word)
            
            self.is_reading = True
            self.engine.say(text)
            self.engine.runAndWait()
            self.is_reading = False
    
    def stop(self):
        """Stop speaking on active TTS engine"""
        self.is_reading = False
        
        if self.coqui_engine:
            self.coqui_engine.stop()
        elif self.engine:
            self.engine.stop()
    
    def save_to_file(self, text: str, filename: str, language: Optional[str] = None, 
                     speaker: Optional[str] = None):
        """
        Save speech to audio file using best available TTS engine
        
        Args:
            text: Text to convert to speech
            filename: Output file path
            language: Language code (Coqui TTS: 'en', 'pt', 'es', etc.)
            speaker: Speaker name (Coqui TTS only)
            
        Returns:
            True if successful, False otherwise
        """
        if self.coqui_engine:
            # Use Coqui TTS for high-quality natural voice
            return self.coqui_engine.save_to_file(text, filename, language=language, speaker=speaker)
        elif self.engine:
            # Use pyttsx3 for basic TTS
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            return True
        return False
    
    def get_engine_info(self) -> dict:
        """Get information about active TTS engine"""
        if self.coqui_engine:
            info = self.coqui_engine.get_model_info()
            info['engine_type'] = 'coqui'
            return info
        else:
            return {
                'engine_type': 'pyttsx3',
                'voices': len(self.list_voices()) if self.engine else 0
            }
