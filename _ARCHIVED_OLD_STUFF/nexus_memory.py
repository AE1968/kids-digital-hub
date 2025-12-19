"""
Nexus Memory System - Persistent Conversation Storage
Stores all conversations with unlimited capacity using JSON files
"""

import json
import os
from datetime import datetime

MEMORY_DIR = 'memory'
CONVERSATIONS_FILE = os.path.join(MEMORY_DIR, 'conversations.json')
USERS_FILE = os.path.join(MEMORY_DIR, 'users.json')
CONTEXT_FILE = os.path.join(MEMORY_DIR, 'context.json')

def init_memory():
    """Initialize memory directory and files"""
    if not os.path.exists(MEMORY_DIR):
        os.makedirs(MEMORY_DIR)
    
    for file in [CONVERSATIONS_FILE, USERS_FILE, CONTEXT_FILE]:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                json.dump({}, f)

def save_conversation(user_id, user_message, nexus_reply):
    """Save a conversation turn to memory"""
    init_memory()
    
    with open(CONVERSATIONS_FILE, 'r') as f:
        conversations = json.load(f)
    
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({
        'timestamp': datetime.now().isoformat(),
        'user': user_message,
        'nexus': nexus_reply
    })
    
    with open(CONVERSATIONS_FILE, 'w') as f:
        json.dump(conversations, f, indent=2)

def get_conversation_history(user_id, limit=10):
    """Retrieve recent conversation history for a user"""
    init_memory()
    
    try:
        with open(CONVERSATIONS_FILE, 'r') as f:
            conversations = json.load(f)
        
        user_history = conversations.get(user_id, [])
        return user_history[-limit:]  # Return last N conversations
    except:
        return []

def get_context_for_prompt(user_id):
    """Build context string from conversation history"""
    history = get_conversation_history(user_id, limit=5)
    
    if not history:
        return ""
    
    context_lines = ["Previous conversation context:"]
    for turn in history:
        context_lines.append(f"USER: {turn['user']}")
        context_lines.append(f"NEXUS: {turn['nexus']}")
    
    return "\n".join(context_lines)

def update_user_profile(user_id, name=None, preferences=None):
    """Update user profile information"""
    init_memory()
    
    with open(USERS_FILE, 'r') as f:
        users = json.load(f)
    
    if user_id not in users:
        users[user_id] = {
            'first_seen': datetime.now().isoformat(),
            'name': name or 'Unknown',
            'preferences': preferences or {}
        }
    else:
        if name:
            users[user_id]['name'] = name
        if preferences:
            users[user_id]['preferences'].update(preferences)
    
    users[user_id]['last_seen'] = datetime.now().isoformat()
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def get_user_profile(user_id):
    """Get user profile"""
    init_memory()
    
    try:
        with open(USERS_FILE, 'r') as f:
            users = json.load(f)
        return users.get(user_id, {})
    except:
        return {}
