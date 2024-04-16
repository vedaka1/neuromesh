up_sql = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE,
);
"""
