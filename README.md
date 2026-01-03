# Read Me Book - AI-Powered PDF to Audiobook Converter

Um aplicativo inteligente que converte PDFs (livros digitalizados ou nativos) em audiobooks, com recursos avançados de IA para extração, organização e produção de conteúdo para audiolivros profissionais.

## 🎯 Características

### Processamento Inteligente com IA
- **Extração Avançada de Texto**: IA open-source para extrair e organizar texto de PDFs
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
- **Síntese de Voz Natural**: TTS open-source (pyttsx3) com vozes naturais
- **Controles Completos**: Play, Pause, Stop com feedback visual
- **Ajuste de Velocidade**: 50-300 palavras por minuto
- **Controle de Volume**: Ajuste fino do volume de leitura
- **Navegação por Capítulos**: Índice lateral interativo

### Exportação e Análise
- **Exportar Estrutura**: Salva análise completa em JSON
- **Metadados Detalhados**: Informações sobre duração estimada, contagem de palavras
- **Análise de Documento**: Identifica estrutura (introdução, índice, bibliografia, etc.)

## 📋 Requisitos

- Python 3.8 ou superior
- Sistema operacional: Windows, Linux ou macOS
- Para OCR (opcional): Tesseract OCR instalado no sistema

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/GabrielaMoretti/read-me-book.git
cd read-me-book
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. (Opcional) Para suporte a OCR, instale o Tesseract:
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
├── ocr_processor.py           # OCR para PDFs digitalizados
├── tts_engine.py              # Motor de síntese de voz
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
- Detecção de capítulos multinível
- Exportação para formato estruturado (JSON)
- Suporte a modo com e sem IA

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

### tts_engine.py
Motor de síntese de voz:
- Configuração e gerenciamento do TTS
- Controle de velocidade e volume
- Suporte a múltiplas vozes
- Conversão texto-fala natural

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
- Suporte futuro para:
  - **spaCy**: Processamento de linguagem natural
  - **transformers**: Modelos de IA para análise de texto

### Áudio
- **pyttsx3**: Síntese de voz (TTS) open-source

### Web e API (Preparado para futuro)
- **Flask**: Framework web
- **FastAPI**: Framework API moderno
- **SQLAlchemy**: ORM para banco de dados

## 📝 Exemplos de Uso Programático

### Processamento Básico de PDF

```python
from pdf_processor import PDFProcessor

# Carregar e processar PDF
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

# Configurar TTS
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

### Em Desenvolvimento
- [ ] Interface web com Flask/FastAPI
- [ ] Sistema de notas e marcadores persistentes
- [ ] Suporte a múltiplas vozes e idiomas avançado
- [ ] Modo de comparação lado a lado

### Planejadas
- [ ] Exportar audiobook para MP3/M4B
- [ ] Integração com modelos de IA mais avançados (GPT, BERT)
- [ ] Detecção de figuras e tabelas
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

**Para análise avançada de IA** (Futuro):
```bash
pip install spacy transformers torch
```

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

