"""
Audiobook Application GUI
Main application with chapter navigation and text highlighting
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from pdf_processor import PDFProcessor
from tts_engine import TTSEngine


class AudiobookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Read Me Book - PDF to Audiobook")
        self.root.geometry("1000x700")
        
        self.pdf_processor = None
        self.tts_engine = TTSEngine()
        self.current_chapter = 0
        self.is_reading = False
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the user interface"""
        # Top frame for controls
        control_frame = tk.Frame(self.root, bg="#2c3e50", height=60)
        control_frame.pack(side=tk.TOP, fill=tk.X)
        control_frame.pack_propagate(False)
        
        # Load PDF button
        self.load_btn = tk.Button(
            control_frame, 
            text="📁 Load PDF",
            command=self.load_pdf,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.load_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Play/Pause button
        self.play_btn = tk.Button(
            control_frame,
            text="▶ Play",
            command=self.toggle_play,
            bg="#27ae60",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.play_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Stop button
        self.stop_btn = tk.Button(
            control_frame,
            text="⬛ Stop",
            command=self.stop_reading,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10,
            state=tk.DISABLED
        )
        self.stop_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Speed control
        tk.Label(control_frame, text="Speed:", bg="#2c3e50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=(20, 5))
        self.speed_scale = tk.Scale(
            control_frame,
            from_=50,
            to=300,
            orient=tk.HORIZONTAL,
            command=self.change_speed,
            bg="#34495e",
            fg="white",
            highlightthickness=0
        )
        self.speed_scale.set(150)
        self.speed_scale.pack(side=tk.LEFT, padx=5)
        
        # Main content frame
        content_frame = tk.Frame(self.root)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Left sidebar for chapters
        self.chapter_frame = tk.Frame(content_frame, bg="#ecf0f1", width=250)
        self.chapter_frame.pack(side=tk.LEFT, fill=tk.Y)
        self.chapter_frame.pack_propagate(False)
        
        tk.Label(
            self.chapter_frame,
            text="Chapters",
            bg="#34495e",
            fg="white",
            font=("Arial", 14, "bold"),
            pady=10
        ).pack(fill=tk.X)
        
        # Chapter list
        chapter_scroll = tk.Scrollbar(self.chapter_frame)
        chapter_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.chapter_listbox = tk.Listbox(
            self.chapter_frame,
            yscrollcommand=chapter_scroll.set,
            bg="#ecf0f1",
            font=("Arial", 10),
            selectbackground="#3498db",
            selectmode=tk.SINGLE
        )
        self.chapter_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.chapter_listbox.bind('<<ListboxSelect>>', self.on_chapter_select)
        chapter_scroll.config(command=self.chapter_listbox.yview)
        
        # Right frame for text display
        text_frame = tk.Frame(content_frame)
        text_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Text display with scrollbar
        text_scroll = tk.Scrollbar(text_frame)
        text_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_display = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=text_scroll.set,
            bg="white",
            font=("Arial", 12),
            padx=20,
            pady=20,
            spacing3=5
        )
        self.text_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        text_scroll.config(command=self.text_display.yview)
        
        # Configure text tags for highlighting
        self.text_display.tag_configure("highlight", background="#ffeb3b", foreground="#000")
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready to load PDF",
            bg="#34495e",
            fg="white",
            anchor=tk.W,
            font=("Arial", 10),
            padx=10,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def load_pdf(self):
        """Load a PDF file"""
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        self.status_bar.config(text=f"Loading {filename}...")
        self.root.update()
        
        try:
            self.pdf_processor = PDFProcessor(filename)
            self.pdf_processor.extract_text()
            chapters = self.pdf_processor.detect_chapters()
            
            # Update chapter list
            self.chapter_listbox.delete(0, tk.END)
            if chapters:
                for i, chapter in enumerate(chapters):
                    self.chapter_listbox.insert(tk.END, f"{i+1}. {chapter['title']}")
            else:
                self.chapter_listbox.insert(tk.END, "Full Document")
            
            # Display text
            text = self.pdf_processor.get_text_for_reading()
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(1.0, text)
            
            # Enable controls
            self.play_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.NORMAL)
            
            self.status_bar.config(text=f"Loaded: {filename} ({len(self.pdf_processor.pages)} pages)")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load PDF: {str(e)}")
            self.status_bar.config(text="Error loading PDF")
    
    def toggle_play(self):
        """Toggle play/pause"""
        if self.is_reading:
            self.stop_reading()
        else:
            self.start_reading()
    
    def start_reading(self):
        """Start reading the text"""
        if not self.pdf_processor:
            messagebox.showwarning("Warning", "Please load a PDF first")
            return
        
        self.is_reading = True
        self.play_btn.config(text="⏸ Pause", bg="#f39c12")
        self.status_bar.config(text="Reading...")
        
        # Get text to read
        if self.current_chapter < len(self.pdf_processor.chapters):
            text = self.pdf_processor.get_chapter_text(self.current_chapter)
        else:
            text = self.pdf_processor.get_text_for_reading()
        
        # Start reading in a separate thread
        thread = threading.Thread(target=self._read_text, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _read_text(self, text):
        """Read text in a separate thread"""
        try:
            self.tts_engine.speak(text)
        except Exception as e:
            print(f"Error during reading: {e}")
        finally:
            self.is_reading = False
            self.root.after(0, self._reading_finished)
    
    def _reading_finished(self):
        """Called when reading is finished"""
        self.play_btn.config(text="▶ Play", bg="#27ae60")
        self.status_bar.config(text="Finished reading")
    
    def stop_reading(self):
        """Stop reading"""
        if self.is_reading:
            self.tts_engine.stop()
            self.is_reading = False
            self.play_btn.config(text="▶ Play", bg="#27ae60")
            self.status_bar.config(text="Stopped")
    
    def on_chapter_select(self, event):
        """Handle chapter selection"""
        selection = self.chapter_listbox.curselection()
        if selection:
            self.current_chapter = selection[0]
            
            # Update text display
            if self.pdf_processor and self.pdf_processor.chapters:
                text = self.pdf_processor.get_chapter_text(self.current_chapter)
                self.text_display.delete(1.0, tk.END)
                self.text_display.insert(1.0, text)
                
                chapter = self.pdf_processor.chapters[self.current_chapter]
                self.status_bar.config(text=f"Chapter: {chapter['title']}")
    
    def change_speed(self, value):
        """Change reading speed"""
        self.tts_engine.set_rate(int(float(value)))


def main():
    root = tk.Tk()
    app = AudiobookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
