from datetime import datetime
from pathlib import Path
import re
import secrets
import string
import json

class BaseModel:
    BASE_DIR = Path(__file__).resolve().parent.parent
    DB_DIR = BASE_DIR / 'db'

    def save(self):
        self.DB_DIR.mkdir(parents=True, exist_ok=True)
        table_path = self.DB_DIR / f'{self.__class__.__name__}.json'

        existing_data = []
        if table_path.exists():
            with open(table_path, 'r') as f:
                existing_data = json.load(f)

        # Update existing entry or add new one
        entry_data = {k: str(v) for k, v in self.__dict__.items()}
        
        # Find and update existing entry or append new one
        updated = False
        for i, entry in enumerate(existing_data):
            if entry.get('domain') == self.domain:
                existing_data[i] = entry_data
                updated = True
                break
        
        if not updated:
            existing_data.append(entry_data)

        with open(table_path, 'w') as f:
            json.dump(existing_data, f, indent=2)

    @classmethod
    def get(cls):
        table_path = cls.DB_DIR / f'{cls.__name__}.json'
        if not table_path.exists():
            return []
        
        with open(table_path, 'r') as f:
            return json.load(f)

    @classmethod
    def delete(cls, domain):
        table_path = cls.DB_DIR / f'{cls.__name__}.json'
        if not table_path.exists():
            return False

        with open(table_path, 'r') as f:
            data = json.load(f)

        filtered_data = [entry for entry in data if entry.get('domain') != domain]
        
        if len(filtered_data) == len(data):
            return False

        with open(table_path, 'w') as f:
            json.dump(filtered_data, f, indent=2)
        return True

class Password(BaseModel):
    MIN_LENGTH = 8
    
    def __init__(self, domain=None, password=None, notes=None):
        self.domain = domain
        self.password = password
        self.notes = notes
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

    @staticmethod
    def generate_password(length=16, use_special=True, use_numbers=True, use_uppercase=True):
        if length < Password.MIN_LENGTH:
            raise ValueError(f"Password length must be at least {Password.MIN_LENGTH} characters")

        chars = string.ascii_lowercase
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += string.punctuation

        while True:
            password = ''.join(secrets.choice(chars) for _ in range(length))
            if Password.validate_password(password):
                return password

    @staticmethod
    def validate_password(password):
        if len(password) < Password.MIN_LENGTH:
            return False
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            return False
            
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            return False
            
        # Check for at least one digit
        if not re.search(r'\d', password):
            return False
            
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
            
        return True

    @classmethod
    def list_domains(cls):
        entries = cls.get()
        return [entry['domain'] for entry in entries]

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
        self.save()

# p1 = Password(domain='Youtube', password='abcd')
# p1.save()
# Password.get()