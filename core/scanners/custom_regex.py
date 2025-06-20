# Custom regex scanner
import re
import os
import yaml

def load_custom_patterns(pattern_file="core/scanners/custom_rules.yaml"):
    with open(pattern_file, "r") as f:
        rules = yaml.safe_load(f)
    return [re.compile(r) for r in rules.get("patterns", [])]

def run_custom_regex_scan(repo_path, patterns):
    print("  - Running CustomRegex scanner...")
    results = []

    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if file.endswith(('.js', '.env', '.py', '.json', '.yml', '.ts', '.html', '.go')):
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
                except:
                    continue
    return results

