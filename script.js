async function sendLinkToBackend() {
    const inputUrl = document.getElementById('videoLink').value;
    if (!inputUrl) {
        alert('Please paste a working URL link first!');
        return;
    }

    const resultView = document.getElementById('resultView');
    const videoTitle = document.getElementById('videoTitle');
    const downloadActionBtn = document.getElementById('downloadActionBtn');
    
    // 🎨 Update the on-screen text instructions
    videoTitle.innerText = "Link processed! Click the button below:";
    resultView.style.display = 'block';

    // 🔗 Format the clean destination link string path
    const directPortalUrl = "https://save-tube.com" + encodeURIComponent(inputUrl);
    
    // ⚡ THE FIX: Assign the raw text address to the link. 
    // We do NOT add any script-based click listeners here.
    downloadActionBtn.href = directPortalUrl;
}
