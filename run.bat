@echo off
echo 🚀 Starting GenAI Sports Tournament Calendar...
echo.

echo 🔧 Activating virtual environment...
call venv\Scripts\activate
if %errorlevel% neq 0 (
    echo ❌ Error activating virtual environment. Run setup.bat first!
    pause
    exit /b 1
)

echo ✅ Virtual environment activated!

echo.
echo 🎯 Choose what to run:
echo.
echo 1. Streamlit App (Web Interface) - RECOMMENDED
echo 2. FastAPI Server (Backend API)
echo 3. Collect Data
echo 4. Export Data
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo 🚀 Starting Streamlit app...
    echo 🌐 The app will open in your browser at http://localhost:8501
    echo 💡 Press Ctrl+C to stop the app
    python main.py streamlit
) else if "%choice%"=="2" (
    echo 🚀 Starting FastAPI server...
    echo 🌐 API will be available at http://localhost:8000
    echo 📖 API docs at http://localhost:8000/docs
    echo 💡 Press Ctrl+C to stop the server
    python main.py api
) else if "%choice%"=="3" (
    echo 🔍 Collecting tournament data...
    python main.py collect
    pause
) else if "%choice%"=="4" (
    echo 📤 Exporting data...
    python main.py export
    pause
) else if "%choice%"=="5" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice. Please run the script again.
    pause
    exit /b 1
)
