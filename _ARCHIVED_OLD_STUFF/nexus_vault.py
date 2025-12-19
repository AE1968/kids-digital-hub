"""
Nexus Secure Vault - Encrypted Storage System
Stores passwords, codes, API keys, and sensitive information
"""

import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
import base64
import hashlib

VAULT_DIR = 'memory/vault'
VAULT_FILE = os.path.join(VAULT_DIR, 'secure_data.enc')
KEY_FILE = os.path.join(VAULT_DIR, 'vault.key')

def init_vault():
    """Initialize secure vault"""
    if not os.path.exists(VAULT_DIR):
        os.makedirs(VAULT_DIR)
    
    # Generate encryption key if doesn't exist
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
    
    # Initialize empty vault if doesn't exist
    if not os.path.exists(VAULT_FILE):
        save_vault_data({
            'passwords': {},
            'api_keys': {},
            'codes': {},
            'notes': {},
            'created_at': datetime.now().isoformat()
        })

def get_cipher():
    """Get encryption cipher"""
    with open(KEY_FILE, 'rb') as f:
        key = f.read()
    return Fernet(key)

def save_vault_data(data):
    """Save encrypted vault data"""
    cipher = get_cipher()
    encrypted_data = cipher.encrypt(json.dumps(data).encode())
    
    with open(VAULT_FILE, 'wb') as f:
        f.write(encrypted_data)

def load_vault_data():
    """Load and decrypt vault data"""
    try:
        cipher = get_cipher()
        with open(VAULT_FILE, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = cipher.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode())
    except:
        return {
            'passwords': {},
            'api_keys': {},
            'codes': {},
            'notes': {}
        }

def store_password(service_name, username, password, notes=None):
    """Store a password securely"""
    init_vault()
    data = load_vault_data()
    
    data['passwords'][service_name] = {
        'username': username,
        'password': password,
        'notes': notes,
        'created_at': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat()
    }
    
    save_vault_data(data)

def get_password(service_name):
    """Retrieve a password"""
    init_vault()
    data = load_vault_data()
    return data['passwords'].get(service_name)

def store_api_key(service_name, api_key, notes=None):
    """Store an API key"""
    init_vault()
    data = load_vault_data()
    
    data['api_keys'][service_name] = {
        'key': api_key,
        'notes': notes,
        'created_at': datetime.now().isoformat()
    }
    
    save_vault_data(data)

def get_api_key(service_name):
    """Retrieve an API key"""
    init_vault()
    data = load_vault_data()
    return data['api_keys'].get(service_name)

def store_code(code_name, code_value, notes=None):
    """Store any code or sensitive info"""
    init_vault()
    data = load_vault_data()
    
    data['codes'][code_name] = {
        'value': code_value,
        'notes': notes,
        'created_at': datetime.now().isoformat()
    }
    
    save_vault_data(data)

def get_code(code_name):
    """Retrieve a code"""
    init_vault()
    data = load_vault_data()
    return data['codes'].get(code_name)

def store_note(note_name, content):
    """Store a secure note"""
    init_vault()
    data = load_vault_data()
    
    data['notes'][note_name] = {
        'content': content,
        'created_at': datetime.now().isoformat()
    }
    
    save_vault_data(data)

def get_note(note_name):
    """Retrieve a note"""
    init_vault()
    data = load_vault_data()
    return data['notes'].get(note_name)

def list_all_entries():
    """List all vault entries (without revealing sensitive data)"""
    init_vault()
    data = load_vault_data()
    
    return {
        'passwords': list(data['passwords'].keys()),
        'api_keys': list(data['api_keys'].keys()),
        'codes': list(data['codes'].keys()),
        'notes': list(data['notes'].keys())
    }

def delete_entry(category, entry_name):
    """Delete an entry from vault"""
    init_vault()
    data = load_vault_data()
    
    if category in data and entry_name in data[category]:
        del data[category][entry_name]
        save_vault_data(data)
        return True
    
    return False

def export_vault_backup(backup_path):
    """Export encrypted vault backup"""
    init_vault()
    
    import shutil
    shutil.copy(VAULT_FILE, backup_path)
    return backup_path

# Initialize vault on import
init_vault()
