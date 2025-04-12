import sqlite3
from utils import haversine_distance
import uuid

DB_FILE = 'cypress.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lat REAL,
            lon REAL,
            description TEXT,
            issue_type TEXT,
            unique_id TEXT,
            image BLOB
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False

def validate_user(username, password):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = c.fetchone()
    conn.close()
    return user is not None

def save_report(lat, lon, description, issue_type, image_blob):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    unique_id = str(uuid.uuid4())
    c.execute('''
        INSERT INTO reports (lat, lon, description, issue_type, unique_id, image)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (lat, lon, description, issue_type, unique_id, image_blob))
    conn.commit()   
    conn.close()

def get_reports():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT lat, lon, description, issue_type, unique_id FROM reports')
    rows = c.fetchall()
    conn.close()
    return [{
        'lat': r[0],
        'lon': r[1],
        'description': r[2], 
        'issue_type': r[3],
        'unique_id': r[4],
    } for r in rows]

def is_duplicate(lat, lon, threshold=0.1):
    reports = get_reports()
    for report in reports:
        dist = haversine_distance(lat, lon, report['lat'], report['lon'])
        if dist < threshold:
            return True
    return False

def delete_report(unique_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM reports WHERE unique_id = ?', (unique_id,))
    conn.commit()
    conn.close()

def get_report_image(unique_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT image FROM reports WHERE unique_id = ?', (unique_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None