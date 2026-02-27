# Скрипт: 8 веток (каждая = одна папка), в main только README.
# Запуск из корня репозитория: .\scripts\create-branches.ps1

$ErrorActionPreference = "Stop"

$repoRoot = $PSScriptRoot + "\.."
Set-Location $repoRoot

$pairs = @(
    @{ Folder = "01_backend_Bewise";     Branch = "bewise" },
    @{ Folder = "02_backend_AppBooster"; Branch = "appbooster" },
    @{ Folder = "03_backend_Ivelum";     Branch = "ivelum" },
    @{ Folder = "04_backend_UpTrader";   Branch = "uptrader" },
    @{ Folder = "05_backend_MStroy";     Branch = "mstroy" },
    @{ Folder = "06_analytics_WhoIsBlogger"; Branch = "whoisblogger" },
    @{ Folder = "07_analytics_Cian";      Branch = "cian" },
    @{ Folder = "08_analytics_Amazon";   Branch = "amazon" }
)

# 1) Убедиться, что мы на main
git checkout main

# 2) Убрать все папки заданий из индекса (в main остаётся только README)
$folders = $pairs | ForEach-Object { $_.Folder }
foreach ($f in $folders) {
    if (Test-Path $f) {
        git rm -r --cached $f 2>$null
    }
}
git add README.md
$status = git status --short
if ($status) {
    git commit -m "main: только README с таблицей заданий"
}

# 3) Для каждой папки: ветка с коротким именем, в ней только README + эта папка
foreach ($p in $pairs) {
    $folder = $p.Folder
    $branch = $p.Branch
    if (-not (Test-Path $folder)) {
        Write-Host "Пропуск: папка $folder не найдена"
        continue
    }
    git checkout main
    git checkout -b $branch
    git add README.md
    git add $folder
    git commit -m "Задание: $folder"
    Write-Host "Ветка создана: $branch (папка $folder)"
}

git checkout main
Write-Host ""
Write-Host "Готово. Локальные ветки:"
git branch
Write-Host ""
Write-Host "Запушить все ветки: git push -u origin bewise appbooster ivelum uptrader mstroy whoisblogger cian amazon"
Write-Host "Или по одной: git push -u origin bewise"