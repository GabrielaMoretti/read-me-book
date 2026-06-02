# Read Me Book 📚

Converte PDFs em audiobooks localmente, sem enviar seus arquivos para nenhum servidor.

---

## Pré-requisitos

- Python 3.9+
- Linux: `sudo apt-get install espeak espeak-ng` (motor de voz padrão)
- Windows / macOS: motor de voz nativo já incluso

---

## Instalação

```bash
git clone https://github.com/GabrielaMoretti/read-me-book.git
cd read-me-book

# Dependências obrigatórias
pip install pdfplumber pypdf pyttsx3 Pillow

# UI moderna (recomendado)
pip install ttkbootstrap
```

### Opcionais (instale separadamente)

| Recurso | Comando | Observação |
|---|---|---|
| Voz natural (Coqui TTS) | `pip install TTS` | ~4 GB de modelos |
| OCR para PDFs escaneados | `pip install pytesseract pdf2image` + Tesseract | Ver abaixo |
| Layout avançado (multi-coluna) | `pip install deepdoctection[pt]` | ~2 GB |

**Tesseract (OCR):**
- Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`
- Windows: [Instalador oficial](https://github.com/UB-Mannheim/tesseract/wiki)

---

## Uso

```bash
python audiobook_app.py
```

1. **📁 Abrir PDF** — selecione seu arquivo
2. Capítulos detectados aparecem na barra lateral
3. Clique em um capítulo para navegar
4. **▶ Play** para ouvir / **⬛ Stop** para parar
5. **💾 Exportar JSON** salva a análise completa do documento

### Atalhos de teclado

| Tecla | Ação |
|---|---|
| `Ctrl+O` | Abrir PDF |
| `Ctrl+S` | Exportar JSON |
| `Espaço` | Play / Pause |
| `Esc` | Parar |
| `Ctrl+D` | Alternar tema claro/escuro |

---

## Uso programático

```python
from pdf_processor import PDFProcessor
from tts_engine import TTSEngine

# carregar e processar
proc = PDFProcessor("livro.pdf")
proc.extract_text()
proc.detect_chapters()

# ler em voz alta
tts = TTSEngine()
tts.set_rate(160)
tts.speak(proc.get_text_for_reading())

# ou salvar em arquivo
tts.save_to_file(proc.get_chapter_text(0), "capitulo1.wav", language="pt")

# exportar análise
proc.export_to_json("analise.json")
```

### OCR para PDFs escaneados

```python
from ocr_processor import OCRProcessor

ocr = OCRProcessor(language="por")
if ocr.is_scanned_pdf("documento.pdf"):
    pages = ocr.extract_text_from_pdf("documento.pdf")
    for p in pages:
        print(f"Página {p['page_number']} ({p['ocr_confidence']:.0f}% confiança)")
        print(p["text"])
```

---

## Estrutura do projeto

```
read-me-book/
├── audiobook_app.py      # Interface gráfica principal
├── pdf_processor.py      # Extração e estruturação de texto
├── tts_engine.py         # Motor de síntese de voz
├── ocr_processor.py      # OCR para PDFs escaneados
├── coqui_tts_engine.py   # TTS natural (Coqui) – opcional
├── deepdoc_processor.py  # Layout avançado – opcional
└── requirements.txt      # Dependências
```

---

## Problemas comuns

**"Nenhum motor TTS disponível" no Linux**
```bash
sudo apt-get install espeak espeak-ng
```

**OCR não reconhece texto**
- Verifique se o Tesseract está instalado: `tesseract --version`
- Use DPI 300+ para melhor qualidade

**Interface antiga (sem tema)**
```bash
pip install ttkbootstrap
```

---

## Licença

MIT — livre para uso pessoal e comercial.
