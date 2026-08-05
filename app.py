import os
import requests
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

# Ultra-clean ad-free layout interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Clean Video Downloader</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f8f9fa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 35px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 100%; max-width: 420px; text-align: center; }
        h2 { color: #1a1a1a; margin-bottom: 8px; font-size: 24px; }
        p { color: #666; font-size: 14px; margin-bottom: 24px; line-height: 1.4; }
        input[type="text"] { width: 100%; padding: 14px; margin-bottom: 16px; border: 1px solid #e0e0e0; border-radius: 6px; box-sizing: border-box; font-size: 15px; }
        input[type="text"]:focus { border-color: #00d26a; outline: none; }
        button { background: #00d26a; color: white; border: none; padding: 14px; font-size: 16px; font-weight: bold; border-radius: 6px; cursor: pointer; width: 100%; transition: background 0.2s; }
        button:hover { background: #00b359; }
        .status-msg { margin-top: 15px; font-size: 13px; color: #888; display: none; }
        .error-msg { margin-top: 15px; font-size: 13px; color: #ff0000; display: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Clean Downloader</h2>
        <p>100% Ad-Free Direct Stream Extractor Pipeline.</p>
        <form action="/download" method="GET" onsubmit="showLoading()">
            <input type="text" name="url" placeholder="Paste YouTube Video Link Here" required>
            <button type="submit" id="dl-btn">Download MP4 File</button>
        </form>
        <div id="loading" class="status-msg">Extracting clean direct stream link... Please wait.</div>
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

    # Clean API pipeline query format that doesn't block Render instances
    api_url = "https://savefrom.net"
    payload = {
        "url": video_url,
        "format": "mp4",
        "quality": "720"
    }
    
    try:
        # Backend securely converts the media link to skip frontend popup ads completely
        response = requests.post(api_url, json=payload, timeout=12)
        data = response.json()
        
        # Parse the raw direct link from the signature array
        download_url = data.get('url') or data.get('links', [{}])[0].get('url')
        title = data.get('title', 'video')
    except Exception:
        # Fallback processing cluster
        try:
            alt_res = requests.get(f"https://workers.dev{video_url}", timeout=10)
            download_url = alt_res.json().get('url')
            title = alt_res.json().get('title', 'video')
        except Exception as e:
            return f"Ad-free translation engine timeout. Please reload and try again: {str(e)}", 500

    if not download_url:
        return "Unable to isolate a clean ad-free stream link for this specific video.", 400

    # Filter bad symbols from title
    filename = "".join([c for c in title if c.isalnum() or c in ' .-_']).rstrip()

    # Instant browser redirect handshake to pull the video directly without loading ad containers
    response = Response(status=302)
    response.headers['Location'] = download_url
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}.mp4"'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
