import requests

# Add standard browser headers to bypass bot mitigation securely
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Fetch the raw URLhaus text list
source_url = "https://abuse.ch"
response = requests.get(source_url, headers=headers)
lines = response.text.splitlines()

clean_urls = set()

for line in lines:
    line = line.strip()
    
    # 1. Skip comment headers and empty lines
    if not line or line.startswith('#'):
        continue
        
    # 2. Strip transport protocol prefixes (case-insensitive)
    if line.lower().startswith('http://'):
        line = line[7:]
    elif line.lower().startswith('https://'):
        line = line[8:]
    elif line.lower().startswith('ftp://'):
        line = line[6:]
        
    # 3. Add to set (This preserves the full paths, ports, and IPs, minus the protocol)
    if line:
        clean_urls.add(line)

# Save the sorted, clean URLs to the flat file
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
