@app.route('/api/extract')
def extract_api():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"success": False, "error": "URL parameter is missing"}), 400

    # Modern high-capacity translation engine endpoint that does not block Render IPs
    api_url = f"https://deat.xyz{video_url}"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=12)
        data = response.json()
        
        # Parse standard direct stream blocks cleanly
        download_url = data.get('url') or data.get('download')
        title = data.get('title', 'Converted_Media_File')
        
        # Fallback to secondary stream mapping if nested inside arrays
        if not download_url and 'formats' in data:
            # Filters and extracts the highest progressive mp4 quality block
            mp4_formats = [f for f in data['formats'] if f.get('ext') == 'mp4' and f.get('url')]
            if mp4_formats:
                download_url = mp4_formats[-1]['url']
                
    except Exception:
        # Emergency backup pipeline node if primary cluster is saturated
        try:
            alt_res = requests.get(f"https://vercel.app{video_url}", timeout=10)
            alt_data = alt_res.json()
            download_url = alt_data.get('url')
            title = alt_data.get('title', 'Download_Asset')
        except Exception as e:
            return jsonify({"success": False, "error": f"Ad-free infrastructure timeout. Please retry: {str(e)}"}), 500

    if not download_url:
        return jsonify({"success": False, "error": "Unable to isolate direct MP4 source links for this video configuration."}), 400

    return jsonify({
        "success": True,
        "title": title,
        "download_url": download_url
    })
