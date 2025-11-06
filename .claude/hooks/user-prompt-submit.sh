#!/bin/bash
# Auto-commit and push changes after significant modifications
# This hook runs after I make changes to files

# Check if there are any changes
if [[ -n $(git status -s) ]]; then
    # Stage all changes
    git add -A

    # Create commit with automatic message
    git commit -m "Auto-update: Changes made via Claude Code on $(date '+%Y-%m-%d %H:%M')" --no-verify

    # Push to GitHub
    git push origin main --quiet

    echo "✅ Changes automatically committed and pushed to GitHub"
fi
