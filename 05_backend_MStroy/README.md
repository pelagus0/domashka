# 05_backend_MStroy

Реализация TreeStore как FastAPI‑сервиса с хранением элементов в PostgreSQL.

## Запуск в Docker

Из папки `05_backend_MStroy`:

```bash
docker compose up --build
```

Swagger: `http://localhost:8003/docs`

## Быстрый старт

1. Загрузить тестовый набор элементов:

```bash
curl -X POST "http://localhost:8003/api/v1/items/seed"
```

2. Получить детей/родителей:

```bash
curl "http://localhost:8003/api/v1/items/4/children"
curl "http://localhost:8003/api/v1/items/7/parents"
```

