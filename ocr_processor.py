"""
OCR Module for Scanned PDFs
Uses Tesseract OCR for text extraction from images
"""
import warnings
warnings.filterwarnings('ignore')

try:
    import pytesseract
    from pdf2image import convert_from_path
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
    Image = None  # Define placeholder for type hints

from typing import List, Dict, Optional, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING and not OCR_AVAILABLE:
    from PIL import Image


class OCRProcessor:
    """
    OCR processor for extracting text from scanned PDFs
    """
    
    def __init__(self, language: str = 'eng'):
        """
        Initialize OCR processor
        
        Args:
            language: Tesseract language code (eng, por, spa, etc.)
        """
        if not OCR_AVAILABLE:
            raise ImportError(
                "OCR dependencies not available. Install with:\n"
                "pip install pytesseract pdf2image\n"
                "Also install Tesseract: https://github.com/tesseract-ocr/tesseract"
            )
        
        self.language = language
        self.dpi = 300  # Higher DPI for better OCR quality
    
    def extract_text_from_pdf(self, pdf_path: str, 
                              start_page: Optional[int] = None,
                              end_page: Optional[int] = None) -> List[Dict]:
        """
        Extract text from scanned PDF using OCR
        
        Args:
            pdf_path: Path to PDF file
            start_page: First page to process (1-indexed)
            end_page: Last page to process (1-indexed)
            
        Returns:
            List of dictionaries with page number and extracted text
        """
        pages_data = []
        
        try:
            # Convert PDF pages to images
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                first_page=start_page,
                last_page=end_page
            )
            
            # Process each image with OCR
            for i, image in enumerate(images, start=start_page or 1):
                text = self._extract_text_from_image(image)
                
                pages_data.append({
                    'page_number': i,
                    'text': text,
                    'ocr_confidence': self._get_ocr_confidence(image)
                })
        
        except Exception as e:
            raise RuntimeError(f"OCR processing failed: {str(e)}")
        
        return pages_data
    
    def _extract_text_from_image(self, image) -> str:
        """
        Extract text from a single image using Tesseract
        
        Args:
            image: PIL Image object
            
        Returns:
            Extracted text
        """
        # Preprocess image for better OCR
        processed_image = self._preprocess_image(image)
        
        # Extract text
        text = pytesseract.image_to_string(
            processed_image,
            lang=self.language,
            config='--psm 1'  # Automatic page segmentation
        )
        
        return text
    
    def _preprocess_image(self, image) -> 'Image':
        """
        Preprocess image to improve OCR quality
        
        Args:
            image: Input image
            
        Returns:
            Preprocessed image
        """
        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')
        
        # Could add more preprocessing here:
        # - Noise reduction
        # - Contrast enhancement
        # - Binarization
        
        return image
    
    def _get_ocr_confidence(self, image) -> float:
        """
        Get OCR confidence score for an image
        
        Args:
            image: PIL Image object
            
        Returns:
            Average confidence score (0-100)
        """
        try:
            data = pytesseract.image_to_data(
                image,
                lang=self.language,
                output_type=pytesseract.Output.DICT
            )
            
            # Calculate average confidence
            confidences = [int(conf) for conf in data['conf'] if conf != '-1']
            
            if confidences:
                return sum(confidences) / len(confidences)
            
        except Exception:
            pass
        
        return 0.0
    
    def extract_text_from_image_file(self, image_path: str) -> str:
        """
        Extract text from a single image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            Extracted text
        """
        image = Image.open(image_path)
        return self._extract_text_from_image(image)
    
    def is_scanned_pdf(self, pdf_path: str, sample_pages: int = 3) -> bool:
        """
        Determine if a PDF is scanned (image-based) or native (text-based)
        
        Args:
            pdf_path: Path to PDF file
            sample_pages: Number of pages to sample
            
        Returns:
            True if PDF appears to be scanned
        """
        try:
            import pdfplumber
            
            with pdfplumber.open(pdf_path) as pdf:
                text_chars = 0
                pages_checked = 0
                
                # Check first few pages
                for page in pdf.pages[:sample_pages]:
                    text = page.extract_text()
                    if text:
                        text_chars += len(text.strip())
                    pages_checked += 1
                
                # If very little text found, likely scanned
                avg_chars = text_chars / pages_checked if pages_checked > 0 else 0
                return avg_chars < 50  # Threshold for scanned detection
        
        except Exception:
            return False
    
    @staticmethod
    def get_supported_languages() -> List[str]:
        """
        Get list of available Tesseract languages
        
        Returns:
            List of language codes
        """
        if not OCR_AVAILABLE:
            return []
        
        try:
            languages = pytesseract.get_languages()
            return languages
        except Exception:
            return ['eng']  # Default fallback
    
    def set_language(self, language: str):
        """
        Set OCR language
        
        Args:
            language: Tesseract language code
        """
        self.language = language
    
    def set_dpi(self, dpi: int):
        """
        Set DPI for PDF to image conversion
        
        Args:
            dpi: Dots per inch (recommended: 200-400)
        """
        if 100 <= dpi <= 600:
            self.dpi = dpi
        else:
            raise ValueError("DPI must be between 100 and 600")
