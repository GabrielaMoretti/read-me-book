"""
Read Me Book – Interface Principal
GUI moderna com ttkbootstrap (fallback para tkinter padrão).
"""
from __future__ import annotations

import json
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

# ── ttkbootstrap (opcional) ──────────────────────────────────────────────────
try:
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *
    _MODERN = True
except ImportError:
    import tkinter.ttk as ttk  # type: ignore[no-redef]
    # constantes compatíveis
    BOTH = tk.BOTH; X = tk.X; Y = tk.Y
    TOP = tk.TOP; BOTTOM = tk.BOTTOM; LEFT = tk.LEFT; RIGHT = tk.RIGHT
    WORD = tk.WORD; END = tk.END; NORMAL = tk.NORMAL; DISABLED = tk.DISABLED
    YES = True; SINGLE = tk.SINGLE; HORIZONTAL = tk.HORIZONTAL
    _MODERN = False

from pdf_processor import PDFProcessor
from tts_engine import TTSEngine


def _btn(parent, text, cmd, style=None, **kw):
    """Cria botão compatível com ttkbootstrap e ttk padrão."""
    kwargs = dict(text=text, command=cmd, **kw)
    if _MODERN and style:
        kwargs["bootstyle"] = style
    return ttk.Button(parent, **kwargs)


def _scale(parent, style=None, **kw):
    kwargs = dict(**kw)
    if _MODERN and style:
        kwargs["bootstyle"] = style
    return ttk.Scale(parent, **kwargs)


class App:
    # ── inicialização ─────────────────────────────────────────────────────────

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Read Me Book")
        self.root.geometry("1200x760")
        self.root.minsize(900, 600)

        # estado da aplicação
        self.processor: PDFProcessor | None = None
        self._tts: TTSEngine | None = None
        self._tts_error: str = ""
        self._reading = False
        self._read_thread: threading.Thread | None = None
        self._dark = False
        self._all_chapters: list[dict] = []

        # inicializa TTS em background para não travar a UI
        threading.Thread(target=self._init_tts, daemon=True).start()

        self._build_ui()
        self._bind_keys()

    def _init_tts(self):
        try:
            self._tts = TTSEngine()
        except Exception as exc:
            self._tts_error = str(exc)

    # ── construção da UI ──────────────────────────────────────────────────────

    def _build_ui(self):
        if _MODERN:
            self._style = ttk.Style("cosmo")

        # toolbar
        toolbar = ttk.Frame(self.root, padding=(10, 8))
        toolbar.pack(side=TOP, fill=X)
        self._build_toolbar(toolbar)

        # separador
        ttk.Separator(self.root, orient=HORIZONTAL).pack(fill=X)

        # corpo principal (sidebar + painel direito)
        body = ttk.PanedWindow(self.root, orient=HORIZONTAL)
        body.pack(fill=BOTH, expand=YES, padx=6, pady=6)
        self._build_sidebar(body)
        self._build_main(body)

        # barra de status
        self._build_statusbar()

    def _build_toolbar(self, parent):
        # esquerda – arquivo
        left = ttk.Frame(parent)
        left.pack(side=LEFT)

        self._btn_load = _btn(left, "📁  Abrir PDF", self._open_pdf, "primary", width=14)
        self._btn_load.pack(side=LEFT, padx=(0, 6))

        self._btn_export = _btn(
            left, "💾  Exportar JSON", self._export_json, "info", width=16
        )
        self._btn_export.pack(side=LEFT)
        self._btn_export.config(state=DISABLED)

        # centro – controles de leitura
        center = ttk.Frame(parent)
        center.pack(side=LEFT, padx=40)

        self._btn_play = _btn(center, "▶  Play", self._toggle_play, "success", width=11)
        self._btn_play.pack(side=LEFT, padx=4)
        self._btn_play.config(state=DISABLED)

        self._btn_stop = _btn(center, "⬛  Stop", self._stop, "danger", width=11)
        self._btn_stop.pack(side=LEFT, padx=4)
        self._btn_stop.config(state=DISABLED)

        # direita – tema
        right = ttk.Frame(parent)
        right.pack(side=RIGHT)

        self._btn_theme = _btn(right, "🌙  Escuro", self._toggle_theme, "secondary", width=13)
        self._btn_theme.pack(side=RIGHT)

    def _build_sidebar(self, parent):
        sidebar = ttk.Frame(parent, padding=8)
        parent.add(sidebar, weight=1)

        ttk.Label(sidebar, text="📚  Capítulos", font=("TkDefaultFont", 13, "bold")).pack(
            anchor="w", pady=(0, 8)
        )

        # busca
        search_row = ttk.Frame(sidebar)
        search_row.pack(fill=X, pady=(0, 6))
        ttk.Label(search_row, text="🔍").pack(side=LEFT, padx=(0, 4))
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", self._filter_chapters)
        ttk.Entry(search_row, textvariable=self._search_var).pack(
            side=LEFT, fill=X, expand=YES
        )

        # listbox
        lf = ttk.Frame(sidebar)
        lf.pack(fill=BOTH, expand=YES)
        sb = ttk.Scrollbar(lf)
        sb.pack(side=RIGHT, fill=Y)
        self._listbox = tk.Listbox(
            lf,
            yscrollcommand=sb.set,
            selectmode=SINGLE,
            font=("TkDefaultFont", 11),
            relief="flat",
            activestyle="none",
            highlightthickness=0,
            bd=0,
        )
        self._listbox.pack(side=LEFT, fill=BOTH, expand=YES)
        self._listbox.bind("<<ListboxSelect>>", self._on_chapter_select)
        sb.config(command=self._listbox.yview)

        self._chapter_info = ttk.Label(
            sidebar, text="Nenhum capítulo carregado", font=("TkDefaultFont", 9)
        )
        self._chapter_info.pack(anchor="w", pady=(6, 0))

    def _build_main(self, parent):
        main = ttk.Frame(parent, padding=8)
        parent.add(main, weight=3)

        # controles de velocidade e volume
        ctrl = ttk.Labelframe(main, text="⚙️  Configurações de Leitura", padding=10)
        ctrl.pack(fill=X, pady=(0, 8))

        self._build_slider(ctrl, "Velocidade (WPM):", 50, 300, 150, self._on_speed)
        self._build_slider(ctrl, "Volume:", 0, 100, 90, self._on_volume, pct=True)

        # área de texto
        tf = ttk.Labelframe(main, text="📖  Conteúdo", padding=8)
        tf.pack(fill=BOTH, expand=YES)

        tc = ttk.Frame(tf)
        tc.pack(fill=BOTH, expand=YES)
        tsb = ttk.Scrollbar(tc)
        tsb.pack(side=RIGHT, fill=Y)

        self._text = tk.Text(
            tc,
            wrap=WORD,
            yscrollcommand=tsb.set,
            font=("Georgia", 12),
            padx=20,
            pady=16,
            spacing3=6,
            relief="flat",
            state="normal",
        )
        self._text.pack(side=LEFT, fill=BOTH, expand=YES)
        tsb.config(command=self._text.yview)

        self._text.tag_configure(
            "chapter_title", font=("Georgia", 15, "bold"), spacing1=12, spacing3=8
        )

    def _build_slider(self, parent, label, from_, to, init, cmd, pct=False):
        row = ttk.Frame(parent)
        row.pack(fill=X, pady=4)
        ttk.Label(row, text=label, width=20).pack(side=LEFT)

        var = tk.IntVar(value=init)
        lbl_text = f"{init}{'%' if pct else ''}"
        lbl = ttk.Label(row, text=lbl_text, width=6)

        def _update(val):
            v = int(float(val))
            lbl.config(text=f"{v}{'%' if pct else ''}")
            cmd(v)

        sl = _scale(
            row,
            style="info" if not pct else "success",
            from_=from_,
            to=to,
            variable=var,
            command=_update,
            orient=HORIZONTAL,
        )
        sl.pack(side=LEFT, fill=X, expand=YES, padx=(0, 8))
        lbl.pack(side=LEFT)

    def _build_statusbar(self):
        bar = ttk.Frame(self.root)
        bar.pack(side=BOTTOM, fill=X)
        ttk.Separator(self.root, orient=HORIZONTAL).pack(side=BOTTOM, fill=X)
        self._status = ttk.Label(bar, text="Pronto.", padding=(8, 4))
        self._status.pack(side=LEFT, fill=X, expand=YES)
        self._progress = ttk.Progressbar(bar, mode="indeterminate", length=120)
        self._progress.pack(side=RIGHT, padx=8, pady=4)

    # ── atalhos ───────────────────────────────────────────────────────────────

    def _bind_keys(self):
        self.root.bind("<Control-o>", lambda _: self._open_pdf())
        self.root.bind("<Control-s>", lambda _: self._export_json())
        self.root.bind("<Control-d>", lambda _: self._toggle_theme())
        self.root.bind("<Escape>", lambda _: self._stop())
        self.root.bind("<space>", self._space_key)

    def _space_key(self, event):
        if isinstance(self.root.focus_get(), (tk.Entry, tk.Text)):
            return
        self._toggle_play()
        return "break"

    # ── lógica de negócio ─────────────────────────────────────────────────────

    def _open_pdf(self):
        path = filedialog.askopenfilename(
            title="Selecionar PDF",
            filetypes=[("PDFs", "*.pdf"), ("Todos", "*.*")],
        )
        if not path:
            return
        self._set_status(f"Carregando {Path(path).name}…")
        self._progress.start()
        self.root.update_idletasks()
        threading.Thread(target=self._load_pdf, args=(path,), daemon=True).start()

    def _load_pdf(self, path: str):
        try:
            proc = PDFProcessor(path, use_ai=True)
            proc.extract_text()
            chapters = proc.detect_chapters()
            self.root.after(0, lambda: self._after_load(proc, chapters, path))
        except Exception as exc:
            self.root.after(0, lambda: self._load_error(str(exc)))

    def _after_load(self, proc: PDFProcessor, chapters: list, path: str):
        self._progress.stop()
        self.processor = proc
        self._all_chapters = chapters

        # preenche listbox
        self._listbox.delete(0, END)
        if chapters:
            for i, c in enumerate(chapters):
                self._listbox.insert(END, f"{i + 1}. {c['title']}")
            self._chapter_info.config(text=f"{len(chapters)} capítulo(s) encontrado(s)")
        else:
            self._listbox.insert(END, "Documento completo")
            self._chapter_info.config(text="Nenhum capítulo detectado")

        # exibe texto
        text = proc.get_text_for_reading()
        self._set_text(text)

        # habilita botões
        for btn in (self._btn_play, self._btn_stop, self._btn_export):
            btn.config(state=NORMAL)

        pages = len(proc.pages)
        ch = len(chapters)
        self._set_status(f"{Path(path).name}  —  {pages} página(s), {ch} capítulo(s)")

    def _load_error(self, msg: str):
        self._progress.stop()
        messagebox.showerror("Erro ao carregar PDF", msg)
        self._set_status("Erro ao carregar PDF.")

    # ── reprodução ────────────────────────────────────────────────────────────

    def _toggle_play(self):
        if self._reading:
            self._stop()
        else:
            self._play()

    def _play(self):
        if not self.processor:
            messagebox.showwarning("Aviso", "Carregue um PDF primeiro.")
            return
        if self._tts is None:
            if self._tts_error:
                messagebox.showerror("TTS indisponível", self._tts_error)
            else:
                messagebox.showinfo("Aguarde", "Motor TTS ainda está inicializando. Tente novamente em instantes.")
            return

        sel = self._listbox.curselection()
        if sel and self._all_chapters:
            idx = sel[0]
            text = self.processor.get_chapter_text(idx)
        else:
            text = self.processor.get_text_for_reading()

        if not text.strip():
            messagebox.showinfo("Sem conteúdo", "Nenhum texto para ler nesta seleção.")
            return

        self._reading = True
        self._btn_play.config(text="⏸  Pause")
        self._set_status("Lendo…")

        self._read_thread = threading.Thread(
            target=self._read_worker, args=(text,), daemon=True
        )
        self._read_thread.start()

    def _read_worker(self, text: str):
        try:
            self._tts.speak(text)
        except Exception as exc:
            self.root.after(0, lambda: messagebox.showerror("Erro TTS", str(exc)))
        finally:
            self._reading = False
            self.root.after(0, self._reading_done)

    def _reading_done(self):
        self._btn_play.config(text="▶  Play")
        self._set_status("Leitura concluída.")

    def _stop(self):
        if self._tts:
            self._tts.stop()
        self._reading = False
        self._btn_play.config(text="▶  Play")
        self._set_status("Parado.")

    # ── capítulos ─────────────────────────────────────────────────────────────

    def _on_chapter_select(self, _event):
        sel = self._listbox.curselection()
        if not sel or not self.processor:
            return
        idx = sel[0]
        if self._all_chapters:
            text = self.processor.get_chapter_text(idx)
            title = self._all_chapters[idx]["title"]
            self._set_text(text, title=title)
            self._set_status(f"Capítulo: {title}")

    def _filter_chapters(self, *_):
        query = self._search_var.get().lower()
        self._listbox.delete(0, END)
        for i, c in enumerate(self._all_chapters):
            if query in c["title"].lower():
                self._listbox.insert(END, f"{i + 1}. {c['title']}")

    # ── controles ─────────────────────────────────────────────────────────────

    def _on_speed(self, value: int):
        if self._tts:
            self._tts.set_rate(value)

    def _on_volume(self, value: int):
        if self._tts:
            self._tts.set_volume(value / 100)

    # ── exportar ──────────────────────────────────────────────────────────────

    def _export_json(self):
        if not self.processor:
            messagebox.showwarning("Aviso", "Carregue um PDF primeiro.")
            return
        dest = filedialog.asksaveasfilename(
            title="Salvar análise como JSON",
            defaultextension=".json",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
        )
        if not dest:
            return
        try:
            self.processor.export_to_json(dest)
            messagebox.showinfo("Exportado", f"Salvo em:\n{dest}")
            self._set_status(f"Exportado para {Path(dest).name}")
        except Exception as exc:
            messagebox.showerror("Erro ao exportar", str(exc))

    # ── tema ──────────────────────────────────────────────────────────────────

    def _toggle_theme(self):
        if not _MODERN:
            messagebox.showinfo(
                "UI moderna não disponível",
                "Instale ttkbootstrap para usar temas:\n  pip install ttkbootstrap",
            )
            return
        self._dark = not self._dark
        self._style.theme_use("darkly" if self._dark else "cosmo")
        self._btn_theme.config(text="☀️  Claro" if self._dark else "🌙  Escuro")

    # ── helpers ───────────────────────────────────────────────────────────────

    def _set_status(self, msg: str):
        self._status.config(text=msg)

    def _set_text(self, text: str, title: str = ""):
        self._text.config(state="normal")
        self._text.delete("1.0", END)
        if title:
            self._text.insert("1.0", title + "\n\n", "chapter_title")
        self._text.insert(END, text)
        self._text.see("1.0")


# ── entry point ───────────────────────────────────────────────────────────────

def main():
    if _MODERN:
        root = ttk.Window(themename="cosmo")
    else:
        root = tk.Tk()
    app = App(root)  # noqa: F841
    root.mainloop()


if __name__ == "__main__":
    main()
