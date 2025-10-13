"""
PDF Processor Module
Handles PDF text extraction and content filtering
"""
import re
import pdfplumber
from typing import List, Dict, Tuple


class PDFProcessor:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.pages = []
        self.chapters = []
        
    def extract_text(self) -> List[Dict]:
        """Extract text from PDF pages"""
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
