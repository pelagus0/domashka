# Восстановление папок 01-07 из Git (если нет) и запуск задания 1-8
# Использование: .\restore-and-run.ps1 4   или   .\restore-and-run.ps1 08

param(
    [Parameter(Mandatory=$true)]
    [ValidateRange(1, 8)]
    [int]$TaskNumber
)

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

$folders = @{
    1 = "01_backend_Bewise"
    2 = "02_backend_AppBooster"
    3 = "03_backend_Ivelum"
    4 = "04_backend_UpTrader"
    5 = "05_backend_MStroy"
    6 = "06_analytics_WhoIsBlogger"
    7 = "07_analytics_Cian"
    8 = "08_analytics_Amazon"
}

$ports = @{
    1 = 8000
    2 = 8001
    3 = 8002
    4 = 8000
    5 = 8003
}

$folder = $folders[$TaskNumber]
$path = Join-Path $root $folder

# Восстановить папку из Git, если не существует
if (-not (Test-Path $path)) {
    Write-Host "Папка $folder не найдена. Восстанавливаю из Git..." -ForegroundColor Yellow
    Push-Location $root
    try {
        git fetch origin 2>$null
        git checkout origin/main -- $folder
        if (-not (Test-Path $path)) {
            git checkout main -- $folder 2>$null
        }
    } finally {
        Pop-Location
    }
    if (-not (Test-Path $path)) {
        Write-Host "Не удалось восстановить $folder. Выполните: git fetch origin; git checkout origin/main -- $folder" -ForegroundColor Red
        exit 1
    }
    Write-Host "Готово: $folder" -ForegroundColor Green
}

Set-Location $path

if ($TaskNumber -le 5) {
    $port = $ports[$TaskNumber]
    Write-Host "Запуск задания $TaskNumber (Docker). После старта откройте http://localhost:$port" -ForegroundColor Cyan
    docker compose up --build
} else {
    Write-Host "Запуск задания $TaskNumber (Docker + Python). Сначала поднимите БД:" -ForegroundColor Cyan
    Write-Host "  docker compose up -d" -ForegroundColor Gray
    Write-Host "  python run.py" -ForegroundColor Gray
    docker compose up -d
    if ($LASTEXITCODE -eq 0) {
        python run.py
    }
}
