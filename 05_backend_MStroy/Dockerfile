FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY mstroy_app /app/mstroy_app

EXPOSE 8003

CMD ["python", "-m", "uvicorn", "mstroy_app.main:app", "--host", "0.0.0.0", "--port", "8003"]

