"""
Text-to-Speech Engine Module
Handles audio conversion using pyttsx3
"""
import pyttsx3
from typing import Callable


class TTSEngine:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.is_reading = False
        self.paused = False
        self._setup_voice()
        
    def _setup_voice(self):
        """Configure voice settings"""
        voices = self.engine.getProperty('voices')
        # Set to first available voice (can be customized)
        if voices:
            self.engine.setProperty('voice', voices[0].id)
        
        # Set speech rate (words per minute)
        self.engine.setProperty('rate', 150)
        
        # Set volume (0.0 to 1.0)
        self.engine.setProperty('volume', 0.9)
    
    def set_rate(self, rate: int):
        """Set speech rate (words per minute)"""
        self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.engine.setProperty('volume', volume)
    
    def list_voices(self):
        """Get available voices"""
        return self.engine.getProperty('voices')
    
    def set_voice(self, voice_id: str):
        """Set voice by ID"""
        self.engine.setProperty('voice', voice_id)
    
    def speak(self, text: str, on_word: Callable = None):
        """Speak the given text"""
        if on_word:
            self.engine.connect('started-word', on_word)
        
        self.is_reading = True
        self.engine.say(text)
        self.engine.runAndWait()
        self.is_reading = False
    
    def stop(self):
        """Stop speaking"""
        self.is_reading = False
        self.engine.stop()
    
    def save_to_file(self, text: str, filename: str):
        """Save speech to audio file"""
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
