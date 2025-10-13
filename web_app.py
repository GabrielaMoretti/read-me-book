"""
Web Application using FastAPI
Modern web interface for PDF to Audiobook converter
"""
from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import os
import uuid
import json
from datetime import datetime
from pathlib import Path
import sqlite3
from pdf_processor import PDFProcessor
from tts_engine import TTSEngine
import base64
import io

app = FastAPI(title="Read Me Book", description="PDF to Audiobook Converter")

# Setup directories
UPLOAD_DIR = Path("uploads")
STATIC_DIR = Path("static")
TEMPLATES_DIR = Path("templates")

UPLOAD_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Setup templates
templates = Jinja2Templates(directory="templates")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize TTS engine (optional)
try:
    tts_engine = TTSEngine()
    print("✓ TTS Engine initialized successfully")
except Exception as e:
    print(f"⚠ TTS Engine initialization failed: {e}")
    print("  Web interface will work without TTS functionality")
    tts_engine = None

# Database setup
def init_database():
    """Initialize SQLite database"""
    conn = sqlite3.connect('audiobooks.db')
    cursor = conn.cursor()
    
    # Books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            filename TEXT NOT NULL,
            file_path TEXT NOT NULL,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_pages INTEGER,
            total_chapters INTEGER,
            current_chapter INTEGER DEFAULT 0,
            current_position INTEGER DEFAULT 0
        )
    ''')
    
    # Chapters table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT,
            chapter_number INTEGER,
            title TEXT,
            start_page INTEGER,
            end_page INTEGER,
            content TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    # Annotations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT,
            chapter_id INTEGER,
            annotation_text TEXT,
            position INTEGER,
            created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (book_id) REFERENCES books (id),
            FOREIGN KEY (chapter_id) REFERENCES chapters (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_database()

class BookManager:
    """Manages book operations and database interactions"""
    
    @staticmethod
    def save_book(book_id: str, title: str, filename: str, file_path: str, processor: PDFProcessor):
        """Save book information to database"""
        conn = sqlite3.connect('audiobooks.db')
        cursor = conn.cursor()
        
        # Save book
        cursor.execute('''
            INSERT OR REPLACE INTO books 
            (id, title, filename, file_path, total_pages, total_chapters)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (book_id, title, filename, file_path, len(processor.pages), len(processor.chapters)))
        
        # Save chapters
        cursor.execute('DELETE FROM chapters WHERE book_id = ?', (book_id,))
        for i, chapter in enumerate(processor.chapters):
            cursor.execute('''
                INSERT INTO chapters 
                (book_id, chapter_number, title, start_page, content)
                VALUES (?, ?, ?, ?, ?)
            ''', (book_id, i, chapter['title'], chapter['page'], processor.get_chapter_text(i)))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_books():
        """Get all books from database"""
        conn = sqlite3.connect('audiobooks.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books ORDER BY upload_date DESC')
        books = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': book[0],
                'title': book[1],
                'filename': book[2],
                'upload_date': book[4],
                'total_pages': book[5],
                'total_chapters': book[6],
                'current_chapter': book[7]
            }
            for book in books
        ]
    
    @staticmethod
    def get_book(book_id: str):
        """Get specific book with chapters"""
        conn = sqlite3.connect('audiobooks.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
        book = cursor.fetchone()
        
        if not book:
            conn.close()
            return None
        
        cursor.execute('SELECT * FROM chapters WHERE book_id = ? ORDER BY chapter_number', (book_id,))
        chapters = cursor.fetchall()
        
        conn.close()
        
        return {
            'id': book[0],
            'title': book[1],
            'filename': book[2],
            'file_path': book[3],
            'total_pages': book[5],
            'total_chapters': book[6],
            'current_chapter': book[7],
            'chapters': [
                {
                    'id': ch[0],
                    'number': ch[2],
                    'title': ch[3],
                    'start_page': ch[4],
                    'content': ch[6]
                }
                for ch in chapters
            ]
        }
    
    @staticmethod
    def save_annotation(book_id: str, chapter_id: int, text: str, position: int = 0):
        """Save annotation for a chapter"""
        conn = sqlite3.connect('audiobooks.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO annotations (book_id, chapter_id, annotation_text, position)
            VALUES (?, ?, ?, ?)
        ''', (book_id, chapter_id, text, position))
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_annotations(book_id: str, chapter_id: int = None):
        """Get annotations for book or specific chapter"""
        conn = sqlite3.connect('audiobooks.db')
        cursor = conn.cursor()
        
        if chapter_id:
            cursor.execute('''
                SELECT * FROM annotations 
                WHERE book_id = ? AND chapter_id = ?
                ORDER BY created_date DESC
            ''', (book_id, chapter_id))
        else:
            cursor.execute('''
                SELECT * FROM annotations 
                WHERE book_id = ?
                ORDER BY created_date DESC
            ''', (book_id,))
        
        annotations = cursor.fetchall()
        conn.close()
        
        return [
            {
                'id': ann[0],
                'text': ann[3],
                'position': ann[4],
                'created_date': ann[5]
            }
            for ann in annotations
        ]

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with book library"""
    books = BookManager.get_books()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})

@app.get("/reader/{book_id}", response_class=HTMLResponse)
async def reader(request: Request, book_id: str):
    """Book reader interface"""
    book = BookManager.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return templates.TemplateResponse("reader.html", {"request": request, "book": book})

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload and process PDF"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Generate unique ID for the book
    book_id = str(uuid.uuid4())
    
    # Save uploaded file
    file_path = UPLOAD_DIR / f"{book_id}_{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Process PDF
        processor = PDFProcessor(str(file_path))
        pages = processor.extract_text()
        chapters = processor.detect_chapters()
        
        # Save to database
        title = file.filename.replace('.pdf', '')
        BookManager.save_book(book_id, title, file.filename, str(file_path), processor)
        
        return JSONResponse({
            "success": True,
            "book_id": book_id,
            "title": title,
            "pages": len(pages),
            "chapters": len(chapters)
        })
        
    except Exception as e:
        # Clean up file if processing failed
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

@app.get("/api/book/{book_id}")
async def get_book_api(book_id: str):
    """Get book details API"""
    book = BookManager.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.get("/api/book/{book_id}/chapter/{chapter_number}")
async def get_chapter(book_id: str, chapter_number: int):
    """Get specific chapter content"""
    book = BookManager.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if chapter_number >= len(book['chapters']):
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter = book['chapters'][chapter_number]
    annotations = BookManager.get_annotations(book_id, chapter['id'])
    
    return {
        "chapter": chapter,
        "annotations": annotations
    }

@app.post("/api/book/{book_id}/chapter/{chapter_id}/annotation")
async def add_annotation(book_id: str, chapter_id: int, annotation: dict):
    """Add annotation to chapter"""
    text = annotation.get('text', '').strip()
    position = annotation.get('position', 0)
    
    if not text:
        raise HTTPException(status_code=400, detail="Annotation text is required")
    
    BookManager.save_annotation(book_id, chapter_id, text, position)
    return {"success": True, "message": "Annotation saved"}

@app.post("/api/tts/speak")
async def speak_text(data: dict):
    """Convert text to speech"""
    text = data.get('text', '')
    if not text:
        raise HTTPException(status_code=400, detail="Text is required")
    
    try:
        if tts_engine:
            # Use server-side TTS if available
            # For web implementation, the actual TTS is handled by the browser
            return {"success": True, "message": "Text will be spoken via browser TTS"}
        else:
            return {"success": True, "message": "Using browser Web Speech API for TTS"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS Error: {str(e)}")

@app.delete("/api/book/{book_id}")
async def delete_book(book_id: str):
    """Delete book and its data"""
    book = BookManager.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Delete file
    file_path = Path(book['file_path'])
    if file_path.exists():
        file_path.unlink()
    
    # Delete from database
    conn = sqlite3.connect('audiobooks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM annotations WHERE book_id = ?', (book_id,))
    cursor.execute('DELETE FROM chapters WHERE book_id = ?', (book_id,))
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    
    return {"success": True, "message": "Book deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)