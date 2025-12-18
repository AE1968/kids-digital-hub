"""
Nexus Task Tracking System
Keeps track of all task lists and progress for Adrian
"""

import json
import os
from datetime import datetime

TASKS_FILE = 'memory/tasks.json'

def init_tasks():
    """Initialize tasks file"""
    if not os.path.exists('memory'):
        os.makedirs('memory')
    
    if not os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'w') as f:
            json.dump({
                'lists': {},
                'current_context': {},
                'history': []
            }, f, indent=2)

def save_task_list(list_name, tasks, current_position=None):
    """Save or update a task list"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        data = json.load(f)
    
    data['lists'][list_name] = {
        'tasks': tasks,
        'current_position': current_position,
        'last_updated': datetime.now().isoformat(),
        'total_tasks': len(tasks),
        'completed': sum(1 for t in tasks if isinstance(t, dict) and t.get('completed', False))
    }
    
    # Update history
    data['history'].append({
        'timestamp': datetime.now().isoformat(),
        'action': 'update_list',
        'list_name': list_name,
        'position': current_position
    })
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_task_list(list_name):
    """Retrieve a task list"""
    init_tasks()
    
    try:
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)
        return data['lists'].get(list_name)
    except:
        return None

def update_current_context(context_info):
    """Update what Adrian is currently working on"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        data = json.load(f)
    
    data['current_context'] = {
        'info': context_info,
        'timestamp': datetime.now().isoformat()
    }
    
    data['history'].append({
        'timestamp': datetime.now().isoformat(),
        'action': 'context_update',
        'context': context_info
    })
    
    with open(TASKS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def get_current_context():
    """Get current work context"""
    init_tasks()
    
    try:
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)
        return data.get('current_context', {})
    except:
        return {}

def get_all_lists():
    """Get all task lists"""
    init_tasks()
    
    try:
        with open(TASKS_FILE, 'r') as f:
            data = json.load(f)
        return data.get('lists', {})
    except:
        return {}

def mark_task_complete(list_name, task_index):
    """Mark a specific task as complete"""
    init_tasks()
    
    with open(TASKS_FILE, 'r') as f:
        data = json.load(f)
    
    if list_name in data['lists']:
        tasks = data['lists'][list_name]['tasks']
        if 0 <= task_index < len(tasks):
            if isinstance(tasks[task_index], dict):
                tasks[task_index]['completed'] = True
            else:
                tasks[task_index] = {
                    'task': tasks[task_index],
                    'completed': True,
                    'completed_at': datetime.now().isoformat()
                }
            
            data['lists'][list_name]['tasks'] = tasks
            data['lists'][list_name]['completed'] = sum(1 for t in tasks if isinstance(t, dict) and t.get('completed', False))
            data['lists'][list_name]['last_updated'] = datetime.now().isoformat()
            
            with open(TASKS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
    
    return False

# Initialize with current project status
def init_project_tasks():
    """Initialize with today's work"""
    save_task_list('Tomorrow_Priority', [
        {'task': 'Finalizare rest site Kids Digital Hub', 'completed': False},
        {'task': 'Atribuții și responsabilități pentru Nexus', 'completed': False},
        {'task': 'Creare fabrică nouă de produse (cu Nexus în control)', 'completed': False}
    ], current_position=0)
    
    update_current_context({
        'project': 'Kids Digital Hub',
        'focus': 'Nexus AI Integration',
        'status': 'Nexus Core Complete - Ready for tomorrow'
    })

# Auto-initialize on import
init_project_tasks()
