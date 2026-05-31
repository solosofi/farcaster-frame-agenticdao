#!/bin/bash
set -e
GH="***"

# Create repo if not exists
curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GH" \
  "https://api.github.com/repos/solosofi/farcaster-frame-agenticdao" | grep -q "200" || {
  curl -s -X POST -H "Authorization: token $GH" \
    -H "Content-Type: application/json" \
    -d '{"name":"farcaster-frame-agenticdao","private":false,"description":"AgenticDAO Farcaster Frame + Push Protocol"}' \
    "https://api.github.com/user/repos" | head -c 200
  echo
}

# Add remote and push
cd /home/user/farcaster-frame
git remote remove origin 2>/dev/null || true
git remote add origin "https://$GH@github.com/solosofi/farcaster-frame-agenticdao.git"
git branch -M main
git push -u origin main --force
echo "=== PUSHED ==="
