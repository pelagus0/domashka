# 01_backend_Bewise

Решение тестового задания Bewise: FastAPI‑сервис, который по запросу скачивает вопросы викторины из публичного API и сохраняет их в PostgreSQL, гарантируя уникальность.

## Требования

- Python 3.11+
- Docker + Docker Compose (для запуска в контейнерах)

## Локальный запуск (без Docker)

1. Перейдите в папку задания:

```bash
cd 01_backend_Bewise
```

2. Создайте и активируйте виртуальное окружение, установите зависимости:

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

3. Поднимите PostgreSQL (например, через Docker Compose) и задайте переменную окружения:

```bash
setx DATABASE_URL "postgresql+psycopg://postgres:postgres@localhost:5432/bewise"
```

4. Запустите приложение:

```bash
python -m uvicorn bewise_app.main:app --host 0.0.0.0 --port 8000
```

Сервис будет доступен по `http://localhost:8000`, swagger — `http://localhost:8000/docs`.

## Запуск в Docker

Из папки `01_backend_Bewise`:

```bash
docker compose up --build
```

API будет доступно по `http://localhost:8000`.

## Пример запроса

```bash
curl -X POST "http://localhost:8000/api/v1/questions" ^
  -H "Content-Type: application/json" ^
  -d "{\"questions_num\": 3}"
```

Ответ:
- либо предыдущий сохранённый вопрос,
- либо `{}` если в БД ещё ничего не было.

