import requests

# Fetch the raw URLHaus text list
source_url = "https://urlhaus.abuse.ch/downloads/text/"
response = requests.get(source_url)
lines = response.text.splitlines()

clean_urls = set()

for line in lines:
    line = line.strip()
    
    # 1. Skip comment headers and empty lines
    if not line or line.startswith('#'):
        continue
        
    # 2. Strip protocols if they somehow exist (handling edge cases)
    if line.startswith('http://'):
        line = line[7:]
    elif line.startswith('https://'):
        line = line[8:]
        
    try:
        # 3. Isolate the host part to inspect it for raw IPs
        # Example line: tradingengineers.in/path/file.php
        host_part = line.split('/')[0]
        
        # Strip out port numbers if present (e.g., 59.96.140.224:60418 -> 59.96.140.224)
        if ':' in host_part:
            host_part = host_part.split(':')[0]
            
        # 4. Filter out raw IP addresses (so it's purely a clean text URL list for PA)
        clean_host = host_part.replace('.', '')
        if not clean_host.isdigit() and line:
            clean_urls.add(line)
            
    except Exception:
        continue

# Save the sorted, clean URLs to the flat file
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
