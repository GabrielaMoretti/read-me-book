"""
Modern Audiobook Application GUI with Enhanced Features
Uses ttkbootstrap for modern UI design
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import json
from pathlib import Path

try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    MODERN_UI = True
except ImportError:
    import tkinter.ttk as ttk
    MODERN_UI = False

from pdf_processor import PDFProcessor
from tts_engine import TTSEngine


class ModernAudiobookApp:
    """Modern audiobook application with enhanced UI and features"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Read Me Book - AI-Powered Audiobook Creator")
        self.root.geometry("1200x800")
        
        # Application state
        self.pdf_processor = None
        self.tts_engine = TTSEngine()
        self.current_chapter = 0
        self.is_reading = False
        self.dark_mode = False
        
        # Setup UI
        self._setup_modern_ui()
        
        # Keyboard shortcuts
        self._setup_shortcuts()
    
    def _setup_modern_ui(self):
        """Setup modern user interface"""
        # Configure theme
        if MODERN_UI:
            self.style = ttk.Style("darkly" if self.dark_mode else "cosmo")
        
        # Main container with padding
        main_container = ttk.Frame(self.root, padding=0)
        main_container.pack(fill=BOTH, expand=YES)
        
        # Top toolbar
        self._create_toolbar(main_container)
        
        # Content area with sidebar and main panel
        content_paned = ttk.PanedWindow(main_container, orient=HORIZONTAL)
        content_paned.pack(fill=BOTH, expand=YES, padx=5, pady=5)
        
        # Left sidebar for chapters
        self._create_sidebar(content_paned)
        
        # Right panel for text and controls
        self._create_main_panel(content_paned)
        
        # Status bar
        self._create_status_bar(main_container)
    
    def _create_toolbar(self, parent):
        """Create top toolbar with file and control buttons"""
        toolbar = ttk.Frame(parent, padding=10)
        toolbar.pack(fill=X, side=TOP)
        
        # File operations
        btn_frame_left = ttk.Frame(toolbar)
        btn_frame_left.pack(side=LEFT)
        
        self.load_btn = ttk.Button(
            btn_frame_left,
            text="📁 Load PDF",
            command=self.load_pdf,
            bootstyle="primary" if MODERN_UI else None,
            width=15
        )
        self.load_btn.pack(side=LEFT, padx=5)
        
        self.export_btn = ttk.Button(
            btn_frame_left,
            text="💾 Export Structure",
            command=self.export_structure,
            bootstyle="info" if MODERN_UI else None,
            width=15,
            state=DISABLED
        )
        self.export_btn.pack(side=LEFT, padx=5)
        
        # Playback controls
        btn_frame_center = ttk.Frame(toolbar)
        btn_frame_center.pack(side=LEFT, padx=50)
        
        self.play_btn = ttk.Button(
            btn_frame_center,
            text="▶ Play",
            command=self.toggle_play,
            bootstyle="success" if MODERN_UI else None,
            width=12,
            state=DISABLED
        )
        self.play_btn.pack(side=LEFT, padx=5)
        
        self.pause_btn = ttk.Button(
            btn_frame_center,
            text="⏸ Pause",
            command=self.pause_reading,
            bootstyle="warning" if MODERN_UI else None,
            width=12,
            state=DISABLED
        )
        self.pause_btn.pack(side=LEFT, padx=5)
        
        self.stop_btn = ttk.Button(
            btn_frame_center,
            text="⬛ Stop",
            command=self.stop_reading,
            bootstyle="danger" if MODERN_UI else None,
            width=12,
            state=DISABLED
        )
        self.stop_btn.pack(side=LEFT, padx=5)
        
        # Settings
        btn_frame_right = ttk.Frame(toolbar)
        btn_frame_right.pack(side=RIGHT)
        
        self.theme_btn = ttk.Button(
            btn_frame_right,
            text="🌙 Dark Mode" if not self.dark_mode else "☀️ Light Mode",
            command=self.toggle_theme,
            bootstyle="secondary" if MODERN_UI else None,
            width=15
        )
        self.theme_btn.pack(side=RIGHT, padx=5)
    
    def _create_sidebar(self, parent):
        """Create sidebar with chapter navigation"""
        sidebar_frame = ttk.Frame(parent, padding=10)
        parent.add(sidebar_frame, weight=1)
        
        # Sidebar header
        header = ttk.Label(
            sidebar_frame,
            text="📚 Chapters",
            font=("Helvetica", 14, "bold")
        )
        header.pack(fill=X, pady=(0, 10))
        
        # Chapter filter
        filter_frame = ttk.Frame(sidebar_frame)
        filter_frame.pack(fill=X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="🔍").pack(side=LEFT, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_chapters)
        search_entry = ttk.Entry(filter_frame, textvariable=self.search_var)
        search_entry.pack(side=LEFT, fill=X, expand=YES)
        
        # Chapter list with scrollbar
        list_frame = ttk.Frame(sidebar_frame)
        list_frame.pack(fill=BOTH, expand=YES)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        self.chapter_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("Helvetica", 11),
            selectmode=SINGLE,
            relief=FLAT,
            highlightthickness=0
        )
        self.chapter_listbox.pack(side=LEFT, fill=BOTH, expand=YES)
        self.chapter_listbox.bind('<<ListboxSelect>>', self.on_chapter_select)
        scrollbar.config(command=self.chapter_listbox.yview)
        
        # Chapter info
        self.chapter_info_label = ttk.Label(
            sidebar_frame,
            text="No chapters loaded",
            font=("Helvetica", 9),
            justify=CENTER
        )
        self.chapter_info_label.pack(fill=X, pady=(10, 0))
    
    def _create_main_panel(self, parent):
        """Create main content panel"""
        main_frame = ttk.Frame(parent, padding=10)
        parent.add(main_frame, weight=3)
        
        # Control panel
        control_panel = ttk.Labelframe(
            main_frame,
            text="⚙️ Reading Settings",
            padding=10
        )
        control_panel.pack(fill=X, pady=(0, 10))
        
        # Speed control
        speed_frame = ttk.Frame(control_panel)
        speed_frame.pack(fill=X, pady=5)
        
        ttk.Label(speed_frame, text="Speed (WPM):").pack(side=LEFT, padx=(0, 10))
        self.speed_var = tk.IntVar(value=150)
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=50,
            to=300,
            variable=self.speed_var,
            command=self.change_speed,
            bootstyle="info" if MODERN_UI else None
        )
        self.speed_scale.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        self.speed_label = ttk.Label(speed_frame, text="150", width=5)
        self.speed_label.pack(side=LEFT)
        
        # Volume control
        volume_frame = ttk.Frame(control_panel)
        volume_frame.pack(fill=X, pady=5)
        
        ttk.Label(volume_frame, text="Volume:").pack(side=LEFT, padx=(0, 10))
        self.volume_var = tk.DoubleVar(value=0.9)
        self.volume_scale = ttk.Scale(
            volume_frame,
            from_=0.0,
            to=1.0,
            variable=self.volume_var,
            command=self.change_volume,
            bootstyle="success" if MODERN_UI else None
        )
        self.volume_scale.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        self.volume_label = ttk.Label(volume_frame, text="90%", width=5)
        self.volume_label.pack(side=LEFT)
        
        # Text display area
        text_frame = ttk.Labelframe(
            main_frame,
            text="📖 Content",
            padding=10
        )
        text_frame.pack(fill=BOTH, expand=YES)
        
        # Create text widget with scrollbar
        text_container = ttk.Frame(text_frame)
        text_container.pack(fill=BOTH, expand=YES)
        
        text_scroll = ttk.Scrollbar(text_container)
        text_scroll.pack(side=RIGHT, fill=Y)
        
        self.text_display = tk.Text(
            text_container,
            wrap=WORD,
            yscrollcommand=text_scroll.set,
            font=("Georgia", 12),
            padx=20,
            pady=20,
            spacing3=8,
            relief=FLAT
        )
        self.text_display.pack(side=LEFT, fill=BOTH, expand=YES)
        text_scroll.config(command=self.text_display.yview)
        
        # Configure text tags
        self.text_display.tag_configure("highlight", background="#FFD700", foreground="#000")
        self.text_display.tag_configure("chapter_title", font=("Georgia", 16, "bold"), spacing1=10, spacing3=10)
    
    def _create_status_bar(self, parent):
        """Create bottom status bar"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=X, side=BOTTOM)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready to load PDF",
            font=("Helvetica", 10),
            padding=5
        )
        self.status_label.pack(side=LEFT, fill=X, expand=YES)
        
        self.progress_bar = ttk.Progressbar(
            status_frame,
            mode='indeterminate',
            bootstyle="info" if MODERN_UI else None
        )
        self.progress_bar.pack(side=RIGHT, padx=5)
    
    def _setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        self.root.bind('<Control-o>', lambda e: self.load_pdf())
        self.root.bind('<Control-s>', lambda e: self.export_structure())
        self.root.bind('<space>', lambda e: self.toggle_play())
        self.root.bind('<Escape>', lambda e: self.stop_reading())
        self.root.bind('<Control-d>', lambda e: self.toggle_theme())
    
    def load_pdf(self):
        """Load a PDF file"""
        filename = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        self.status_label.config(text=f"Loading {Path(filename).name}...")
        self.progress_bar.start()
        self.root.update()
        
        # Load in background thread
        thread = threading.Thread(target=self._load_pdf_thread, args=(filename,))
        thread.daemon = True
        thread.start()
    
    def _load_pdf_thread(self, filename):
        """Load PDF in background thread"""
        try:
            # Create processor with AI enabled
            self.pdf_processor = PDFProcessor(filename, use_ai=True)
            self.pdf_processor.extract_text()
            chapters = self.pdf_processor.detect_chapters()
            
            # Update UI on main thread
            self.root.after(0, lambda: self._update_after_load(filename, chapters))
            
        except Exception as e:
            self.root.after(0, lambda: self._show_load_error(str(e)))
    
    def _update_after_load(self, filename, chapters):
        """Update UI after PDF is loaded"""
        self.progress_bar.stop()
        
        # Update chapter list
        self.chapter_listbox.delete(0, END)
        if chapters:
            for i, chapter in enumerate(chapters):
                display_text = f"{i+1}. {chapter['title']}"
                self.chapter_listbox.insert(END, display_text)
            self.chapter_info_label.config(text=f"{len(chapters)} chapters found")
        else:
            self.chapter_listbox.insert(END, "Full Document")
            self.chapter_info_label.config(text="No chapters detected")
        
        # Display text
        text = self.pdf_processor.get_text_for_reading()
        self.text_display.delete(1.0, END)
        self.text_display.insert(1.0, text)
        
        # Enable controls
        self.play_btn.config(state=NORMAL)
        self.pause_btn.config(state=NORMAL)
        self.stop_btn.config(state=NORMAL)
        self.export_btn.config(state=NORMAL)
        
        pages = len(self.pdf_processor.pages)
        self.status_label.config(text=f"Loaded: {Path(filename).name} ({pages} pages, {len(chapters)} chapters)")
    
    def _show_load_error(self, error):
        """Show error message"""
        self.progress_bar.stop()
        messagebox.showerror("Error", f"Failed to load PDF: {error}")
        self.status_label.config(text="Error loading PDF")
    
    def toggle_play(self):
        """Toggle play/pause"""
        if self.is_reading:
            self.pause_reading()
        else:
            self.start_reading()
    
    def start_reading(self):
        """Start reading the text"""
        if not self.pdf_processor:
            messagebox.showwarning("Warning", "Please load a PDF first")
            return
        
        self.is_reading = True
        self.play_btn.config(text="⏸ Pause")
        self.status_label.config(text="Reading...")
        
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
        self.play_btn.config(text="▶ Play")
        self.status_label.config(text="Finished reading")
    
    def pause_reading(self):
        """Pause reading"""
        if self.is_reading:
            self.tts_engine.stop()
            self.is_reading = False
            self.play_btn.config(text="▶ Play")
            self.status_label.config(text="Paused")
    
    def stop_reading(self):
        """Stop reading"""
        if self.is_reading:
            self.tts_engine.stop()
            self.is_reading = False
            self.play_btn.config(text="▶ Play")
            self.status_label.config(text="Stopped")
    
    def on_chapter_select(self, event):
        """Handle chapter selection"""
        selection = self.chapter_listbox.curselection()
        if selection:
            self.current_chapter = selection[0]
            
            # Update text display
            if self.pdf_processor and self.pdf_processor.chapters:
                text = self.pdf_processor.get_chapter_text(self.current_chapter)
                self.text_display.delete(1.0, END)
                
                # Add chapter title with formatting
                chapter = self.pdf_processor.chapters[self.current_chapter]
                self.text_display.insert(1.0, f"{chapter['title']}\n\n", "chapter_title")
                self.text_display.insert(END, text)
                
                self.status_label.config(text=f"Chapter: {chapter['title']}")
    
    def filter_chapters(self, *args):
        """Filter chapters based on search text"""
        search_text = self.search_var.get().lower()
        
        if not self.pdf_processor or not self.pdf_processor.chapters:
            return
        
        self.chapter_listbox.delete(0, END)
        
        for i, chapter in enumerate(self.pdf_processor.chapters):
            if search_text in chapter['title'].lower():
                display_text = f"{i+1}. {chapter['title']}"
                self.chapter_listbox.insert(END, display_text)
    
    def change_speed(self, value):
        """Change reading speed"""
        speed = int(float(value))
        self.tts_engine.set_rate(speed)
        self.speed_label.config(text=str(speed))
    
    def change_volume(self, value):
        """Change volume"""
        volume = float(value)
        self.tts_engine.set_volume(volume)
        self.volume_label.config(text=f"{int(volume * 100)}%")
    
    def export_structure(self):
        """Export document structure to JSON"""
        if not self.pdf_processor:
            messagebox.showwarning("Warning", "Please load a PDF first")
            return
        
        filename = filedialog.asksaveasfilename(
            title="Save structure as",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if not filename:
            return
        
        try:
            structure = self.pdf_processor.export_to_json()
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(structure, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Success", f"Structure exported to {Path(filename).name}")
            self.status_label.config(text=f"Exported to {Path(filename).name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {str(e)}")
    
    def toggle_theme(self):
        """Toggle between light and dark mode"""
        if not MODERN_UI:
            messagebox.showinfo("Info", "Install ttkbootstrap for theme support:\npip install ttkbootstrap")
            return
        
        self.dark_mode = not self.dark_mode
        theme = "darkly" if self.dark_mode else "cosmo"
        self.style.theme_use(theme)
        
        btn_text = "☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode"
        self.theme_btn.config(text=btn_text)


def main():
    """Main entry point"""
    if MODERN_UI:
        root = ttk.Window(themename="cosmo")
    else:
        root = tk.Tk()
    
    app = ModernAudiobookApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
