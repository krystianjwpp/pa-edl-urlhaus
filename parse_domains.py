import re
import requests

# Standard browser headers to bypass bot mitigation securely
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Fetch the raw URLhaus text list
source_url = "https://urlhaus.abuse.ch/downloads/text/"
response = requests.get(source_url, headers=headers)
lines = response.text.splitlines()

clean_urls = set()

for line in lines:
    line = line.strip()
    
    # 1. Skip comment headers and empty lines
    if not line or line.startswith('#'):
        continue
        
    # 2. Hard-strip any protocol prefix (http, https, ftp) at the absolute beginning of the line
    processed_line = re.sub(r'^[a-zA-Z]+://', '', line)
        
    # 3. Add the completely cleaned line to the set to push into the file
    if processed_line:
        clean_urls.add(processed_line)

# Save the sorted, clean URLs to the flat file
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
