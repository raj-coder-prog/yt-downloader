async function processMediaLink() {
    const inputUrl = document.getElementById('videoLink').value;
    if (!inputUrl) {
        alert('Please paste a working URL link first!');
        return;
    }

    const resultView = document.getElementById('resultView');
    const videoStatusTitle = document.getElementById('videoStatusTitle');
    const nativeSaveBtn = document.getElementById('nativeSaveBtn');
    
    // Reset UI to processing mode
    videoStatusTitle.innerText = "Connecting to unblocked stream node...";
    resultView.style.display = 'block';
    nativeSaveBtn.style.display = 'none';

    try {
        // We route the extract query through a robust cross-origin bypass engine
        const proxyGateway = "https://allorigins.win";
        const targetExtractor = "https://cobalt.tools";

        const response = await fetch(proxyGateway + encodeURIComponent(targetExtractor), {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                url: inputUrl,
                vQuality: "480", // Optimized 480p format ensures instant extraction on mobile pipelines
                isAudioOnly: false
            })
        });

        const packageData = await response.json();
        // Parse the encoded payload body out of the bridge server response container
        const cleanPayload = JSON.parse(packageData.contents);

        if (cleanPayload && cleanPayload.url) {
            videoStatusTitle.innerText = "Video Decoded Successfully!";
            
            // Inject the raw direct MP4 streaming file URL straight into our local button asset
            nativeSaveBtn.href = cleanPayload.url;
            
            // Instructs your phone browser to save the item directly rather than launching a window
            nativeSaveBtn.setAttribute('download', 'video.mp4');
            nativeSaveBtn.style.display = 'block';
        } else {
            // Drop directly into a clean automatic mirror stream proxy layout if endpoint is crowded
            videoStatusTitle.innerText = "Port congested. Trying mirror pipeline node...";
            executeFallbackStream(inputUrl);
        }

    } catch (err) {
         executeFallbackStream(inputUrl);
    }
}

async function executeFallbackStream(videoLinkUrl) {
    const videoStatusTitle = document.getElementById('videoStatusTitle');
    const nativeSaveBtn = document.getElementById('nativeSaveBtn');

    try {
        const fallbackEngineUrl = "https://devextent.com" + encodeURIComponent(videoLinkUrl);
        const response = await fetch(fallbackEngineUrl);
        const data = await response.json();

        if (data && data.download_url) {
            videoStatusTitle.innerText = data.title || "Media File Decoded!";
            nativeSaveBtn.href = data.download_url;
            nativeSaveBtn.setAttribute('download', 'video.mp4');
            nativeSaveBtn.style.display = 'block';
        } else {
            videoStatusTitle.innerText = "Conversion nodes currently throttled. Try a different video link.";
        }
    } catch(e) {
        videoStatusTitle.innerText = "All native web extraction systems are busy. Try again shortly.";
    }
}
