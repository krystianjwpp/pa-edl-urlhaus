import urllib.parse
import requests

# Fetch the raw URLHaus text list
source_url = "https://abuse.ch"
response = requests.get(source_url)
lines = response.text.splitlines()

clean_urls = set()

for line in lines:
    line = line.strip()
    # 1. Skip comment headers
    if not line or line.startswith('#'):
        continue
        
    try:
        # 2. Check if the line has a protocol schema
        if not line.startswith(('http://', 'https://')):
            continue
            
        # 3. Parse the URL
        parsed = urllib.parse.urlparse(line)
        hostname = parsed.netloc
        
        # Strip out port numbers from host assessment if present (e.g., 59.96.140.224:60418 -> 59.96.140.224)
        host_only = hostname.split(':')[0] if ':' in hostname else hostname
        
        # 4. Filter out raw IP addresses (Palo Alto URL EDLs reject raw IPs)
        clean_host = host_only.replace('.', '')
        if not clean_host.isdigit():
            # 5. Reconstruct the URL WITHOUT the http:// or https:// prefix
            # Palo Alto URL lists expect formats like: ://domain.com
            path_and_query = parsed.path
            if parsed.query:
                path_and_query += '?' + parsed.query
                
            pa_url_format = f"{hostname}{path_and_query}"
            clean_urls.add(pa_url_format)
            
    except Exception:
        continue

# Save the sorted, clean URLs to a flat file
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
