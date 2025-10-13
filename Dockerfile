# Dockerfile for Read Me Book Web Application
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    espeak \
    espeak-data \
    libespeak1 \
    libespeak-dev \
    festival \
    festvox-kallpc16k \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p uploads static/css static/js templates

# Expor porta
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "web_app:app", "--host", "0.0.0.0", "--port", "8000"]