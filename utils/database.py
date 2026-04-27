# utils/database.py
# All SQLite helpers: init, CRUD, queries

import sqlite3
import hashlib
import json
from datetime import datetime

DB_PATH = "intelliwatt.db"


# ── Helpers ──────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _connect():
    return sqlite3.connect(DB_PATH)


# ── Schema & Seed ────────────────────────────────────────────

def init_db():
    conn = _connect()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT NOT NULL,
            email TEXT,
            role TEXT NOT NULL DEFAULT 'tech',
            building_assigned INTEGER,
            avatar TEXT DEFAULT '👤',
            created_at TEXT NOT NULL,
            last_login TEXT,
            theme TEXT DEFAULT 'light',
            language TEXT DEFAULT 'fr',
            notifications INTEGER DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS archive_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            action TEXT,
            building TEXT,
            data_json TEXT,
            created_at TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS opt_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            batiment TEXT,
            avant_kwh REAL,
            apres_kwh REAL,
            economie_pct REAL,
            economie_da REAL,
            periode TEXT,
            created_at TEXT
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS device_controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            building_id INTEGER,
            device_type TEXT,
            device_name TEXT,
            status INTEGER DEFAULT 1,
            last_updated TEXT,
            updated_by TEXT
        )
    ''')

    # Default accounts
    admin_hash = hash_password("admin2024")
    c.execute('''
        INSERT OR IGNORE INTO users
        (username, password_hash, full_name, email, role, avatar, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', ("admin", admin_hash, "Administrateur Système",
          "admin@batna2.dz", "admin", "👨‍💼", datetime.now().isoformat()))

    tech_hash = hash_password("tech1234")
    c.execute('''
        INSERT OR IGNORE INTO users
        (username, password_hash, full_name, email, role, building_assigned, avatar, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', ("tech01", tech_hash, "Ahmed Benali",
          "a.benali@batna2.dz", "tech", 1, "👨‍🔧", datetime.now().isoformat()))

    # Seed devices
    c.execute("SELECT COUNT(*) FROM device_controls")
    if c.fetchone()[0] == 0:
        devices = []
        for b_id in range(1, 9):
            devices.extend([
                (b_id, "lumiere",   f"Éclairage Zone A — Bât {b_id}",  1),
                (b_id, "lumiere",   f"Éclairage Zone B — Bât {b_id}",  1),
                (b_id, "porte",     f"Porte Principale — Bât {b_id}",  1),
                (b_id, "fenetre",   f"Fenêtres Sud — Bât {b_id}",      1),
                (b_id, "chauffage", f"Chauffage Central — Bât {b_id}", 1),
                (b_id, "clim",      f"Climatisation — Bât {b_id}",     0),
            ])
        now = datetime.now().isoformat()
        c.executemany(
            "INSERT INTO device_controls (building_id,device_type,device_name,status,last_updated,updated_by) VALUES (?,?,?,?,?,?)",
            [(d[0], d[1], d[2], d[3], now, "system") for d in devices],
        )

    conn.commit()
    conn.close()


# ── Auth ─────────────────────────────────────────────────────

def verify_login(username: str, password: str):
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM users WHERE username=? AND password_hash=?",
        (username, hash_password(password)),
    )
    user = c.fetchone()
    if user:
        c.execute(
            "UPDATE users SET last_login=? WHERE username=?",
            (datetime.now().isoformat(), username),
        )
        conn.commit()
    conn.close()
    return user


def create_user(username, password, full_name, email, role, building_assigned, avatar="👤"):
    conn = _connect()
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (username,password_hash,full_name,email,role,building_assigned,avatar,created_at)
            VALUES (?,?,?,?,?,?,?,?)
        ''', (username, hash_password(password), full_name, email, role,
              building_assigned, avatar, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        return True, "Compte créé avec succès !"
    except sqlite3.IntegrityError:
        conn.close()
        return False, "Nom d'utilisateur déjà utilisé."


# ── User profile ─────────────────────────────────────────────

def update_password(user_id, old_password, new_password):
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE id=?", (user_id,))
    row = c.fetchone()
    if not row or row[0] != hash_password(old_password):
        conn.close()
        return False, "Ancien mot de passe incorrect."
    c.execute("UPDATE users SET password_hash=? WHERE id=?",
              (hash_password(new_password), user_id))
    conn.commit()
    conn.close()
    return True, "Mot de passe mis à jour avec succès !"


def update_profile(user_id, full_name, email, avatar):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE users SET full_name=?,email=?,avatar=? WHERE id=?",
              (full_name, email, avatar, user_id))
    conn.commit()
    conn.close()


def update_preferences(user_id, theme, language, notifications):
    conn = _connect()
    c = conn.cursor()
    c.execute("UPDATE users SET theme=?,language=?,notifications=? WHERE id=?",
              (theme, language, notifications, user_id))
    conn.commit()
    conn.close()


def get_all_users():
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "SELECT id,username,full_name,email,role,building_assigned,avatar,created_at,last_login"
        " FROM users ORDER BY created_at DESC"
    )
    users = c.fetchall()
    conn.close()
    return users


# ── Devices ──────────────────────────────────────────────────

def get_device_controls(building_id=None):
    conn = _connect()
    c = conn.cursor()
    if building_id:
        c.execute(
            "SELECT * FROM device_controls WHERE building_id=? ORDER BY device_type,device_name",
            (building_id,),
        )
    else:
        c.execute("SELECT * FROM device_controls ORDER BY building_id,device_type")
    devices = c.fetchall()
    conn.close()
    return devices


def toggle_device(device_id, new_status, username):
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "UPDATE device_controls SET status=?,last_updated=?,updated_by=? WHERE id=?",
        (new_status, datetime.now().isoformat(), username, device_id),
    )
    conn.commit()
    conn.close()


# ── Archive ──────────────────────────────────────────────────

def save_archive(user_id, username, action, building, data):
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "INSERT INTO archive_log (user_id,username,action,building,data_json,created_at) VALUES (?,?,?,?,?,?)",
        (user_id, username, action, building, json.dumps(data), datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def get_archive_log(limit=50):
    conn = _connect()
    c = conn.cursor()
    c.execute("SELECT * FROM archive_log ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows


# ── Optimisation history ─────────────────────────────────────

def save_opt_history(user_id, data: dict):
    conn = _connect()
    c = conn.cursor()
    c.execute('''
        INSERT INTO opt_history (user_id,batiment,avant_kwh,apres_kwh,economie_pct,economie_da,periode,created_at)
        VALUES (?,?,?,?,?,?,?,?)
    ''', (user_id, data["batiment"], data["avant_kwh"], data["apres_kwh"],
          data["economie_pct"], data["economie_da"], data["periode"],
          datetime.now().isoformat()))
    conn.commit()
    conn.close()


def get_opt_history(user_id, limit=20):
    conn = _connect()
    c = conn.cursor()
    c.execute(
        "SELECT * FROM opt_history WHERE user_id=? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    )
    rows = c.fetchall()
    conn.close()
    return rows
