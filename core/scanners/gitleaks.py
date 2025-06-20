# Gitleaks integration
import subprocess

def run_gitleaks(repo_path, output_path):
    print("  - Running Gitleaks...")
    try:
        subprocess.run([
            "gitleaks", "detect",
            "--source", repo_path,
            "--report-path", output_path,
            "--no-banner"
        ])
    except Exception as e:
        print(f"    [!] Gitleaks failed: {e}")

