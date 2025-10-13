#!/bin/bash

# Read Me Book - Web Application Launcher
# Script para inicializar o aplicativo web

echo "🚀 Read Me Book - Inicializando aplicação web..."
echo "================================================"

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale o Python 3.7+ para continuar."
    exit 1
fi

# Verificar se o pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 não encontrado. Instale o pip para continuar."
    exit 1
fi

# Criar diretório virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📚 Instalando dependências..."
pip install -r requirements.txt

# Criar diretórios necessários
echo "📁 Criando diretórios necessários..."
mkdir -p uploads
mkdir -p static/css
mkdir -p static/js
mkdir -p templates

# Verificar se todos os arquivos necessários existem
required_files=(
    "web_app.py"
    "pdf_processor.py"
    "tts_engine.py"
    "templates/index.html"
    "templates/reader.html"
    "static/css/style.css"
    "static/css/reader.css"
    "static/js/main.js"
    "static/js/reader.js"
)

echo "✅ Verificando arquivos necessários..."
missing_files=()
for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

if [ ${#missing_files[@]} -ne 0 ]; then
    echo "❌ Arquivos necessários não encontrados:"
    for file in "${missing_files[@]}"; do
        echo "   - $file"
    done
    echo "Por favor, certifique-se de que todos os arquivos estão presentes."
    exit 1
fi

echo "✅ Todos os arquivos necessários encontrados!"
echo ""
echo "🌟 Iniciando servidor web..."
echo "   URL: http://localhost:8000"
echo "   Para parar o servidor, pressione Ctrl+C"
echo ""

# Iniciar o servidor
python3 web_app.py