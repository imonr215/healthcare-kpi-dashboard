"""
run_all.py

Regenerates the dataset and rebuilds index.html from scratch.

Run:
    python run_all.py
"""

import subprocess
import sys


def run(script):
    print(f"\n{'=' * 60}\nRunning {script}\n{'=' * 60}")
    result = subprocess.run([sys.executable, script])
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    run("src/generate_data.py")
    run("src/build_dashboard.py")
    print("\nDone. Open index.html in a browser, or deploy it via GitHub Pages.")
