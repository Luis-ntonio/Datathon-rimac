# Usa una imagen base oficial de Python
FROM python:3.10-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

RUN apt-get update
# Copia el archivo de requisitos al directorio de trabajo
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el contenido del directorio actual al directorio de trabajo en el contenedor
COPY . .

EXPOSE 7860
# Especifica el comando por defecto para ejecutar cuando el contenedor se inicie
# CMD ["python", "main.py"]