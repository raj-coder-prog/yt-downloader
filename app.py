import os
from flask import Flask, redirect

app = Flask(__name__)

@app.route('/')
def home():
    # Instantly routes your browser to a working download framework 
    # This bypasses all Render server IP restrictions and iframe security errors
    return redirect("https://savefrom.net", code=302)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
