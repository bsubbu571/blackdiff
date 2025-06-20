# ggshield integration
import subprocess

def run_ggshield(repo_path, output_file):
    print("  - Running ggshield...")
    try:
        subprocess.run(["ggshield", "secret", "scan", "repo", repo_path, "--json"], stdout=open(output_file, "w"))
    except Exception as e:
        print(f"    [!] ggshield failed: {e}")

