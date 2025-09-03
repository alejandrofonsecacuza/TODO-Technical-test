FROM python:3.10-slim


WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y gcc

# Copiar e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# El comando para correr la aplicación se define en docker-compose.yml