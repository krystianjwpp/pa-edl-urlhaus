import requests

# 1. Add standard browser headers to securely bypass Cloudflare bot mitigation
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Fetch the raw URLHaus text list
source_url = "https://urlhaus.abuse.ch/downloads/text/"
response = requests.get(source_url, headers=headers)
lines = response.text.splitlines()

clean_urls = set()

for line in lines:
    line = line.strip()
    
    # 2. Skip comment headers and empty lines
    if not line or line.startswith('#'):
        continue
        
    # 3. Strip protocols if they exist
    if line.startswith('http://'):
        line = line[7:]
    elif line.startswith('https://'):
        line = line[8:]
        
    try:
        # 4. Extract the hostname to filter out raw IP addresses
        if '/' in line:
            host_string = line.split('/', 1)[0]
        else:
            host_string = line
            
        # Strip out port numbers if present (e.g., domain.com:8080 -> domain.com)
        if ':' in host_string:
            host_string = host_string.split(':')[0]
            
        # 5. Filter out raw IP addresses so Palo Alto URL lists accept it seamlessly
        clean_host_check = host_string.replace('.', '')
        if not clean_host_check.isdigit() and line:
            clean_urls.add(line)
            
    except Exception:
        continue

# Save the sorted, clean URLs to the flat file
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
