# Ветки и GitHub

## Правило

- **main** — в ветке только **README.md** (ФИО, группа, таблица заданий со ссылками).
- **8 веток** — каждая ветка = одна папка с заданием. Имена веток короткие.

## Соответствие: папка → ветка

| Папка | Ветка |
|-------|--------|
| `01_backend_Bewise` | **bewise** |
| `02_backend_AppBooster` | **appbooster** |
| `03_backend_Ivelum` | **ivelum** |
| `04_backend_UpTrader` | **uptrader** |
| `05_backend_MStroy` | **mstroy** |
| `06_analytics_WhoIsBlogger` | **whoisblogger** |
| `07_analytics_Cian` | **cian** |
| `08_analytics_Amazon` | **amazon** |

---

## Как сделать 8 веток (один раз)

В корне репозитория (`C:\Users\rifer\PycharmProjects\domashka`) выполните:

```powershell
.\scripts\create-branches.ps1
```

Скрипт:

1. Переключается на **main**.
2. Удаляет из индекса все 8 папок заданий (в main остаётся только README) и делает коммит.
3. Для каждой папки создаёт ветку с коротким именем, добавляет в неё только **README.md** и **эту папку**, коммитит.

После этого запушьте ветки на GitHub:

```powershell
git push -u origin bewise appbooster ivelum uptrader mstroy whoisblogger cian amazon
```

Или по одной:

```powershell
git push -u origin bewise
git push -u origin appbooster
# ...
```

---

## Если скрипт не запускается

Сделайте то же вручную (из корня репозитория):

```powershell
git checkout main

# Убрать папки из main (оставить только README)
git rm -r --cached 01_backend_Bewise 02_backend_AppBooster 03_backend_Ivelum 04_backend_UpTrader 05_backend_MStroy 06_analytics_WhoIsBlogger 07_analytics_Cian 08_analytics_Amazon
git add README.md
git commit -m "main: только README"

# Ветка bewise = main + папка 01
git checkout -b bewise
git add README.md 01_backend_Bewise
git commit -m "Задание: 01_backend_Bewise"
git checkout main

# Ветка appbooster = main + папка 02
git checkout -b appbooster
git add README.md 02_backend_AppBooster
git commit -m "Задание: 02_backend_AppBooster"
git checkout main

# Аналогично для ivelum, uptrader, mstroy, whoisblogger, cian, amazon
git checkout -b ivelum
git add README.md 03_backend_Ivelum
git commit -m "Задание: 03_backend_Ivelum"
git checkout main

git checkout -b uptrader
git add README.md 04_backend_UpTrader
git commit -m "Задание: 04_backend_UpTrader"
git checkout main

git checkout -b mstroy
git add README.md 05_backend_MStroy
git commit -m "Задание: 05_backend_MStroy"
git checkout main

git checkout -b whoisblogger
git add README.md 06_analytics_WhoIsBlogger
git commit -m "Задание: 06_analytics_WhoIsBlogger"
git checkout main

git checkout -b cian
git add README.md 07_analytics_Cian
git commit -m "Задание: 07_analytics_Cian"
git checkout main

git checkout -b amazon
git add README.md 08_analytics_Amazon
git commit -m "Задание: 08_analytics_Amazon"
git checkout main
```

---

## Переключение между ветками

```powershell
git checkout main        # только README
git checkout bewise      # README + 01_backend_Bewise
git checkout appbooster  # README + 02_backend_AppBooster
git branch               # список локальных веток
```

---

## Pull Request на GitHub

Для каждого задания создаётся отдельный PR:

- **bewise** → main  
- **appbooster** → main  
- **ivelum** → main  
- и т.д.

В PR будет видно только добавление одной папки (и README, если он менялся).
