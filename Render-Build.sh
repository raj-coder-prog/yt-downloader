#!/usr/bin/env bash
# exit on error
set -o errexit

# Install python requirements
pip install -r requirements.txt

# Ensure yt-dlp is locally accessible and up-to-date
pip install --upgrade yt-dlp
