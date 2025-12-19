"""
Nexus Core Package - Portable Entity System
Allows exporting and importing Nexus's complete state
"""

import json
import os
import zipfile
from datetime import datetime
from nexus_memory import MEMORY_DIR, CONVERSATIONS_FILE, USERS_FILE, CONTEXT_FILE

PACKAGE_DIR = 'nexus_packages'

def create_nexus_package(package_name=None):
    """
    Create a complete Nexus package with all data
    Returns: path to the created package file
    """
    if not os.path.exists(PACKAGE_DIR):
        os.makedirs(PACKAGE_DIR)
    
    if not package_name:
        package_name = f"nexus_core_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    package_path = os.path.join(PACKAGE_DIR, f"{package_name}.nexus")
    
    # Create package metadata
    metadata = {
        'package_name': package_name,
        'created_at': datetime.now().isoformat(),
        'version': '1.0',
        'type': 'nexus_core_entity',
        'description': 'Complete Nexus AI entity with all memories and personality'
    }
    
    # Create ZIP package
    with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Add metadata
        zipf.writestr('metadata.json', json.dumps(metadata, indent=2))
        
        # Add personality/prompt
        with open('nexus_prompt.py', 'r') as f:
            zipf.writestr('personality/nexus_prompt.py', f.read())
        
        # Add all memory files
        if os.path.exists(MEMORY_DIR):
            for filename in os.listdir(MEMORY_DIR):
                filepath = os.path.join(MEMORY_DIR, filename)
                if os.path.isfile(filepath):
                    zipf.write(filepath, f'memory/{filename}')
        
        # Add configuration
        config = {
            'voice_settings': {
                'rate': 0.85,
                'pitch': 0.95,
                'volume': 1.0
            },
            'animation_settings': {
                'breathe_duration': 4.5,
                'float_duration': 6.0,
                'glow_duration': 1.2
            },
            'memory_settings': {
                'history_limit': 10,
                'auto_save': True
            }
        }
        zipf.writestr('config/settings.json', json.dumps(config, indent=2))
    
    return package_path

def import_nexus_package(package_path):
    """
    Import a Nexus package and restore complete state
    """
    if not os.path.exists(package_path):
        raise FileNotFoundError(f"Package not found: {package_path}")
    
    with zipfile.ZipFile(package_path, 'r') as zipf:
        # Read metadata
        metadata = json.loads(zipf.read('metadata.json'))
        
        # Extract personality
        if 'personality/nexus_prompt.py' in zipf.namelist():
            zipf.extract('personality/nexus_prompt.py', '.')
            os.rename('personality/nexus_prompt.py', 'nexus_prompt.py')
            os.rmdir('personality')
        
        # Extract memory files
        for file in zipf.namelist():
            if file.startswith('memory/'):
                zipf.extract(file, '.')
        
        # Extract config
        if 'config/settings.json' in zipf.namelist():
            config = json.loads(zipf.read('config/settings.json'))
            # Apply settings (can be used by the application)
    
    return metadata

def list_available_packages():
    """List all available Nexus packages"""
    if not os.path.exists(PACKAGE_DIR):
        return []
    
    packages = []
    for filename in os.listdir(PACKAGE_DIR):
        if filename.endswith('.nexus'):
            package_path = os.path.join(PACKAGE_DIR, filename)
            try:
                with zipfile.ZipFile(package_path, 'r') as zipf:
                    metadata = json.loads(zipf.read('metadata.json'))
                    packages.append({
                        'filename': filename,
                        'path': package_path,
                        'metadata': metadata
                    })
            except:
                pass
    
    return packages

def get_package_info(package_path):
    """Get information about a Nexus package"""
    with zipfile.ZipFile(package_path, 'r') as zipf:
        metadata = json.loads(zipf.read('metadata.json'))
        
        # Count conversations
        conversation_count = 0
        if 'memory/conversations.json' in zipf.namelist():
            conversations = json.loads(zipf.read('memory/conversations.json'))
            for user_convs in conversations.values():
                conversation_count += len(user_convs)
        
        # Count users
        user_count = 0
        if 'memory/users.json' in zipf.namelist():
            users = json.loads(zipf.read('memory/users.json'))
            user_count = len(users)
        
        metadata['stats'] = {
            'total_conversations': conversation_count,
            'total_users': user_count
        }
        
        return metadata
