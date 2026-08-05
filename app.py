import os
import requests
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

# Polished clean UI layout
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Video Downloader</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 420px; text-align: center; }
        h2 { color: #1a1a1a; margin-bottom: 8px; font-size: 24px; }
        p { color: #666; font-size: 14px; margin-bottom: 24px; line-height: 1.4; }
        input[type="text"] { width: 100%; padding: 14px; margin-bottom: 16px; border: 1px solid #e0e0e0; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        input[type="text"]:focus { border-color: #ff0000; outline: none; }
        button { background: #ff0000; color: white; border: none; padding: 14px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; transition: background 0.2s; }
        button:hover { background: #cc0000; }
        .status-msg { margin-top: 15px; font-size: 13px; color: #888; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Downloader</h2>
        <p>Bypassing server blocks via clean backend stream proxy routing.</p>
        <form action="/download" method="GET" onsubmit="showLoading()">
            <input type="text" name="url" placeholder="Paste YouTube Video Link Here" required>
            <button type="submit" id="dl-btn">Extract & Download MP4</button>
        </form>
        <div id="loading" class="status-msg">Resolving link and starting streaming pipeline... Please wait.</div>
    </div>
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('dl-btn').innerText = 'Processing Stream...';
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "URL parameter missing", 400

    # The backend handles the request securely using clean HTTP requests
    # This completely eliminates "Failed to fetch" browser blocks!
    payload = {
        'url': video_url,
        'videoQuality': '720',
        'downloadMode': 'video'
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post('https://cobalt.tools', json=payload, headers=headers, timeout=10)
        data = response.json()
        download_url = data.get('url')
    except Exception:
        # Fallback cluster route if primary API is under heavy traffic load
        try:
            response = requests.post('https://wuk.sh', json={'url': video_url}, headers=headers, timeout=10)
            data = response.json()
            download_url = data.get('url')
        except Exception as e:
            return f"Extraction Engine Failure. Link resolution timed out: {str(e)}", 500

    if not download_url:
        return "Could not resolve an active media download link from this URL string.", 400

    # 302 Redirection handoff directly to your mobile phone download browser manager
    response = Response(status=302)
    response.headers['Location'] = download_url
    response.headers['Content-Disposition'] = 'attachment; filename="video.mp4"'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
