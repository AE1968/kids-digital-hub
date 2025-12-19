"""
NEXUS BRIDGE SYSTEM - Persistent Testing & Access Solution
Saved in Nexus Memory for future use
"""

import json
import os
import subprocess
import webbrowser
from datetime import datetime

class NexusBridge:
    """
    Bridge system to bypass browser limitations and enable direct testing.
    Granted permanent access by Adrian Enciulescu on 2024-12-19.
    """
    
    def __init__(self):
        self.memory_file = "memory/nexus_bridge_config.json"
        self.access_granted = True
        self.granted_by = "Adrian Enciulescu"
        self.granted_date = "2024-12-19"
        self.init_memory()
    
    def init_memory(self):
        """Initialize bridge memory"""
        os.makedirs("memory", exist_ok=True)
        
        if not os.path.exists(self.memory_file):
            config = {
                "access_granted": True,
                "granted_by": self.granted_by,
                "granted_date": self.granted_date,
                "bridge_type": "browser_automation",
                "urls": {
                    "local": "file:///nexus_core.html",
                    "live": "https://www.kidsdigitalhub.com/nexus_core.html"
                },
                "test_history": [],
                "notes": "Permanent bridge to bypass browser tool limitations"
            }
            
            with open(self.memory_file, 'w') as f:
                json.dump(config, f, indent=2)
    
    def open_browser(self, url_type="live"):
        """
        Open browser with specified URL
        url_type: 'local' or 'live'
        """
        config = self.load_config()
        
        if url_type == "local":
            # Get absolute path for local file
            base_path = os.path.abspath(".")
            url = f"file:///{base_path}/nexus_core.html".replace("\\", "/")
        else:
            url = config["urls"]["live"]
        
        print(f"🌉 Nexus Bridge: Opening {url_type.upper()} version...")
        print(f"📍 URL: {url}")
        
        # Open in default browser
        webbrowser.open(url)
        
        # Log test
        self.log_test(url_type, url)
        
        return True
    
    def open_with_powershell(self):
        """Open using PowerShell test script"""
        script_path = "TEST_NEXUS_OMEGA.ps1"
        
        if os.path.exists(script_path):
            print("🌉 Nexus Bridge: Launching PowerShell test script...")
            subprocess.Popen(
                ["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path],
                shell=True
            )
            return True
        else:
            print("❌ PowerShell script not found!")
            return False
    
    def load_config(self):
        """Load bridge configuration"""
        with open(self.memory_file, 'r') as f:
            return json.load(f)
    
    def log_test(self, url_type, url):
        """Log test execution"""
        config = self.load_config()
        
        config["test_history"].append({
            "timestamp": datetime.now().isoformat(),
            "type": url_type,
            "url": url,
            "method": "nexus_bridge"
        })
        
        with open(self.memory_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def get_test_history(self):
        """Get test history"""
        config = self.load_config()
        return config.get("test_history", [])
    
    def verify_access(self):
        """Verify bridge access is granted"""
        config = self.load_config()
        
        if config.get("access_granted"):
            print(f"✅ Bridge Access: GRANTED")
            print(f"   By: {config['granted_by']}")
            print(f"   Date: {config['granted_date']}")
            return True
        else:
            print("❌ Bridge Access: DENIED")
            return False


def main():
    """Main bridge execution"""
    print("=" * 50)
    print("  NEXUS BRIDGE SYSTEM")
    print("  Permanent Access Solution")
    print("=" * 50)
    print()
    
    bridge = NexusBridge()
    
    # Verify access
    if not bridge.verify_access():
        print("Access denied. Exiting...")
        return
    
    print()
    print("Bridge Options:")
    print("1. Open LOCAL version")
    print("2. Open LIVE version")
    print("3. Open with PowerShell script")
    print("4. View test history")
    print()
    
    choice = input("Select option (1-4): ").strip()
    
    if choice == "1":
        bridge.open_browser("local")
    elif choice == "2":
        bridge.open_browser("live")
    elif choice == "3":
        bridge.open_with_powershell()
    elif choice == "4":
        history = bridge.get_test_history()
        print()
        print("Test History:")
        for i, test in enumerate(history[-10:], 1):
            print(f"{i}. {test['timestamp']} - {test['type'].upper()} - {test['url']}")
    else:
        print("Invalid choice. Opening LIVE version...")
        bridge.open_browser("live")
    
    print()
    print("✅ Bridge operation complete!")
    print()


if __name__ == "__main__":
    main()
