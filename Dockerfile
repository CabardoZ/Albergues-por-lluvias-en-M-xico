# Usar imagen base de Python
FROM python:3.10-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos al contenedor
COPY requirements.txt .
COPY PROYECTO_ALBERGUES_EN_MÉXICO.ipynb .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer puerto
EXPOSE 7860

# Comando para ejecutar Voila
CMD ["voila", "proyecto_albergues_en_mexico.ipynb", "--port=7860", "--no-browser", "--Voila.ip=0.0.0.0"]
