import os
import subprocess
from flask import Flask, request, Response, render_template_string

app = Flask(__name__)

# Simple, responsive HTML Interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cloud Video Downloader</title>
    <style>
        body { font-family: sans-serif; background: #f4f4f9; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .container { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 100%; max-width: 450px; text-align: center; }
        input[type="text"] { width: 90%; padding: 12px; margin: 15px 0; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #ff0000; color: white; border: none; padding: 12px 20px; font-size: 16px; border-radius: 4px; cursor: pointer; width: 95%; }
        button:hover { background: #cc0000; }
        p { color: #666; font-size: 14px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>YouTube Video Downloader</h2>
        <p>Enter the video link below to stream download directly to your device.</p>
        <form action="/download" method="GET">
            <input type="text" name="url" placeholder="Paste YouTube Link Here" required>
            <button type="submit">Download MP4</button>
        </form>
    </div>
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
        return "URL parameter is missing", 400

    # Command to get the video's streamable URL without downloading it to the server
    # It targets standard progressive mp4 formats (typically up to 720p) so audio/video are combined.
    cmd = [
        'yt-dlp',
        '-f', 'bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]', 
        '-g', 
        video_url
    ]
    
    try:
        # Get the direct stream URL from YouTube
        stream_url = subprocess.check_output(cmd).decode('utf-8').strip().split('\n')[0]
    except Exception as e:
        return f"Error resolving video stream: {str(e)}", 500

    # Fetch title for the filename
    try:
        title_cmd = ['yt-dlp', '--get-title', video_url]
        filename = subprocess.check_output(title_cmd).decode('utf-8').strip()
        filename = "".join([c for c in filename if c.isalpha() or c.isdigit() or c in ' .-_']).rstrip()
    except:
        filename = "video"

    # Dynamic redirect directly to the source stream for zero-bloat server pipeline
    # This prevents Render from running out of RAM or disk space.
    response = Response(status=302)
    response.headers['Location'] = stream_url
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}.mp4"'
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
