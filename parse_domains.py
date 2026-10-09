import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

source_url = "https://urlhaus.abuse.ch/downloads/text/"
response = requests.get(source_url, headers=headers)
lines = response.text.splitlines()

clean_urls = set()

for line in lines:
    line = line.strip()
    
    # Skip metadata headers, comments, and empty lines securely
    if not line or line.startswith('#'):
        continue
        
    # Palo Alto URL Lists handle protocols, paths, and raw IPs natively. 
    # Simply add the raw line to deduplicate absolute identical paths.
    clean_urls.add(line)

with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
