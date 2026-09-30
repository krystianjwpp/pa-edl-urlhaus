import os

# ==========================================
# 1. PROCESS LOCAL URLHAUS DATA
# ==========================================
clean_urls = set()

if os.path.exists("raw_urlhaus.txt"):
    with open("raw_urlhaus.txt", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
        
    for line in lines:
        line = line.strip()
        # Skip HTML structural lines or comments
        if not line or line.startswith('#') or '<html' in line.lower() or '<doctype' in line.lower():
            continue
            
        if line.startswith('http://'): line = line[7:]
        elif line.startswith('https://'): line = line[8:]
        
        # Isolate the host structure to filter out direct IP links
        if '/' in line:
            host_string = line.split('/', 1)[0]
        else:
            host_string = line
            
        if ':' in host_string:
            host_string = host_string.split(':')[0]
            
        clean_host_check = host_string.replace('.', '')
        if not clean_host_check.isdigit() and line:
            clean_urls.add(line)

# ==========================================
# 2. PROCESS LOCAL EMERGING THREATS DATA
# ==========================================
clean_domains = set()

if os.path.exists("raw_et.txt"):
    with open("raw_et.txt", "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().splitlines()
        
    for line in lines:
        line = line.strip()
        # Skip tracking objects, JSON structures, or comments
        if not line or line.startswith('#') or '{' in line or '"' in line or 'localhost' in line:
            continue
            
        clean_host_check = line.replace('.', '')
        if not clean_host_check.isdigit():
            clean_domains.add(line.lower())

# ==========================================
# 3. WRITE THE CLEAN PA-COMPATIBLE LISTS
# ==========================================
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")

with open("pa-clean-domains.txt", "w") as f:
    for domain in sorted(clean_domains):
        f.write(f"{domain}\n")
