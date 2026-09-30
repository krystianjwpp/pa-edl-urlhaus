import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ==========================================
# 1. PROCESS URLHAUS (VIA DUAL-SCRIBED MIRROR)
# ==========================================
# Using the clean text mirror hosted on GitHub to completely bypass Cloudflare blocks
urlhaus_source = "https://githubusercontent.com"
clean_urls = set()

try:
    response = requests.get(urlhaus_source, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        # Skip comments or HTML components if any exist
        if not line or line.startswith('#') or '<html' in line.lower() or '{' in line:
            continue
            
        # Strip protocols
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
except Exception as e:
    print(f"Error processing URLHaus: {e}")

# ==========================================
# 2. PROCESS EMERGING THREATS (VIA SCRUBBED MIRROR)
# ==========================================
# Using a clean raw domain mirror instead of the Proofpoint tracker portal
et_source = "https://githubusercontent.com" 
# Alternative fallback option if you prefer a strict OSINT domain compiler:
et_source_alt = "https://githubusercontent.com"

clean_domains = set()

try:
    response = requests.get(et_source_alt, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        # Skip comments or invalid data structures
        if not line or line.startswith('#') or '{' in line or '"' in line or 'localhost' in line:
            continue
            
        clean_host_check = line.replace('.', '')
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
