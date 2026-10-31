#!/bin/sh
# Push 2028-kindle to GitHub (with pull first)
# Reads token from ~/github_token

set -eu

REPO_DIR="/home/petark/Documents/2028/2028-kindle"
GH_USER="peterkokosharov"
GH_REPO="2028-book"
TOKEN_FILE="$HOME/github_token"

cd "$REPO_DIR"

if [ -f "$TOKEN_FILE" ] && [ -r "$TOKEN_FILE" ]; then
    GH_TOKEN="$(cat "$TOKEN_FILE" | tr -d '[:space:]')"
    [ -n "$GH_TOKEN" ] || { echo "Token file empty: $TOKEN_FILE" >&2; exit 1; }
    echo "Using token from $TOKEN_FILE"
else
    echo "Token file not found: $TOKEN_FILE"
    printf "Enter GitHub token for %s: " "$GH_USER"
    stty -echo 2>/dev/null || true
    read -r GH_TOKEN
    stty echo 2>/dev/null || true
    echo
    [ -n "$GH_TOKEN" ] || { echo "Empty token" >&2; exit 1; }
fi

# init remote if missing
git remote get-url origin >/dev/null 2>&1 || \
  git remote add origin "https://${GH_USER}:${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git"

# ensure main branch
git branch -M main

# pull remote changes first (rebase to keep history clean)
git pull --rebase origin main

# push
git push -u origin main