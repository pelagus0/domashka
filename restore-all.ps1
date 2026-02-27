# Восстанавливает все папки заданий 01-07 из ветки main на GitHub.
# Запустите один раз в корне проекта: .\restore-all.ps1

$ErrorActionPreference = "Stop"
$root = $PSScriptRoot

$folders = @(
    "01_backend_Bewise",
    "02_backend_AppBooster",
    "03_backend_Ivelum",
    "04_backend_UpTrader",
    "05_backend_MStroy",
    "06_analytics_WhoIsBlogger",
    "07_analytics_Cian"
)

Push-Location $root
try {
    Write-Host "Fetch с GitHub..." -ForegroundColor Cyan
    git fetch origin
    $restored = 0
    foreach ($f in $folders) {
        if (-not (Test-Path $f)) {
            Write-Host "  Восстанавливаю $f" -ForegroundColor Yellow
            git checkout origin/main -- $f 2>$null
            if (Test-Path $f) { $restored++ }
        }
    }
    if ($restored -eq 0) {
        Write-Host "Все папки уже на месте." -ForegroundColor Green
    } else {
        Write-Host "Готово. Восстановлено папок: $restored" -ForegroundColor Green
    }
} finally {
    Pop-Location
}
