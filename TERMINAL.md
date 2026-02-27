# Работа с заданиями 1–8 в терминале PyCharm

## Один раз: восстановить все папки

Если видите только одно задание (например, 08), выполните в корне проекта:

```powershell
.\restore-all.ps1
```

После этого появятся папки 01_backend_Bewise … 07_analytics_Cian.

---

## Запуск задания по номеру

В корне проекта (`domashka`):

```powershell
.\restore-and-run.ps1 4
```

Подставьте число от 1 до 8. Скрипт при необходимости восстановит папку из Git, перейдёт в неё и запустит Docker (для 01–05) или Docker + `python run.py` (для 06–08).

---

## Ручная работа с любым заданием

Переход в папку и запуск вручную:

| № | Команды | Открыть в браузере |
|---|--------|---------------------|
| 1 | `cd 01_backend_Bewise` → `docker compose up --build` | http://localhost:8000/docs |
| 2 | `cd 02_backend_AppBooster` → `docker compose up --build` | http://localhost:8001/docs |
| 3 | `cd 03_backend_Ivelum` → `docker compose up --build` | http://localhost:8002/ |
| 4 | `cd 04_backend_UpTrader` → `docker compose up --build` | http://localhost:8000/ |
| 5 | `cd 05_backend_MStroy` → `docker compose up --build` | http://localhost:8003/docs |
| 6 | `cd 06_analytics_WhoIsBlogger` → `docker compose up -d` → `python run.py` | вывод в консоль |
| 7 | `cd 07_analytics_Cian` → `docker compose up -d` → `python run.py` | вывод в консоль |
| 8 | `cd 08_analytics_Amazon` → `docker compose up -d` → `python run.py` | вывод в консоль |

Терминал в PyCharm всегда открывайте из корня проекта (`C:\Users\rifer\PycharmProjects\domashka`).
