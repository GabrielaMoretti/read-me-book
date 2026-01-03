"""
Natural Text-to-Speech Engine using Coqui TTS
Provides high-quality, natural-sounding voice synthesis with advanced features
"""
import warnings
warnings.filterwarnings('ignore')

from typing import Callable, Optional, List
import os

# Default model for Coqui TTS (can be overridden in __init__)
DEFAULT_COQUI_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# Check if Coqui TTS is available
try:
    from TTS.api import TTS
    from TTS.utils.manage import ModelManager
    COQUI_AVAILABLE = True
except ImportError:
    COQUI_AVAILABLE = False


class CoquiTTSEngine:
    """
    Natural TTS engine using Coqui TTS
    Supports advanced features like voice cloning, emotion, and natural intonation
    """
    
    def __init__(self, model_name: Optional[str] = None, use_gpu: bool = False):
        """
        Initialize Coqui TTS engine
        
        Args:
            model_name: TTS model to use (default: automatic selection)
            use_gpu: Whether to use GPU acceleration (requires CUDA)
        """
        if not COQUI_AVAILABLE:
            raise ImportError(
                "Coqui TTS not available. Install with:\n"
                "pip install TTS\n"
                "Note: This is a large package and will download model files on first use"
            )
        
        self.use_gpu = use_gpu
        self.model_name = model_name
        self.tts = None
        self.is_reading = False
        self._initialize_tts()
    
    def _initialize_tts(self):
        """Initialize the TTS model"""
        try:
            if self.model_name:
                # Use specified model
                self.tts = TTS(model_name=self.model_name, gpu=self.use_gpu)
            else:
                # Auto-select best multilingual model using constant
                try:
                    self.tts = TTS(model_name=DEFAULT_COQUI_MODEL, gpu=self.use_gpu)
                except Exception:
                    # Fallback to a lighter model
                    self.tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", gpu=self.use_gpu)
        
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize Coqui TTS: {str(e)}\n"
                "Please ensure models are properly downloaded or select a different model."
            )
    
    def list_available_models(self) -> List[str]:
        """
        Get list of available TTS models
        
        Returns:
            List of model names
        """
        try:
            manager = ModelManager()
            return manager.list_models()
        except Exception:
            return []
    
    def list_speakers(self) -> List[str]:
        """
        Get list of available speakers for current model
        
        Returns:
            List of speaker names/IDs
        """
        if not self.tts:
            return []
        
        try:
            if hasattr(self.tts, 'speakers') and self.tts.speakers:
                return self.tts.speakers
        except Exception:
            pass
        
        return []
    
    def list_languages(self) -> List[str]:
        """
        Get list of supported languages for current model
        
        Returns:
            List of language codes
        """
        if not self.tts:
            return []
        
        try:
            if hasattr(self.tts, 'languages') and self.tts.languages:
                return self.tts.languages
        except Exception:
            pass
        
        return []
    
    def speak(self, text: str, language: Optional[str] = None, 
              speaker: Optional[str] = None) -> bool:
        """
        Speak the given text (not implemented for Coqui - use save_to_file instead)
        
        Args:
            text: Text to speak
            language: Language code (e.g., 'en', 'pt', 'es')
            speaker: Speaker name/ID
            
        Returns:
            False (direct speaking not supported, use save_to_file)
        """
        # Coqui TTS generates audio files rather than direct playback
        # Users should use save_to_file() and play the resulting audio file
        print("Note: Coqui TTS generates audio files. Use save_to_file() method instead.")
        return False
    
    def save_to_file(self, text: str, filename: str, 
                     language: Optional[str] = None,
                     speaker: Optional[str] = None,
                     speaker_wav: Optional[str] = None,
                     emotion: Optional[str] = None) -> bool:
        """
        Generate audio file from text with natural voice
        
        Args:
            text: Text to convert to speech
            filename: Output audio file path (e.g., 'output.wav')
            language: Language code for multilingual models (e.g., 'en', 'pt', 'es')
            speaker: Speaker name/ID for multi-speaker models
            speaker_wav: Path to audio file for voice cloning (XTTS models)
            emotion: Emotion style (model-dependent)
            
        Returns:
            True if successful, False otherwise
        """
        if not self.tts:
            print("TTS engine not initialized")
            return False
        
        try:
            self.is_reading = True
            
            # Build kwargs based on available parameters
            tts_kwargs = {}
            
            # Add language if supported and provided
            if language and self.list_languages():
                tts_kwargs['language'] = language
            
            # Add speaker if supported and provided
            if speaker and self.list_speakers():
                tts_kwargs['speaker'] = speaker
            
            # Add voice cloning reference if provided (XTTS feature)
            if speaker_wav and os.path.exists(speaker_wav):
                tts_kwargs['speaker_wav'] = speaker_wav
            
            # Add emotion if supported (model-dependent)
            if emotion:
                tts_kwargs['emotion'] = emotion
            
            # Generate audio
            self.tts.tts_to_file(text=text, file_path=filename, **tts_kwargs)
            
            self.is_reading = False
            return True
        
        except Exception as e:
            self.is_reading = False
            print(f"Error generating audio: {str(e)}")
            return False
    
    def save_to_file_with_splits(self, text: str, output_dir: str,
                                 max_chars: int = 500,
                                 language: Optional[str] = None,
                                 speaker: Optional[str] = None) -> List[str]:
        """
        Save long text to multiple audio files (splitting by sentences/paragraphs)
        
        Args:
            text: Text to convert
            output_dir: Directory to save audio files
            max_chars: Maximum characters per audio file
            language: Language code
            speaker: Speaker name/ID
            
        Returns:
            List of generated audio file paths
        """
        import re
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Split text into chunks
        chunks = self._split_text(text, max_chars)
        
        audio_files = []
        for i, chunk in enumerate(chunks):
            filename = os.path.join(output_dir, f"part_{i+1:03d}.wav")
            
            if self.save_to_file(chunk, filename, language=language, speaker=speaker):
                audio_files.append(filename)
            else:
                print(f"Warning: Failed to generate audio for chunk {i+1}")
        
        return audio_files
    
    def _split_text(self, text: str, max_chars: int) -> List[str]:
        """
        Split text into chunks suitable for TTS processing
        
        Args:
            text: Input text
            max_chars: Maximum characters per chunk
            
        Returns:
            List of text chunks
        """
        import re
        
        # Split by sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chars:
                current_chunk += sentence + " "
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def clone_voice(self, speaker_wav: str, text: str, output_file: str,
                   language: str = "en") -> bool:
        """
        Clone voice from audio sample and generate speech
        (Requires XTTS model)
        
        Args:
            speaker_wav: Path to reference audio file (clean, 6-30 seconds)
            text: Text to synthesize
            output_file: Output audio file path
            language: Language code
            
        Returns:
            True if successful, False otherwise
        """
        if not os.path.exists(speaker_wav):
            print(f"Speaker audio file not found: {speaker_wav}")
            return False
        
        return self.save_to_file(
            text=text,
            filename=output_file,
            language=language,
            speaker_wav=speaker_wav
        )
    
    def stop(self):
        """Stop current TTS operation"""
        self.is_reading = False
    
    def get_model_info(self) -> dict:
        """
        Get information about current model
        
        Returns:
            Dictionary with model information
        """
        info = {
            'model_name': self.model_name or 'auto-selected',
            'gpu_enabled': self.use_gpu,
            'speakers': self.list_speakers(),
            'languages': self.list_languages(),
            'supports_voice_cloning': 'xtts' in str(self.model_name).lower() if self.model_name else False
        }
        return info
    
    @staticmethod
    def is_available() -> bool:
        """Check if Coqui TTS is available"""
        return COQUI_AVAILABLE
