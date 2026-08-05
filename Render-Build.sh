#!/usr/bin/env bash
# exit on error
set -o errexit

echo ">>> Installing dependencies..."
pip install -r requirements.txt
pip install --upgrade yt-dlp

echo ">>> Setting up Node.js standalone runtime for yt-dlp challenge solving..."
# Create a local folder inside your project directory to store Node binaries
mkdir -p $HOME/node_runtime
cd $HOME/node_runtime

# Download a lightweight portable binary version of Node.js
curl -sL https://nodejs.org | tar -xJ --strip-components=1

# Inject Node path directly into the global environment system path so yt-dlp detects it
export PATH=$HOME/node_runtime/bin:$PATH

echo ">>> Node.js successfully installed version:"
node -v
