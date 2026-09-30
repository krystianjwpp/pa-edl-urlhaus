import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# ==========================================
# 1. PROCESS URLHAUS (FOR YOUR URL EDL)
# ==========================================
urlhaus_source = "https://abuse.ch"
clean_urls = set()

try:
    response = requests.get(urlhaus_source, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('http://'): line = line[7:]
        elif line.startswith('https://'): line = line[8:]
        
        # IP Verification
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
# 2. PROCESS EMERGING THREATS (FOR YOUR DOMAIN EDL)
# ==========================================
et_source = "https://emergingthreats.net"
clean_domains = set()

try:
    response = requests.get(et_source, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        # Skip comments, blank lines, or generic placeholders
        if not line or line.startswith('#') or "localhost" in line:
            continue
            
        # Ensure it's not a raw IP address
        clean_host_check = line.replace('.', '')
        if not clean_host_check.isdigit():
            clean_domains.add(line.lower())
except Exception as e:
    print(f"Error processing Emerging Threats: {e}")

# ==========================================
# 3. WRITE BOTH FILES TO YOUR REPOSITORY
# ==========================================
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")

with open("pa-clean-domains.txt", "w") as f:
    for domain in sorted(clean_domains):
        f.write(f"{domain}\n")
