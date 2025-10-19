from flask import Flask, Response, render_template_string, request, redirect
import requests, re, time
from collections import deque

app = Flask(__name__)

RAW_LUA_URL = "https://raw.githubusercontent.com/SkibidiHub111/Ghoul/refs/heads/main/Ghoul"

WINDOW = 60
MAX_PER_WINDOW = 15
BLOCK_TIME = 300
visitors, blocked = {}, {}

def is_blocked(ip):
    t = blocked.get(ip)
    if t and time.time() < t:
        return True
    if t and time.time() >= t:
        del blocked[ip]
    return False

def record(ip):
    now = time.time()
    dq = visitors.get(ip)
    if not dq:
        dq = deque()
        visitors[ip] = dq
    while dq and dq[0] < now - WINDOW:
        dq.popleft()
    dq.append(now)
    if len(dq) > MAX_PER_WINDOW:
        blocked[ip] = now + BLOCK_TIME
        visitors.pop(ip, None)
        return False
    return True

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>No. 1 HUB - Not Authorized</title>
<style>
body{margin:0;padding:0;height:100vh;display:flex;align-items:center;justify-content:center;flex-direction:column;
background:#0e0e17;color:#fff;font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto;font-weight:500;text-align:center;}
h1{font-size:50px;margin:0;}
p{font-size:24px;margin:10px 0 0;}
span{font-size:26px;margin:0 6px;}
.logo{font-size:22px;letter-spacing:1px;color:#aaa;text-transform:uppercase;margin-bottom:12px;}
.card{padding:40px 50px;border-radius:20px;background:rgba(255,255,255,0.04);box-shadow:0 8px 30px rgba(0,0,0,0.6);}
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
"""

@app.route("/")
def index():
    ip = request.remote_addr or "unknown"
    if is_blocked(ip):
        return Response("Too many requests", status=429)
    if not record(ip):
        return Response("Too many requests", status=429)
    user_agent = (request.headers.get("User-Agent") or "").lower()
    if "mozilla" not in user_agent:
        return redirect("/raw.lua")
    return render_template_string(HTML)

@app.route("/raw.lua")
def raw():
    ip = request.remote_addr or "unknown"
    if is_blocked(ip):
        return Response("Too many requests", status=429)
    if not record(ip):
        return Response("Too many requests", status=429)
    try:
        r = requests.get(RAW_LUA_URL, timeout=8)
        if r.status_code != 200:
            return Response("Error tải Lua", status=502)
        txt = r.text
        txt = re.sub(r"--[^\n]*", "", txt)
        txt = re.sub(r"--\[\[[\s\S]*?\]\]", "", txt)
        txt = "\n".join(x for x in txt.splitlines() if x.strip() != "")
        return Response(txt, mimetype="text/plain", headers={"Access-Control-Allow-Origin": "*"})
    except Exception:
        return Response("Error tải file", status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
