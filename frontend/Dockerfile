# Apparantly, python 3.13.2 has issues with psycopg2, default to 3.12
FROM python:3.12-alpine 

WORKDIR /app

RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev

COPY frontend/requirements.txt .
RUN pip install -r requirements.txt

COPY frontend/ .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONWARNINGS="ignore:This is a development server"

EXPOSE 8181

CMD ["python", "app.py"] 