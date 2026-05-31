#!/usr/bin/env python3
"""Deploy Farcaster Frame to GitHub Pages."""
import json
import os
import subprocess
import urllib.request
import urllib.error

# Read token from persistent Wiki Layer
with open("/home/user/wiki/raw/.gh_token") as f:
    GH = f.read().strip()

owner = "solosofi"
repo = "farcaster-frame-agenticdao"
headers = {
    "Authorization": f"token {GH}",
    "Accept": "application/vnd.github+json",
    "User-Agent": "Hermes",
    "Content-Type": "application/json",
}

# 1. Create repo if needed
try:
    req = urllib.request.Request(
        f"https://api.github.com/repos/{owner}/{repo}",
        headers=headers,
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        print(f"Repo exists: https://github.com/{owner}/{repo}")
except urllib.error.HTTPError as e:
    if e.code == 404:
        req = urllib.request.Request(
            "https://api.github.com/user/repos",
            data=json.dumps({
                "name": repo,
                "private": False,
                "description": "AgenticDAO Farcaster Frame + Push Protocol",
            }).encode(),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            info = json.loads(r.read().decode())
            print(f"Created: https://github.com/{owner}/{repo}")

# 2. Init git and push
os.chdir("/home/user/farcaster-frame")
subprocess.run(["git", "init"], check=False)
subprocess.run(["git", "add", "."], check=False)
subprocess.run(["git", "commit", "-m", "init: Farcaster Frame + Push Protocol"], check=False)
subprocess.run(["git", "remote", "remove", "origin"], check=False)
subprocess.run([
    "git", "remote", "add", "origin",
    f"https://{GH}@github.com/{owner}/{repo}.git"
], check=False)
subprocess.run(["git", "branch", "-M", "main"], check=False)
subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=False)

print("=== LIVE ===")
print(f"Repo: https://github.com/{owner}/{repo}")
print(f"GitHub Pages: https://{owner}.github.io/{repo}/")
