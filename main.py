#!/usr/bin/env python3

import sys
import os
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    if len(sys.argv) < 2:
        print("🎯 GenAI Sports Tournament Calendar")
        print("=" * 40)
        print("Usage: python main.py <command>")
        print("\nCommands:")
        print("  init      - Initialize database")
        print("  collect   - Collect tournament data")
        print("  export    - Export data to CSV/JSON")
        print("  streamlit - Run Streamlit app (opens in browser)")
        print("  api       - Run FastAPI server")
        print("  help      - Show this help message")
        return

    command = sys.argv[1].lower()
    
    if command == "help":
        main()
        return
        
    elif command == "init":
        print("🗄️  Initializing database...")
        try:
            from db_utils import init_database
            init_database()
            print("✅ Database initialized successfully!")
        except Exception as e:
            print(f"❌ Error initializing database: {e}")
            print("💡 Make sure you have activated your virtual environment")
        
    elif command == "collect":
        print("🔍 Collecting tournament data...")
        try:
            from data_collection import collect_tournaments
            tournaments = collect_tournaments()
            print(f"✅ Collected {len(tournaments)} tournaments")
        except Exception as e:
            print(f"❌ Error collecting data: {e}")
            print("💡 Make sure you have set up your .env file with OPENAI_API_KEY")
        
    elif command == "export":
        print("📤 Exporting data...")
        try:
            from export import export_to_csv, export_to_json
            export_to_csv()
            export_to_json()
            print("✅ Data exported successfully!")
        except Exception as e:
            print(f"❌ Error exporting data: {e}")
        
    elif command == "streamlit":
        print("🚀 Starting Streamlit app...")
        print("🌐 The app will open in your browser at http://localhost:8501")
        print("💡 Press Ctrl+C to stop the app")
        run_command("streamlit run src/app.py --server.port 8501")
        
    elif command == "api":
        print("🚀 Starting FastAPI server...")
        print("🌐 API will be available at http://localhost:8000")
        print("📖 API docs at http://localhost:8000/docs")
        print("💡 Press Ctrl+C to stop the server")
        run_command("uvicorn src.api:app --host 0.0.0.0 --port 8000 --reload")
        
    else:
        print(f"❌ Unknown command: {command}")
        print("💡 Use 'python main.py help' to see available commands")

if __name__ == "__main__":
    main()
