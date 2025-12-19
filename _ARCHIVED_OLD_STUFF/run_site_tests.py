import os
import re
from urllib.parse import unquote
import datetime

# Configuration
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
REPORT_FILE = os.path.join(PROJECT_ROOT, "TEST_REPORT.md")
HTML_EXTENSIONS = ['.html', '.htm']
IMAGE_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.ico']
IGNORE_DIRS = ['.git', '.bgit', '.netlify', 'node_modules', '__pycache__', '.agent']
IGNORE_LINKS = ['#', 'javascript:void(0)', 'javascript:;']

def get_all_html_files(root_dir):
    html_files = []
    for root, dirs, files in os.walk(root_dir):
        # Filter ignored dirs
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for file in files:
            if any(file.endswith(ext) for ext in HTML_EXTENSIONS):
                html_files.append(os.path.join(root, file))
    return html_files

def check_file_exists(base_path, relative_link):
    # Handle external links
    if relative_link.startswith(('http://', 'https://', 'mailto:', 'tel:')):
        return "EXTERNAL"
    
    # Handle anchors
    if '#' in relative_link:
        relative_link = relative_link.split('#')[0]
    
    if not relative_link:
        return True # Just an anchor on same page

    # Handle query params
    if '?' in relative_link:
        relative_link = relative_link.split('?')[0]

    # Resolve path
    # If starts with /, it's relative to project root (usually)
    # If not, it's relative to base_path
    
    if relative_link.startswith('/'):
        target_path = os.path.join(PROJECT_ROOT, relative_link.lstrip('/'))
    else:
        target_path = os.path.join(os.path.dirname(base_path), relative_link)
    
    # Decoding HTML entities/URL encoding
    target_path = unquote(target_path)

    return os.path.exists(target_path) and os.path.isfile(target_path)

def scan_file(file_path):
    issues = []
    stats = {'links': 0, 'images': 0, 'scripts': 0}
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. EXTRACT LINKS (href)
        # Regex for href="..." -> simplified
        links = re.findall(r'href=["\'](.*?)["\']', content)
        for link in links:
            if link in IGNORE_LINKS: continue
            stats['links'] += 1
            status = check_file_exists(file_path, link)
            if status == False:
                issues.append(f"❌ BROKEN LINK: `{link}` not found.")
        
        # 2. EXTRACT IMAGES (src)
        images = re.findall(r'src=["\'](.*?)["\']', content)
        for img in images:
            # Skip external scripts/images for now or marked as check
            stats['images'] += 1
            status = check_file_exists(file_path, img)
            if status == False:
                issues.append(f"❌ MISSING ASSET: `{img}` not found.")
                
        # 3. CHECK TITLE
        if '<title>' not in content.lower():
            issues.append("⚠️ MISSING TAG: `<title>` tag is missing.")

        # 4. CHECK VIEWPORT (SEO)
        if 'viewport' not in content.lower():
            issues.append("⚠️ MISSING SEO: `viewport` meta tag missing.")

    except Exception as e:
        issues.append(f"🔥 ERROR: Could not read file. {str(e)}")
        
    return issues, stats

def generate_report():
    print("🚀 STARTING AUTOMATED TESTS...")
    files = get_all_html_files(PROJECT_ROOT)
    
    total_issues = 0
    total_files = 0
    
    report_content = [
        f"# 🧪 AUTOMATED TEST REPORT",
        f"**Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Project Root:** `{PROJECT_ROOT}`",
        "",
        "## 🔍 SCAN RESULTS",
        ""
    ]
    
    for file_path in files:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        print(f"Scanning: {rel_path}...")
        issues, stats = scan_file(file_path)
        total_files += 1
        
        status_icon = "✅" if not issues else "❌"
        if not issues:
            # report_content.append(f"### {status_icon} {rel_path}")
            # report_content.append(f"- Links: {stats['links']} | Assets: {stats['images']} | OK")
            pass 
        else:
            total_issues += len(issues)
            report_content.append(f"### {status_icon} {rel_path}")
            report_content.append(f"**Stats:** Links: {stats['links']} | Assets: {stats['images']}")
            report_content.append("### Issues Found:")
            for issue in issues:
                report_content.append(f"- {issue}")
            report_content.append("")
            
    report_content.append("---")
    report_content.append("## 📊 SUMMARY")
    report_content.append(f"- **Files Scanned:** {total_files}")
    report_content.append(f"- **Total Issues Found:** {total_issues}")
    
    if total_issues == 0:
        report_content.append("\n## 🎉 PERFECT SCORE! NO ISSUES FOUND.")
        print("\n✅ TESTS PASSED! No issues found.")
    else:
        print(f"\n⚠️ TESTS FINISHED WITH {total_issues} ISSUES. Check TEST_REPORT.md")

    with open(REPORT_FILE, "w", encoding='utf-8') as f:
        f.write("\n".join(report_content))
        
    print(f"📄 Report generated: {REPORT_FILE}")

if __name__ == "__main__":
    generate_report()
