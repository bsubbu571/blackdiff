import os
import json

def generate_markdown_report(output_dir, org_name):
    report_path = f"{output_dir}/{org_name}_report.md"
    with open(report_path, "w") as report:
        report.write(f"# 🔐 BlackStrike Scan Report for `{org_name}`\n\n")

        for fname in os.listdir(output_dir):
            if fname.endswith(".json") or fname.endswith(".txt"):
                repo_name = fname.replace("_gitleaks.json", "").replace("_ggshield.json", "").replace("_credentials.txt", "").replace("_custom.txt", "").replace("_trufflehog.txt", "")
                report.write(f"## 🗂️ Repository: `{repo_name}`\n\n")
                report.write(f"### 📄 File: `{fname}`\n\n")

                path = os.path.join(output_dir, fname)
                if fname.endswith(".json"):
                    try:
                        with open(path, "r") as jf:
                            data = json.load(jf)
                            if isinstance(data, list) and len(data) > 0:
                                for item in data:
                                    match = item.get("Match", "N/A")
                                    file = item.get("File", "Unknown")
                                    author = item.get("Author", "N/A")
                                    line = item.get("StartLine", "?")
                                    report.write(f"- `{match}` found in `{file}` at line {line} by `{author}`\n")
                    except:
                        report.write("⚠️ Could not parse JSON.\n")
                else:
                    try:
                        with open(path, "r") as tf:
                            lines = tf.readlines()
                            for line in lines:
                                report.write(f"- {line.strip()}\n")
                    except:
                        report.write("⚠️ Could not read TXT file.\n")
                report.write("\n---\n\n")
    return report_path

