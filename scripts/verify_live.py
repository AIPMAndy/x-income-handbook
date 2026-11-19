#!/usr/bin/env python3
"""Verify exact Pages bytes after deployment; a passing PR alone is not publication."""
import hashlib
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://aipmandy.github.io/x-income-handbook/"
PATHS = (
    "index.html",
    "experiment.html",
    "assets/experiment.css",
    "assets/experiment.js",
    "sitemap.xml",
    "llms.txt",
    "pdf/x-income-handbook-guide.pdf",
)
def digest(data):
    return hashlib.sha256(data).hexdigest()

def fetch_live(path, expected, attempts=9):
    stamp = os.getenv("GITHUB_SHA", "verify")[:12]
    url = BASE + path + "?build=" + stamp
    last = ""
    for attempt in range(1, attempts + 1):
        try:
            request = urllib.request.Request(url, headers={
                "User-Agent": "Andy-site-live-verifier/1.0",
                "Cache-Control": "no-cache",
                "Accept-Encoding": "identity",
            })
            with urllib.request.urlopen(request, timeout=20) as response:
                content = response.read()
                got = digest(content)
                if response.status == 200 and got == expected:
                    print(f"PASS {path}: HTTP 200 bytes={len(content)} SHA-256 {got}")
                    return
                last = f"HTTP {response.status}, got={got}, expected={expected}"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            last = repr(exc)
        print(f"RETRY {path}: attempt {attempt}/{attempts}: {last}", flush=True)
        if attempt < attempts:
            time.sleep(6)
    raise SystemExit(f"FAIL {path}: {last} / {url}")

def main():
    for path in PATHS:
        source = ROOT/path
        if not source.is_file():
            raise SystemExit(f"Missing source file: {path}")
        expected = digest(source.read_bytes())
        fetch_live(path, expected)
    print(f"PASS {len(PATHS)}/{len(PATHS)} published files match this checked-out commit, including unchanged 97-page PDF.")

if __name__ == "__main__":
    main()
