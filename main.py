import argparse
from core.github.github_api import fetch_org_repos
from core.github.discover_orgs import discover_possible_github_orgs
from core.scanners.scanner_runner import run_scanners_on_repo
from utils.report_generator import generate_markdown_report
from core.passive.subdomain_finder import get_subdomains_crtsh

def scan_org(org_name):
    print(f"\n[+] Fetching repos from GitHub org: {org_name}")
    repos = fetch_org_repos(org_name)
    if not repos:
        print("[!] No repositories found or API error.")
        return
    print(f"[+] Found {len(repos)} repos. Starting scans...\n")
    for repo in repos:
        run_scanners_on_repo(repo)
    generate_markdown_report("results", org_name)

def main():
    parser = argparse.ArgumentParser(description="BlackStrike CLI")
    parser.add_argument("--org", help="GitHub organization name to scan")
    parser.add_argument("--domain", help="Company domain to discover GitHub orgs from")
    args = parser.parse_args()

    if args.org:
        scan_org(args.org)

    elif args.domain:
        subdomains = get_subdomains_crtsh(args.domain)
        print(f"[+] Found {len(subdomains)} subdomains")

        related_orgs = set()
        for sub in subdomains:
            parts = sub.split(".")
            if parts[0] not in ['www', 'mail', 'ftp'] and len(parts[0]) > 2:
                related_orgs.add(parts[0].lower())

        gh_orgs = discover_possible_github_orgs(args.domain)
        all_orgs = related_orgs.union(gh_orgs)
        print(f"[+] Final GitHub org candidates: {all_orgs}")

        for org in all_orgs:
            scan_org(org)

    else:
        print("❌ Please provide --org OR --domain")

if __name__ == "__main__":
    main()

