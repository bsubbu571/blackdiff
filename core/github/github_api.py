
import requests

def fetch_org_repos(org_name, github_token=None):
    headers = {
        "Accept": "application/vnd.github+json"
    }
    if github_token:
        headers["Authorization"] = f"Bearer {github_token}"

    repos = []
    page = 1

    while True:
        url = f"https://api.github.com/orgs/{org_name}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"[!] Failed to fetch repos for org: {org_name} - Status: {response.status_code}")
            break

        data = response.json()
        if not data:
            break

        for repo in data:
            repos.append(repo["clone_url"])

        page += 1

    return repos

# Example usage
if __name__ == "__main__":
    org = "uber"
    repos = fetch_org_repos(org)
    print(f"[+] Found {len(repos)} public repositories in org '{org}'")
    for r in repos:
        print(r)
