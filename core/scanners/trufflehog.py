# TruffleHog integration
import subprocess

def run_trufflehog(repo_path, output_path):
    print("  - Running TruffleHog...")
    try:
        subprocess.run([
            "trufflehog", "filesystem",
            repo_path
        ], stdout=open(output_path, "w"))
    except Exception as e:
        print(f"    [!] TruffleHog failed: {e}")

