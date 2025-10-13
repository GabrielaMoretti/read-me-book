# Read Me Book - PDF to Audiobook Converter

Um aplicativo inteligente que converte PDFs (livros digitalizados ou nativos) em audiobooks, com capacidade de identificar e filtrar elementos não essenciais como cabeçalhos, rodapés e números de página.

## 🎯 Características

- **Extração Inteligente de Texto**: Extrai texto de PDFs com filtragem automática de cabeçalhos, rodapés e números de página
- **Detecção de Capítulos**: Identifica automaticamente capítulos e suas posições no documento
- **Navegação por Capítulos**: Interface com índice lateral para fácil navegação entre capítulos
- **Síntese de Voz Natural**: Utiliza biblioteca TTS open-source (pyttsx3) para leitura natural
- **Acompanhamento de Leitura**: Interface que permite acompanhar o texto enquanto é lido
- **Controle de Velocidade**: Ajuste a velocidade de leitura conforme sua preferência
- **Interface Intuitiva**: GUI desenvolvida em tkinter com design limpo e fácil de usar

## 📋 Requisitos

- Python 3.7 ou superior
- Sistema operacional: Windows, Linux ou macOS

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

## 💻 Como Usar

1. Execute o aplicativo:
```bash
python audiobook_app.py
```

2. Clique em "📁 Load PDF" para selecionar um arquivo PDF

3. O aplicativo irá:
   - Extrair o texto do PDF
   - Detectar capítulos automaticamente
   - Exibir o índice de capítulos na barra lateral
   - Mostrar o texto na área principal

4. Use os controles:
   - **▶ Play**: Inicia a leitura do capítulo ou documento
   - **⏸ Pause**: Pausa a leitura
   - **⬛ Stop**: Para completamente a leitura
   - **Speed**: Ajusta a velocidade de leitura (50-300 palavras/minuto)

5. Navegue pelos capítulos clicando no índice lateral

## 🏗️ Estrutura do Projeto

```
read-me-book/
│
├── audiobook_app.py      # Aplicação GUI principal
├── pdf_processor.py      # Módulo de processamento de PDF
├── tts_engine.py         # Motor de síntese de voz
├── requirements.txt      # Dependências do projeto
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Este arquivo
```

## 🔧 Módulos

### pdf_processor.py
Responsável por:
- Extrair texto de PDFs usando pdfplumber
- Limpar texto removendo cabeçalhos, rodapés e números de página
- Detectar capítulos usando padrões de regex
- Organizar o conteúdo para leitura

### tts_engine.py
Responsável por:
- Configurar e gerenciar o motor TTS (pyttsx3)
- Controlar velocidade e volume da voz
- Gerenciar diferentes vozes disponíveis no sistema
- Converter texto em fala

### audiobook_app.py
Aplicação principal que:
- Fornece interface gráfica com tkinter
- Integra processamento de PDF e TTS
- Gerencia navegação por capítulos
- Controla reprodução de áudio
- Exibe texto com destaque durante a leitura

## 🎨 Funcionalidades Detalhadas

### Extração Inteligente de Conteúdo
O aplicativo usa heurísticas para identificar e remover:
- Números de página
- Cabeçalhos repetitivos
- Rodapés
- Linhas muito curtas nas bordas das páginas

### Detecção de Capítulos
Identifica capítulos usando padrões como:
- "Chapter" ou "Capítulo" seguido de número
- Títulos em letras maiúsculas
- Numeração de seções

### Interface do Usuário
- **Área de Controle**: Botões de carregamento, play/pause, stop e controle de velocidade
- **Índice Lateral**: Lista de capítulos para navegação rápida
- **Área de Texto**: Exibição do conteúdo com formatação adequada
- **Barra de Status**: Informações sobre o estado atual do aplicativo

## 🛠️ Tecnologias Utilizadas

- **Python 3**: Linguagem principal
- **tkinter**: Interface gráfica
- **pdfplumber**: Extração de texto de PDFs
- **pyttsx3**: Síntese de voz (TTS) open-source
- **PyPDF2**: Suporte adicional para manipulação de PDFs

## 📝 Licença

Este projeto é open-source e está disponível sob a licença MIT.

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Enviar pull requests

## 👥 Autor

Gabriela Moretti

## 🌐 Versão Web

O aplicativo agora inclui uma **interface web moderna** desenvolvida com FastAPI! 

### ✨ Funcionalidades da Versão Web:

- **🔄 Persistência de Dados**: SQLite para salvar livros, capítulos e anotações
- **📝 Sistema de Anotações**: Adicione notas em cada capítulo 
- **📚 Biblioteca Pessoal**: Gerencie sua coleção de audiolivros
- **🎯 Navegação Intuitiva**: Interface responsiva para desktop e mobile
- **⚡ API REST**: Backend robusto com FastAPI
- **🔊 TTS Web**: Síntese de voz usando Web Speech API
- **💾 Configurações Salvas**: Preferências de velocidade e formatação

### 🚀 Como Usar a Versão Web:

#### Opção 1: Script Automático
```bash
# Clone o repositório
git clone https://github.com/GabrielaMoretti/read-me-book.git
cd read-me-book

# Execute o script de inicialização
./start_web.sh
```

#### Opção 2: Manual
```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar servidor
python web_app.py
```

#### Opção 3: Docker
```bash
# Usando Docker Compose
docker-compose up -d

# Ou apenas Docker
docker build -t readmebook .
docker run -p 8000:8000 readmebook
```

**Acesse:** http://localhost:8000

### 📱 Características da Interface Web:

1. **Página Inicial**: Upload e biblioteca de PDFs
2. **Leitor**: Interface completa de leitura com:
   - Player de áudio com controles
   - Navegação por capítulos
   - Sistema de anotações
   - Configurações de texto
   - Atalhos de teclado

### 🗂️ Estrutura de Arquivos Web:
```
web_app.py              # Aplicação FastAPI
templates/              # Templates HTML
├── index.html         # Página principal
└── reader.html        # Interface de leitura
static/                # Arquivos estáticos
├── css/
│   ├── style.css      # Estilos gerais
│   └── reader.css     # Estilos do leitor
└── js/
    ├── main.js        # JavaScript principal
    └── reader.js      # JavaScript do leitor
```

## 🖥️ Versão Desktop (Original)

A versão desktop com tkinter continua disponível:

```bash
python audiobook_app.py
```

## 🔮 Melhorias Futuras

### ✅ Implementado na Versão Web:
- [x] Sistema de anotações
- [x] Biblioteca pessoal com histórico
- [x] Interface moderna e responsiva
- [x] Configurações salvas do usuário

### 🔄 Em Desenvolvimento:
- [ ] Exportar audiobook para arquivo MP3
- [ ] Suporte para múltiplas vozes e idiomas
- [ ] Marcadores e favoritos avançados
- [ ] Detecção melhorada de layout para PDFs complexos
- [ ] Suporte para OCR em PDFs digitalizados
- [ ] Modo escuro
- [ ] Sincronização em nuvem
- [ ] API mobile para aplicativo nativo