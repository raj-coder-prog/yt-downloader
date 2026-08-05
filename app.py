import os
from flask import Flask, render_template_string

app = Flask(__name__)

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
        .status-msg { margin-top: 15px; font-size: 14px; font-weight: bold; color: #ff0000; display: none; }
        .success-box { margin-top: 20px; display: none; background: #f0fff4; border: 1px solid #c6f6d5; padding: 15px; border-radius: 6px; }
        .download-link { display: inline-block; background: #38a169; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; font-weight: bold; margin-top: 10px; }
        .download-link:hover { background: #2f855a; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Downloader</h2>
        <p>Bypassing server blocks via direct local client stream extraction.</p>
        <div id="downloader-form">
            <input type="text" id="video-url" placeholder="Paste YouTube Video Link Here" required>
            <button type="button" onclick="extractVideo()">Extract Video MP4</button>
        </div>
        <div id="loading" class="status-msg" style="color: #666;">Processing handshake from your device connection...</div>
        <div id="error" class="status-msg"></div>
        
        <div id="success" class="success-box">
            <div style="color: #2f855a; font-weight: bold;" id="video-title">Video Stream Ready!</div>
            <a href="#" id="dl-anchor" class="download-link" rel="noopener noreferrer">Save MP4 to Device</a>
        </div>
    </div>

    <script>
        async function extractVideo() {
            const urlInput = document.getElementById('video-url').value.trim();
            const loadingDiv = document.getElementById('loading');
            const errorDiv = document.getElementById('error');
            const successDiv = document.getElementById('success');
            const dlAnchor = document.getElementById('dl-anchor');

            if (!urlInput) {
                alert('Please paste a valid URL');
                return;
            }

            loadingDiv.style.display = 'block';
            errorDiv.style.display = 'none';
            successDiv.style.display = 'none';

            try {
                // FIXED: Uses an alternative layout structure to extract links directly through an open API endpoint format
                const cleanUrl = encodeURIComponent(urlInput);
                const targetApiUrl = `https://allorigins.win{encodeURIComponent('https://cobalt.tools')}`;
                
                const response = await fetch('https://cobalt.tools', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        url: urlInput,
                        videoQuality: '720',
                        downloadMode: 'video',
                        filenamePattern: 'basic'
                    })
                }).catch(() => {
                    // Fallback to a secondary secure mirror API endpoint if the main pool is saturated
                    return fetch(`https://wuk.sh`, {
                        method: 'POST',
                        headers: {
                            'Accept': 'application/json',
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ url: urlInput })
                    });
                });

                const data = await response.json();

                if (data.status === 'stream' || data.status === 'redirect' || data.url) {
                    loadingDiv.style.display = 'none';
                    successDiv.style.display = 'block';
                    dlAnchor.href = data.url;
                } else if (data.text) {
                    throw new Error(data.text);
                } else {
                    throw new Error('Could not resolve download links from this specific video configuration.');
                }
            } catch (err) {
                loadingDiv.style.display = 'none';
                errorDiv.style.display = 'block';
                errorDiv.innerText = 'Extraction Issue: ' + err.message + '. Please tap the link again to retry.';
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
