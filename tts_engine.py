"""
TTS Engine
Motor de síntese de voz. Usa Coqui TTS se disponível, caso contrário pyttsx3.
"""
from __future__ import annotations

import threading
from typing import Callable, Optional

# ── Coqui TTS (opcional, voz natural) ───────────────────────────────────────
try:
    from coqui_tts_engine import CoquiTTSEngine
    _COQUI_OK = True
except Exception:
    _COQUI_OK = False

COQUI_AVAILABLE = _COQUI_OK

# ── pyttsx3 (padrão) ────────────────────────────────────────────────────────
try:
    import pyttsx3 as _pyttsx3
    _PYTTSX3_OK = True
except Exception:
    _PYTTSX3_OK = False


class TTSEngine:
    """
    Motor TTS unificado.
    - Prefere Coqui TTS (voz natural) se instalado.
    - Usa pyttsx3 como fallback.
    - Levanta RuntimeError com instrução clara se nenhum estiver disponível.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self.is_reading = False
        self._engine = None          # pyttsx3
        self._coqui: Optional[CoquiTTSEngine] = None

        if _COQUI_OK:
            try:
                self._coqui = CoquiTTSEngine()
                print("[TTS] Usando Coqui TTS (voz natural)")
                return
            except Exception as exc:
                print(f"[TTS] Coqui TTS falhou, tentando pyttsx3: {exc}")

        if _PYTTSX3_OK:
            try:
                self._engine = _pyttsx3.init()
                self._configure_pyttsx3()
                print("[TTS] Usando pyttsx3")
                return
            except Exception as exc:
                raise RuntimeError(
                    f"pyttsx3 falhou ao inicializar: {exc}\n\n"
                    "No Linux instale: sudo apt-get install espeak espeak-ng\n"
                    "No Windows/macOS o motor nativo deveria funcionar automaticamente."
                ) from exc

        raise RuntimeError(
            "Nenhum motor TTS disponível.\n"
            "Instale pyttsx3:  pip install pyttsx3\n"
            "Linux também precisa:  sudo apt-get install espeak"
        )

    # ── configuração ─────────────────────────────────────────────────────────

    def _configure_pyttsx3(self):
        if not self._engine:
            return
        voices = self._engine.getProperty("voices")
        if voices:
            self._engine.setProperty("voice", voices[0].id)
        self._engine.setProperty("rate", 150)
        self._engine.setProperty("volume", 0.9)

    # ── propriedades ─────────────────────────────────────────────────────────

    def set_rate(self, rate: int):
        """Define velocidade de leitura (palavras por minuto). Só pyttsx3."""
        if self._engine:
            self._engine.setProperty("rate", max(50, min(rate, 400)))

    def set_volume(self, volume: float):
        """Define volume (0.0 – 1.0). Só pyttsx3."""
        if self._engine:
            self._engine.setProperty("volume", max(0.0, min(volume, 1.0)))

    def list_voices(self) -> list:
        if self._coqui:
            return self._coqui.list_speakers()
        if self._engine:
            return self._engine.getProperty("voices") or []
        return []

    def set_voice(self, voice_id: str):
        if self._engine:
            self._engine.setProperty("voice", voice_id)

    # ── leitura ──────────────────────────────────────────────────────────────

    def speak(self, text: str, on_word: Optional[Callable] = None):
        """Lê o texto em voz alta (bloqueante; chame de uma thread separada)."""
        if not text.strip():
            return
        with self._lock:
            self.is_reading = True
            try:
                if self._coqui:
                    # Coqui não faz streaming direto; avisa o usuário
                    print("[TTS] Coqui TTS: use save_to_file() para gerar áudio.")
                    return
                if self._engine:
                    if on_word:
                        self._engine.connect("started-word", on_word)
                    self._engine.say(text)
                    self._engine.runAndWait()
            finally:
                self.is_reading = False

    def stop(self):
        """Interrompe a leitura em andamento."""
        self.is_reading = False
        if self._coqui:
            self._coqui.stop()
        if self._engine:
            try:
                self._engine.stop()
            except Exception:
                pass

    def save_to_file(
        self,
        text: str,
        filename: str,
        language: Optional[str] = None,
        speaker: Optional[str] = None,
    ) -> bool:
        """Salva a fala em arquivo de áudio."""
        if self._coqui:
            return self._coqui.save_to_file(
                text, filename, language=language, speaker=speaker
            )
        if self._engine:
            try:
                self._engine.save_to_file(text, filename)
                self._engine.runAndWait()
                return True
            except Exception as exc:
                print(f"[TTS] Erro ao salvar arquivo: {exc}")
                return False
        return False

    def get_engine_info(self) -> dict:
        if self._coqui:
            info = self._coqui.get_model_info()
            info["engine_type"] = "coqui"
            return info
        return {
            "engine_type": "pyttsx3",
            "voices": len(self.list_voices()),
        }
