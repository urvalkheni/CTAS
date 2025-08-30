import json
import os
import uuid
from datetime import datetime
import hashlib

class AuthManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.api_keys_file = "data/api_keys.json"
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        """Ensure data files exist"""
        os.makedirs("data", exist_ok=True)
        
        if not os.path.exists(self.users_file):
            # Create default users for demo
            default_users = [
                {
                    "_id": str(uuid.uuid4()),
                    "name": "Admin User",
                    "email": "admin@coastalguardian.com",
                    "passwordHash": self._hash_password("demo123"),
                    "role": "authority",
                    "location": {"type": "Point", "coordinates": [72.8777, 19.0760]},
                    "points": 0,
                    "preferences": {"sms": True, "email": True, "push": False},
                    "createdAt": datetime.now().isoformat(),
                    "updatedAt": datetime.now().isoformat()
                },
                {
                    "_id": str(uuid.uuid4()),
                    "name": "NGO Representative",
                    "email": "ngo@coastalguardian.com",
                    "passwordHash": self._hash_password("demo123"),
                    "role": "ngo",
                    "location": {"type": "Point", "coordinates": [74.1240, 15.2993]},
                    "points": 0,
                    "preferences": {"sms": True, "email": True, "push": True},
                    "createdAt": datetime.now().isoformat(),
                    "updatedAt": datetime.now().isoformat()
                },
                {
                    "_id": str(uuid.uuid4()),
                    "name": "Community Member",
                    "email": "community@coastalguardian.com",
                    "passwordHash": self._hash_password("demo123"),
                    "role": "community",
                    "location": {"type": "Point", "coordinates": [80.2707, 13.0827]},
                    "points": 0,
                    "preferences": {"sms": False, "email": True, "push": False},
                    "createdAt": datetime.now().isoformat(),
                    "updatedAt": datetime.now().isoformat()
                }
            ]
            
            with open(self.users_file, 'w') as f:
                json.dump({"users": default_users}, f, indent=2)
        
        if not os.path.exists(self.api_keys_file):
            with open(self.api_keys_file, 'w') as f:
                json.dump({"api_keys": {}}, f, indent=2)
    
    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_users(self):
        """Load users from file"""
        try:
            with open(self.users_file, 'r') as f:
                data = json.load(f)
                return data.get("users", [])
        except FileNotFoundError:
            return []
    
    def _save_users(self, users):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump({"users": users}, f, indent=2)
    
    def login(self, email, password, role):
        """Authenticate user"""
        users = self._load_users()
        
        for user in users:
            if (user['email'] == email and 
                user['passwordHash'] == self._hash_password(password) and
                user['role'] == role):
                return user
        
        return None
    
    def register(self, name, email, password, role, lat, lng):
        """Register new user"""
        users = self._load_users()
        
        # Check if email already exists
        if any(user['email'] == email for user in users):
            return None
        
        new_user = {
            "_id": str(uuid.uuid4()),
            "name": name,
            "email": email,
            "passwordHash": self._hash_password(password),
            "role": role,
            "location": {"type": "Point", "coordinates": [lng, lat]},
            "points": 0,
            "preferences": {"sms": True, "email": True, "push": False},
            "createdAt": datetime.now().isoformat(),
            "updatedAt": datetime.now().isoformat()
        }
        
        users.append(new_user)
        self._save_users(users)
        
        return new_user
    
    def get_user_by_id(self, user_id):
        """Get user by ID"""
        users = self._load_users()
        for user in users:
            if user['_id'] == user_id:
                return user
        return None
    
    def update_user(self, user_id, updates):
        """Update user information"""
        users = self._load_users()
        
        for i, user in enumerate(users):
            if user['_id'] == user_id:
                users[i].update(updates)
                users[i]['updatedAt'] = datetime.now().isoformat()
                self._save_users(users)
                return users[i]
        
        return None
    
    def add_points(self, user_id, points):
        """Add points to user"""
        users = self._load_users()
        
        for i, user in enumerate(users):
            if user['_id'] == user_id:
                users[i]['points'] += points
                users[i]['updatedAt'] = datetime.now().isoformat()
                self._save_users(users)
                return users[i]
        
        return None
    
    def generate_api_key(self, user_id):
        """Generate API key for user"""
        api_key = f"cg_{uuid.uuid4().hex}"
        
        try:
            with open(self.api_keys_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {"api_keys": {}}
        
        data["api_keys"][api_key] = {
            "user_id": user_id,
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        
        with open(self.api_keys_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        return api_key
    
    def validate_api_key(self, api_key):
        """Validate API key"""
        try:
            with open(self.api_keys_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            return None
        
        key_data = data["api_keys"].get(api_key)
        if key_data and key_data["active"]:
            return self.get_user_by_id(key_data["user_id"])
        
        return None
    
    def get_all_users(self):
        """Get all users"""
        return self._load_users()
    
    def get_users_by_role(self, role):
        """Get users by role"""
        users = self._load_users()
        return [user for user in users if user['role'] == role]
