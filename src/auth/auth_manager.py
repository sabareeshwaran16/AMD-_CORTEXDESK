"""Authentication system for CortexDesk"""
import hashlib
import secrets
import json
import os
from datetime import datetime, timedelta

class AuthManager:
    def __init__(self, data_dir="data"):
        self.users_file = os.path.join(data_dir, "users.json")
        self.sessions_file = os.path.join(data_dir, "sessions.json")
        self._ensure_files()
    
    def _ensure_files(self):
        os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({}, f)
        if not os.path.exists(self.sessions_file):
            with open(self.sessions_file, 'w') as f:
                json.dump({}, f)
    
    def _hash_password(self, password: str, salt: str) -> str:
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    
    def signup(self, username: str, password: str, email: str) -> dict:
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if username in users:
            return {"success": False, "error": "Username already exists"}
        
        salt = secrets.token_hex(16)
        hashed = self._hash_password(password, salt)
        
        users[username] = {
            "email": email,
            "password": hashed,
            "salt": salt,
            "created_at": datetime.now().isoformat()
        }
        
        with open(self.users_file, 'w') as f:
            json.dump(users, f, indent=2)
        
        return {"success": True, "message": "Account created"}
    
    def login(self, username: str, password: str) -> dict:
        with open(self.users_file, 'r') as f:
            users = json.load(f)
        
        if username not in users:
            return {"success": False, "error": "Invalid credentials"}
        
        user = users[username]
        hashed = self._hash_password(password, user["salt"])
        
        if hashed != user["password"]:
            return {"success": False, "error": "Invalid credentials"}
        
        token = secrets.token_urlsafe(32)
        
        with open(self.sessions_file, 'r') as f:
            sessions = json.load(f)
        
        sessions[token] = {
            "username": username,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=7)).isoformat()
        }
        
        with open(self.sessions_file, 'w') as f:
            json.dump(sessions, f, indent=2)
        
        return {"success": True, "token": token, "username": username, "email": user["email"]}
    
    def logout(self, token: str) -> dict:
        with open(self.sessions_file, 'r') as f:
            sessions = json.load(f)
        
        if token in sessions:
            del sessions[token]
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            return {"success": True}
        
        return {"success": False, "error": "Invalid session"}
    
    def verify_token(self, token: str):
        with open(self.sessions_file, 'r') as f:
            sessions = json.load(f)
        
        if token not in sessions:
            return None
        
        session = sessions[token]
        expires = datetime.fromisoformat(session["expires_at"])
        
        if datetime.now() > expires:
            del sessions[token]
            with open(self.sessions_file, 'w') as f:
                json.dump(sessions, f, indent=2)
            return None
        
        return session
