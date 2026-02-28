# 02_backend_AppBooster

Сервис A/B‑экспериментов: по `Device-Token` возвращает назначенные варианты экспериментов и сохраняет распределение в PostgreSQL.

## Запуск в Docker

Из папки `02_backend_AppBooster`:

```bash
docker compose up --build
```

Swagger: `http://localhost:8001/docs`

## Пример запроса

```bash
curl -X GET "http://localhost:8001/api/v1/experiments" ^
  -H "Device-Token: device-123"
```

Статистика:

```bash
curl -X GET "http://localhost:8001/api/v1/stats"
```

