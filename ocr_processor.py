"""
OCR Processor
Extrai texto de PDFs escaneados via Tesseract.
Só carrega se pytesseract e pdf2image estiverem instalados.
"""
from __future__ import annotations

from typing import Optional

try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False


class OCRProcessor:
    """Extrai texto de PDFs digitalizados (baseados em imagem)."""

    def __init__(self, language: str = "eng"):
        if not OCR_AVAILABLE:
            raise ImportError(
                "Dependências OCR não instaladas.\n"
                "Execute:  pip install pytesseract pdf2image\n"
                "E instale o Tesseract no sistema:\n"
                "  Ubuntu/Debian : sudo apt-get install tesseract-ocr\n"
                "  macOS         : brew install tesseract\n"
                "  Windows       : https://github.com/UB-Mannheim/tesseract/wiki"
            )
        self.language = language
        self.dpi = 300

    # ── extração ─────────────────────────────────────────────────────────────

    def extract_text_from_pdf(
        self,
        pdf_path: str,
        start_page: Optional[int] = None,
        end_page: Optional[int] = None,
    ) -> list[dict]:
        """Extrai texto página a página via OCR."""
        try:
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=start_page,
                last_page=end_page,
            )
        except Exception as exc:
            raise RuntimeError(f"Falha ao converter PDF para imagem: {exc}") from exc

        pages_data = []
        for i, image in enumerate(images, start=start_page or 1):
            text = self._ocr_image(image)
            confidence = self._confidence(image)
            pages_data.append(
                {"page_number": i, "text": text, "ocr_confidence": confidence}
            )
        return pages_data

    def _ocr_image(self, image: "Image.Image") -> str:
        gray = image.convert("L") if image.mode != "L" else image
        return pytesseract.image_to_string(gray, lang=self.language, config="--psm 1")

    def _confidence(self, image: "Image.Image") -> float:
        try:
            data = pytesseract.image_to_data(
                image, lang=self.language, output_type=pytesseract.Output.DICT
            )
            confs = [int(c) for c in data["conf"] if str(c) != "-1"]
            return round(sum(confs) / len(confs), 1) if confs else 0.0
        except Exception:
            return 0.0

    # ── utilitários ──────────────────────────────────────────────────────────

    def is_scanned_pdf(self, pdf_path: str, sample_pages: int = 3) -> bool:
        """Retorna True se o PDF parece ser baseado em imagem (escaneado)."""
        try:
            import pdfplumber
            with pdfplumber.open(pdf_path) as pdf:
                chars = sum(
                    len((p.extract_text() or "").strip())
                    for p in pdf.pages[:sample_pages]
                )
                avg = chars / min(sample_pages, len(pdf.pages))
            return avg < 50
        except Exception:
            return False

    def set_dpi(self, dpi: int):
        if not (100 <= dpi <= 600):
            raise ValueError("DPI deve ser entre 100 e 600")
        self.dpi = dpi

    @staticmethod
    def get_supported_languages() -> list[str]:
        if not OCR_AVAILABLE:
            return []
        try:
            return pytesseract.get_languages()
        except Exception:
            return ["eng"]
