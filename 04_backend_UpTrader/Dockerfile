FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "until python -c \"import psycopg; psycopg.connect('postgresql://postgres:postgres@db:5432/uptrader')\" 2>/dev/null; do echo 'Waiting for postgres...'; sleep 2; done && python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]
