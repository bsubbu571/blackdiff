import argparse
from core.github.github_api import fetch_org_repos
from core.scanners.scanner_runner import run_scanners_on_repo
from utils.report_generator import generate_markdown_report

def main():
    parser = argparse.ArgumentParser(description="BlackStrike CLI")
    parser.add_argument("--org", help="GitHub organization name to scan", required=True)
    args = parser.parse_args()

    org_name = args.org
    print(f"\n[+] Fetching repos from GitHub org: {org_name}")
    repos = fetch_org_repos(org_name)

    if not repos:
        print("[!] No repositories found or API error.")
        return

    print(f"[+] Found {len(repos)} repos. Starting scans...\n")

    for repo in repos:
        run_scanners_on_repo(repo)

    generate_markdown_report("results", org_name)

if __name__ == "__main__":
    main()

