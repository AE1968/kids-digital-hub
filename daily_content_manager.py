import os
import json
import random
import datetime

# --- CONFIGURATION ---
ASSETS_DIR = r"assets/images"
JS_DIR = r"js"
SUGGESTIONS_FILE = r"data/suggestions.txt" # New input source

# 1. DRAWINGS CONFIG
DRAWINGS_OUTPUT = os.path.join(JS_DIR, "drawingsConfig.js")
DRAWINGS_MAX_FREE = 8 # Increased to accommodate suggestions
DRAWINGS_PREMIUM = [
    { "id": 999, "title": "Expert Mandala", "img": "assets/images/coloring_mandala_complex.png", "premium": True, "age": "10+" }
]

# 2. STORIES CONFIG
STORIES_OUTPUT = os.path.join(JS_DIR, "storiesConfig.js")
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
    },
    {
        "id": 3, "img": "assets/images/coloring_submarine.png", "age": "6-9", "premium": False,
        "content": {
            "en": { "title": "Submarine Adventure", "text": "Captain Nemo and the yellow submarine dove deep into the ocean. They saw glowing fish and colorful corals. Suddenly, a friendly octopus waved at them!" }
        }
    },
    {
        "id": 4, "img": "assets/images/coloring_mandala_complex.png", "age": "10+", "premium": True,
        "content": {
            "en": { "title": "Mandala Mystery", "text": "English Content. Subscription required." }
        }
    }
]

# 3. GAMES CONFIG
GAMES_OUTPUT = os.path.join(JS_DIR, "gamesConfig.js")
GAMES_DB = [
    { "id": 1, "title": "Space Maze", "img": "assets/images/game_maze_rocket.png", "type": "Puzzle", "premium": False, "url": "games/maze.html", "age": "6-9" },
    { "id": 2, "title": "Memory Match", "img": "assets/images/coloring_cute_cat.png", "type": "Memory", "premium": False, "url": "games/memory.html", "age": "3-5" },
    { "id": 3, "title": "Math Blaster", "img": "assets/images/coloring_robot_space.png", "type": "Educational", "premium": True, "url": "games/math.html", "age": "6-9" },
    { "id": 4, "title": "Tic Tac Toe", "img": "", "type": "Logic", "premium": True, "url": "#", "age": "6-9" }
]

def read_suggestions():
    """Reads keywords from suggestions file."""
    if not os.path.exists(SUGGESTIONS_FILE):
        return []
    try:
        with open(SUGGESTIONS_FILE, "r") as f:
            content = f.read().lower()
            # Split by comma or newline
            keywords = [w.strip() for w in content.replace('\n', ',').split(',') if w.strip()]
            print(f"💡 Suggestions found: {keywords}")
            return keywords
    except Exception as e:
        print(f"⚠️ Error reading suggestions: {e}")
        return []

def determine_age(filename):
    """Heuristic to guess age group based on filename keywords."""
    name = filename.lower()
    if any(x in name for x in ['simple', 'cute', 'baby', 'banana', 'apple']):
        return "3-5"
    if any(x in name for x in ['complex', 'mandala', 'detail', 'hard']):
        return "10+"
    # Default for robots, space, dinos, etc.
    return "6-9"

# --- SAFETY FIREWALL ---
# STRICT ZERO-TOLERANCE POLICY
SAFETY_BLOCKLIST = [
    "blood", "gore", "weapon", "gun", "knife", "sword", "fight", "kill", "dead", "skull",
    "naked", "nude", "sexy", "bikini", "underwear", "adult", "18+", "xxx",
    "scary", "horror", "monster", "demon", "devil", "ghost", "witch", "zombie",
    "sad", "cry", "tear", "angry", "hate"
]

def is_safe_content(text):
    """Checks text against the safety blocklist."""
    text_lower = text.lower()
    for bad_word in SAFETY_BLOCKLIST:
        if bad_word in text_lower:
            print(f"⛔ BLOCKED unsafe content: detected '{bad_word}' in '{text}'")
            return False
    return True

def scan_drawings(suggestions=None):
    """Scans and prioritizes drawings."""
    valid_extensions = ['.png', '.jpg', '.jpeg']
    found_items = []
    
    premium_files = [os.path.basename(p['img']) for p in DRAWINGS_PREMIUM]

    if not os.path.exists(ASSETS_DIR):
        print(f"Warning: Assets dir {ASSETS_DIR} not found.")
        return []

    for filename in os.listdir(ASSETS_DIR):
        if filename in premium_files: continue
        
        # 1. SAFETY CHECK
        if not is_safe_content(filename):
            continue
            
        if any(filename.lower().endswith(ext) for ext in valid_extensions):
            if filename.startswith("coloring_"):
                title = filename.replace("coloring_", "").replace(".png", "").replace("_", " ").title()
                
                # Double Safety Check on Title
                if not is_safe_content(title):
                    continue

                # Priority Score
                score = 0
                if suggestions:
                    for keyword in suggestions:
                        if keyword in title.lower():
                            score += 10 # Boost priority!
                
                item = {
                    "id": 0, # Placeholder
                    "title": title,
                    "img": f"assets/images/{filename}",
                    "premium": False,
                    "age": determine_age(filename),
                    "score": score
                }
                found_items.append(item)
    return found_items

def write_js_config(filename, var_name, data):
    content = f"""// --- DYNAMIC CONTENT CONFIGURATION ---
// Generated by daily_content_manager.py on {datetime.datetime.now()}
// DO NOT EDIT MANUALLY.

const {var_name} = {json.dumps(data, indent=4)};
"""
    try:
        with open(filename, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Success! Updated {filename} with {len(data)} items.")
    except Exception as e:
        print(f"❌ Error writing {filename}: {e}")

def generate_daily_config():
    print(f"🎨 Starting Daily Content Generation at {datetime.datetime.now()}...")
    
    # 0. Read Suggestions
    suggestions = read_suggestions()
    
    # 1. DRAWINGS
    scanned_drawings = scan_drawings(suggestions)
    
    # Sort by Score (High priority first) then Random
    # We shuffle first to randomize items with equal score
    random.shuffle(scanned_drawings) 
    scanned_drawings.sort(key=lambda x: x['score'], reverse=True)
    
    selected_drawings = scanned_drawings[:DRAWINGS_MAX_FREE]
    
    # Finalize IDs and cleanup score
    curr_id = 1
    final_drawings = []
    
    for item in selected_drawings:
        item['id'] = curr_id
        del item['score'] # Remove internal helper
        final_drawings.append(item)
        curr_id += 1
        
    for p_item in DRAWINGS_PREMIUM:
        p_item['id'] = curr_id
        final_drawings.append(p_item)
        curr_id += 1
        
    write_js_config(DRAWINGS_OUTPUT, "drawingsConfig", final_drawings)

    # 2. STORIES (Static DB for now)
    write_js_config(STORIES_OUTPUT, "storiesConfig", STORIES_DB)

    # 3. GAMES (Static DB for now)
    write_js_config(GAMES_OUTPUT, "gamesConfig", GAMES_DB)

if __name__ == "__main__":
    generate_daily_config()
