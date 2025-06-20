import requests
import re

def get_subdomains_crtsh(domain):
    print(f"[+] Getting subdomains from crt.sh for: {domain}")
    url = f"https://crt.sh/?q=%.{domain}&output=json"
    try:
        r = requests.get(url, timeout=10)
        subdomains = set()
        for entry in r.json():
            name = entry["name_value"]
            for sub in name.split("\n"):
                if domain in sub:
                    subdomains.add(sub.strip())
        return list(subdomains)
    except Exception as e:
        print(f"[!] crt.sh error: {e}")
        return []

