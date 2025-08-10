import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DB_PATH = Path("data/initial.db")
DB_PATH.parent.mkdir(exist_ok=True)

def get_connection():
    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

def init_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tournaments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tournament_name TEXT NOT NULL,
                sport TEXT NOT NULL,
                level TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                tournament_url TEXT,
                streaming_links TEXT,
                tournament_image TEXT,
                summary TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_sport ON tournaments(sport)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_level ON tournaments(level)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_start_date ON tournaments(start_date)")
        
        conn.commit()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()

def insert_tournament(tournament_data: Dict) -> bool:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO tournaments (
                tournament_name, sport, level, start_date, end_date,
                tournament_url, streaming_links, tournament_image, summary
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tournament_data.get('tournament_name'),
            tournament_data.get('sport'),
            tournament_data.get('level'),
            tournament_data.get('start_date'),
            tournament_data.get('end_date'),
            tournament_data.get('tournament_url'),
            tournament_data.get('streaming_links'),
            tournament_data.get('tournament_image'),
            tournament_data.get('summary')
        ))
        
        conn.commit()
        logger.info(f"Inserted tournament: {tournament_data.get('tournament_name')}")
        return True
        
    except Exception as e:
        logger.error(f"Error inserting tournament: {e}")
        return False
    finally:
        conn.close()

def get_all_tournaments() -> List[Dict]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM tournaments ORDER BY start_date ASC")
        rows = cursor.fetchall()
        
        tournaments = []
        for row in rows:
            tournament = dict(row)
            tournament['start_date'] = str(tournament['start_date'])
            tournament['end_date'] = str(tournament['end_date'])
            tournament['last_updated'] = str(tournament['last_updated'])
            tournaments.append(tournament)
        
        return tournaments
        
    except Exception as e:
        logger.error(f"Error fetching tournaments: {e}")
        return []
    finally:
        conn.close()

def get_tournaments_by_filter(sport: Optional[str] = None, level: Optional[str] = None) -> List[Dict]:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM tournaments WHERE 1=1"
        params = []
        
        if sport:
            query += " AND sport = ?"
            params.append(sport)
        
        if level:
            query += " AND level = ?"
            params.append(level)
        
        query += " ORDER BY start_date ASC"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        tournaments = []
        for row in rows:
            tournament = dict(row)
            tournament['start_date'] = str(tournament['start_date'])
            tournament['end_date'] = str(tournament['end_date'])
            tournament['last_updated'] = str(tournament['last_updated'])
            tournaments.append(tournament)
        
        return tournaments
        
    except Exception as e:
        logger.error(f"Error fetching filtered tournaments: {e}")
        return []
    finally:
        conn.close()

def get_tournament_stats() -> Dict:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM tournaments")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT sport, COUNT(*) as count FROM tournaments GROUP BY sport")
        sport_stats = {row['sport']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute("SELECT level, COUNT(*) as count FROM tournaments GROUP BY level")
        level_stats = {row['level']: row['count'] for row in cursor.fetchall()}
        
        return {
            'total_tournaments': total,
            'sport_distribution': sport_stats,
            'level_distribution': level_stats
        }
        
    except Exception as e:
        logger.error(f"Error fetching tournament stats: {e}")
        return {}
    finally:
        conn.close()

def clear_tournaments():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tournaments")
        conn.commit()
        logger.info("All tournaments cleared from database")
        
    except Exception as e:
        logger.error(f"Error clearing tournaments: {e}")
        raise
    finally:
        conn.close()
