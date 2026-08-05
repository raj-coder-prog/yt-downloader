#!/usr/bin/env bash
# exit on error
set -o errexit

echo ">>> Processing python dependencies..."
pip install -r requirements.txt
pip install --upgrade yt-dlp

echo ">>> Setting up local standalone Node.js workspace binaries..."
mkdir -p $HOME/node_runtime
cd $HOME/node_runtime

# Download the portable Node.js binaries
curl -sL https://nodejs.org | tar -xJ --strip-components=1

# Safely inject path locally without overwriting Render's system engine
export PATH="$HOME/node_runtime/bin:$PATH"

echo ">>> Node.js successfully initialized engine instance version:"
node -v
