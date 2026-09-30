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
        # Skip comments or HTML junk
        if not line or line.startswith('#') or '<html' in line.lower() or '{' in line:
            continue
            
        # Clean the string down for URL processing
        raw_url = line
        if raw_url.startswith('http://'): raw_url = raw_url[7:]
        elif raw_url.startswith('https://'): raw_url = raw_url[8:]
        
        # Safely extract the host section out of the line to evaluate if it's an IP address
        host_section = raw_url.split('/')[0] if '/' in raw_url else raw_url
        host_section = host_section.split(':')[0] if ':' in host_section else host_section
        
        # Strip dots to check if the string contains only digits (indicating a raw IP address)
        ip_check = host_section.replace('.', '')
        if not ip_check.isdigit() and raw_url:
            clean_urls.add(raw_url)
except Exception as e:
    print(f"Error processing URLHaus: {e}")

# ==========================================
# 2. PROCESS DOMAINS (FOR YOUR DOMAIN EDL)
# ==========================================
domain_source = "https://githubusercontent.com"
clean_domains = set()

try:
    response = requests.get(domain_source, headers=headers)
    lines = response.text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#') or '{' in line or '"' in line or 'localhost' in line:
            continue
            
        # Safely extract the naked domain string element
        naked_domain = line.split('/')[0] if '/' in line else line
        naked_domain = naked_domain.split(':')[0] if ':' in naked_domain else naked_domain
        
        ip_check = naked_domain.replace('.', '')
        if not ip_check.isdigit() and naked_domain:
            clean_domains.add(naked_domain.lower())
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
