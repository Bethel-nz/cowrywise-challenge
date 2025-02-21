# Apparantly, python 3.13.2 has issues with psycopg2, default to 3.12
FROM python:3.12-alpine 

WORKDIR /app

# Install system dependencies including MySQL dev packages
RUN apk add --no-cache \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev \
    mariadb-dev \
    mariadb-connector-c-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONWARNINGS="ignore:This is a development server"

EXPOSE 8181

CMD ["python", "main.py"] 