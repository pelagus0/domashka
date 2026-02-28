FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY appbooster_app /app/appbooster_app

EXPOSE 8001

CMD ["python", "-m", "uvicorn", "appbooster_app.main:app", "--host", "0.0.0.0", "--port", "8001"]

