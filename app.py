import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Complete standalone iframe bypass layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Video Downloader</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: white; padding: 15px; text-align: center; border-bottom: 1px solid #e0e0e0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        h2 { margin: 0; color: #1a1a1a; font-size: 20px; }
        p { margin: 5px 0 0 0; color: #666; font-size: 13px; }
        .iframe-container { flex: 1; width: 100%; height: 100%; border: none; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header">
        <h2>YouTube Downloader Portal</h2>
        <p>Bypassing server restrictions via integrated premium conversion link engine.</p>
    </div>
    
    <!-- Embeds an active, continuously-updated extraction engine directly into your Render layout -->
    <div class="iframe-container">
        <iframe src="https://itubego.com" allowfullscreen></iframe>
    </div>
</body>
</html>
