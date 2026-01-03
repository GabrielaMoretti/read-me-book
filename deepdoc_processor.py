"""
Advanced PDF Layout Extraction using deepdoctection
Provides enhanced layout analysis for complex PDFs with columns, tables, and images
"""
import warnings
warnings.filterwarnings('ignore')

from typing import List, Dict, Optional, TYPE_CHECKING

# Check if deepdoctection is available
try:
    from deepdoctection import analyzer
    from deepdoctection.datapoint import Page
    DEEPDOC_AVAILABLE = True
except ImportError:
    DEEPDOC_AVAILABLE = False
    if TYPE_CHECKING:
        from deepdoctection.datapoint import Page


class DeepDocProcessor:
    """
    Advanced PDF processor using deepdoctection for layout analysis
    Handles complex PDFs with columns, tables, images, and structured layouts
    """
    
    def __init__(self, language: str = 'en'):
        """
        Initialize deepdoctection processor
        
        Args:
            language: Document language ('en', 'pt', etc.)
        """
        if not DEEPDOC_AVAILABLE:
            raise ImportError(
                "deepdoctection not available. Install with:\n"
                "pip install deepdoctection[pt]\n"
                "Note: This is a heavy dependency with significant disk space requirements"
            )
        
        self.language = language
        self.analyzer = None
        self._initialize_analyzer()
    
    def _initialize_analyzer(self):
        """Initialize the deepdoctection analyzer with optimal settings"""
        try:
            # Create analyzer with layout detection enabled
            # Note: Using default model configuration for better compatibility
            # Models are automatically managed by deepdoctection
            self.analyzer = analyzer.get_dd_analyzer()
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize deepdoctection analyzer: {str(e)}\n"
                "Please ensure all model dependencies are properly installed."
            )
    
    def extract_text_with_layout(self, pdf_path: str) -> List[Dict]:
        """
        Extract text with advanced layout analysis
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of page dictionaries with enhanced layout information
        """
        if not self.analyzer:
            raise RuntimeError("Analyzer not initialized")
        
        pages_data = []
        
        try:
            # Analyze document
            df = self.analyzer.analyze(path=pdf_path)
            
            for page_idx, page in enumerate(df, start=1):
                page_data = self._process_page(page, page_idx)
                pages_data.append(page_data)
        
        except Exception as e:
            raise RuntimeError(f"deepdoctection processing failed: {str(e)}")
        
        return pages_data
    
    def _process_page(self, page: 'Page', page_number: int) -> Dict:
        """
        Process a single page with layout analysis
        
        Args:
            page: deepdoctection Page object
            page_number: Page number (1-indexed)
            
        Returns:
            Dictionary with page data and layout information
        """
        # Extract text content in reading order
        text_content = []
        layout_elements = []
        
        # Get all layout elements sorted by reading order
        if hasattr(page, 'layouts'):
            for layout in page.layouts:
                element_info = {
                    'type': layout.category_name if hasattr(layout, 'category_name') else 'text',
                    'text': layout.text if hasattr(layout, 'text') else '',
                    'bbox': self._get_bbox(layout),
                    'reading_order': layout.reading_order if hasattr(layout, 'reading_order') else 0
                }
                
                layout_elements.append(element_info)
                
                # Collect text in reading order
                if element_info['text']:
                    text_content.append(element_info['text'])
        
        # Sort by reading order
        layout_elements.sort(key=lambda x: x['reading_order'])
        
        # Combine all text
        full_text = '\n'.join(text_content)
        
        return {
            'page_number': page_number,
            'text': full_text,
            'layout_elements': layout_elements,
            'has_tables': any(el['type'] == 'table' for el in layout_elements),
            'has_images': any(el['type'] == 'figure' for el in layout_elements),
            'columns': self._detect_columns(layout_elements)
        }
    
    def _get_bbox(self, layout) -> Optional[Dict]:
        """Extract bounding box from layout element"""
        if hasattr(layout, 'bbox'):
            bbox = layout.bbox
            return {
                'x': bbox.x if hasattr(bbox, 'x') else 0,
                'y': bbox.y if hasattr(bbox, 'y') else 0,
                'width': bbox.width if hasattr(bbox, 'width') else 0,
                'height': bbox.height if hasattr(bbox, 'height') else 0
            }
        return None
    
    def _detect_columns(self, layout_elements: List[Dict]) -> int:
        """
        Detect number of columns in layout
        
        Args:
            layout_elements: List of layout elements with bounding boxes
            
        Returns:
            Estimated number of columns
        """
        if not layout_elements:
            return 1
        
        # Simple column detection based on x-coordinates clustering
        x_coords = []
        for elem in layout_elements:
            if elem['bbox']:
                x_coords.append(elem['bbox']['x'])
        
        if not x_coords or len(x_coords) <= 1:
            return 1
        
        # Use a simple heuristic: if elements are widely separated horizontally, likely multi-column
        x_coords.sort()
        gaps = []
        for i in range(1, len(x_coords)):
            gaps.append(x_coords[i] - x_coords[i-1])
        
        # If we have significant gaps, likely multi-column
        if gaps:
            avg_gap = sum(gaps) / len(gaps)
            large_gaps = [g for g in gaps if g > avg_gap * 2]
            return len(large_gaps) + 1
        
        return 1
    
    def extract_tables(self, pdf_path: str) -> List[Dict]:
        """
        Extract tables from PDF with structure preservation
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            List of table dictionaries with data and metadata
        """
        if not self.analyzer:
            raise RuntimeError("Analyzer not initialized")
        
        tables = []
        
        try:
            df = self.analyzer.analyze(path=pdf_path)
            
            for page_idx, page in enumerate(df, start=1):
                if hasattr(page, 'tables'):
                    for table_idx, table in enumerate(page.tables):
                        table_data = {
                            'page': page_idx,
                            'table_number': table_idx + 1,
                            'data': self._extract_table_data(table),
                            'bbox': self._get_bbox(table) if hasattr(table, 'bbox') else None
                        }
                        tables.append(table_data)
        
        except Exception as e:
            raise RuntimeError(f"Table extraction failed: {str(e)}")
        
        return tables
    
    def _extract_table_data(self, table) -> List[List[str]]:
        """Extract structured data from table"""
        data = []
        
        if hasattr(table, 'rows'):
            for row in table.rows:
                row_data = []
                if hasattr(row, 'cells'):
                    for cell in row.cells:
                        cell_text = cell.text if hasattr(cell, 'text') else ''
                        row_data.append(cell_text)
                data.append(row_data)
        
        return data
    
    def get_document_structure(self, pdf_path: str) -> Dict:
        """
        Analyze overall document structure
        
        Args:
            pdf_path: Path to PDF file
            
        Returns:
            Dictionary with document structure analysis
        """
        pages_data = self.extract_text_with_layout(pdf_path)
        
        # Compute statistics in single pass for better performance
        total_tables = 0
        total_images = 0
        max_columns = 1
        
        for page in pages_data:
            if page['has_tables']:
                total_tables += 1
            if page['has_images']:
                total_images += 1
            if page['columns'] > max_columns:
                max_columns = page['columns']
        
        return {
            'total_pages': len(pages_data),
            'total_tables': total_tables,
            'total_images': total_images,
            'max_columns': max_columns,
            'has_complex_layout': max_columns > 1 or total_tables > 0,
            'pages': pages_data
        }
    
    @staticmethod
    def is_available() -> bool:
        """Check if deepdoctection is available"""
        return DEEPDOC_AVAILABLE
