import os
import json
import random
import datetime

# --- CONFIGURATION ---
ASSETS_DIR = r"assets/images"
JS_DIR = r"js"
SUGGESTIONS_FILE = r"data/suggestions.txt"

# 1. DRAWINGS CONFIG
DRAWINGS_OUTPUT = os.path.join(JS_DIR, "drawingsConfig.js")
DRAWINGS_MAX_FREE = 12 # Increased allowance
DRAWINGS_PREMIUM = [
    { "id": 999, "title": "Expert Mandala", "img": "assets/images/coloring_mandala_complex.png", "premium": True, "age": "10+" }
]

# 2. STORIES CONFIG
STORIES_OUTPUT = os.path.join(JS_DIR, "storiesConfig.js")
# Template for dynamic stories based on suggestions
STORY_TEMPLATES = [
    "Once upon a time, there was a magical {kw}. It lived in a land of wonder!",
    "The brave little {kw} decided to go on a big adventure across the ocean.",
    "Did you ever see a {kw} flying through the night sky? It's a beautiful sight!"
]

def generate_story_from_suggestion(keyword):
    """Creates a basic English story from a keyword."""
    return {
        "id": random.randint(100, 999), 
        "img": "assets/images/logo_ae.png", # Placeholder
        "age": "3-5", 
        "premium": False,
        "content": {
            "en": { 
                "title": f"The {keyword.title()} Adventure", 
                "text": random.choice(STORY_TEMPLATES).format(kw=keyword) 
            }
        }
    }

STORIES_DB = [
    {
        "id": 1, "img": "assets/images/coloring_robot_space.png", "age": "3-5", "premium": False,
        "content": {
            "en": { "title": "Sparky the Robot", "text": "Once upon a time, there was a little robot named Sparky. He loved to fly among the stars. One day, he landed on a purple planet where the rocks sang happy songs!" }
        }
    },
    {
        "id": 2, "img": "assets/images/coloring_dino.png", "age": "3-5", "premium": False,
        "content": {
            "en": { "title": "The Shy Dino", "text": "Dino was a big dinosaur with a very small voice. 'Squeak!' he said. His friends laughed, but Dino didn't mind. He talked to the butterflies and ants." }
        }
    }
]

# 3. GAMES CONFIG
GAMES_OUTPUT = os.path.join(JS_DIR, "gamesConfig.js")
GAMES_DB = [
    { "id": 1, "title": "Space Maze", "img": "assets/images/game_maze_rocket.png", "type": "Puzzle", "premium": False, "url": "games/maze.html", "age": "6-9" },
    { "id": 2, "title": "Memory Match", "img": "assets/images/coloring_cute_cat.png", "type": "Memory", "premium": False, "url": "games/memory.html", "age": "3-5" },
    { "id": 3, "title": "Math Blaster", "img": "assets/images/coloring_robot_space.png", "type": "Educational", "premium": True, "url": "games/math.html", "age": "6-9" }
]

def read_suggestions():
    """Reads keywords from suggestions file."""
    if not os.path.exists(SUGGESTIONS_FILE):
        return []
    try:
        with open(SUGGESTIONS_FILE, "r") as f:
            content = f.read().lower()
            keywords = [w.strip() for w in content.replace('\n', ',').split(',') if w.strip()]
            print(f"💡 Suggestions found: {keywords}")
            return keywords
    except Exception as e:
        print(f"⚠️ Error reading suggestions: {e}")
        return []

def determine_age(filename):
    """Heuristic to guess age group based on filename keywords."""
    name = filename.lower()
    if any(x in name for x in ['simple', 'cute', 'baby', 'banana', 'apple']): return "3-5"
    if any(x in name for x in ['complex', 'mandala', 'detail', 'hard']): return "10+"
    return "6-9"

# SAFETY BLOCKLIST (English Only)
SAFETY_BLOCKLIST = [
    "blood", "gore", "weapon", "gun", "knife", "sword", "fight", "kill", "dead", "skull",
    "naked", "nude", "sexy", "bikini", "underwear", "adult", "scary", "horror"
]

def is_safe_content(text):
    text_lower = text.lower()
    for bad_word in SAFETY_BLOCKLIST:
        if bad_word in text_lower:
            print(f"⛔ BLOCKED unsafe content: detected '{bad_word}'")
            return False
    return True

def scan_drawings(suggestions=None):
    valid_extensions = ['.png', '.jpg', '.jpeg']
    found_items = []
    
    if not os.path.exists(ASSETS_DIR): return []

    for filename in os.listdir(ASSETS_DIR):
        if not is_safe_content(filename): continue
        if any(filename.lower().endswith(ext) for ext in valid_extensions):
            if filename.startswith("coloring_"):
                title = filename.replace("coloring_", "").replace(".png", "").replace(".jpg", "").replace("_", " ").title()
                score = 0
                if suggestions:
                    for keyword in suggestions:
                        if keyword in title.lower(): score += 10
                
                found_items.append({
                    "id": 0, "title": title, "img": f"assets/images/{filename}",
                    "premium": False, "age": determine_age(filename), "score": score
                })
    return found_items

def write_js_config(filename, var_name, data):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content = f"// Generated by daily_content_manager.py on {timestamp}\nconst {var_name} = {json.dumps(data, indent=4)};"
    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
    print(f"✅ Updated {filename}")

def generate_daily_config():
    print(f"🚀 Starting content sync...")
    suggestions = read_suggestions()
    
    # 1. DRAWINGS
    scanned = scan_drawings(suggestions)
    random.shuffle(scanned) 
    scanned.sort(key=lambda x: x['score'], reverse=True)
    
    final_drawings = []
    for i, item in enumerate(scanned[:DRAWINGS_MAX_FREE]):
        item['id'] = i + 1
        del item['score']
        final_drawings.append(item)
    
    write_js_config(DRAWINGS_OUTPUT, "drawingsConfig", final_drawings)

    # 2. STORIES (Inject suggestions)
    dynamic_stories = list(STORIES_DB)
    for kw in suggestions[:2]: # Max 2 dynamic stories per day
        dynamic_stories.append(generate_story_from_suggestion(kw))
    write_js_config(STORIES_OUTPUT, "storiesConfig", dynamic_stories)

    # 3. GAMES
    write_js_config(GAMES_OUTPUT, "gamesConfig", GAMES_DB)

if __name__ == "__main__":
    generate_daily_config()
