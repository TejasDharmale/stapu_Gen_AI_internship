Write-Host "🎯 GenAI Sports Tournament Calendar - Setup" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python 3.8+ first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error creating virtual environment." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Virtual environment created successfully!" -ForegroundColor Green

Write-Host ""
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error activating virtual environment." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Virtual environment activated!" -ForegroundColor Green

Write-Host ""
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error installing dependencies." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green

Write-Host ""
Write-Host "📝 Setting up environment file..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item "env_example.txt" ".env"
    Write-Host "✅ Environment file created (.env)" -ForegroundColor Green
    Write-Host ""
    Write-Host "⚠️  IMPORTANT: You need to edit .env file with your OpenAI API key" -ForegroundColor Yellow
    Write-Host "   Get free `$5 credit at: https://platform.openai.com/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📝 Opening .env file for editing..." -ForegroundColor Yellow
    Start-Process notepad ".env"
} else {
    Write-Host "✅ Environment file already exists (.env)" -ForegroundColor Green
}

Write-Host ""
Write-Host "🗄️  Initializing database..." -ForegroundColor Yellow
python main.py init
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Error initializing database." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🎉 Setup completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "🚀 To run the application:" -ForegroundColor Cyan
Write-Host "   1. Activate virtual environment: venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "   2. Run Streamlit app: python main.py streamlit" -ForegroundColor White
Write-Host "   3. Or run API server: python main.py api" -ForegroundColor White
Write-Host ""
Write-Host "💡 The app will open in your browser automatically!" -ForegroundColor Cyan
Write-Host ""
Read-Host "Press Enter to exit"
