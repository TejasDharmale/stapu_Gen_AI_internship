-- Tournament Database Schema
CREATE TABLE tournaments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tournament_name TEXT NOT NULL,
    sport TEXT NOT NULL,
    level TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    official_url TEXT,
    streaming_links TEXT,
    tournament_image TEXT,
    summary TEXT,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_sport ON tournaments(sport);
CREATE INDEX idx_level ON tournaments(level);
CREATE INDEX idx_start_date ON tournaments(start_date);
CREATE INDEX idx_sport_level ON tournaments(sport, level);