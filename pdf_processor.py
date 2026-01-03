"""
Enhanced PDF Processor Module
Handles PDF text extraction with AI-powered content filtering and organization
"""
import re
import pdfplumber
from typing import List, Dict, Tuple, Optional

# Check AI availability at module level
try:
    from ai_text_analyzer import AITextAnalyzer
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# Check deepdoctection availability
try:
    from deepdoc_processor import DeepDocProcessor, DEEPDOC_AVAILABLE
except ImportError:
    DEEPDOC_AVAILABLE = False


class PDFProcessor:
    def __init__(self, pdf_path: str, use_ai: bool = True):
        """
        Initialize PDF processor with integrated advanced features
        
        Args:
            pdf_path: Path to PDF file
            use_ai: Enable AI-powered analysis (default: True)
        """
        self.pdf_path = pdf_path
        self.pages = []
        self.chapters = []
        self.use_ai = use_ai and AI_AVAILABLE
        self.ai_analyzer = AITextAnalyzer() if self.use_ai else None
        self.structured_content = None
        self.document_structure = None
        
        # Try to use deepdoctection if available, otherwise use pdfplumber
        self.deepdoc_processor = None
        if DEEPDOC_AVAILABLE:
            try:
                self.deepdoc_processor = DeepDocProcessor()
            except Exception as e:
                print(f"Note: deepdoctection unavailable, using standard extraction: {e}")
                self.deepdoc_processor = None
        
    def extract_text(self) -> List[Dict]:
        """
        Extract text from PDF pages using best available method
        Automatically uses deepdoctection if available, otherwise pdfplumber
        """
        # Try deepdoctection first for better layout analysis
        if self.deepdoc_processor:
            return self._extract_with_deepdoctection()
        
        # Fall back to standard extraction
        return self._extract_with_pdfplumber()
    
    def _extract_with_deepdoctection(self) -> List[Dict]:
        """Extract text using deepdoctection for advanced layout analysis"""
        try:
            pages_data = self.deepdoc_processor.extract_text_with_layout(self.pdf_path)
            
            # Convert to standard format and add cleaned text
            for page_data in pages_data:
                page_data['cleaned_text'] = self._clean_text(page_data['text'], page_data['page_number'])
            
            self.pages = pages_data
            return pages_data
        
        except Exception as e:
            print(f"Note: deepdoctection extraction failed, using standard method: {e}")
            return self._extract_with_pdfplumber()
    
    def _extract_with_pdfplumber(self) -> List[Dict]:
        """Standard extraction using pdfplumber"""
        pages_data = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    pages_data.append({
                        'page_number': i + 1,
                        'text': text,
                        'cleaned_text': self._clean_text(text, i + 1)
                    })
        
        self.pages = pages_data
        return pages_data
    
    def _clean_text(self, text: str, page_num: int) -> str:
        """Remove headers, footers, and page numbers from text"""
        lines = text.split('\n')
        cleaned_lines = []
        
        # Skip first and last 2 lines (likely headers/footers)
        content_lines = lines[2:-2] if len(lines) > 4 else lines
        
        for line in content_lines:
            # Skip lines that are just page numbers
            if re.match(r'^\s*\d+\s*$', line):
                continue
            # Skip very short lines at edges (likely headers/footers)
            if len(line.strip()) < 3:
                continue
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def detect_chapters(self) -> List[Dict]:
        """Detect chapter headings in the document"""
        if self.use_ai and self.ai_analyzer:
            # Use AI-powered chapter detection
            chapters = self.ai_analyzer.detect_chapters_advanced(self.pages)
            self.chapters = chapters
            return chapters
        
        # Fallback to basic pattern matching
        chapters = []
        chapter_patterns = [
            r'^(Chapter|CHAPTER|Capítulo|CAPÍTULO)\s+(\d+|[IVXLCDM]+)',
            r'^(\d+)\.\s+[A-Z]',
            r'^[A-Z][A-Z\s]{10,}$'  # ALL CAPS headings
        ]
        
        for page_data in self.pages:
            lines = page_data['text'].split('\n')
            for i, line in enumerate(lines):
                line = line.strip()
                for pattern in chapter_patterns:
                    if re.match(pattern, line):
                        chapters.append({
                            'title': line,
                            'page': page_data['page_number'],
                            'position': i
                        })
                        break
        
        self.chapters = chapters
        return chapters
    
    def get_text_for_reading(self) -> str:
        """Get cleaned text suitable for reading"""
        all_text = []
        for page in self.pages:
            all_text.append(page['cleaned_text'])
        return '\n\n'.join(all_text)
    
    def get_chapter_text(self, chapter_index: int) -> str:
        """Get text for a specific chapter"""
        if not self.chapters or chapter_index >= len(self.chapters):
            return self.get_text_for_reading()
        
        start_page = self.chapters[chapter_index]['page']
        end_page = self.chapters[chapter_index + 1]['page'] if chapter_index + 1 < len(self.chapters) else len(self.pages) + 1
        
        chapter_text = []
        for page in self.pages:
            if start_page <= page['page_number'] < end_page:
                chapter_text.append(page['cleaned_text'])
        
        return '\n\n'.join(chapter_text)
    
    def get_structured_content_for_audiobook(self) -> Optional[Dict]:
        """
        Get structured content optimized for audiobook production
        Returns organized text with metadata for each chapter
        """
        if not self.use_ai or not self.ai_analyzer:
            return None
        
        if not self.structured_content:
            self.structured_content = self.ai_analyzer.organize_text_for_audiobook(
                self.pages, self.chapters
            )
        
        return self.structured_content
    
    def get_document_structure(self) -> Optional[Dict]:
        """Get overall document structure analysis"""
        if not self.use_ai or not self.ai_analyzer:
            return None
        
        if not self.document_structure:
            self.document_structure = self.ai_analyzer.identify_document_structure(self.pages)
        
        return self.document_structure
    
    def get_footnotes_and_references(self) -> Optional[Dict]:
        """Extract footnotes and references from the document"""
        if not self.use_ai or not self.ai_analyzer:
            return None
        
        return self.ai_analyzer.extract_footnotes_and_references(self.pages)
    
    def export_to_json(self) -> Dict:
        """Export document analysis to JSON-serializable format"""
        export_data = {
            'pdf_path': self.pdf_path,
            'total_pages': len(self.pages),
            'chapters': self.chapters,
            'structured_content': self.get_structured_content_for_audiobook(),
            'document_structure': self.get_document_structure(),
            'footnotes_references': self.get_footnotes_and_references(),
            'extraction_method': 'deepdoctection' if self.deepdoc_processor else 'pdfplumber'
        }
        
        # Add deepdoctection-specific data if used
        if self.deepdoc_processor:
            try:
                deepdoc_structure = self.deepdoc_processor.get_document_structure(self.pdf_path)
                export_data['deepdoctection_analysis'] = {
                    'total_tables': deepdoc_structure['total_tables'],
                    'total_images': deepdoc_structure['total_images'],
                    'max_columns': deepdoc_structure['max_columns'],
                    'has_complex_layout': deepdoc_structure['has_complex_layout']
                }
            except Exception:
                pass
        
        return export_data
