"""
PDF Processor
Extrai e organiza texto de PDFs com detecção de capítulos.
Usa pdfplumber como base e ativa deepdoctection automaticamente se instalado.
"""
from __future__ import annotations

import re
import json
from pathlib import Path
from typing import Optional

import pdfplumber

# ── deepdoctection (opcional) ────────────────────────────────────────────────
try:
    from deepdoc_processor import DeepDocProcessor
    _DEEPDOC_OK = True
except Exception:
    _DEEPDOC_OK = False

# ── padrões de capítulo ──────────────────────────────────────────────────────
_CHAPTER_RE = re.compile(
    r"""
    ^(
        (Chapter|CHAPTER|Capítulo|CAPÍTULO|Chapitre|Kapitel)\s+(\d+|[IVXLCDM]+)  # "Chapter 1"
      | (Part|PART|Parte|PARTE)\s+(\d+|[IVXLCDM]+)                                # "Part I"
      | (Section|SECTION|Seção|SEÇÃO)\s+\d+                                        # "Section 3"
      | \d+\.\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]                                                   # "1. Título"
      | [IVXLCDM]{1,6}\.\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ]                                       # "IV. Título"
      | [A-ZÁÉÍÓÚÂÊÔÃÕÇ][A-ZÁÉÍÓÚÂÊÔÃÕÇ\s]{8,60}$                                 # TÍTULO EM CAIXA ALTA
    )
    """,
    re.VERBOSE,
)

_PAGE_NUM_RE = re.compile(r"^\s*\d{1,4}\s*$")


class PDFProcessor:
    """Extrai, limpa e estrutura texto de PDFs para leitura em voz alta."""

    def __init__(self, pdf_path: str, use_ai: bool = True):
        self.pdf_path = str(pdf_path)
        self.use_ai = use_ai
        self.pages: list[dict] = []       # [{page_number, text, cleaned_text}, ...]
        self.chapters: list[dict] = []    # [{title, page, position}, ...]
        self._structured: Optional[dict] = None

        # tenta deepdoctection
        self._deepdoc: Optional[DeepDocProcessor] = None
        if _DEEPDOC_OK:
            try:
                self._deepdoc = DeepDocProcessor()
            except Exception as exc:
                print(f"[PDF] deepdoctection indisponível, usando pdfplumber: {exc}")

    # ── extração ─────────────────────────────────────────────────────────────

    def extract_text(self) -> list[dict]:
        """Extrai texto de todas as páginas (melhor método disponível)."""
        if self._deepdoc:
            return self._extract_deepdoc()
        return self._extract_pdfplumber()

    def _extract_pdfplumber(self) -> list[dict]:
        pages_data: list[dict] = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, page in enumerate(pdf.pages, start=1):
                    raw = page.extract_text() or ""
                    pages_data.append(
                        {
                            "page_number": i,
                            "text": raw,
                            "cleaned_text": self._clean(raw),
                        }
                    )
        except Exception as exc:
            raise RuntimeError(f"Falha ao abrir PDF: {exc}") from exc
        self.pages = pages_data
        return pages_data

    def _extract_deepdoc(self) -> list[dict]:
        try:
            pages_data = self._deepdoc.extract_text_with_layout(self.pdf_path)  # type: ignore[union-attr]
            for p in pages_data:
                p["cleaned_text"] = self._clean(p["text"])
            self.pages = pages_data
            return pages_data
        except Exception as exc:
            print(f"[PDF] deepdoctection falhou, usando pdfplumber: {exc}")
            return self._extract_pdfplumber()

    # ── limpeza ──────────────────────────────────────────────────────────────

    @staticmethod
    def _clean(text: str) -> str:
        """Remove cabeçalhos, rodapés e números de página."""
        lines = text.split("\n")
        # remove primeiras e últimas 2 linhas (prováveis cabeçalho/rodapé)
        body = lines[2:-2] if len(lines) > 6 else lines
        kept = []
        for line in body:
            stripped = line.strip()
            if not stripped:
                continue
            if _PAGE_NUM_RE.match(stripped):
                continue
            if len(stripped) < 3:
                continue
            kept.append(stripped)
        return "\n".join(kept)

    # ── capítulos ────────────────────────────────────────────────────────────

    def detect_chapters(self) -> list[dict]:
        """Detecta títulos de capítulo em todas as páginas."""
        chapters: list[dict] = []
        seen: set[str] = set()

        for page_data in self.pages:
            lines = page_data["text"].split("\n")
            for i, raw_line in enumerate(lines):
                line = raw_line.strip()
                if not line or line in seen:
                    continue
                if _CHAPTER_RE.match(line):
                    seen.add(line)
                    chapters.append(
                        {
                            "title": line,
                            "page": page_data["page_number"],
                            "position": i,
                        }
                    )

        self.chapters = chapters
        return chapters

    # ── acesso ao texto ──────────────────────────────────────────────────────

    def get_text_for_reading(self) -> str:
        """Retorna todo o texto limpo, pronto para leitura."""
        return "\n\n".join(p["cleaned_text"] for p in self.pages)

    def get_chapter_text(self, chapter_index: int) -> str:
        """Retorna o texto limpo de um capítulo específico."""
        if not self.chapters or chapter_index >= len(self.chapters):
            return self.get_text_for_reading()

        start = self.chapters[chapter_index]["page"]
        end = (
            self.chapters[chapter_index + 1]["page"]
            if chapter_index + 1 < len(self.chapters)
            else len(self.pages) + 1
        )
        parts = [
            p["cleaned_text"]
            for p in self.pages
            if start <= p["page_number"] < end
        ]
        return "\n\n".join(parts)

    # ── análise estruturada ──────────────────────────────────────────────────

    def get_structured_content(self) -> dict:
        """Retorna estrutura organizada por capítulos com metadados."""
        if self._structured:
            return self._structured

        _WPM_SLOW, _WPM_MED, _WPM_FAST = 130, 150, 180

        def _duration(words: int) -> dict:
            return {
                "slow_min": round(words / _WPM_SLOW, 1),
                "medium_min": round(words / _WPM_MED, 1),
                "fast_min": round(words / _WPM_FAST, 1),
            }

        total_words = sum(
            len(p["cleaned_text"].split()) for p in self.pages
        )

        structured_chapters = []
        for idx, chap in enumerate(self.chapters):
            text = self.get_chapter_text(idx)
            words = len(text.split())
            paragraphs = [s.strip() for s in text.split("\n\n") if s.strip()]
            structured_chapters.append(
                {
                    "index": idx,
                    "title": chap["title"],
                    "page_start": chap["page"],
                    "word_count": words,
                    "paragraphs": paragraphs,
                    "estimated_duration": _duration(words),
                }
            )

        self._structured = {
            "metadata": {
                "total_pages": len(self.pages),
                "total_chapters": len(self.chapters),
                "total_words": total_words,
                "estimated_duration": _duration(total_words),
                "extraction_method": "deepdoctection" if self._deepdoc else "pdfplumber",
            },
            "chapters": structured_chapters,
        }
        return self._structured

    def get_document_structure(self) -> dict:
        """Detecta seções especiais (índice, introdução, bibliografia…)."""
        flags = {
            "has_table_of_contents": False,
            "has_introduction": False,
            "has_preface": False,
            "has_epilogue": False,
            "has_bibliography": False,
            "has_index": False,
        }
        keywords = {
            "has_table_of_contents": {"table of contents", "índice", "sumário", "contents"},
            "has_introduction": {"introduction", "introdução"},
            "has_preface": {"preface", "prefácio"},
            "has_epilogue": {"epilogue", "epílogo"},
            "has_bibliography": {"bibliography", "bibliografia", "referências", "references"},
            "has_index": {"index", "índice remissivo"},
        }
        # verifica primeiras e últimas 10 páginas
        sample = self.pages[:10] + self.pages[-10:]
        for page in sample:
            lower = page["text"].lower()
            for flag, words in keywords.items():
                if any(w in lower for w in words):
                    flags[flag] = True
        return flags

    def export_to_json(self, output_path: Optional[str] = None) -> dict:
        """Exporta análise completa em JSON."""
        data = {
            "pdf_path": self.pdf_path,
            "document_structure": self.get_document_structure(),
            **self.get_structured_content(),
        }
        if output_path:
            Path(output_path).write_text(
                json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        return data
