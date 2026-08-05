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

    # Inject the local Node.js path dynamically inside the executing environment block
    env_config = os.environ.copy()
    env_config["PATH"] = f"/opt/render/project/src/node_runtime/bin:{env_config.get('PATH', '')}"

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
        # Run command with custom localized env array safely
        stream_out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, env=env_config).decode('utf-8').strip()
        stream_urls = stream_out.split('\n')
        target_stream = stream_urls
    except subprocess.CalledProcessError as e:
        return f"Extraction Engine Failure: {e.output.decode('utf-8')}", 500
    except Exception as e:
        return f"Error executing pipeline sequence: {str(e)}", 500
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

    # Fetch title using the same localized environment variables
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
            
        filename = subprocess.check_output(title_cmd, stderr=subprocess.DEVNULL, env=env_config).decode('utf-8').strip()
        filename = "".join([c for c in filename if c.isalnum() or c in ' .-_']).rstrip()
    except:
        filename = "cloud_download"
    finally:
        if cookie_path and os.path.exists(cookie_path):
            os.remove(cookie_path)

    response = Response(status=302)
    response.headers['Location'] = target_stream
    response.headers['Content-Disposition'] = f'attachment; filename="{filename}.mp4"'
    return response
