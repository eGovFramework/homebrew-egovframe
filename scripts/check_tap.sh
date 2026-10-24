#!/usr/bin/env bash
# Validate every cask. Only the documented legacy style exemption is skipped;
# all casks still go through readall and audit. Run from the checkout root.
set -euo pipefail
default_tap() {
  local repo=${GITHUB_REPOSITORY:-}
  if [ -z "$repo" ]; then
    repo=$(git remote get-url origin 2>/dev/null | sed -E 's#.*github\.com[:/]([^/]+/[^/.]+)(\.git)?$#\1#')
  fi
  repo=${repo:-eGovFramework/homebrew-egovframe}
  printf '%s\n' "$repo" | tr '[:upper:]' '[:lower:]' | sed 's#/homebrew-#/#'
}
tap=${1:-$(default_tap)}
all=()
style=()
for file in Casks/*.rb; do
  name=$(basename "$file" .rb)
  all+=("$tap/$name")
  if grep -qxF "$name" .github/style-exempt.txt; then
    echo "style-exempt: $name (see .github/style-exempt.txt)"
  else
    style+=("$tap/$name")
  fi
done

brew readall --aliases --os=all --arch=all "$tap"
brew style "${style[@]}"
brew audit --cask --except=installed "${all[@]}"
