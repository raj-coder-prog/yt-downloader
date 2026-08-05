#!/usr/bin/env bash
# exit on error
set -o errexit

# Core module setups
pip install -r requirements.txt

# Force update engine modules to bypass routine API signature rotations
pip install --upgrade yt-dlp
