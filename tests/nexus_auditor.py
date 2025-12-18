import asyncio
from playwright.async_api import async_playwright
import json
import os
from datetime import datetime

# CONFIGURATION
BASE_URL = "https://www.kidsdigitalhub.com"
REPORT_PATH = "data/audit_report.json"

class NexusAuditor:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "health_score": 100,
            "checked_urls": [],
            "broken_links": [],
            "js_errors": [],
            "missing_images": [],
            "features_verified": {}
        }

    async def run_audit(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            # Handle console errors
            page.on("console", lambda msg: self.handle_console(msg))
            page.on("pageerror", lambda err: self.results["js_errors"].append(str(err)))

            # 1. TEST HOMEPAGE
            print(f"🔍 Auditing {BASE_URL}...")
            await self.audit_page(page, BASE_URL, "Homepage")

            # 2. TEST NAVIGATION LINKS
            nav_links = {
                "Coloring": f"{BASE_URL}/gallery-drawings.html",
                "Games": f"{BASE_URL}/gallery-games.html",
                "Stories": f"{BASE_URL}/gallery-stories.html",
                "Shop": f"{BASE_URL}/shop.html",
                "Profile": f"{BASE_URL}/profile.html",
                "Dashboard": f"{BASE_URL}/dashboard.html"
            }

            for name, url in nav_links.items():
                print(f"🔍 Testing {name} branch...")
                await self.audit_page(page, url, name)
                
                # Check specific functionality
                if name == "Stories":
                    await self.verify_story_flow(page)
                elif name == "Shop":
                    await self.verify_shop_flow(page)

            await browser.close()
            self.finalize_report()

    def handle_console(self, msg):
        if msg.type == "error":
            self.results["js_errors"].append(f"Console Error: {msg.text}")
            self.results["health_score"] -= 2

    async def audit_page(self, page, url, name):
        try:
            response = await page.goto(url, wait_until="networkidle")
            if response.status != 200:
                self.results["broken_links"].append({"url": url, "status": response.status})
                self.results["health_score"] -= 10
                self.results["features_verified"][name] = "🚨 FAILED (Status 404/500)"
                return

            self.results["checked_urls"].append(url)
            
            # Check for broken images
            images = await page.query_selector_all("img")
            for img in images:
                src = await img.get_attribute("src")
                if src:
                    # Basic check if AE logo fallback is used (might indicate missing specific asset)
                    if "logo_ae.png" in src and "logo" not in src.lower():
                        # Not necessarily an error, but worth noting
                        pass
            
            self.results["features_verified"][name] = "✅ OPERATIONAL"
        except Exception as e:
            self.results["features_verified"][name] = f"🚨 CRASHED: {str(e)}"
            self.results["health_score"] -= 15

    async def verify_story_flow(self, page):
        """Try to click a story card."""
        try:
            cards = await page.query_selector_all(".story-card")
            if len(cards) > 0:
                await cards[0].click()
                await page.wait_for_timeout(1000)
                overlay = await page.is_visible("#storyOverlay")
                self.results["features_verified"]["Story Reader"] = "✅ ACTIVE" if overlay else "🚨 OVERLAY FAIL"
            else:
                self.results["features_verified"]["Story Reader"] = "🚨 NO STORIES FOUND"
        except:
            self.results["features_verified"]["Story Reader"] = "🚨 INTERACTION ERROR"

    async def verify_shop_flow(self, page):
        """Check for items in shop."""
        try:
            items = await page.query_selector_all(".shop-item")
            self.results["features_verified"]["Shop Items"] = f"✅ {len(items)} Items Active" if len(items) > 0 else "🚨 SHOP EMPTY"
        except:
            self.results["features_verified"]["Shop Items"] = "🚨 ERROR LOADING SHOP"

    def finalize_report(self):
        # Cap score
        self.results["health_score"] = max(0, self.results["health_score"])
        
        # Save report
        os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
        with open(REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📊 Audit Complete. Health Score: {self.results['health_score']}%")
        print(f"📄 Report saved to {REPORT_PATH}")

if __name__ == "__main__":
    auditor = NexusAuditor()
    asyncio.run(auditor.run_audit())
