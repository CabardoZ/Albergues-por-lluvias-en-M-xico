FROM python:3.10-slim

# Instalar dependencias básicas
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar los archivos del Space
COPY . /app

# Instalar librerías
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto requerido
EXPOSE 7860

# Ejecutar el notebook con Voila
CMD ["voila", "--port=7860", "--no-browser", "--Voila.ip=0.0.0.0", "PROYECTO_ALBERGUES_EN_MÉXICO.ipynb"]
