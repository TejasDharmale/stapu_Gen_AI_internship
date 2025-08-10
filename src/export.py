import csv
import json
import logging
from pathlib import Path
from typing import List, Dict
from db_utils import get_all_tournaments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def export_to_csv(filename: str = "tournaments.csv") -> bool:
    try:
        tournaments = get_all_tournaments()
        
        if not tournaments:
            logger.warning("No tournaments to export")
            return False
        
        fieldnames = [
            'Tournament Name', 'Sport', 'Level', 'Start Date', 'End Date',
            'Tournament Official URL', 'Streaming Partners/Links', 
            'Tournament Image', 'Summary of Tournament'
        ]
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for tournament in tournaments:
                writer.writerow({
                    'Tournament Name': tournament.get('tournament_name', 'N/A'),
                    'Sport': tournament.get('sport', 'N/A'),
                    'Level': tournament.get('level', 'N/A'),
                    'Start Date': tournament.get('start_date', 'N/A'),
                    'End Date': tournament.get('end_date', 'N/A'),
                    'Tournament Official URL': tournament.get('tournament_url', 'N/A'),
                    'Streaming Partners/Links': tournament.get('streaming_links', 'N/A'),
                    'Tournament Image': tournament.get('tournament_image', 'N/A'),
                    'Summary of Tournament': tournament.get('summary', 'N/A')
                })
        
        logger.info(f"Exported {len(tournaments)} tournaments to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting to CSV: {e}")
        return False

def export_to_json(filename: str = "tournaments.json") -> bool:
    try:
        tournaments = get_all_tournaments()
        
        if not tournaments:
            logger.warning("No tournaments to export")
            return False
        
        export_data = []
        for tournament in tournaments:
            export_data.append({
                'Tournament Name': tournament.get('tournament_name', 'N/A'),
                'Sport': tournament.get('sport', 'N/A'),
                'Level': tournament.get('level', 'N/A'),
                'Start Date': tournament.get('start_date', 'N/A'),
                'End Date': tournament.get('end_date', 'N/A'),
                'Tournament Official URL': tournament.get('tournament_url', 'N/A'),
                'Streaming Partners/Links': tournament.get('streaming_links', 'N/A'),
                'Tournament Image': tournament.get('tournament_image', 'N/A'),
                'Summary of Tournament': tournament.get('summary', 'N/A')
            })
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported {len(tournaments)} tournaments to {filename}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting to JSON: {e}")
        return False

def create_sample_files():
    try:
        sample_tournaments = [
            {
                'Tournament Name': 'Cricket Premier League 2025',
                'Sport': 'Cricket',
                'Level': 'National',
                'Start Date': '2025-03-15',
                'End Date': '2025-05-15',
                'Tournament Official URL': 'https://example.com/cpl2025',
                'Streaming Partners/Links': 'Hotstar, Sony Sports',
                'Tournament Image': 'https://example.com/cpl2025.jpg',
                'Summary of Tournament': 'Annual cricket tournament featuring top teams from across the country'
            },
            {
                'Tournament Name': 'Football Championship 2025',
                'Sport': 'Football',
                'Level': 'International',
                'Start Date': '2025-06-01',
                'End Date': '2025-07-15',
                'Tournament Official URL': 'https://example.com/fc2025',
                'Streaming Partners/Links': 'ESPN+, DAZN',
                'Tournament Image': 'https://example.com/fc2025.jpg',
                'Summary of Tournament': 'International football championship with teams from multiple continents'
            },
            {
                'Tournament Name': 'Badminton Open 2025',
                'Sport': 'Badminton',
                'Level': 'State',
                'Start Date': '2025-04-10',
                'End Date': '2025-04-20',
                'Tournament Official URL': 'https://example.com/bo2025',
                'Streaming Partners/Links': 'YouTube Live',
                'Tournament Image': 'https://example.com/bo2025.jpg',
                'Summary of Tournament': 'State-level badminton tournament for amateur and professional players'
            }
        ]
        
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        
        csv_file = exports_dir / "sample.csv"
        json_file = exports_dir / "sample.json"
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Tournament Name', 'Sport', 'Level', 'Start Date', 'End Date',
                'Tournament Official URL', 'Streaming Partners/Links', 
                'Tournament Image', 'Summary of Tournament'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(sample_tournaments)
        
        with open(json_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(sample_tournaments, jsonfile, indent=2, ensure_ascii=False)
        
        logger.info(f"Sample files created: {csv_file}, {json_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error creating sample files: {e}")
        return False

def export_filtered_data(sport: str = None, level: str = None, format: str = "csv") -> bool:
    try:
        from db_utils import get_tournaments_by_filter
        
        tournaments = get_tournaments_by_filter(sport=sport, level=level)
        
        if not tournaments:
            logger.warning("No tournaments found with the specified filters")
            return False
        
        exports_dir = Path("exports")
        exports_dir.mkdir(exist_ok=True)
        
        if format.lower() == "csv":
            filename = exports_dir / f"tournaments_{sport or 'all'}_{level or 'all'}.csv"
            return export_to_csv(str(filename))
        elif format.lower() == "json":
            filename = exports_dir / f"tournaments_{sport or 'all'}_{level or 'all'}.json"
            return export_to_json(str(filename))
        else:
            logger.error(f"Unsupported format: {format}")
            return False
            
    except Exception as e:
        logger.error(f"Error exporting filtered data: {e}")
        return False

if __name__ == "__main__":
    create_sample_files()
    export_to_csv()
    export_to_json()
