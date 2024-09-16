FROM python:3.11.10-bookworm

# Instalar dependências necessárias
RUN apt-get update && \
    apt-get install -y postgis && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY distritos/ /app/distritos/
COPY load_data.sql /app/load_data.sql

CMD ["python", "api.py"]