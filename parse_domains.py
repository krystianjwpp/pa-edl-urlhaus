import requests

# Fetch the raw URLHaus text list
source_url = "https://abuse.ch"
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
        # 3. Extract the hostname component to verify if it's an IP address
        # Split on the first forward slash to separate host from path
        parts = line.split('/', 1)
        host_string = parts[0]
        
        # Strip out the port numbers safely if they exist in the host string
        if ':' in host_string:
            host_string = host_string.split(':')[0]
            
        # 4. Filter out raw IP addresses (Palo Alto URL EDLs strictly reject raw IPs)
        clean_host_check = host_string.replace('.', '')
        if not clean_host_check.isdigit() and line:
            clean_urls.add(line)
            
    except Exception:
        continue

# Save the sorted, clean URLs to the flat file
with open("pa-clean-urls.txt", "w") as f:
    for url_path in sorted(clean_urls):
        f.write(f"{url_path}\n")
