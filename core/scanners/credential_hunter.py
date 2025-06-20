# Detects usernames/passwords in code
import re
import os

def scan_for_credentials(repo_path):
    print("  - Running CredentialHunter...")
    patterns = [
    re.compile(r'(?i)(user(name)?|login)[\s:=\'"]+\w+'),
    re.compile(r'(?i)pass(word)?[\s:=\'"]+\S+'),
    re.compile(r'(?i)(auth|token)[\s:=\'"]+\S+')
]

    results = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.py', '.js', '.env', '.json', '.yml', '.ts', '.txt')):
                try:
                    with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                        for i, line in enumerate(f):
                            for pattern in patterns:
                                if pattern.search(line):
                                    results.append({
                                        "file": os.path.join(root, file),
                                        "line": i + 1,
                                        "match": line.strip()
                                    })
                except Exception:
                    continue
    return results

