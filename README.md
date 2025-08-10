# Stapu GenAI Internship Project

## What This App Does

This is a **GenAI-powered sports tournament calendar application** that:

- **Collects** upcoming sports tournaments from the web using AI
- **Displays** them in a beautiful web interface
- **Filters** tournaments by sport, level, and date
- **Exports** data to CSV/JSON formats
- **Supports** multiple sports: Cricket, Football, Badminton, Running, Gym, Cycling, Swimming, Kabaddi, Yoga, Basketball, Chess, Table Tennis
- **Covers** various levels: Corporate, School, College, Club, District, State, Regional, National, International

## Quick Start

1. **Setup**: `python -m venv venv && venv\Scripts\activate`
2. **Install**: `pip install -r requirements.txt`
3. **Configure**: Copy `env_example.txt` to `.env` and add your OpenAI API key
4. **Initialize**: `python main.py init`
5. **Run**: `python main.py streamlit`

The app will open in your browser at http://localhost:8501

## Features

- **AI-Powered Data Collection**: Automatically finds and extracts tournament information
- **Interactive Web Interface**: Built with Streamlit for easy navigation
- **Database Storage**: SQLite database for persistent data
- **Export Options**: Download data in multiple formats
- **Real-time Updates**: Collect fresh data on demand

That's it! A simple but powerful sports tournament discovery tool powered by AI.
