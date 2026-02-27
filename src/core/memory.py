import time
import sqlite3
import json
from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import os

class WorkingMemory:
    def __init__(self):
        self.memory: Dict[str, Any] = {}
        self.ttl: Dict[str, float] = {}
    
    def write(self, key: str, value: Any, ttl_seconds: int = 3600):
        self.memory[key] = value
        self.ttl[key] = time.time() + ttl_seconds
    
    def read(self, key: str) -> Optional[Any]:
        if key in self.ttl and time.time() > self.ttl[key]:
            del self.memory[key]
            del self.ttl[key]
            return None
        return self.memory.get(key)
    
    def clear(self, key: str):
        self.memory.pop(key, None)
        self.ttl.pop(key, None)

class EpisodicMemory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()
    
    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                timestamp DATETIME,
                source_file TEXT,
                content TEXT,
                participants TEXT,
                metadata TEXT
            )
        """)
        self.conn.commit()
    
    def add(self, event_type: str, content: str, source_file: str = "", 
            participants: list = None, metadata: dict = None):
        self.conn.execute(
            "INSERT INTO episodes VALUES (NULL, ?, ?, ?, ?, ?, ?)",
            (event_type, datetime.now(), source_file, content,
             json.dumps(participants or []), json.dumps(metadata or {}))
        )
        self.conn.commit()
    
    def query_recent(self, days: int = 30, event_type: str = None):
        cutoff = datetime.now() - timedelta(days=days)
        query = "SELECT * FROM episodes WHERE timestamp > ?"
        params = [cutoff]
        
        if event_type:
            query += " AND event_type = ?"
            params.append(event_type)
        
        cursor = self.conn.execute(query, params)
        return cursor.fetchall()

class ProceduralMemory:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._init_tables()
    
    def _init_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS corrections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_output TEXT,
                corrected_output TEXT,
                correction_type TEXT,
                timestamp DATETIME
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_type TEXT,
                pattern_data TEXT,
                confidence REAL,
                usage_count INTEGER
            )
        """)
        self.conn.commit()
    
    def record_correction(self, original: str, corrected: str, correction_type: str):
        self.conn.execute(
            "INSERT INTO corrections VALUES (NULL, ?, ?, ?, ?)",
            (original, corrected, correction_type, datetime.now())
        )
        self.conn.commit()
    
    def add_pattern(self, pattern_type: str, pattern_data: dict, confidence: float = 0.5):
        self.conn.execute(
            "INSERT INTO patterns VALUES (NULL, ?, ?, ?, ?)",
            (pattern_type, json.dumps(pattern_data), confidence, 0)
        )
        self.conn.commit()

class EncryptedStorage:
    def __init__(self, key_path: str):
        if os.path.exists(key_path):
            with open(key_path, 'rb') as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            os.makedirs(os.path.dirname(key_path), exist_ok=True)
            with open(key_path, 'wb') as f:
                f.write(self.key)
        self.cipher = Fernet(self.key)
    
    def encrypt(self, data: str) -> bytes:
        return self.cipher.encrypt(data.encode())
    
    def decrypt(self, encrypted_data: bytes) -> str:
        return self.cipher.decrypt(encrypted_data).decode()
