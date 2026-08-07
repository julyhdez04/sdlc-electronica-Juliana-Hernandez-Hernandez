# --- ETAPA 1: Constructor de dependencias ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes si aplica
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python en un directorio local (/install)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# --- ETAPA 2: Imagen Final Limpia y Ligera ---
FROM python:3.12-slim

WORKDIR /app

# Instalar solo la librería runtime de postgresql (libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copiar las librerías de python ya compiladas desde la etapa de construcción
COPY --from=builder /install /usr/local

# Copiar el código de la aplicación
COPY . /app

# Exponer el puerto y definir comando de ejecución
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]