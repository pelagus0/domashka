# 03_backend_Ivelum

Прокси‑сервер для Hacker News: проксирует HTML, подставляет `™` после каждого 6‑буквенного слова и переписывает ссылки так, чтобы навигация оставалась внутри прокси.

## Запуск в Docker

Из папки `03_backend_Ivelum`:

```bash
docker compose up --build
```

Откройте `http://localhost:8002/`.

