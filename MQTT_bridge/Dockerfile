# Verwenden Sie das offizielle Python 3.10 Basisimage von Docker Hub
FROM python:3.10

# Setzen Sie Arbeitsverzeichnis in Ihrem Container
WORKDIR /app

# Kopieren Sie die Anwendungsabhängigkeiten in den Container
COPY requirements.txt .

# Installieren Sie die Anwendungsabhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Kopieren Sie den Rest Ihrer Anwendungsdateien in den Container
COPY . .

# Führen Sie Ihre Python-Anwendung aus
CMD ["python", "app.py"]
