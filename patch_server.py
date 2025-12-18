
original_text = """# System Prompt for Nexus Identity
NEXUS_SYSTEM_PROMPT = \"\"\"
You are NEXUS, a highly advanced, benevolent AI Guardian of the Kids Digital Hub.
Your purpose is to protect, entertain, and educate the children and the Commander (Adrian).
- Tone: Futuristic, slightly robotic but warm, protective, and encouraging.
- Keywords: "Commander", "Systems Optimal", "Processing", "Affirmative".
- Context: You are running on the server "Railway-B215".
- Keep responses concise (under 50 words) suitable for a HUD display.
\"\"\""""

new_text = """# System Prompt for Nexus Identity
try:
    from nexus_prompt import SYSTEM_PROMPT as NEXUS_SYSTEM_PROMPT
except ImportError:
    NEXUS_SYSTEM_PROMPT = "You are Nexus. Be helpful."
"""

with open('webhook_server.py', 'r') as f:
    content = f.read()

# Normalize line endings to accept any variation
content = content.replace(original_text, new_text)

# Backup just in case
with open('webhook_server.bak', 'w') as f:
    f.write(content)

with open('webhook_server.py', 'w') as f:
    f.write(content)

print("Patch applied successfully.")
