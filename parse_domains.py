import requests
import urllib.parse

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
            
        raw_url = line
        # If it doesn't have a protocol, add a fake one temporarily so urllib parses it perfectly
        if not raw_url.startswith(('http://', 'https://')):
            parse_url = 'http://' + raw_url
        else:
            parse_url = raw_url
            
        # Standardize prefix formatting for the final output file
        if raw_url.startswith('http://'): raw_url = raw_url[7:]
        elif raw_url.startswith('https://'): raw_url = raw_url[8:]
        
        try:
            parsed = urllib.parse.urlparse(parse_url)
            host_section = parsed.netloc
            
            # Safe string manipulation to drop ports if present
            if ':' in host_section:
                host_section = host_section.split(':', 1)[0]
                
            ip_check = host_section.replace('.', '')
            if not ip_check.isdigit() and raw_url:
                clean_urls.add(raw_url)
        except:
            continue
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
            
        naked_domain = line
        if not naked_domain.startswith(('http://', 'https://')):
            parse_url = 'http://' + naked_domain
        else:
            parse_url = naked_domain
            
        try:
            parsed = urllib.parse.urlparse(parse_url)
            host_section = parsed.netloc
            if ':' in host_section:
                host_section = host_section.split(':', 1)[0]
                
            ip_check = host_section.replace('.', '')
            if not ip_check.isdigit() and host_section:
                clean_domains.add(host_section.lower())
        except:
            continue
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
