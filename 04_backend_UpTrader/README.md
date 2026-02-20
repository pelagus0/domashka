# 04_backend_UpTrader

Django‑приложение для древовидного меню через template tag `{% draw_menu 'menu_name' %}`.

## Запуск в Docker (полный стек)

Из папки `04_backend_UpTrader`:

```bash
docker compose up --build
```

Сайт: `http://localhost:8000/`, админка: `http://localhost:8000/admin/`

Создание суперпользователя (при первом запуске):

```bash
docker compose exec web python manage.py createsuperuser
```

## Локальный запуск (только БД в Docker)

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Откройте:
- сайт: `http://127.0.0.1:8000/`
- админку: `http://127.0.0.1:8000/admin/`

