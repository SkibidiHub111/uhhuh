from flask import Flask, Response, render_template_string
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template_string("""
    <html>
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>No. 1 HUB - Not Authorized</title>
    <style>
    body{margin:0;height:100vh;display:flex;align-items:center;justify-content:center;flex-direction:column;
    background:#0e0e17;color:#fff;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto;text-align:center;}
    .logo{font-size:22px;letter-spacing:1px;color:#aaa;text-transform:uppercase;margin-bottom:12px;}
    .card{padding:40px 50px;border-radius:20px;background:rgba(255,255,255,0.04);box-shadow:0 8px 30px rgba(0,0,0,0.6);}
    span{font-size:26px;margin:0 6px;}
    p{font-size:24px;margin:10px 0 0;}
    .small{color:#999;font-size:18px;margin-top:12px;}
    </style>
    </head>
    <body>
    <div class="card">
    <div class="logo">No. 1 HUB</div>
    <div><span>⛔</span><strong>Not Authorized</strong><span>⛔</span></div>
    <p>You are not allowed to view these files.</p>
    <p class="small">Close this page & proceed.</p>
    </div>
    </body>
    </html>
    """)

@app.route("/raw.lua")
def lua():
    url = "https://raw.githubusercontent.com/SkibidiHub111/Ghoul/refs/heads/main/Ghoul"
    return Response(requests.get(url).text, mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
