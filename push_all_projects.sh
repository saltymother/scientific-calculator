#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "=========================================================="
echo "🚀 Antigravity / Gemini Multi-Project GitHub Pusher"
echo "=========================================================="

PROJECTS=(
  "physics_wonderland:physics-wonderland"
  "mouse_the_tunnel_maze:mouse-the-tunnel-maze"
  "penguin_beyond_the_door:penguin-beyond-the-door"
  "tortoise_hare_3d:tortoise-and-hare-3d"
  "men_health_looksmaxxing:men-health-looksmaxxing"
  "history_chronicles:chronicles-of-bharatavarsha"
  "shinigami_the_golden_pot:shinigami-the-golden-pot"
  "vietnam_cinematic:vietnam-cinematic"
  "the_world_explained:the-world-explained"
  "global_arbitrage_nri:global-arbitrage-nri"
)

SUCCESS_COUNT=0
FAILED_COUNT=0

for item in "${PROJECTS[@]}"; do
  IFS=":" read -r dir repo <<< "$item"
  echo ""
  echo "----------------------------------------------------------"
  echo "📦 Processing: $dir (Repository: saltymother/$repo)"
  echo "----------------------------------------------------------"
  if [ -d "$dir/.git" ]; then
    (
      cd "$dir"
      if git push origin main && (git push origin main:gh-pages 2>/dev/null || true); then
        echo "✅ [$repo] Pushed successfully!"
        echo "🌐 GitHub: https://github.com/saltymother/$repo"
        echo "📄 GitHub Pages: https://saltymother.github.io/$repo/"
      else
        echo "❌ [$repo] Push failed. Ensure the repo exists at https://github.com/new with name '$repo'."
      fi
    )
  else
    echo "⚠️  [$dir] No .git directory found. Skipping."
  fi
done

echo ""
echo "=========================================================="
echo "📦 Processing Root: scientific-calculator"
echo "=========================================================="
if [ -d ".git" ]; then
  if git push origin main 2>/dev/null && (git push origin main:gh-pages 2>/dev/null || true); then
    echo "✅ [scientific-calculator] Pushed successfully!"
    echo "🌐 GitHub: https://github.com/saltymother/scientific-calculator"
    echo "📄 GitHub Pages: https://saltymother.github.io/scientific-calculator/"
  else
    echo "❌ [scientific-calculator] Push failed. Ensure repo exists at https://github.com/new named 'scientific-calculator'."
  fi
fi

echo ""
echo "=========================================================="
echo "🎉 All projects processed."
echo "=========================================================="
