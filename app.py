import os
import subprocess
import tempfile
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

# Polished clean UI layout with visual loaders
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
        <p>Mobile-optimized cloud bypass stream pipeline.</p>
        <form action="/download" method="GET" onsubmit="showLoading()">
            <input type="text" name="url" placeholder="Paste YouTube Video Link Here" required>
            <button type="submit" id="dl-btn">Extract & Download MP4</button>
        </form>
        <div id="loading" class="status-msg">Solving signature handshake and starting streaming pipeline... Please wait.</div>
    </div>
    <script>
        function showLoading() {
            document.getElementById('loading').style.display = 'block';
            document.getElementById('dl-btn').innerText = 'Solving Challenge...';
        }
    </script>
</body>
</html>
"""

def sanitize_mobile_cookies(raw_cookies):
    """
    Cleans up broken Netscape cookies caused by mobile clipboard wrapping.
    Reconstructs wrapped data back into flat single lines.
    """
    if not raw_cookies:
        return ""
    
    cleaned_lines = []
    current_line = ""
    
    raw_lines = raw_cookies.split('\n')
    
    for line in raw_lines:
        line_str = line.strip()
        if not line_str:
            continue
            
        # Check if this line starts a true Netscape row
        if (line_str.startswith('.') or 
            line_str.startswith('youtube.com') or 
            line_str.startswith('#')):
            
            if current_line:
                cleaned_lines.append(current_line)
            current_line = line_str
        else:
            # Re-weld wrapped mobile chunks back onto the parent line
            current_line += line_str

    if current_line:
        cleaned_lines.append(current_line)
        
    return "\n".join(cleaned_lines)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/download')
def download():
    video_url = request.args.get('url')
    if not video_url:
        return "URL parameter missing", 400

    raw_cookie_data = os.environ.get('YT_COOKIES')
    cookie_path = None

    if raw_cookie_data:
        try:
            sanitized_data = sanitize_mobile_cookies(raw_cookie_data)
            temp_cookie_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
            temp_cookie_file.write(sanitized_data)
            temp_cookie_file.close()
            cookie_path = temp_cookie_file.name
        except Exception as e:
            return f"Internal cookie initialization failure: {str(e)}", 500

    # Command optimized with explicit fallbacks and signature-solver configurations
    cmd = [
        'yt-dlp',
        '--no-check-certificates',
        '--extractor-args', 'youtube:player_client=android,web',
        '-f', 'best[ext=mp4]/best', 
        '-g', 
        video_url
    ]

    if cookie_path:
        cmd.extend(['--cookies', cookie_path])
    
    try:
        stream_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8').strip()
        stream_urls = stream_out.split('\n')
        target_stream = stream_urls[0]  # Grab primary stream block url
    except subprocess.CalledProcessError as e:
        return f"Extraction Engine Failure: {e.output.decode('utf-8')}", 500
    except Exception as e:
        return f"Error executing pipeline sequence: {str(e)}", 500
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

    # Fetch title
    try:
        title_cmd = [
            'yt-dlp', 
            '--no-check-certificates',
            '--extractor-args', 'youtube:player_client=android,web',
            '--get-title', 
            video_url
        ]
        if raw_cookie_data:
            sanitized_data = sanitize_mobile_cookies(raw_cookie_data)
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
                f.write(sanitized_data)
                cookie_path = f.name
            title_cmd.extend(['--cookies', cookie_path])
            
        filename = subprocess.check_output(title_cmd, stderr=subprocess.DEVNULL).decode('utf-8').strip()
        filename = "".join([c for c in filename if c.isalnum() or c in ' .-_']).rstrip()
    except:
        filename = "cloud_download"
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

    # Handshake direct redirect 
    response = Response(status=302)
    response.headers['Location'] = target_stream
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}.mp4"'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
