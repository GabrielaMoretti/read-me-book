"""
Example Usage Script
Demonstrates how to use the enhanced PDF processor, AI analyzer, and TTS engine
"""
from pdf_processor import PDFProcessor, AI_AVAILABLE
from tts_engine import TTSEngine
from ai_text_analyzer import AITextAnalyzer
from ocr_processor import OCR_AVAILABLE
import json


def demo_basic_pdf_processing():
    """Example of basic PDF processing"""
    print("\n" + "=" * 70)
    print("DEMO 1: Basic PDF Processing")
    print("=" * 70)
    
    print("\nUsage:")
    print("  processor = PDFProcessor('your_book.pdf', use_ai=True)")
    print("  pages = processor.extract_text()")
    print("  chapters = processor.detect_chapters()")
    print("  text = processor.get_text_for_reading()")
    
    print("\nFeatures:")
    print("  ✓ Extract text from native PDFs")
    print("  ✓ Clean headers, footers, page numbers")
    print("  ✓ Detect chapters with AI patterns")
    print("  ✓ Support for both AI and basic modes")


def demo_ai_text_analysis():
    """Example of AI-powered text analysis"""
    print("\n" + "=" * 70)
    print("DEMO 2: AI-Powered Text Analysis")
    print("=" * 70)
    
    print("\nAI Analyzer Features:")
    print("  ✓ Intelligent content classification")
    print("  ✓ Advanced chapter detection")
    print("  ✓ Footnote and reference extraction")
    print("  ✓ Document structure analysis")
    print("  ✓ Audiobook-ready organization")
    
    if AI_AVAILABLE:
        print("\n✓ AI features are AVAILABLE")
        
        analyzer = AITextAnalyzer()
        
        # Demo line classification
        sample_lines = [
            ("Chapter 1: Introduction", 5, 50),
            ("This is the main content.", 10, 50),
            ("1", 48, 50),  # Page number
            ("Copyright 2024", 49, 50)
        ]
        
        print("\nLine Classification Examples:")
        for line, pos, total in sample_lines:
            line_type = analyzer.classify_line_type(line, pos, total)
            print(f"  '{line}' -> {line_type}")
    else:
        print("\n⚠ AI features not fully initialized (missing heavy ML dependencies)")
        print("  Basic pattern-based analysis is still available")


def demo_structured_content():
    """Example of structured content for audiobook"""
    print("\n" + "=" * 70)
    print("DEMO 3: Structured Content for Audiobook Production")
    print("=" * 70)
    
    print("\nUsage:")
    print("  processor = PDFProcessor('book.pdf', use_ai=True)")
    print("  processor.extract_text()")
    print("  processor.detect_chapters()")
    print("  structure = processor.get_structured_content_for_audiobook()")
    
    print("\nStructured Output Includes:")
    print("  • Chapter-by-chapter organization")
    print("  • Word counts per chapter")
    print("  • Estimated reading durations (slow/medium/fast)")
    print("  • Paragraph segmentation")
    print("  • Page range mapping")
    print("  • Document metadata")
    
    print("\nReading Time Estimation:")
    print("  • Slow: ~130 words/minute")
    print("  • Medium: ~150 words/minute")
    print("  • Fast: ~180 words/minute")


def demo_document_structure():
    """Example of document structure analysis"""
    print("\n" + "=" * 70)
    print("DEMO 4: Document Structure Analysis")
    print("=" * 70)
    
    print("\nUsage:")
    print("  structure = processor.get_document_structure()")
    
    print("\nDetects:")
    print("  ✓ Table of Contents")
    print("  ✓ Introduction/Preface")
    print("  ✓ Chapters and Sections")
    print("  ✓ Epilogue")
    print("  ✓ Bibliography")
    print("  ✓ Index")
    
    print("\nExample Output:")
    structure_example = {
        'has_table_of_contents': True,
        'has_introduction': True,
        'has_bibliography': True,
        'has_index': False
    }
    print(f"  {json.dumps(structure_example, indent=2)}")


def demo_export_features():
    """Example of export features"""
    print("\n" + "=" * 70)
    print("DEMO 5: Export to JSON")
    print("=" * 70)
    
    print("\nUsage:")
    print("  export_data = processor.export_to_json()")
    print("  with open('book_analysis.json', 'w') as f:")
    print("      json.dump(export_data, f, indent=2)")
    
    print("\nExport Contains:")
    print("  • Complete document analysis")
    print("  • All detected chapters")
    print("  • Structured content for audiobook")
    print("  • Document structure information")
    print("  • Footnotes and references")
    print("  • Reading time estimates")


def demo_ocr_support():
    """Example of OCR for scanned PDFs"""
    print("\n" + "=" * 70)
    print("DEMO 6: OCR Support for Scanned PDFs")
    print("=" * 70)
    
    if OCR_AVAILABLE:
        print("\n✓ OCR features are AVAILABLE")
        print("\nUsage:")
        print("  from ocr_processor import OCRProcessor")
        print("  ocr = OCRProcessor(language='eng')")
        print("  pages = ocr.extract_text_from_pdf('scanned.pdf')")
    else:
        print("\n⚠ OCR features NOT available")
        print("\nTo enable OCR:")
        print("  1. Install dependencies:")
        print("     pip install pytesseract pdf2image")
        print("  2. Install Tesseract:")
        print("     • Ubuntu/Debian: sudo apt-get install tesseract-ocr")
        print("     • macOS: brew install tesseract")
        print("     • Windows: Download from tesseract-ocr.github.io")
    
    print("\nSupported Languages:")
    print("  • English (eng)")
    print("  • Portuguese (por)")
    print("  • Spanish (spa)")
    print("  • And 100+ more languages")


def demo_tts_features():
    """Example of TTS features"""
    print("\n" + "=" * 70)
    print("DEMO 7: Text-to-Speech Engine")
    print("=" * 70)
    
    print("\nInitializing TTS engine...")
    
    try:
        tts = TTSEngine()
        
        # List available voices
        voices = tts.list_voices()
        print(f"\n✓ TTS Engine initialized successfully")
        print(f"  Available voices: {len(voices)}")
        
        if voices:
            print("\n  Sample voices:")
            for i, voice in enumerate(voices[:3]):
                print(f"    {i+1}. {voice.name}")
                print(f"       Languages: {voice.languages}")
        
        print("\nTTS Configuration:")
        print("  • Rate: 50-300 words per minute")
        print("  • Volume: 0.0 to 1.0")
        print("  • Multiple voice options")
        
        print("\nUsage:")
        print("  tts.set_rate(150)")
        print("  tts.set_volume(0.9)")
        print("  tts.speak('Your text here')")
        
    except Exception as e:
        print(f"\n⚠ TTS requires audio libraries")
        print(f"  Error: {type(e).__name__}")
        print("\n  Installation:")
        print("  • Linux: sudo apt-get install espeak")
        print("  • Windows: Built-in SAPI5")
        print("  • macOS: Built-in NSSpeechSynthesizer")


def demo_modern_ui():
    """Example of modern UI features"""
    print("\n" + "=" * 70)
    print("DEMO 8: Modern User Interface")
    print("=" * 70)
    
    print("\nRun the modern interface:")
    print("  python modern_audiobook_app.py")
    
    print("\nModern UI Features:")
    print("  ✨ Clean, professional design")
    print("  🌓 Dark mode / Light mode toggle")
    print("  🔍 Chapter search and filter")
    print("  ⌨️  Keyboard shortcuts")
    print("  🎛️  Visual controls for speed & volume")
    print("  📊 Progress indicators")
    print("  💾 Export structure to JSON")
    
    print("\nKeyboard Shortcuts:")
    print("  • Ctrl+O: Open PDF")
    print("  • Ctrl+S: Export structure")
    print("  • Space: Play/Pause")
    print("  • Esc: Stop reading")
    print("  • Ctrl+D: Toggle dark mode")
    
    print("\nClassic UI (Alternative):")
    print("  python audiobook_app.py")


def main():
    """Main example function"""
    print("=" * 70)
    print("READ ME BOOK - Enhanced Feature Demonstrations")
    print("AI-Powered PDF to Audiobook Converter")
    print("=" * 70)
    
    print(f"\nSystem Status:")
    print(f"  AI Analysis: {'✓ Available' if AI_AVAILABLE else '✗ Not available'}")
    print(f"  OCR Support: {'✓ Available' if OCR_AVAILABLE else '✗ Not available'}")
    
    # Run all demos
    demo_basic_pdf_processing()
    demo_ai_text_analysis()
    demo_structured_content()
    demo_document_structure()
    demo_export_features()
    demo_ocr_support()
    demo_tts_features()
    demo_modern_ui()
    
    # Summary
    print("\n" + "=" * 70)
    print("GETTING STARTED")
    print("=" * 70)
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\n2. Run the application:")
    print("   python modern_audiobook_app.py  # Modern UI (recommended)")
    print("   python audiobook_app.py         # Classic UI")
    
    print("\n3. Load a PDF and start reading!")
    
    print("\n" + "=" * 70)
    print("For more information, see README.md")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
