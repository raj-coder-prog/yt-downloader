import os
from flask import Flask, render_template_string

app = Flask(__name__)

# Complete standalone visual interface
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
        .headline { font-size: 36px; font-weight: 800; margin-bottom: 8px; }
        .subheadline { color: var(--text-muted); font-size: 16px; margin-bottom: 32px; max-width: 500px; line-height: 1.5; }
        .search-form { background: var(--card); border-radius: 16px; padding: 8px; display: flex; width: 100%; max-width: 580px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.05); box-sizing: border-box; margin-bottom: 24px; border: 1px solid #e2e8f0; }
        .search-form input { flex: 1; border: none; padding: 16px; font-size: 16px; outline: none; border-radius: 12px; min-width: 0; }
        .search-form button { background: var(--primary); color: white; border: none; padding: 0 28px; font-size: 15px; font-weight: 700; border-radius: 12px; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
        .search-form button:hover { background: var(--primary-hover); transform: translateY(-1px); }
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
        
        <!-- Form action securely handles the extraction externally, bypassing server bans and CORS -->
        <form class="search-form" action="https://9xbuddy.org" method="GET" target="_blank">
            <input type="text" name="url" placeholder="Paste video link here (YouTube, Facebook, etc.)..." required>
            <button type="submit">Extract Media</button>
        </form>
    </main>

    <footer class="footer">
        &copy; 2026 SaveFrom Pro Clone Engine Portal Setup.
    </footer>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
