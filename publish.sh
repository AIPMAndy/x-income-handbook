#!/usr/bin/env bash
set -Eeuo pipefail

# Create and publish this complete static website as a new public GitHub repo.
# Requires gh (GitHub CLI) authenticated to the AIPMAndy account.
OWNER='AIPMAndy'
REPO='x-income-handbook'
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
fail() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
for cmd in gh git python3 node; do
  command -v "$cmd" >/dev/null 2>&1 || fail "Missing command: $cmd"
done
[[ -f index.html && -f LICENSE && -d .github/workflows ]] || fail 'Run from the extracted project folder.'
gh auth status >/dev/null 2>&1 || fail 'Run gh auth login before publishing.'
LOGIN="$(gh api user --jq '.login')"
[[ "$LOGIN" == "$OWNER" ]] || fail "Logged in as $LOGIN. Switch to $OWNER with gh auth switch."
if gh repo view "$OWNER/$REPO" >/dev/null 2>&1; then
  fail "Repository $OWNER/$REPO already exists. Will not overwrite an existing repository."
fi

python3 scripts/check.py
python3 -m unittest discover -s scripts -p 'test_*.py' -q
node --check assets/app.js
node scripts/smoke_dom.cjs

if [[ -d .git ]]; then
  fail 'This folder is already a Git repository. Do not initialize over existing history.'
fi
git init -q -b main
if [[ -z "$(git config user.name || true)" || -z "$(git config user.email || true)" ]]; then
  USER_ID="$(gh api user --jq '.id')"
  git config user.name "$OWNER"
  git config user.email "${USER_ID}+${OWNER}@users.noreply.github.com"
fi
git add -A
git commit -qm 'Release X income handbook V2: 26 chapters and interactive website'

gh repo create "$OWNER/$REPO" --public --description 'Practical 2026 X monetization handbook, 26 chapters, 24 templates and a free interactive site' --source . --remote origin --push
if ! gh api "repos/$OWNER/$REPO/pages" -X POST -f build_type=workflow >/dev/null 2>&1; then
  echo 'Set Settings -> Pages -> Build and deployment -> Source to GitHub Actions.'
fi
printf '\nRepository: https://github.com/%s/%s\nWebsite (after Actions succeeds): https://aipmandy.github.io/%s/\n' "$OWNER" "$REPO" "$REPO"
echo 'Manual task: Settings -> General -> Social preview -> upload assets/social-preview.png'
