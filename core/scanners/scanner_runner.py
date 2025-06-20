import subprocess
import os
from core.scanners.trufflehog import run_trufflehog
from core.scanners.gitleaks import run_gitleaks
from core.scanners.ggshield import run_ggshield
from core.scanners.credential_hunter import scan_for_credentials
from core.scanners.custom_regex import run_custom_regex_scan, load_custom_patterns

from utils.severity_ranker import rank_severity
from utils.token_validator import (
    is_valid_aws_key,
    is_valid_firebase_url,
    is_valid_slack_token,
    is_valid_github_pat,
    is_valid_discord_token
)


def run_scanners_on_repo(repo_url, output_dir="results"):
    print(f"[+] Scanning repo: {repo_url}")
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    target_path = f"{output_dir}/{repo_name}"
    os.makedirs(output_dir, exist_ok=True)

    # Clone repo
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, target_path],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

    # === 1. TruffleHog ===
    run_trufflehog(target_path, f"{output_dir}/{repo_name}_trufflehog.txt")

    # === 2. Gitleaks ===
    run_gitleaks(target_path, f"{output_dir}/{repo_name}_gitleaks.json")

    # === 3. GGShield ===
    run_ggshield(target_path, f"{output_dir}/{repo_name}_ggshield.json")

    # === 4. Credential Hunter ===
    cred_results = scan_for_credentials(target_path)
    with open(f"{output_dir}/{repo_name}_credentials.txt", "w") as f:
        for r in cred_results:
            match = r["match"]
            file_path = r["file"]
            severity = rank_severity(match, file_path)
            f.write(f"{file_path}:{r['line']} - [{severity}] {match}\n")
            print(f"  - [Severity: {severity}] {match[:40]}...")

    # === 5. Secret Validation ===
    print("  - Validating extracted secrets...")
    for r in cred_results:
        match = r["match"]

        if "AKIA" in match:
            print(f"    [AWS Access Key] {match} – manually test secret")
        if "firebaseio.com" in match:
            is_live = is_valid_firebase_url(match)
            print(f"    [Firebase DB] {match} → Live: {is_live}")
        if "xoxb-" in match:
            is_valid = is_valid_slack_token(match)
            print(f"    [Slack Token] {match[:25]}... → Valid: {is_valid}")
        if match.startswith("ghp_") or match.startswith("ghs_"):
            is_valid = is_valid_github_pat(match)
            print(f"    [GitHub Token] {match[:25]}... → Valid: {is_valid}")
        if match.startswith("mfa.") or match.startswith("Bot "):
            is_valid = is_valid_discord_token(match)
            print(f"    [Discord Token] {match[:20]}... → Valid: {is_valid}")

    # === 6. Custom Regex ===
    patterns = load_custom_patterns()
    custom_results = run_custom_regex_scan(target_path, patterns)
    with open(f"{output_dir}/{repo_name}_custom.txt", "w") as f:
        for r in custom_results:
            f.write(f"{r['file']}:{r['line']} - {r['match']}\n")

    print(f"✔ Done scanning {repo_name}!\n")


# Optional test stub
if __name__ == "__main__":
    repos = ["https://github.com/uber/baseweb"]
    for repo in repos:
        run_scanners_on_repo(repo)

