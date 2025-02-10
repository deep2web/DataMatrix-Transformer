FROM python

# Verhindern, dass apt Installationsabfragen stellt
ENV DEBIAN_FRONTEND=noninteractive

# Systempakete aktualisieren und installieren, dann Aufräumen
RUN apt update
RUN apt install -y libdmtx0b

# Kopieren der requirements und Installation der Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Kopieren des Anwendungscodes
COPY . /app
WORKDIR /app

# Startbefehl für die Python-Anwendung
# CMD ["uvicorn", "main:api_route", "--host", "0.0.0.0"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

#CMD["gunicorn", "--bind", ":8000", "--workers", "1", "--threads", "8", "--timeout", "0", "--worker-class", "uvicorn.workers.UvicornWorker", "main:api_route"]

EXPOSE 8000/tcp
ENV PORT 8000