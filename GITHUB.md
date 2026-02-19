# Инструкция: перенос на GitHub

## 1. Создание репозитория

1. Зайдите на [GitHub](https://github.com) → New repository
2. Название: `domashka` или `ru-test-assignments`
3. Создайте репозиторий **без** README, .gitignore, license (у вас уже есть файлы)

## 2. Инициализация Git и первый коммит

```powershell
cd C:\Users\rifer\PycharmProjects\domashka
git init
git add .
git commit -m "Initial commit: все 8 заданий"
git branch -M main
git remote add origin https://github.com/ВАШ_ЛОГИН/domashka.git
git push -u origin main
```

## 3. Ветки по заданиям (PR 1, 2, 3)

Для заданий 1, 2, 3 — отдельные ветки и PR:

```powershell
# Ветка для задания 01
git checkout -b 01_backend_Bewise
git add 01_backend_Bewise/
git add README.md
git commit -m "Задание 01: Bewise Quiz API"
git push -u origin 01_backend_Bewise

# Вернуться на main и создать ветку для 02
git checkout main
git checkout -b 02_backend_AppBooster
git add 02_backend_AppBooster/
git add README.md
git commit -m "Задание 02: AppBooster Experiments API"
git push -u origin 02_backend_AppBooster

# Задание 03
git checkout main
git checkout -b 03_backend_Ivelum
git add 03_backend_Ivelum/
git add README.md
git commit -m "Задание 03: Ivelum Hacker News proxy"
git push -u origin 03_backend_Ivelum
```

## 4. Создание Pull Request

1. На GitHub откройте репозиторий
2. Появится баннер «Compare & pull request» для каждой запушенной ветки
3. Или: Branches → выбрать ветку → «New pull request»
4. Создайте PR из `01_backend_Bewise` → `main`, `02_backend_AppBooster` → `main`, `03_backend_Ivelum` → `main`
5. Названия веток будут видны в списке веток и в PR

## 5. Главная ветка main

На `main` остаётся только общий README.md с:
- ФИО и группа
- Таблица всех заданий (01–08) со ссылками на папки

Задания 4–8 можно либо добавить в main, либо вынести в отдельные ветки по той же схеме.

## 6. Проверка имён веток на GitHub

- **Code** → выпадающий список **main** → там будут все ветки
- **Branches** — полный список веток с именами
- Названия веток (01_backend_Bewise, 02_backend_AppBooster и т.д.) отображаются везде

## 7. Переключение между ветками

```powershell
git checkout main              # на главную
git checkout 01_backend_Bewise # на ветку задания 01
git checkout 02_backend_AppBooster
git branch                    # список локальных веток
git branch -a                 # все ветки (включая remote)
```

## 8. Если уже есть коммиты на main

И нужно оставить на main только README:

```powershell
# Создать ветку со всеми файлами
git checkout -b all-tasks
git push -u origin all-tasks

# Вернуться на main и оставить только README
git checkout main
git rm -r --cached 01_backend_Bewise 02_backend_AppBooster 03_backend_Ivelum 04_backend_UpTrader 05_backend_MStroy 06_analytics_WhoIsBlogger 07_analytics_Cian 08_analytics_Amazon
git commit -m "Main: только README с ссылками на задания"
git push
```

Затем задания добавляются через PR из веток `01_backend_Bewise`, `02_backend_AppBooster` и т.д.
