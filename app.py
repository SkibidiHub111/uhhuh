from flask import Flask, Response
import requests

app = Flask(__name__)

@app.route('/')
def lua_script():
    url = "https://raw.githubusercontent.com/SkibidiHub111/Ghoul/refs/heads/main/Ghoul"
    response = requests.get(url)
    if response.status_code == 200:
        lua_code = response.text
    else:
        lua_code = "Error: Không thể tải file Lua từ URL"
    return Response(lua_code, mimetype='text/plain')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
