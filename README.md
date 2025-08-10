# GenAI Sports Tournament Calendar

A simple GenAI-powered application that collects and displays upcoming sports tournaments.

## 🚀 Quick Start (5 minutes)

### 1. Setup Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables
```bash
# Copy environment file
copy env_example.txt .env

# Edit .env file with your OpenAI API key
# Get free $5 credit at: https://platform.openai.com/
```

### 4. Initialize Database
```bash
python main.py init
```

### 5. Run the Application
```bash
# Option 1: Streamlit UI (Recommended)
python main.py streamlit

# Option 2: FastAPI Backend
python main.py api

# Option 3: Collect data manually
python main.py collect
```

## 🎯 What This App Does

- **Collects** upcoming sports tournaments from the web
- **Displays** them in a beautiful Streamlit interface
- **Filters** by sport, level, and date
- **Exports** data to CSV/JSON
- **Uses AI** to extract and summarize tournament information

## 🏟️ Supported Sports
Cricket, Football, Badminton, Running, Gym, Cycling, Swimming, Kabaddi, Yoga, Basketball, Chess, Table Tennis

## 📊 Supported Levels
Corporate, School, College, Club, District, State, Regional, National, International

## 🔑 Required Setup

**Only one API key needed:**
- **OpenAI API Key**: Get $5 free credit at https://platform.openai.com/
- **Search**: Uses free DuckDuckGo (no API key needed)

## 🛠️ Troubleshooting

### Common Issues:
1. **Port already in use**: Change port in main.py or kill existing process
2. **API key error**: Make sure .env file exists and has correct OPENAI_API_KEY
3. **Import errors**: Make sure virtual environment is activated

### Reset Everything:
```bash
# Delete and recreate virtual environment
rmdir /s venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py init
```

## 📁 Project Structure
```
├── main.py              # Main entry point
├── src/
│   ├── app.py          # Streamlit frontend
│   ├── api.py          # FastAPI backend
│   ├── data_collection.py  # Data collection logic
│   └── db_utils.py     # Database operations
├── data/               # SQLite database
└── exports/            # Exported data files
```

## 🎮 Usage Examples

```bash
# Initialize everything
python main.py init

# Start the web app
python main.py streamlit

# In another terminal, collect data
python main.py collect

# Export data
python main.py export
```

That's it! The app will open in your browser at http://localhost:8501

---

**Need help?** Check the logs or create an issue with error details.
