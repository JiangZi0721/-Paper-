# ==============================================================================
# 自进化智能体前沿论文追踪系统 —— 一键重新启用 Jev 模型分诊引擎脚本
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptsDir = Join-Path $workspaceRoot "scripts"
$backupDir = Join-Path $scriptsDir ".jev_pipeline_disabled"
$jevPipelineDir = Join-Path $scriptsDir "jev_pipeline"
$jevRunner = Join-Path $scriptsDir "run_jev_daily_pipeline.py"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [🚀 启用操作] 正在恢复并启用 Jev 模型深度研判引擎..." -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Cyan

# 1. 从隔离备份中恢复（如果存在）
if (Test-Path $backupDir) {
    $backupPipeline = Join-Path $backupDir "jev_pipeline"
    $backupRunner = Join-Path $backupDir "run_jev_daily_pipeline.py"
    
    if (Test-Path $backupPipeline) {
        Write-Host "[*] 正在从备份恢复 Jev 核心管道包..." -ForegroundColor DarkYellow
        if (Test-Path $jevPipelineDir) {
            Remove-Item -Path $jevPipelineDir -Recurse -Force
        }
        Move-Item -Path $backupPipeline -Destination $scriptsDir -Force
    }
    
    if (Test-Path $backupRunner) {
        Write-Host "[*] 正在从备份恢复 Jev 执行入口..." -ForegroundColor DarkYellow
        Move-Item -Path $backupRunner -Destination $scriptsDir -Force
    }
    
    # 清理空备份目录
    if ((Get-ChildItem -Path $backupDir).Count -eq 0) {
        Remove-Item -Path $backupDir -Force
    }
}

# 2. 检查必要文件
if (-not (Test-Path $jevPipelineDir) -or -not (Test-Path $jevRunner)) {
    Write-Error "[-] 错误: Jev 核心组件不完整，请检查 scripts/jev_pipeline/ 和 scripts/run_jev_daily_pipeline.py！"
    exit 1
}

# 3. 检查环境变量
$apiKey = $env:JEV_API_KEY
if (-not $apiKey) {
    $apiKey = $env:OPENJEV_API_KEY
}
if (-not $apiKey) {
    Write-Host "[!] 警告: 未检测到 JEV_API_KEY 或 OPENJEV_API_KEY 环境变量！" -ForegroundColor Red
    Write-Host "    执行前请先设置: `$env:JEV_API_KEY = '你的密钥'" -ForegroundColor Yellow
} else {
    Write-Host "[√] 检测到有效 Jev API Key 凭证配置" -ForegroundColor Green
}

# 4. 语法编译检查
$proc = Start-Process python -ArgumentList @("-m", "py_compile", "`"$jevRunner`"") -NoNewWindow -Wait -PassThru
if ($proc.ExitCode -ne 0) {
    Write-Error "[-] Jev 流水线编译失败，退出码: $($proc.ExitCode)"
    exit 1
}

Write-Host "[√] Jev 流水线语法校验通过: run_jev_daily_pipeline.py" -ForegroundColor Green
Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [SUCCESS] Jev 模型分诊引擎已就绪！" -ForegroundColor Green
Write-Host " 运行命令:" -ForegroundColor White
Write-Host "   python scripts/run_jev_daily_pipeline.py" -ForegroundColor Yellow
Write-Host "   python scripts/run_jev_daily_pipeline.py --date YYYY-MM-DD" -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Cyan
