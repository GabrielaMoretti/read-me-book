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
    def __init__(self, use_coqui: bool = False, coqui_model: Optional[str] = None):
        """
        Initialize TTS engine
        
        Args:
            use_coqui: Use Coqui TTS instead of pyttsx3 (requires Coqui TTS installed)
            coqui_model: Specific Coqui model to use (optional)
        """
        self.use_coqui = use_coqui and COQUI_AVAILABLE
        self.engine = None
        self.coqui_engine = None
        self.is_reading = False
        self.paused = False
        
        if self.use_coqui:
            try:
                self.coqui_engine = CoquiTTSEngine(model_name=coqui_model)
                print("Coqui TTS engine initialized successfully")
            except Exception as e:
                print(f"Warning: Failed to initialize Coqui TTS: {e}")
                print("Falling back to pyttsx3")
                self.use_coqui = False
                self._init_pyttsx3()
        else:
            self._init_pyttsx3()
    
    def _init_pyttsx3(self):
        """Initialize pyttsx3 engine"""
        self.engine = pyttsx3.init()
        self._setup_voice()
        
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
        """Get available voices"""
        if self.use_coqui and self.coqui_engine:
            return self.coqui_engine.list_speakers()
        elif self.engine:
            return self.engine.getProperty('voices')
        return []
    
    def set_voice(self, voice_id: str):
        """Set voice by ID - pyttsx3 only"""
        if self.engine:
            self.engine.setProperty('voice', voice_id)
    
    def speak(self, text: str, on_word: Callable = None):
        """Speak the given text"""
        if self.use_coqui and self.coqui_engine:
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
        """Stop speaking"""
        self.is_reading = False
        
        if self.use_coqui and self.coqui_engine:
            self.coqui_engine.stop()
        elif self.engine:
            self.engine.stop()
    
    def save_to_file(self, text: str, filename: str, language: Optional[str] = None, 
                     speaker: Optional[str] = None):
        """
        Save speech to audio file
        
        Args:
            text: Text to convert to speech
            filename: Output file path
            language: Language code (Coqui TTS only, e.g., 'en', 'pt', 'es')
            speaker: Speaker name (Coqui TTS only)
        """
        if self.use_coqui and self.coqui_engine:
            # Use Coqui TTS for high-quality natural voice
            return self.coqui_engine.save_to_file(text, filename, language=language, speaker=speaker)
        elif self.engine:
            # Use pyttsx3 for basic TTS
            self.engine.save_to_file(text, filename)
            self.engine.runAndWait()
            return True
        return False
    
    def get_engine_info(self) -> dict:
        """Get information about current TTS engine"""
        if self.use_coqui and self.coqui_engine:
            info = self.coqui_engine.get_model_info()
            info['engine_type'] = 'coqui'
            return info
        else:
            return {
                'engine_type': 'pyttsx3',
                'voices': len(self.list_voices()) if self.engine else 0
            }
