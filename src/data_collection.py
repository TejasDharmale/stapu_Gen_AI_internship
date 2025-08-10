import requests
import logging
from datetime import datetime, timedelta
from dateutil import parser
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import random
import time
import openai
import os
from dotenv import load_dotenv

load_dotenv()

from db_utils import insert_tournament

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SPORTS = [
    "Cricket", "Football", "Badminton", "Running", "Gym", 
    "Cycling", "Swimming", "Kabaddi", "Yoga", "Basketball", 
    "Chess", "Table Tennis"
]

LEVELS = [
    "Corporate", "School", "College/University", "Club/Academy",
    "District", "State", "Zonal/Regional", "National", "International"
]

class TournamentCollector:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            logger.error("OpenAI API key not found in environment variables")
    
    def generate_search_queries(self, sport: str, level: str, count: int = 5) -> List[str]:
        try:
            prompt = f"Generate {count} specific search queries to find upcoming {sport} tournaments at {level} level happening after {datetime.now().strftime('%Y-%m-%d')}. Focus on official tournament websites, sports organizations, and event calendars. Return only the search queries, one per line."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sports tournament researcher. Generate specific, targeted search queries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            
            queries = response.choices[0].message.content.strip().split('\n')
            return [q.strip() for q in queries if q.strip()][:count]
            
        except Exception as e:
            logger.error(f"Error generating queries with OpenAI: {e}")
            return self._generate_fallback_queries(sport, level, count)
    
    def _generate_fallback_queries(self, sport: str, level: str, count: int) -> List[str]:
        base_queries = [
            f"{sport} {level} tournament 2025",
            f"{sport} {level} championship 2025",
            f"{sport} {level} league 2025",
            f"upcoming {sport} {level} events 2025",
            f"{sport} {level} competition 2025"
        ]
        return base_queries[:count]
    
    def search_web(self, query: str) -> List[Dict]:
        try:
            search_url = "https://api.duckduckgo.com/"
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = self.session.get(search_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            if 'AbstractURL' in data and data['AbstractURL']:
                results.append({
                    'title': data.get('AbstractText', ''),
                    'url': data['AbstractURL'],
                    'snippet': data.get('AbstractText', '')
                })
            
            for result in data.get('Results', [])[:5]:
                results.append({
                    'title': result.get('Title', ''),
                    'url': result.get('FirstURL', ''),
                    'snippet': result.get('Text', '')
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error searching web: {e}")
            return []
    
    def extract_tournament_data(self, search_results: List[Dict], sport: str, level: str) -> List[Dict]:
        tournaments = []
        
        for result in search_results:
            try:
                tournament_data = self._extract_from_content(result, sport, level)
                if tournament_data:
                    tournaments.append(tournament_data)
            except Exception as e:
                logger.error(f"Error extracting data from result: {e}")
                continue
        
        return tournaments
    
    def _extract_from_content(self, result: Dict, sport: str, level: str) -> Optional[Dict]:
        try:
            content = f"{result.get('title', '')} {result.get('snippet', '')}"
            
            prompt = f"""
            Extract tournament information from this text about {sport} at {level} level:
            "{content}"
            
            Return a JSON object with these fields:
            - tournament_name: Tournament name
            - start_date: Start date (YYYY-MM-DD format)
            - end_date: End date (YYYY-MM-DD format)
            - tournament_url: Official URL if found
            - summary: Brief description (max 100 words)
            
            If no tournament info found, return null.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data extraction specialist. Extract only tournament information and return valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            try:
                import json
                data = json.loads(response.choices[0].message.content.strip())
                
                if data and isinstance(data, dict):
                    tournament = {
                        'tournament_name': data.get('tournament_name', ''),
                        'sport': sport,
                        'level': level,
                        'start_date': data.get('start_date', ''),
                        'end_date': data.get('end_date', ''),
                        'tournament_url': data.get('tournament_url', result.get('url', '')),
                        'streaming_links': self._suggest_streaming_links(data.get('tournament_name', ''), sport),
                        'tournament_image': '',
                        'summary': data.get('summary', '')
                    }
                    
                    if self._validate_tournament_data(tournament):
                        return tournament
                        
            except json.JSONDecodeError:
                logger.warning("Failed to parse JSON response from OpenAI")
                
        except Exception as e:
            logger.error(f"Error extracting tournament data: {e}")
        
        return None
    
    def _validate_tournament_data(self, tournament: Dict) -> bool:
        required_fields = ['tournament_name', 'start_date', 'end_date']
        
        for field in required_fields:
            if not tournament.get(field):
                return False
        
        try:
            start_date = parser.parse(tournament['start_date'])
            end_date = parser.parse(tournament['end_date'])
            
            if start_date < datetime.now() or end_date < start_date:
                return False
                
        except:
            return False
        
        return True
    
    def _suggest_streaming_links(self, tournament_name: str, sport: str) -> str:
        try:
            prompt = f"Suggest 2-3 streaming platforms or TV channels that might broadcast {sport} tournaments like '{tournament_name}'. Return only the platform names separated by commas."
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sports broadcasting expert. Suggest relevant streaming platforms."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error suggesting streaming links: {e}")
            return "N/A"
    
    def collect_tournaments(self, max_per_sport: int = 3) -> List[Dict]:
        all_tournaments = []
        
        for sport in SPORTS:
            for level in LEVELS:
                try:
                    logger.info(f"Collecting {sport} tournaments at {level} level...")
                    
                    queries = self.generate_search_queries(sport, level, 3)
                    sport_tournaments = []
                    
                    for query in queries:
                        search_results = self.search_web(query)
                        tournaments = self.extract_tournament_data(search_results, sport, level)
                        
                        for tournament in tournaments:
                            if len(sport_tournaments) >= max_per_sport:
                                break
                            
                            if self._is_unique_tournament(tournament, sport_tournaments):
                                sport_tournaments.append(tournament)
                                if insert_tournament(tournament):
                                    all_tournaments.append(tournament)
                                    logger.info(f"Added tournament: {tournament['tournament_name']}")
                        
                        time.sleep(1)
                    
                    logger.info(f"Collected {len(sport_tournaments)} {sport} tournaments at {level} level")
                    
                except Exception as e:
                    logger.error(f"Error collecting {sport} tournaments at {level} level: {e}")
                    continue
        
        logger.info(f"Total tournaments collected: {len(all_tournaments)}")
        return all_tournaments
    
    def _is_unique_tournament(self, tournament: Dict, existing_tournaments: List[Dict]) -> bool:
        for existing in existing_tournaments:
            if (existing['tournament_name'].lower() == tournament['tournament_name'].lower() or
                existing['start_date'] == tournament['start_date']):
                return False
        return True

def collect_tournaments() -> List[Dict]:
    collector = TournamentCollector()
    return collector.collect_tournaments()

if __name__ == "__main__":
    tournaments = collect_tournaments()
    print(f"Collected {len(tournaments)} tournaments")
