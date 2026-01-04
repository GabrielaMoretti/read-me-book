# Read Me Book - AI-Powered PDF to Audiobook Converter

Um aplicativo inteligente que converte PDFs (livros digitalizados ou nativos) em audiobooks, com recursos avançados de IA para extração, organização e produção de conteúdo para audiolivros profissionais.

## 🎯 Características

### Processamento Inteligente com IA
- **Extração Avançada de Texto**: IA open-source para extrair e organizar texto de PDFs
- **deepdoctection (Integrado)**: Extração avançada de layout automática
  - Ativação automática quando instalado
  - Detecção de múltiplas colunas
  - Extração de tabelas com estrutura preservada
  - Identificação de imagens e figuras
  - Ordem de leitura otimizada
  - Fallback inteligente para pdfplumber
- **Detecção Inteligente de Capítulos**: Identifica automaticamente capítulos com NLP
- **Organização Estruturada**: Separa automaticamente:
  - Capítulos e seções
  - Cabeçalhos e rodapés
  - Notas de rodapé e referências
  - Conteúdo principal
- **Roteirização para Audiobook**: Organiza texto de forma otimizada para produção de audiobooks
- **Suporte a OCR**: Extrai texto de PDFs digitalizados usando Tesseract

### Interface Moderna
- **Design Moderno**: Interface atualizada com ttkbootstrap
- **Modo Escuro/Claro**: Alternância entre temas para conforto visual
- **Acessibilidade**: Atalhos de teclado e navegação otimizada
- **Busca de Capítulos**: Filtro de busca na lista de capítulos
- **Painel de Controles**: Controles intuitivos para velocidade e volume

### Recursos de Leitura
- **Síntese de Voz Natural**: Sistema TTS inteligente com seleção automática
- **Coqui TTS (Integrado)**: Narração profissional automática quando disponível
  - Ativação automática quando instalado
  - Vozes naturais e expressivas
  - Suporte a 16+ idiomas (incluindo Português)
  - Clonagem de voz a partir de amostras de áudio
  - Controle de entonação e emoção
  - Qualidade de audiobook profissional
  - Fallback inteligente para pyttsx3
- **Controles Completos**: Play, Pause, Stop com feedback visual
- **Ajuste de Velocidade**: 50-300 palavras por minuto (pyttsx3)
- **Controle de Volume**: Ajuste fino do volume de leitura (pyttsx3)
- **Navegação por Capítulos**: Índice lateral interativo

### Exportação e Análise
- **Exportar Estrutura**: Salva análise completa em JSON
- **Metadados Detalhados**: Informações sobre duração estimada, contagem de palavras
- **Análise de Documento**: Identifica estrutura (introdução, índice, bibliografia, etc.)

## 📋 Requisitos

### Requisitos Básicos
- Python 3.8 ou superior
- Sistema operacional: Windows, Linux ou macOS

### Requisitos Opcionais
- **Para OCR**: Tesseract OCR instalado no sistema
- **Para deepdoctection**: ~2GB espaço em disco para modelos
- **Para Coqui TTS**: ~4GB espaço em disco para modelos

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/GabrielaMoretti/read-me-book.git
cd read-me-book
```

2. Instale as dependências básicas:
```bash
pip install -r requirements.txt
```

3. (Recomendado) Instale recursos avançados para melhor qualidade:
   
   **deepdoctection** - Extração avançada de layout (recomendado para PDFs complexos):
   ```bash
   pip install deepdoctection[pt]
   ```
   Nota: Pacote grande (~2GB). Ativa automaticamente quando instalado.
   
   **Coqui TTS** - Voz natural profissional (recomendado para audiobooks de qualidade):
   ```bash
   pip install TTS
   ```
   Nota: Requer ~4GB de espaço. Ativa automaticamente quando instalado.

4. (Opcional) Para suporte a OCR, instale o Tesseract:
   - **Ubuntu/Debian**: `sudo apt-get install tesseract-ocr`
   - **macOS**: `brew install tesseract`
   - **Windows**: Baixe em https://github.com/UB-Mannheim/tesseract/wiki

## 💻 Como Usar

### Interface Moderna (Recomendado)

Execute a aplicação moderna com interface aprimorada:
```bash
python modern_audiobook_app.py
```

### Interface Clássica

Execute a interface clássica:
```bash
python audiobook_app.py
```

### Funcionalidades Principais

1. **Carregar PDF**: Clique em "📁 Load PDF" ou pressione `Ctrl+O`
2. **Navegação**: Use a barra lateral para navegar entre capítulos
3. **Buscar Capítulos**: Digite na caixa de busca para filtrar capítulos
4. **Controles de Leitura**:
   - **▶ Play**: Inicia leitura (`Espaço`)
   - **⏸ Pause**: Pausa a leitura
   - **⬛ Stop**: Para completamente (`Esc`)
5. **Ajustar Configurações**: Use os controles deslizantes para velocidade e volume
6. **Exportar Estrutura**: Salve análise do documento em JSON (`Ctrl+S`)
7. **Alternar Tema**: Mude entre modo claro/escuro (`Ctrl+D`)

### Atalhos de Teclado

- `Ctrl+O`: Abrir PDF
- `Ctrl+S`: Exportar estrutura
- `Espaço`: Play/Pause
- `Esc`: Stop
- `Ctrl+D`: Alternar tema

## 🏗️ Estrutura do Projeto

```
read-me-book/
│
├── modern_audiobook_app.py    # Aplicação GUI moderna (recomendado)
├── audiobook_app.py           # Aplicação GUI clássica
├── pdf_processor.py           # Processamento de PDF com IA
├── ai_text_analyzer.py        # Análise inteligente de texto
├── deepdoc_processor.py       # Extração avançada com deepdoctection (opcional)
├── ocr_processor.py           # OCR para PDFs digitalizados
├── tts_engine.py              # Motor de síntese de voz
├── coqui_tts_engine.py        # TTS natural com Coqui (opcional)
├── requirements.txt           # Dependências do projeto
├── example_usage.py           # Exemplos de uso
└── README.md                  # Este arquivo
```

## 🔧 Módulos

### ai_text_analyzer.py
Análise inteligente de texto usando IA:
- Classificação automática de conteúdo (capítulos, cabeçalhos, rodapés, notas)
- Detecção avançada de capítulos com múltiplos padrões
- Organização estruturada para produção de audiobooks
- Extração de notas de rodapé e referências
- Análise de estrutura do documento
- Estimativa de tempo de leitura

### pdf_processor.py (Aprimorado)
Processamento avançado de PDF:
- Extração de texto com limpeza inteligente
- Integração com módulo de IA para análise profunda
- Suporte opcional para deepdoctection
- Detecção de capítulos multinível
- Exportação para formato estruturado (JSON)
- Suporte a modo com e sem IA

### deepdoc_processor.py (Novo - Opcional)
Extração avançada de layout com deepdoctection:
- Análise de layout complexo (colunas, tabelas, imagens)
- Detecção automática da ordem de leitura
- Extração de tabelas com estrutura preservada
- Identificação de cabeçalhos e rodapés
- Suporte para documentos acadêmicos e revistas
- Fallback automático para pdfplumber se indisponível

### ocr_processor.py
OCR para PDFs digitalizados:
- Extração de texto com Tesseract OCR
- Pré-processamento de imagens para melhor qualidade
- Detecção automática de PDFs digitalizados
- Suporte a múltiplos idiomas
- Cálculo de confiança do OCR

### modern_audiobook_app.py
Interface moderna e acessível:
- Design moderno com ttkbootstrap
- Modo claro e escuro
- Atalhos de teclado completos
- Busca e filtro de capítulos
- Controles visuais aprimorados
- Barra de progresso
- Exportação de estrutura

### tts_engine.py (Aprimorado)
Motor de síntese de voz com múltiplos backends:
- Suporte para pyttsx3 (padrão, leve)
- Integração opcional com Coqui TTS (voz natural)
- Configuração e gerenciamento do TTS
- Controle de velocidade e volume
- Suporte a múltiplas vozes
- Conversão texto-fala natural
- Fallback automático entre engines

### coqui_tts_engine.py (Novo - Opcional)
Motor TTS natural com Coqui:
- Vozes ultra-realistas e expressivas
- Suporte a 16+ idiomas (en, pt, es, fr, de, etc.)
- Clonagem de voz a partir de amostras de áudio
- Controle de entonação e emoção
- Múltiplos speakers disponíveis
- Qualidade profissional de audiobook
- Geração de arquivos WAV de alta qualidade

## 🛠️ Tecnologias Utilizadas

### Core
- **Python 3.8+**: Linguagem principal
- **tkinter**: Interface gráfica base
- **ttkbootstrap**: Framework moderno para UI

### Processamento de Documentos
- **pdfplumber**: Extração avançada de texto de PDFs
- **pypdf**: Manipulação de PDFs
- **pytesseract**: OCR para PDFs digitalizados
- **pdf2image**: Conversão de PDF para imagem

### Inteligência Artificial e NLP
- **Análise Heurística**: Classificação inteligente de conteúdo
- **Pattern Matching Avançado**: Detecção de estrutura documental
- **deepdoctection (Opcional)**: Análise de layout com deep learning
- Suporte futuro para:
  - **spaCy**: Processamento de linguagem natural
  - **transformers**: Modelos de IA para análise de texto

### Áudio
- **pyttsx3**: Síntese de voz (TTS) open-source
- **Coqui TTS (Opcional)**: TTS neural de alta qualidade

### Web e API (Preparado para futuro)
- **Flask**: Framework web
- **FastAPI**: Framework API moderno
- **SQLAlchemy**: ORM para banco de dados

## 📝 Exemplos de Uso Programático

### Processamento Básico de PDF

```python
from pdf_processor import PDFProcessor

# Carregar e processar PDF (usa deepdoctection automaticamente se instalado)
processor = PDFProcessor('livro.pdf', use_ai=True)
processor.extract_text()

# Detectar capítulos
chapters = processor.detect_chapters()
print(f"Encontrados {len(chapters)} capítulos")

# Obter estrutura organizada para audiobook
structure = processor.get_structured_content_for_audiobook()
```

### Análise Avançada

```python
# Analisar estrutura do documento
doc_structure = processor.get_document_structure()
print(f"Tem índice: {doc_structure['has_table_of_contents']}")
print(f"Tem introdução: {doc_structure['has_introduction']}")

# Extrair notas de rodapé e referências
notes = processor.get_footnotes_and_references()
print(f"Notas de rodapé: {len(notes['footnotes'])}")

# Exportar análise completa
processor.export_to_json()
```

### OCR para PDFs Digitalizados

```python
from ocr_processor import OCRProcessor

# Verificar se PDF é digitalizado
ocr = OCRProcessor(language='por')
if ocr.is_scanned_pdf('documento_digitalizado.pdf'):
    # Extrair texto com OCR
    pages = ocr.extract_text_from_pdf('documento_digitalizado.pdf')
    for page in pages:
        print(f"Página {page['page_number']}: {page['ocr_confidence']:.1f}% confiança")
```

### Síntese de Voz Personalizada

```python
from tts_engine import TTSEngine

# Configurar TTS padrão (pyttsx3)
tts = TTSEngine()
tts.set_rate(160)  # palavras por minuto
tts.set_volume(0.95)

# Listar vozes disponíveis
voices = tts.list_voices()
for voice in voices:
    print(f"{voice.name}: {voice.languages}")

# Ler texto
tts.speak("Este é um exemplo de leitura personalizada.")
```

### Extração Avançada com deepdoctection (Integrado)

```python
from pdf_processor import PDFProcessor

# deepdoctection é usado automaticamente se estiver instalado
processor = PDFProcessor('documento_complexo.pdf', use_ai=True)
pages = processor.extract_text()

# Verificar informações de layout (disponível se deepdoctection usado)
for page in pages:
    if 'layout_elements' in page:
        print(f"Página {page['page_number']}: {page['columns']} coluna(s)")
        if page['has_tables']:
            print("  - Contém tabelas")
        if page['has_images']:
            print("  - Contém imagens")

# Exportar análise incluindo dados do deepdoctection
analysis = processor.export_to_json()
if 'deepdoctection_analysis' in analysis:
    dd = analysis['deepdoctection_analysis']
    print(f"Total de tabelas: {dd['total_tables']}")
    print(f"Total de imagens: {dd['total_images']}")
    print(f"Layout complexo: {dd['has_complex_layout']}")
```

### Voz Natural com Coqui TTS (Integrado)

```python
from tts_engine import TTSEngine

# Coqui TTS é usado automaticamente se estiver instalado
tts = TTSEngine()

# Gerar audiobook com voz natural em Português
tts.save_to_file(
    "Este é um exemplo de narração natural em português.",
    "output.wav",
    language="pt"
)

# Verificar qual engine está ativo
info = tts.get_engine_info()
print(f"Engine: {info['engine_type']}")
if info['engine_type'] == 'coqui':
    print(f"Idiomas suportados: {info['languages']}")
    print(f"Clonagem de voz: {info['supports_voice_cloning']}")
```

### Clonagem de Voz com Coqui TTS (Avançado)

```python
from coqui_tts_engine import CoquiTTSEngine

# Inicializar com modelo XTTS para clonagem de voz
coqui = CoquiTTSEngine(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Clonar voz a partir de amostra de áudio (6-30 segundos)
texto = "Este audiobook foi narrado com voz clonada em português brasileiro."
coqui.clone_voice(
    speaker_wav="minha_voz.wav",  # Amostra de áudio limpa
    text=texto,
    output_file="audiobook_clonado.wav",
    language="pt"
)

# Gerar audiobook completo em múltiplos arquivos
audio_files = coqui.save_to_file_with_splits(
    text=texto_completo,
    output_dir="audiobook_chapters",
    max_chars=500,
    language="pt"
)
print(f"Gerados {len(audio_files)} arquivos de áudio")
```

### Fluxo Completo: PDF Complexo → Audiobook Natural

```python
from pdf_processor import PDFProcessor
from tts_engine import TTSEngine

# 1. Extrair com melhor método disponível (automático)
processor = PDFProcessor('livro.pdf', use_ai=True)
processor.extract_text()
chapters = processor.detect_chapters()
structure = processor.get_structured_content_for_audiobook()

# 2. Gerar audiobook com melhor TTS disponível (automático)
tts = TTSEngine()

for i, chapter in enumerate(structure['chapters']):
    filename = f"chapter_{i+1:02d}.wav"
    print(f"Gerando {filename}...")
    
    tts.save_to_file(
        text=chapter['content'],
        filename=filename,
        language="pt"
    )
    
print("Audiobook completo gerado com sucesso!")
print(f"Engine usado: {tts.get_engine_info()['engine_type']}")
```

## 🎨 Capturas de Tela

A interface moderna oferece:
- ✨ Design limpo e profissional
- 🌓 Modo escuro para reduzir fadiga visual
- 📚 Navegação intuitiva por capítulos
- 🎛️ Controles visuais para velocidade e volume
- 🔍 Busca e filtro de capítulos em tempo real

## 🔬 Recursos Avançados de IA

### Classificação Automática de Conteúdo
O sistema classifica automaticamente cada linha do documento:
- **Capítulos**: Identificação de títulos e divisões
- **Cabeçalhos**: Elementos repetitivos no topo das páginas
- **Rodapés**: Informações no final das páginas
- **Notas de Rodapé**: Referências numeradas
- **Conteúdo**: Texto principal para leitura

### Organização para Produção de Audiobook
- Estrutura hierárquica de capítulos
- Contagem de palavras por seção
- Estimativa de duração de leitura (lenta/média/rápida)
- Divisão em parágrafos otimizados
- Metadados completos para cada seção

### Análise de Documento
Identifica automaticamente:
- Índice (Table of Contents)
- Introdução e Prefácio
- Capítulos e Seções
- Epílogo
- Bibliografia
- Índice Remissivo

## 📊 Formato de Exportação JSON

A estrutura exportada contém:
```json
{
  "metadata": {
    "total_pages": 250,
    "total_chapters": 12,
    "estimated_reading_time": {
      "slow": 192.3,
      "medium": 166.7,
      "fast": 138.9
    }
  },
  "chapters": [
    {
      "number": 1,
      "title": "Capítulo 1: Introdução",
      "page_range": [10, 25],
      "word_count": 2500,
      "paragraphs": ["...", "..."],
      "estimated_duration": {...}
    }
  ]
}
```

## 🌍 Suporte a Idiomas

### TTS (Text-to-Speech)
- Português
- Inglês
- Espanhol
- E outros idiomas suportados pelo sistema

### OCR
- Português (por)
- Inglês (eng)
- Espanhol (spa)
- E mais de 100 idiomas via Tesseract

## 🚧 Melhorias Futuras

### Implementado ✅
- [x] **deepdoctection**: Extração avançada integrada (ativa automaticamente)
- [x] **Coqui TTS**: Narração natural integrada (ativa automaticamente)
- [x] Clonagem de voz para audiobooks personalizados
- [x] Suporte a múltiplos idiomas (16+ com Coqui TTS)
- [x] Seleção automática do melhor método disponível
- [x] Fallback inteligente entre métodos

### Em Desenvolvimento
- [ ] Interface web com Flask/FastAPI
- [ ] Sistema de notas e marcadores persistentes
- [ ] Modo de comparação lado a lado
- [ ] Integração na interface gráfica (deepdoctection + Coqui TTS)

### Planejadas
- [ ] Exportar audiobook para MP3/M4B
- [ ] Integração com modelos de IA mais avançados (GPT, BERT)
- [ ] Suporte para ePub e outros formatos
- [ ] Aplicativo mobile
- [ ] Sincronização na nuvem
- [ ] Compartilhamento de anotações

## ⚠️ Notas de Instalação

### Dependências Opcionais

**Para interface moderna** (Recomendado):
```bash
pip install ttkbootstrap
```

**Para OCR** (PDFs digitalizados):
```bash
pip install pytesseract pdf2image
# + instalar Tesseract no sistema
```

**Para deepdoctection** (Extração avançada - Recomendado):
```bash
pip install deepdoctection[pt]
```
Nota: Pacote grande (~2GB) com modelos de deep learning. **Ativa automaticamente** quando instalado - sem necessidade de configuração adicional!

**Para Coqui TTS** (Voz natural - Recomendado):
```bash
pip install TTS
```
Nota: Requer ~4GB de espaço em disco. Modelos são baixados automaticamente. **Ativa automaticamente** quando instalado!

### Dependências Mínimas
Para usar apenas funcionalidades básicas:
```bash
pip install pdfplumber pyttsx3
```

## 🐛 Solução de Problemas

### Erro ao executar TTS
- **Linux**: Instale espeak: `sudo apt-get install espeak`
- **Windows**: O SAPI5 já vem instalado
- **macOS**: O NSSpeechSynthesizer já vem instalado

### OCR não funciona
- Verifique se o Tesseract está instalado: `tesseract --version`
- Configure o caminho se necessário: `pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'`

### Interface moderna não carrega
- Instale ttkbootstrap: `pip install ttkbootstrap`
- Use a interface clássica como alternativa: `python audiobook_app.py`

## 📝 Licença

Este projeto é open-source e está disponível sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests
- Melhorar a documentação

## 👥 Autor

Gabriela Moretti

## 🙏 Agradecimentos

- Comunidade open-source Python
- Desenvolvedores do pyttsx3, pdfplumber e Tesseract
- Todos os contribuidores do projeto

---

**Desenvolvido com ❤️ para tornar a leitura mais acessível através da tecnologia**

