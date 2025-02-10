FROM python:3.8-slim

# Verhindern, dass apt Installationsabfragen stellt
ENV DEBIAN_FRONTEND=noninteractive

# Systempakete aktualisieren und installieren, dann Aufräumen
RUN sudo apt update && \
sudo apt install -y libdmtx0t64

# Kopieren der requirements und Installation der Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Kopieren des Anwendungscodes
COPY . /app
WORKDIR /app

# Startbefehl für die Python-Anwendung
CMD ["python", "main.py"]
