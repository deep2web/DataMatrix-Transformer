FROM python:3.8-slim

# Verhindern, dass apt Installationsabfragen stellt
ENV DEBIAN_FRONTEND=noninteractive

# Systempakete aktualisieren und installieren, dann Aufräumen
RUN apt-get update && \
    apt-get install -y \
        libdmtx0t64 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Kopieren der requirements und Installation der Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Kopieren des Anwendungscodes
COPY . /app
WORKDIR /app

# Startbefehl für die Python-Anwendung
CMD ["python", "main.py"]
