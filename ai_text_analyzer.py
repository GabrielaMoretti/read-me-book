"""
AI-Powered Text Analysis Module
Uses NLP and machine learning for intelligent text organization
"""
import re
from typing import List, Dict, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


class AITextAnalyzer:
    """
    AI-powered text analyzer for intelligent content organization
    Uses heuristics and patterns for text classification without requiring heavy ML models
    """
    
    def __init__(self):
        self.chapter_patterns = [
            r'^(Chapter|CHAPTER|Capítulo|CAPÍTULO)\s+(\d+|[IVXLCDM]+)',
            r'^(\d+)\.\s+[A-Z]',
            r'^[A-Z][A-Z\s]{10,}$',
            r'^(Part|PART|Parte|PARTE)\s+(\d+|[IVXLCDM]+)',
            r'^(Section|SECTION|Seção|SEÇÃO)\s+(\d+)',
        ]
        
        self.header_patterns = [
            r'^\d+\s*$',  # Page numbers
            r'^[A-Z\s]+$',  # All caps short lines
            r'^\s*\d+\s*\|\s*',  # Page markers with pipes
        ]
        
        self.footer_patterns = [
            r'^\d+\s*$',  # Page numbers
            r'^Copyright',
            r'^©',
            r'^\s*\d+\s*$',
        ]
    
    def classify_line_type(self, line: str, position: int, total_lines: int) -> str:
        """
        Classify a line as: chapter, header, footer, footnote, or content
        
        Args:
            line: The text line to classify
            position: Line position in page (0-indexed)
            total_lines: Total number of lines in page
            
        Returns:
            str: Classification type
        """
        line = line.strip()
        
        if not line:
            return 'empty'
        
        # Check if it's a chapter heading
        for pattern in self.chapter_patterns:
            if re.match(pattern, line):
                return 'chapter'
        
        # Check if it's likely a header (first few lines)
        if position < 3 and len(line) < 50:
            for pattern in self.header_patterns:
                if re.match(pattern, line):
                    return 'header'
        
        # Check if it's likely a footer (last few lines)
        if position >= total_lines - 3 and len(line) < 50:
            for pattern in self.footer_patterns:
                if re.match(pattern, line):
                    return 'footer'
        
        # Check if it's a footnote
        if re.match(r'^\s*\d+\s+', line) and len(line) < 150:
            return 'footnote'
        
        # Check for reference markers
        if re.match(r'^\[\d+\]', line):
            return 'reference'
        
        return 'content'
    
    def detect_chapters_advanced(self, pages_data: List[Dict]) -> List[Dict]:
        """
        Advanced chapter detection using pattern matching and context analysis
        
        Args:
            pages_data: List of page dictionaries with text
            
        Returns:
            List of detected chapters with metadata
        """
        chapters = []
        
        for page_data in pages_data:
            lines = page_data['text'].split('\n')
            page_num = page_data['page_number']
            
            for i, line in enumerate(lines):
                line_type = self.classify_line_type(line, i, len(lines))
                
                if line_type == 'chapter':
                    # Extract chapter number and title
                    chapter_info = self._extract_chapter_info(line)
                    chapters.append({
                        'title': line.strip(),
                        'chapter_number': chapter_info['number'],
                        'type': chapter_info['type'],
                        'page': page_num,
                        'line_position': i,
                        'confidence': 0.9
                    })
        
        return chapters
    
    def _extract_chapter_info(self, chapter_line: str) -> Dict:
        """Extract chapter number and type from chapter line"""
        # Try to find chapter number
        roman_match = re.search(r'[IVXLCDM]+', chapter_line)
        arabic_match = re.search(r'\d+', chapter_line)
        
        chapter_type = 'chapter'
        if 'part' in chapter_line.lower() or 'parte' in chapter_line.lower():
            chapter_type = 'part'
        elif 'section' in chapter_line.lower() or 'seção' in chapter_line.lower():
            chapter_type = 'section'
        
        number = None
        if arabic_match:
            number = int(arabic_match.group())
        elif roman_match:
            number = self._roman_to_int(roman_match.group())
        
        return {
            'number': number,
            'type': chapter_type
        }
    
    def _roman_to_int(self, s: str) -> int:
        """Convert Roman numerals to integers"""
        roman = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
        result = 0
        prev_value = 0
        
        for char in reversed(s):
            value = roman.get(char, 0)
            if value < prev_value:
                result -= value
            else:
                result += value
            prev_value = value
        
        return result
    
    def organize_text_for_audiobook(self, pages_data: List[Dict], chapters: List[Dict]) -> Dict:
        """
        Organize text into a structured format optimized for audiobook production
        
        Args:
            pages_data: List of page dictionaries
            chapters: List of detected chapters
            
        Returns:
            Structured content dictionary
        """
        structured_content = {
            'metadata': {
                'total_pages': len(pages_data),
                'total_chapters': len(chapters),
                'estimated_reading_time': self._estimate_reading_time(pages_data)
            },
            'chapters': []
        }
        
        # Organize content by chapters
        for i, chapter in enumerate(chapters):
            start_page = chapter['page']
            end_page = chapters[i + 1]['page'] if i + 1 < len(chapters) else len(pages_data) + 1
            
            # Extract chapter content
            chapter_content = self._extract_chapter_content(
                pages_data, start_page, end_page, chapter['line_position']
            )
            
            structured_content['chapters'].append({
                'number': chapter.get('chapter_number'),
                'title': chapter['title'],
                'type': chapter.get('type', 'chapter'),
                'page_range': [start_page, end_page - 1],
                'content': chapter_content['text'],
                'paragraphs': chapter_content['paragraphs'],
                'word_count': chapter_content['word_count'],
                'estimated_duration': chapter_content['estimated_duration']
            })
        
        return structured_content
    
    def _extract_chapter_content(self, pages_data: List[Dict], 
                                  start_page: int, end_page: int,
                                  start_line: int = 0) -> Dict:
        """Extract and organize content for a chapter"""
        content_lines = []
        paragraphs = []
        current_paragraph = []
        
        for page in pages_data:
            page_num = page['page_number']
            
            if start_page <= page_num < end_page:
                lines = page['text'].split('\n')
                
                # Skip to start line on first page
                start_idx = start_line + 1 if page_num == start_page else 0
                
                for i, line in enumerate(lines[start_idx:], start=start_idx):
                    line_type = self.classify_line_type(line, i, len(lines))
                    
                    if line_type == 'content':
                        content_lines.append(line.strip())
                        
                        # Build paragraphs
                        if line.strip():
                            current_paragraph.append(line.strip())
                        elif current_paragraph:
                            paragraphs.append(' '.join(current_paragraph))
                            current_paragraph = []
        
        # Add last paragraph if exists
        if current_paragraph:
            paragraphs.append(' '.join(current_paragraph))
        
        full_text = ' '.join(content_lines)
        word_count = len(full_text.split())
        
        return {
            'text': full_text,
            'paragraphs': paragraphs,
            'word_count': word_count,
            'estimated_duration': self._estimate_duration(word_count)
        }
    
    def _estimate_reading_time(self, pages_data: List[Dict]) -> Dict:
        """Estimate total reading time"""
        total_words = 0
        for page in pages_data:
            total_words += len(page['text'].split())
        
        return self._estimate_duration(total_words)
    
    def _estimate_duration(self, word_count: int) -> Dict:
        """Estimate duration based on word count"""
        # Average reading speed: 150-160 words per minute
        slow_wpm = 130
        medium_wpm = 150
        fast_wpm = 180
        
        return {
            'slow': round(word_count / slow_wpm, 1),
            'medium': round(word_count / medium_wpm, 1),
            'fast': round(word_count / fast_wpm, 1)
        }
    
    def extract_footnotes_and_references(self, pages_data: List[Dict]) -> Dict:
        """Extract footnotes and references from text"""
        footnotes = []
        references = []
        
        for page in pages_data:
            lines = page['text'].split('\n')
            page_num = page['page_number']
            
            for i, line in enumerate(lines):
                line_type = self.classify_line_type(line, i, len(lines))
                
                if line_type == 'footnote':
                    footnotes.append({
                        'page': page_num,
                        'text': line.strip(),
                        'number': self._extract_footnote_number(line)
                    })
                elif line_type == 'reference':
                    references.append({
                        'page': page_num,
                        'text': line.strip()
                    })
        
        return {
            'footnotes': footnotes,
            'references': references
        }
    
    def _extract_footnote_number(self, line: str) -> Optional[int]:
        """Extract footnote number from line"""
        match = re.match(r'^\s*(\d+)\s+', line)
        if match:
            return int(match.group(1))
        return None
    
    def identify_document_structure(self, pages_data: List[Dict]) -> Dict:
        """
        Analyze document to identify overall structure
        
        Returns:
            Dictionary with document structure information
        """
        structure = {
            'has_table_of_contents': False,
            'has_introduction': False,
            'has_preface': False,
            'has_epilogue': False,
            'has_bibliography': False,
            'has_index': False,
            'sections': []
        }
        
        # Scan first few pages for special sections
        for page in pages_data[:10]:
            text_lower = page['text'].lower()
            
            if 'table of contents' in text_lower or 'índice' in text_lower:
                structure['has_table_of_contents'] = True
            if 'introduction' in text_lower or 'introdução' in text_lower:
                structure['has_introduction'] = True
            if 'preface' in text_lower or 'prefácio' in text_lower:
                structure['has_preface'] = True
        
        # Scan last few pages for special sections
        for page in pages_data[-10:]:
            text_lower = page['text'].lower()
            
            if 'epilogue' in text_lower or 'epílogo' in text_lower:
                structure['has_epilogue'] = True
            if 'bibliography' in text_lower or 'bibliografia' in text_lower:
                structure['has_bibliography'] = True
            if 'index' in text_lower:
                structure['has_index'] = True
        
        return structure
