import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Complete premium interface design matching corporate download suites
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaveFrom Pro - Premium Video Downloader Clone</title>
    <style>
        :root { --primary: #00d26a; --primary-hover: #00b359; --bg: #f4f6f8; --card: #ffffff; --text: #1e293b; --text-muted: #64748b; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 0; display: flex; flex-direction: column; min-height: 100vh; }
        .navbar { background: var(--card); border-bottom: 1px solid #e2e8f0; padding: 16px 24px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.02); }
        .logo { font-size: 22px; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 6px; text-decoration: none; }
        .logo span { color: var(--text); }
        .badge { background: #e0f2fe; color: #0369a1; font-size: 11px; font-weight: 700; padding: 4px 8px; border-radius: 20px; text-transform: uppercase; }
        .main-hero { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 40px 20px; text-align: center; }
        .headline { font-size: 36px; font-weight: 800; tracking: -0.5px; margin-bottom: 8px; }
        .subheadline { color: var(--text-muted); font-size: 16px; margin-bottom: 32px; max-width: 500px; line-height: 1.5; }
        .search-wrapper { background: var(--card); border-radius: 16px; padding: 8px; display: flex; width: 100%; max-width: 580px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05), 0 8px 10px -6px rgba(0,0,0,0.05); box-sizing: border-box; margin-bottom: 24px; border: 1px solid #e2e8f0; }
        .search-wrapper input { flex: 1; border: none; padding: 16px; font-size: 16px; outline: none; border-radius: 12px; min-width: 0; }
        .search-wrapper button { background: var(--primary); color: white; border: none; padding: 0 28px; font-size: 15px; font-weight: 700; border-radius: 12px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
        .search-wrapper button:hover { background: var(--primary-hover); transform: translateY(-1px); }
        .result-card { display: none; background: var(--card); border-radius: 16px; border: 1px solid #e2e8f0; padding: 24px; width: 100%; max-width: 564px; text-align: left; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); box-sizing: border-box; }
        .video-meta { display: flex; gap: 16px; align-items: center; margin-bottom: 20px; }
        .video-icon { background: #fee2e2; color: #ef4444; width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 24px; flex-shrink: 0; }
        .video-details { min-width: 0; }
        .video-title { font-weight: 700; font-size: 16px; margin-bottom: 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .video-duration { color: var(--text-muted); font-size: 13px; }
        .action-btn { display: block; text-align: center; background: #2563eb; color: white; text-decoration: none; padding: 14px; border-radius: 10px; font-weight: 700; font-size: 15px; transition: background 0.2s; }
        .action-btn:hover { background: #1d4ed8; }
        .loader { display: none; font-size: 14px; color: var(--text-muted); font-weight: 500; margin-top: 10px; }
        .error-banner { display: none; color: #b91c1c; background: #fef2f2; border: 1px solid #fca5a5; padding: 12px; border-radius: 8px; font-size: 14px; width: 100%; max-width: 540px; text-align: center; margin-top: 10px; }
        .footer { background: var(--card); border-top: 1px solid #e2e8f0; padding: 20px; text-align: center; font-size: 13px; color: var(--text-muted); }
    </style>
</head>
<body>

    <nav class="navbar">
        <a href="/" class="logo">SaveFrom <span>Pro</span></a>
        <div class="badge">Ad-Free Link Engine</div>
    </nav>

    <main class="main-hero">
        <div class="headline">Online Video Downloader</div>
        <div class="subheadline">Paste any video URL to instantly generate clean, direct MP4 media stream links without page tracking or popup advertisements.</div>
        
        <div class="search-wrapper">
            <input type="text" id="target-url" placeholder="Paste media source link here..." required>
            <button type="button" id="submit-btn" onclick="processExtraction()">Extract Media</button>
        </div>

        <div id="status-loader" class="loader">Querying data cluster matrix... Please wait.</div>
        <div id="error-box" class="error-banner"></div>

        <div id="output-card" class="result-card">
            <div class="video-meta">
                <div class="video-icon">▶</div>
                <div class="video-details">
                    <div id="res-title" class="video-title">Loading title parameters...</div>
                    <div class="video-duration">Format container: High-Definition MP4</div>
                </div>
            </div>
            <a href="#" id="direct-dl-link" class="action-btn" target="_blank" rel="noopener noreferrer">Download Video File</a>
        </div>
    </main>

    <footer class="footer">
        &copy; 2026 SaveFrom Pro Clone Engine Portal Setup. Standard Open Core Distribution Framework.
    </footer>

    <script>
        async function processExtraction() {
            const urlVal = document.getElementById('target-url').value.trim();
            const btn = document.getElementById('submit-btn');
            const loader = document.getElementById('status-loader');
            const errorBox = document.getElementById('error-box');
            const outCard = document.getElementById('output-card');

            if(!urlVal) { alert('Please insert a media tracking link.'); return; }

            // Reset view state
            errorBox.style.display = 'none';
            outCard.style.display = 'none';
            loader.style.display = 'block';
            btn.disabled = true;
            btn.innerText = 'Extracting...';

            try {
                const response = await fetch(`/api/extract?url=${encodeURIComponent(urlVal)}`);
                const result = await response.json();

                if(!response.ok || !result.success) {
                    throw new Error(result.error || 'Failed to extract download properties.');
                }

                // Inject extracted values smoothly
                document.getElementById('res-title').innerText = result.title;
                const dlLink = document.getElementById('direct-dl-link');
                dlLink.href = result.download_url;
                
                // Forces browser file downscaling trigger natively 
                dlLink.setAttribute('download', result.title + '.mp4');

                loader.style.display = 'none';
                outCard.style.display = 'block';
            } catch (err) {
                loader.style.display = 'none';
                errorBox.style.display = 'block';
                errorBox.innerText = err.message;
            } finally {
                btn.disabled = false;
                btn.innerText = 'Extract Media';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/extract')
def extract_api():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "URL parameter is missing"}), 400

    # Payload arguments tracking clean proxy network nodes
    api_url = "https://savefrom.net"
    payload = {"url": video_url, "format": "mp4", "quality": "720"}
    
    try:
        response = requests.post(api_url, json=payload, timeout=12)
        data = response.json()
        download_url = data.get('url') or data.get('links', [{}])[0].get('url')
        title = data.get('title', 'Converted_Media_File')
    except Exception:
        # High availability alternative bridge
        try:
            alt = requests.post('https://wuk.sh', json={'url': video_url}, headers={'Accept': 'application/json', 'Content-Type': 'application/json'}, timeout=10)
            download_url = alt.json().get('url')
            title = alt.json().get('text', 'Download_Asset')
        except Exception as e:
            return jsonify({"success": False, "error": f"API translation infrastructure timeout: {str(e)}"}), 500

    if not download_url:
        return jsonify({"success": False, "error": "Unable to isolate clean streaming source properties for this file URL."}), 400

    return jsonify({
        "success": True,
        "title": title,
        "download_url": download_url
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
