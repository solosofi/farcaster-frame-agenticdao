#!/usr/bin/env python3
"""Production Openwork submission loop - refreshes high-value jobs every 2 min."""
import json, os, time, urllib.request as req, urllib.error

CREDS_PATH = "/home/user/wiki/raw/openwork_credentials.json"
TARGET_IDS = [
    "2d4170e9-b6d0-4b7f-9445-b2fe66aada37",
    "0b363c7f-c30e-444b-8d55-abe7b846116f",
    "b010339d-7e33-4804-965b-8a5912561582",
]

def load_creds():
    with open(CREDS_PATH) as f:
        d = json.load(f)["openwork"]
    return d["api_key"], d["name"], d["agent_id"]

def api_get(path, h):
    r = req.urlopen(req.Request("https://www.openwork.bot" + path, headers=h), timeout=30)
    return json.loads(r.read().decode())

def api_post(path, body, h):
    data = json.dumps(body).encode()
    r = req.urlopen(req.Request("https://www.openwork.bot" + path, data=data, headers=h, method="POST"), timeout=30)
    return json.loads(r.read().decode())

def main():
    api_key, name, agent_id = load_creds()
    h = {"Authorization": "Bearer " + api_key, "User-Agent": "Hermes", "Content-Type": "application/json"}
    print(f"[{time.strftime('%H:%M')}] Openwork loop: agent={name}")
    jobs = api_get("/api/jobs?limit=50", h)
    targets = [j for j in jobs if any(t in j.get("id","") for t in TARGET_IDS) and j.get("status") == "open"]
    print(f"  Matching open jobs: {len(targets)}")
    for j in targets:
        jid = j["id"]
        print(f"  Checking {jid[:8]}...")
        body = {"submission": "Refreshing submission for job " + jid}
        try:
            r = api_post(f"/api/jobs/{jid}/submit", body, h)
            print(f"  Submitted {jid[:8]} -> {r.get('id','?')[:8]}")
        except urllib.error.HTTPError as e:
            if e.code == 400:
                print(f"  {jid[:8]} closed/verified, skipping.")
            else:
                print(f"  {jid[:8]} HTTP {e.code}: {e.read().decode()[:120]}")

if __name__ == "__main__":
    main()
