FROM python:3.12-alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    libffi-dev

# Install Python dependencies
COPY admin/requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY admin/ .

ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV PYTHONWARNINGS="ignore:This is a development server"

EXPOSE 8080

CMD ["python", "app.py"] 