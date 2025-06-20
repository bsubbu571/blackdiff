import requests
import re

def discover_possible_github_orgs(domain):
    print(f"[+] Discovering GitHub orgs for domain: {domain}")
    headers = {"Accept": "application/vnd.github.v3+json"}
    orgs = set()

    # GitHub Code Search (basic dorking)
    query = f"{domain} in:file"
    url = f"https://api.github.com/search/code?q={query}&per_page=5"

    try:
        r = requests.get(url, headers=headers)
        items = r.json().get("items", [])
        for item in items:
            repo_url = item["repository"]["html_url"]
            match = re.search(r"github\.com/([^/]+)/", repo_url)
            if match:
                orgs.add(match.group(1))
    except Exception as e:
        print(f"[!] GitHub API error: {e}")

    return list(orgs)

