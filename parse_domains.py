import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ==========================================
# 1. PROCESS URLHAUS (FOR YOUR URL EDL)
# ==========================================
urlhaus_source = "https://githubusercontent.com"
clean_urls = set()

try:
    response = requests.get(urlhaus_source, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or '<html' in line.lower() or '{' in line:
            continue
            
        if line.startswith('http://'): line = line[7:]
        elif line.startswith('https://'): line = line[8:]
        
        # Safe string splitting to isolate the domain/host
        host_string = line.split('/')[0] if '/' in line else line
        host_string = host_string.split(':')[0] if ':' in host_string else host_string
            
        clean_host_check = host_string.replace('.', '')
        if not clean_host_check.isdigit() and line:
            clean_urls.add(line)
except Exception as e:
    print(f"Error processing URLHaus: {e}")

# ==========================================
# 2. PROCESS DOMAINS (FOR YOUR DOMAIN EDL)
# ==========================================
et_source_alt = "https://githubusercontent.com"
clean_domains = set()

try:
    response = requests.get(et_source_alt, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or '{' in line or '"' in line or 'localhost' in line:
            continue
            
        # Safe string splitting for edge cases
        host_string = line.split('/')[0] if '/' in line else line
        host_string = host_string.split(':')[0] if ':' in host_string else host_string
            
        clean_host_check = host_string.replace('.', '')
        if not clean_host_check.isdigit():
            clean_domains.add(line.lower())
except Exception as e:
    print(f"Error processing Domain Feed: {e}")

# ==========================================
# 3. WRITE THE CLEAN PA-COMPATIBLE LISTS
# ==========================================
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")

with open("pa-clean-domains.txt", "w") as f:
    for domain in sorted(clean_domains):
        f.write(f"{domain}\n")
