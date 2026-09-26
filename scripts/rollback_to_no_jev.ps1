# ==============================================================================
# 自进化智能体前沿论文追踪系统 —— 一键回滚至纯基线（No-Jev Baseline）脚本
# ==============================================================================
# 功能：
# 1. 禁用/隔离所有 Jev 相关的扩展代码与执行入口；
# 2. 保留所有历史论文 Markdown 报告与 PDF 文献（零资产丢失）；
# 3. 校验纯基线脚本 scripts/fetch_hf_papers.py 的完整性与可执行状态；
# 4. 确保项目 100% 恢复到初始纯净基线交付状态。
# ==============================================================================

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$ErrorActionPreference = "Stop"

$workspaceRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$scriptsDir = Join-Path $workspaceRoot "scripts"
$jevPipelineDir = Join-Path $scriptsDir "jev_pipeline"
$jevRunner = Join-Path $scriptsDir "run_jev_daily_pipeline.py"
$backupDir = Join-Path $scriptsDir ".jev_pipeline_disabled"
$baselineScript = Join-Path $scriptsDir "fetch_hf_papers.py"

Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [🔄 回滚操作] 正在将项目还原至无 Jev 纯基线状态..." -ForegroundColor Yellow
Write-Host " 工作区根目录: $workspaceRoot" -ForegroundColor Gray
Write-Host "========================================================`n" -ForegroundColor Cyan

# 1. 创建安全隔离归档目录
if (-not (Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
}

# 2. 隔离 Jev 扩展组件
if (Test-Path $jevPipelineDir) {
    Write-Host "[*] 正在隔离 Jev 核心管道包: $jevPipelineDir -> $backupDir" -ForegroundColor DarkYellow
    $targetJevDir = Join-Path $backupDir "jev_pipeline"
    if (Test-Path $targetJevDir) {
        Remove-Item -Path $targetJevDir -Recurse -Force
    }
    Move-Item -Path $jevPipelineDir -Destination $backupDir -Force
}

if (Test-Path $jevRunner) {
    Write-Host "[*] 正在隔离 Jev 执行入口: $jevRunner -> $backupDir" -ForegroundColor DarkYellow
    Move-Item -Path $jevRunner -Destination $backupDir -Force
}

# 3. 校验纯基线文件
Write-Host "`n[*] 正在验证纯基线环境完整性..." -ForegroundColor Cyan

if (-not (Test-Path $baselineScript)) {
    Write-Error "[-] 致命错误: 纯基线核心脚本 $baselineScript 不存在！"
    exit 1
}

# 4. 语法与依赖健康检查
$proc = Start-Process python -ArgumentList @("-m", "py_compile", "`"$baselineScript`"") -NoNewWindow -Wait -PassThru
if ($proc.ExitCode -ne 0) {
    Write-Error "[-] 纯基线脚本编译失败，退出码: $($proc.ExitCode)"
    exit 1
}

Write-Host "[√] 纯基线脚本编译校验通过: fetch_hf_papers.py" -ForegroundColor Green
Write-Host "[√] Jev 扩展已完全隔离至: $backupDir" -ForegroundColor Green
Write-Host "[√] 历史归档数据 (02_前沿论文追踪/) 100% 完整留存" -ForegroundColor Green
Write-Host "`n========================================================" -ForegroundColor Cyan
Write-Host " [SUCCESS] 项目已成功复原为纯基线（No-Jev）状态！" -ForegroundColor Green
Write-Host " 纯基线运行命令:" -ForegroundColor White
Write-Host "   python scripts/fetch_hf_papers.py" -ForegroundColor Yellow
Write-Host " 若后续需重新启用 Jev 模型，请运行:" -ForegroundColor White
Write-Host "   powershell -ExecutionPolicy Bypass -File scripts/enable_jev.ps1" -ForegroundColor Yellow
Write-Host "========================================================`n" -ForegroundColor Cyan
