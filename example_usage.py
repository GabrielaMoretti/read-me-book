"""
Example Usage Script
Demonstrates how to use the PDF processor and TTS engine without GUI
"""
from pdf_processor import PDFProcessor
from tts_engine import TTSEngine


def process_pdf_example(pdf_path: str):
    """Example of processing a PDF"""
    print(f"Processing PDF: {pdf_path}")
    
    # Initialize processor
    processor = PDFProcessor(pdf_path)
    
    # Extract text
    print("Extracting text from PDF...")
    pages = processor.extract_text()
    print(f"  ✓ Extracted {len(pages)} pages")
    
    # Detect chapters
    print("Detecting chapters...")
    chapters = processor.detect_chapters()
    print(f"  ✓ Found {len(chapters)} chapters:")
    for i, chapter in enumerate(chapters):
        print(f"    {i+1}. {chapter['title']} (Page {chapter['page']})")
    
    # Get clean text
    text = processor.get_text_for_reading()
    print(f"  ✓ Total text length: {len(text)} characters")
    
    return processor


def tts_example(text: str):
    """Example of using text-to-speech"""
    print("\nInitializing Text-to-Speech engine...")
    
    try:
        # Initialize TTS
        tts = TTSEngine()
        
        # List available voices
        voices = tts.list_voices()
        print(f"  ✓ Available voices: {len(voices)}")
        for i, voice in enumerate(voices[:3]):  # Show first 3
            print(f"    {i+1}. {voice.name} ({voice.languages})")
        
        # Configure TTS
        print("\nConfiguring TTS settings...")
        tts.set_rate(150)  # words per minute
        tts.set_volume(0.9)  # 0.0 to 1.0
        print("  ✓ Rate: 150 WPM")
        print("  ✓ Volume: 0.9")
        
        # Note: Actual speech requires audio output
        print("\nNote: To hear the speech, run the GUI application (audiobook_app.py)")
        print("The TTS engine is ready to speak the text.")
        
        return tts
    except Exception as e:
        print(f"  ⚠ TTS engine requires audio libraries (espeak/sapi5)")
        print(f"  ⚠ Error: {type(e).__name__}")
        print("\n  On Linux, install: sudo apt-get install espeak")
        print("  On Windows/Mac, pyttsx3 uses native TTS engines")
        print("\n  The TTS module is ready and will work when audio is available.")
        return None


def main():
    """Main example function"""
    print("=" * 60)
    print("Read Me Book - Example Usage")
    print("=" * 60)
    
    # Example 1: PDF Processing (without actual file)
    print("\n--- Example 1: PDF Processing ---")
    print("Usage:")
    print("  processor = PDFProcessor('your_book.pdf')")
    print("  pages = processor.extract_text()")
    print("  chapters = processor.detect_chapters()")
    print("  text = processor.get_text_for_reading()")
    
    # Example 2: Text-to-Speech
    print("\n--- Example 2: Text-to-Speech ---")
    sample_text = "Hello! This is a sample text for the audiobook reader."
    tts = tts_example(sample_text)
    
    # Example 3: Combined workflow
    print("\n--- Example 3: Complete Workflow ---")
    print("1. Load PDF with PDFProcessor")
    print("2. Extract and clean text")
    print("3. Detect chapters")
    print("4. Initialize TTSEngine")
    print("5. Read chapter by chapter or full document")
    
    print("\n" + "=" * 60)
    print("To use the full application with GUI:")
    print("  python audiobook_app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()
