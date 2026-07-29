function launchDownloadEngine(event) {
    const inputUrl = document.getElementById('videoLink').value;
    
    if (!inputUrl) {
        event.preventDefault();
        alert('Please paste a video link first!');
        return;
    }

    // Explicitly target a stable media extraction platform
    const targetBaseUrl = "https://save-tube.com";
    const finalDestination = targetBaseUrl + encodeURIComponent(inputUrl);

    // Update the link destination on the fly
    const downloadTrigger = document.getElementById('downloadTrigger');
    downloadTrigger.href = finalDestination;
}
