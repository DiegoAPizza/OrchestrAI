# Usamos Python 3.12 (el que configuramos)
FROM python:3.12-slim-trixie

# Evitar que Python escriba archivos .pyc y permitir logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar algunas librerías
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar requerimientos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Comando por defecto (puede ser tu main.py, uvicorn, etc.)
CMD ["python", "main.py"]