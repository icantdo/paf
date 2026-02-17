import streamlit as st
import time
import base64
import os

# ============================================================
# CONFIGURABLE VALUES — Change these for each friend!
# ============================================================

FRIEND_NAME = "Melih Paftie"

# Level 2 — Each challenge gives a Base64 fragment. Types: "text", "image", "audio"
OSINT_CHALLENGES = [
    {
        "type": "image",
        "file": "assets/image1.jpg",
        "question": "Bu kolye kim hediye etti İstanbulda kim hediye etti (discord ismi)",
        "answer": "ereningos",
        "fragment": "SGFwcH",
    },
    {
        "type": "text",
        "question": "İstanbul Maltepe'de hediye edilen yüzüğün rengi",
        "answer": "siyah",
        "fragment": "kgQmlyd",
    },
    {
        "type": "text",
        "question": "Esek",
        "answer": "Deniz",
        "fragment": "GhkYXkg",
    },
    {
        "type": "text",
        "question": "En iyi baba kimede",
        "answer": "Başaran",
        "fragment": "UGFm",
    },
    {
        "type": "audio",
        "file": "assets/audio1.mp3",
        "question": "Bu müziğin ismi",
        "answer": "coins",
        "fragment": "IQ==",
    },
]
# Fragments join to: "SGFwcHkgQmlydGhkYXkgUGFmIQ==" -> "Happy Birthday bro!"

DECODED_MESSAGE = "Happy Birthday Paf!"

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(page_title="SYSTEM BREACH", page_icon="\U0001f480", layout="wide")

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "level" not in st.session_state:
    st.session_state["level"] = "boot"
if "terminal_history" not in st.session_state:
    st.session_state["terminal_history"] = []
if "last_cmd" not in st.session_state:
    st.session_state["last_cmd"] = ""
if "failed" not in st.session_state:
    st.session_state["failed"] = False
if "osint_index" not in st.session_state:
    st.session_state["osint_index"] = 0
if "fragments" not in st.session_state:
    st.session_state["fragments"] = []
if "fragment_just_recovered" not in st.session_state:
    st.session_state["fragment_just_recovered"] = False
if "countdown_start" not in st.session_state:
    st.session_state["countdown_start"] = None  # Set when Level 1 begins
if "lockdown" not in st.session_state:
    st.session_state["lockdown"] = False

COUNTDOWN_SECONDS = 300  # 5 minutes

# ============================================================
# CSS INJECTION
# ============================================================

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');

    html, body, .stApp, .main, .block-container {
        background-color: #0E1117 !important;
        color: #00FF00 !important;
        font-family: 'Fira Code', 'Courier New', monospace !important;
    }

    #MainMenu, footer, header, .stDeployButton, [data-testid="stToolbar"] {
        display: none !important;
    }

    h1, h2, h3, h4, p, span, label, li,
    .stMarkdown, .stText, .stMarkdown p, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #00FF00 !important;
        font-family: 'Fira Code', monospace !important;
    }

    .stTextInput input {
        background-color: #0a0a0a !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
        font-family: 'Fira Code', monospace !important;
        caret-color: #00FF00 !important;
        border-radius: 0 !important;
    }

    .stTextInput input::placeholder {
        color: #005500 !important;
    }

    .stButton > button {
        background-color: transparent !important;
        color: #00FF00 !important;
        border: 1px solid #00FF00 !important;
        font-family: 'Fira Code', monospace !important;
        border-radius: 0 !important;
        transition: all 0.3s ease !important;
    }

    .stButton > button:hover {
        background-color: #00FF00 !important;
        color: #0E1117 !important;
        box-shadow: 0 0 20px #00FF00 !important;
    }

    .stExpander {
        border-color: #00FF00 !important;
    }

    .stExpander summary {
        color: #00FF00 !important;
        font-family: 'Fira Code', monospace !important;
        gap: 8px !important;
    }

    .stExpander summary span {
        overflow: visible !important;
        text-overflow: unset !important;
        white-space: normal !important;
    }

    .stExpander summary svg {
        flex-shrink: 0 !important;
    }

    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }

    @keyframes redflash {
        0% { background-color: #0E1117; }
        20% { background-color: #440000; }
        40% { background-color: #880000; }
        60% { background-color: #440000; }
        80% { background-color: #220000; }
        100% { background-color: #0E1117; }
    }

    @keyframes greenglow {
        0% { text-shadow: 0 0 5px #00FF00; }
        50% { text-shadow: 0 0 30px #00FF00, 0 0 60px #00FF00, 0 0 90px #00FF00; }
        100% { text-shadow: 0 0 5px #00FF00; }
    }

    @keyframes glitch {
        0% { transform: translate(0); }
        20% { transform: translate(-2px, 2px); }
        40% { transform: translate(2px, -2px); }
        60% { transform: translate(-1px, -1px); }
        80% { transform: translate(1px, 1px); }
        100% { transform: translate(0); }
    }

    .scanlines::after {
        content: '';
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        background: repeating-linear-gradient(
            0deg,
            rgba(0,0,0,0.1) 0px,
            rgba(0,0,0,0.1) 1px,
            transparent 1px,
            transparent 3px
        );
        pointer-events: none;
        z-index: 9999;
    }

    .cursor-blink {
        animation: blink 1s infinite;
        color: #00FF00;
    }

    .denied-flash {
        animation: redflash 0.8s ease-in-out;
    }

    .granted-glow {
        animation: greenglow 1.5s ease-in-out;
    }

    .glitch-text {
        animation: glitch 0.3s infinite;
    }
    </style>
    <div class="scanlines"></div>
    """, unsafe_allow_html=True)

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def img_to_base64(path):
    """Encode a local image file to base64 for inline HTML."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def advance_level(next_level):
    """Advance to the next level."""
    st.session_state["level"] = next_level
    st.session_state["failed"] = False

def show_access_denied():
    """Display ACCESS DENIED banner."""
    st.markdown("""
    <div class="denied-flash" style="text-align:center; padding:30px; border:2px solid #FF0000; margin:20px 0; background:#1a0000;">
        <h1 style="color:#FF0000 !important; font-size:48px; font-family:'Fira Code',monospace !important;
                    text-shadow: 0 0 20px #FF0000;">
            ACCESS DENIED
        </h1>
        <p style="color:#FF0000 !important;">Security breach attempt logged. Try again.</p>
    </div>
    """, unsafe_allow_html=True)

def show_access_granted():
    """Display ACCESS GRANTED banner."""
    st.markdown("""
    <div class="granted-glow" style="text-align:center; padding:30px; border:2px solid #00FF00; margin:20px 0; background:#001a00;">
        <h1 style="color:#00FF00 !important; font-size:48px; font-family:'Fira Code',monospace !important;
                    text-shadow: 0 0 30px #00FF00, 0 0 60px #00FF00;">
            ACCESS GRANTED
        </h1>
    </div>
    """, unsafe_allow_html=True)

def render_countdown():
    """Display a live countdown timer at the top of the screen using JS."""
    if st.session_state["countdown_start"] is None:
        return
    elapsed = time.time() - st.session_state["countdown_start"]
    remaining = max(0, COUNTDOWN_SECONDS - elapsed)

    if remaining <= 0 and not st.session_state["lockdown"]:
        st.session_state["lockdown"] = True
        st.rerun()
        return

    mins = int(remaining // 60)
    secs = int(remaining % 60)
    pct = remaining / COUNTDOWN_SECONDS * 100

    # Color shifts from green to yellow to red
    if remaining > 120:
        color = "#00FF00"
        bar_shadow = "0 0 10px #00FF00"
    elif remaining > 60:
        color = "#FFFF00"
        bar_shadow = "0 0 10px #FFFF00"
    else:
        color = "#FF0000"
        bar_shadow = "0 0 15px #FF0000, 0 0 30px #FF0000"

    pulse = ' animation: blink 0.5s infinite;' if remaining < 30 else ''

    st.markdown(f"""
    <div style="position:relative; padding:8px 15px; border:1px solid {color}; background:#0a0a0a;
                margin-bottom:15px; display:flex; align-items:center; gap:15px;">
        <span style="color:{color}; font-size:11px; white-space:nowrap;">SELF-DESTRUCT</span>
        <div style="flex:1; background:#111; height:6px; border-radius:3px; overflow:hidden;">
            <div style="background:{color}; height:6px; width:{pct:.1f}%; border-radius:3px;
                        box-shadow:{bar_shadow}; transition:width 1s linear;"></div>
        </div>
        <span style="color:{color}; font-size:18px; font-family:'Fira Code',monospace; letter-spacing:2px;
                      white-space:nowrap;{pulse}">
            {mins:02d}:{secs:02d}
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Auto-refresh every second using JS
    st.components.v1.html(f"""
    <script>
    setTimeout(function() {{
        // Find the Streamlit rerun mechanism
        const buttons = window.parent.document.querySelectorAll('button');
        // Trigger a soft rerun by dispatching a custom event
        const event = new Event('streamlit:forceRerun');
        window.parent.document.dispatchEvent(event);
        // Fallback: use Streamlit's internal rerun
        if (window.parent.streamlitRerun) window.parent.streamlitRerun();
    }}, 1000);
    </script>
    """, height=0)


def render_lockdown():
    """Display the dramatic SYSTEM LOCKDOWN screen with override button."""
    st.components.v1.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        body { background: #000; margin: 0; }

        @keyframes redPulse {
            0%, 100% { background: #0a0000; border-color: #FF0000; }
            50% { background: #1a0000; border-color: #FF4444; }
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            10% { transform: translateX(-5px); }
            20% { transform: translateX(5px); }
            30% { transform: translateX(-5px); }
            40% { transform: translateX(5px); }
            50% { transform: translateX(0); }
        }

        @keyframes textGlitch {
            0%, 100% { text-shadow: 0 0 20px #FF0000; }
            25% { text-shadow: -3px 0 #FF0000, 3px 0 #00FFFF; }
            50% { text-shadow: 3px 0 #FF0000, -3px 0 #00FFFF; }
            75% { text-shadow: 0 3px #FF0000, 0 -3px #00FFFF; }
        }

        .lockdown-container {
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            height: 100vh; background: #000;
            font-family: 'Fira Code', monospace;
            animation: redPulse 1s infinite;
            border: 3px solid #FF0000;
        }

        .lockdown-icon {
            font-size: 80px; margin-bottom: 20px;
            animation: shake 0.5s infinite;
        }

        .lockdown-title {
            color: #FF0000; font-size: 42px; font-weight: bold;
            animation: textGlitch 0.3s infinite;
            margin-bottom: 15px;
        }

        .lockdown-sub {
            color: #FF4444; font-size: 16px;
            text-align: center; line-height: 2;
        }

        .lockdown-code {
            color: #FF0000; font-size: 12px; opacity: 0.5;
            margin-top: 20px; font-family: monospace;
        }
    </style>
    <div class="lockdown-container">
        <div class="lockdown-icon">&#128274;</div>
        <div class="lockdown-title">SYSTEM LOCKDOWN</div>
        <div class="lockdown-sub">
            COUNTDOWN EXPIRED<br>
            ALL ACCESS POINTS SEALED<br>
            SECURITY PROTOCOL ENGAGED<br><br>
            <span style="color:#FF6600;">EMERGENCY OVERRIDE REQUIRED</span>
        </div>
        <div class="lockdown-code">
            ERR::0x8F2A // TIMEOUT_BREACH_DETECTED // AUTH_REVOKED
        </div>
    </div>
    """, height=500)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(">> EMERGENCY OVERRIDE <<", use_container_width=True, key="override_btn"):
            # Reset countdown and continue from current level
            st.session_state["lockdown"] = False
            st.session_state["countdown_start"] = time.time()
            st.rerun()


def render_fragment_collector():
    """Show the Base64 fragment collection progress at the top of Level 2."""
    total = len(OSINT_CHALLENGES)
    recovered = len(st.session_state["fragments"])

    fragments_html = ""
    for i in range(total):
        if i < recovered:
            frag = st.session_state["fragments"][i]
            fragments_html += f'<span style="color:#00FF00; background:#002200; padding:4px 8px; margin:2px; border:1px solid #00FF00; font-size:14px;">{frag}</span>'
        else:
            fragments_html += f'<span style="color:#333; background:#0a0a0a; padding:4px 8px; margin:2px; border:1px solid #333; font-size:14px;">{"?" * 8}</span>'

    st.markdown(f"""
    <div style="text-align:center; padding:15px; border:1px solid #00FF00; background:#0a0a0a; margin-bottom:20px;">
        <p style="color:#00FF00 !important; margin-bottom:10px; font-size:12px;">
            ENCRYPTED PAYLOAD FRAGMENTS [{recovered}/{total}]
        </p>
        <div style="display:flex; justify-content:center; flex-wrap:wrap; gap:4px;">
            {fragments_html}
        </div>
        <div style="margin-top:10px; background:#111; height:4px; border-radius:2px;">
            <div style="background:#00FF00; height:4px; width:{int(recovered/total*100)}%; border-radius:2px;
                        box-shadow: 0 0 10px #00FF00;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# BOOT SEQUENCE
# ============================================================

def render_boot():
    st.components.v1.html("""
    <style>
        body { margin: 0; overflow: hidden; background: #0E1117; }
        canvas { display: block; }
        .boot-text {
            position: absolute; bottom: 60px; left: 50%;
            transform: translateX(-50%);
            color: #00FF00; font-family: 'Courier New', monospace;
            font-size: 18px; text-align: center;
            text-shadow: 0 0 10px #00FF00;
        }
    </style>
    <canvas id="matrix"></canvas>
    <div class="boot-text">
        INITIALIZING SYSTEM BREACH...<br>
        <span style="font-size:12px; opacity:0.6;">Establishing secure connection</span>
    </div>
    <script>
    const canvas = document.getElementById('matrix');
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const fontSize = 14;
    const cols = Math.floor(canvas.width / fontSize);
    const drops = Array(cols).fill(1);
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲン0123456789ABCDEF';

    function draw() {
        ctx.fillStyle = 'rgba(14,17,23,0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = '#00FF00';
        ctx.font = fontSize + 'px monospace';
        for (let i = 0; i < drops.length; i++) {
            const ch = chars[Math.floor(Math.random() * chars.length)];
            ctx.fillStyle = Math.random() > 0.9 ? '#FFFFFF' : '#00FF00';
            ctx.fillText(ch, i * fontSize, drops[i] * fontSize);
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
            drops[i]++;
        }
    }
    setInterval(draw, 33);
    </script>
    """, height=600)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("[ PRESS ANY KEY TO CONTINUE ]", use_container_width=True, key="boot_btn"):
            advance_level("intro")
            st.rerun()

# ============================================================
# INTRO SCREEN
# ============================================================

def render_intro():
    st.components.v1.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        body {{ background: #0E1117; margin: 0; }}

        @keyframes flicker {{
            0%, 100% {{ opacity: 1; }}
            92% {{ opacity: 1; }}
            93% {{ opacity: 0.3; }}
            94% {{ opacity: 1; }}
            96% {{ opacity: 0.5; }}
            97% {{ opacity: 1; }}
        }}

        @keyframes typewriter {{
            from {{ width: 0; }}
            to {{ width: 100%; }}
        }}

        .warning-container {{
            text-align: center;
            padding: 40px 20px;
            font-family: 'Fira Code', monospace;
            animation: flicker 3s infinite;
        }}

        .warning-title {{
            color: #FF0000;
            font-size: 36px;
            font-weight: bold;
            text-shadow: 0 0 20px #FF0000, 0 0 40px #FF0000;
            margin-bottom: 30px;
        }}

        .warning-box {{
            display: inline-block;
            text-align: left;
            border: 1px solid #FF0000;
            padding: 25px 35px;
            background: rgba(255,0,0,0.05);
            color: #00FF00;
            font-size: 15px;
            line-height: 2;
            max-width: 600px;
        }}

        .highlight {{ color: #FF0000; font-weight: bold; }}
        .cyan {{ color: #00FFFF; }}
    </style>
    <div class="warning-container">
        <div class="warning-title">&#9888; SYSTEM WARNING &#9888;</div>
        <div class="warning-box">
            <span class="highlight">CRITICAL SECURITY ALERT</span><br>
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br><br>
            Target: <span class="highlight">{FRIEND_NAME}</span><br>
            Status: <span class="highlight">BIRTHDAY DATA ENCRYPTED</span><br>
            Threat Level: <span class="highlight">MAXIMUM</span><br><br>
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br><br>
            The encryption key is about to expire.<br>
            To recover the payload, you must bypass<br>
            <span class="cyan">3 SECURITY LAYERS</span>:<br><br>
            &nbsp;&nbsp;[1] <span class="cyan">Terminal Access</span><br>
            &nbsp;&nbsp;[2] <span class="cyan">Social Engineering</span><br>
            &nbsp;&nbsp;[3] <span class="cyan">Cryptographic Decryption</span><br><br>
            <span class="highlight">PROCEED WITH CAUTION.</span>
        </div>
    </div>
    """, height=750)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("\u25b6 INITIATE BREACH", use_container_width=True, key="intro_btn"):
            advance_level(1)
            st.rerun()

# ============================================================
# LEVEL 1 — TERMINAL ACCESS
# ============================================================

def render_level_1():
    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
        <span style="color:#00FFFF; font-size:12px;">SECURITY LAYER 1 OF 3</span>
    </div>
    <h2 style="text-align:center; color:#00FF00 !important; text-shadow: 0 0 10px #00FF00;">
        TERMINAL ACCESS
    </h2>
    <p style="text-align:center; color:#008800 !important; font-size:14px;">
        Gain root access to the system. A terminal awaits your commands.
    </p>
    """, unsafe_allow_html=True)

    # Build terminal output from history
    history = st.session_state["terminal_history"]
    terminal_lines = ""
    for entry in history:
        cmd_display = entry["cmd"].replace("<", "&lt;").replace(">", "&gt;")
        terminal_lines += f'<div><span style="color:#00FFFF;">root@breach</span>:<span style="color:#5555FF;">~</span>$ {cmd_display}</div>'
        if entry.get("output"):
            terminal_lines += f'<div style="color:#00CC00; margin-bottom:5px;">{entry["output"]}</div>'

    st.markdown(f"""
    <div style="background:#0a0a0a; padding:20px; border:1px solid #00FF00;
                font-family:'Fira Code',monospace; min-height:250px; max-height:400px;
                overflow-y:auto; font-size:14px; line-height:1.6;
                box-shadow: 0 0 15px rgba(0,255,0,0.1);">
        {terminal_lines}
        <div>
            <span style="color:#00FFFF;">root@breach</span>:<span style="color:#5555FF;">~</span>$ <span class="cursor-blink">_</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cmd = st.text_input("Command", key="terminal_input", placeholder="Type your command here...",
                        label_visibility="collapsed")

    if cmd and cmd.strip() != st.session_state["last_cmd"]:
        st.session_state["last_cmd"] = cmd.strip()
        cmd_lower = cmd.strip().lower()

        if cmd_lower == "ls":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": '<span style="color:#00FF00;">baslat.sh</span>&nbsp;&nbsp;&nbsp;'
                          '<span style="color:#888;">readme.txt</span>&nbsp;&nbsp;&nbsp;'
                          '<span style="color:#5555FF;">.secret/</span>'
            })
            st.rerun()
        elif cmd_lower in ("bash baslat.sh", "./baslat.sh", "sh baslat.sh"):
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": '<span style="color:#00FF00;">Executing baslat.sh...</span><br>'
                          '<span style="color:#00FF00;">&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608;&#9608; 100%</span><br>'
                          '<span style="color:#00FF00; font-weight:bold;">ACCESS GRANTED - Terminal layer bypassed.</span>'
            })
            st.session_state["last_cmd"] = ""
            advance_level(2)
            st.rerun()
        elif cmd_lower == "cat readme.txt":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": '<span style="color:#888;">NOTE: The system script is in this directory.</span><br>'
                          '<span style="color:#888;">HINT: Try listing files first, then execute the script.</span>'
            })
            st.rerun()
        elif cmd_lower == "ls -la" or cmd_lower == "ls -a":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": 'drwxr-xr-x  2 root root 4096 Feb 17 00:00 <span style="color:#5555FF;">.</span><br>'
                          'drwxr-xr-x  3 root root 4096 Feb 17 00:00 <span style="color:#5555FF;">..</span><br>'
                          '-rwxr-xr-x  1 root root  512 Feb 17 00:00 <span style="color:#00FF00;">baslat.sh</span><br>'
                          '-rw-r--r--  1 root root  128 Feb 17 00:00 readme.txt<br>'
                          'drwx------  2 root root 4096 Feb 17 00:00 <span style="color:#5555FF;">.secret/</span>'
            })
            st.rerun()
        elif cmd_lower == "cd .secret" or cmd_lower == "ls .secret":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": '<span style="color:#FF0000;">Permission denied: insufficient privileges</span>'
            })
            st.rerun()
        elif cmd_lower == "help":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": '<span style="color:#888;">Available commands: ls, cat, bash, cd, help</span><br>'
                          '<span style="color:#888;">TIP: Start by exploring what files are available.</span>'
            })
            st.rerun()
        elif cmd_lower == "pwd":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": '/root/breach'
            })
            st.rerun()
        elif cmd_lower == "whoami":
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": 'root'
            })
            st.rerun()
        else:
            cmd_safe = cmd.strip().replace("<", "&lt;").replace(">", "&gt;")
            st.session_state["terminal_history"].append({
                "cmd": cmd.strip(),
                "output": f'<span style="color:#FF0000;">bash: {cmd_safe}: command not found</span>'
            })
            st.rerun()

# ============================================================
# LEVEL 2 — OSINT (MULTI-CHALLENGE)
# ============================================================

def render_level_2():
    idx = st.session_state["osint_index"]
    total = len(OSINT_CHALLENGES)

    # Check if all challenges are done
    if idx >= total:
        advance_level(3)
        st.rerun()
        return

    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
        <span style="color:#00FFFF; font-size:12px;">SECURITY LAYER 2 OF 3</span>
    </div>
    <h2 style="text-align:center; color:#00FF00 !important; text-shadow: 0 0 10px #00FF00;">
        SOCIAL ENGINEERING
    </h2>
    <p style="text-align:center; color:#008800 !important; font-size:14px;">
        Reconstruct the encrypted memory fragments.
    </p>
    """, unsafe_allow_html=True)

    # Fragment collector
    render_fragment_collector()

    # Show fragment recovered animation
    if st.session_state["fragment_just_recovered"]:
        st.session_state["fragment_just_recovered"] = False
        last_frag = st.session_state["fragments"][-1] if st.session_state["fragments"] else ""
        st.components.v1.html(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
            @keyframes slideIn {{
                0% {{ transform: translateY(-30px); opacity: 0; }}
                50% {{ transform: translateY(5px); opacity: 1; }}
                100% {{ transform: translateY(0); opacity: 1; }}
            }}
            @keyframes glow {{
                0%, 100% {{ text-shadow: 0 0 10px #00FF00; }}
                50% {{ text-shadow: 0 0 30px #00FF00, 0 0 60px #00FF00; }}
            }}
            .recovered {{
                font-family: 'Fira Code', monospace;
                text-align: center; padding: 25px;
                background: #001a00; border: 1px solid #00FF00;
                animation: slideIn 0.5s ease-out;
            }}
            .recovered h2 {{
                color: #00FF00; animation: glow 1.5s infinite;
                font-size: 24px; margin-bottom: 10px;
            }}
            .recovered .frag {{
                color: #00FFFF; font-size: 20px; letter-spacing: 3px;
                margin-top: 10px;
            }}
        </style>
        <div class="recovered">
            <h2>DATA FRAGMENT RECOVERED</h2>
            <div class="frag">{last_frag}</div>
        </div>
        """, height=130)

    challenge = OSINT_CHALLENGES[idx]

    # Fragment label
    st.markdown(f"""
    <div style="text-align:center; padding:10px; margin:15px 0; border:1px dashed #00FF00; background:#0a0a0a;">
        <span style="color:#00FFFF; font-size:16px;">[ FRAGMENT {idx + 1} / {total} ]</span>
    </div>
    """, unsafe_allow_html=True)

    # Render based on challenge type
    if challenge["type"] == "image":
        render_image_challenge(challenge)
    elif challenge["type"] == "audio":
        render_audio_challenge(challenge)
    else:
        render_text_challenge(challenge)

    # Show access denied if failed
    if st.session_state["failed"]:
        show_access_denied()
        st.session_state["failed"] = False


def render_text_challenge(challenge):
    """Render a text-based OSINT challenge."""
    st.markdown(f"""
    <div style="border:1px solid #FF6600; padding:20px; background:#1a1000; margin:15px 0;">
        <p style="color:#FF6600 !important; font-size:12px; margin-bottom:10px;">INTEL REQUIRED</p>
        <p style="color:#00FF00 !important; font-size:16px;">
            {challenge["question"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    answer = st.text_input("Enter response:", key=f"osint_text_{st.session_state['osint_index']}",
                           placeholder="Type your answer...")

    if st.button("SUBMIT", key=f"osint_submit_{st.session_state['osint_index']}"):
        if answer.strip().lower() == challenge["answer"].strip().lower():
            st.session_state["fragments"].append(challenge["fragment"])
            st.session_state["osint_index"] += 1
            st.session_state["fragment_just_recovered"] = True
            st.rerun()
        else:
            st.session_state["failed"] = True
            st.rerun()


def render_image_challenge(challenge):
    """Render an image-based OSINT challenge."""
    st.markdown(f"""
    <div style="border:1px solid #FF6600; padding:20px; background:#1a1000; margin:15px 0;">
        <p style="color:#FF6600 !important; font-size:12px; margin-bottom:10px;">VISUAL INTELLIGENCE</p>
        <p style="color:#00FF00 !important; font-size:16px;">
            {challenge["question"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Show image with glitch/blur effect
    img_b64 = img_to_base64(challenge.get("file", ""))
    if img_b64:
        st.markdown(f"""
        <div style="text-align:center; margin:20px 0;">
            <div style="display:inline-block; border:2px solid #00FF00; padding:5px; background:#0a0a0a;">
                <img src="data:image/png;base64,{img_b64}"
                     style="max-width:400px; width:100%;
                            filter: blur(8px) hue-rotate(90deg) saturate(2);
                            transition: filter 1.5s ease;">
                <p style="color:#FF0000 !important; font-size:11px; margin-top:5px;">
                    CORRUPTED SURVEILLANCE FOOTAGE
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:40px; border:1px dashed #333; margin:20px 0;">
            <p style="color:#555 !important; font-size:12px;">
                [IMAGE FILE NOT FOUND — Add image to assets/ folder]
            </p>
        </div>
        """, unsafe_allow_html=True)

    answer = st.text_input("Identify the target:", key=f"osint_img_{st.session_state['osint_index']}",
                           placeholder="Type your answer...")

    if st.button("ANALYZE", key=f"osint_img_submit_{st.session_state['osint_index']}"):
        if answer.strip().lower() == challenge["answer"].strip().lower():
            st.session_state["fragments"].append(challenge["fragment"])
            st.session_state["osint_index"] += 1
            st.session_state["fragment_just_recovered"] = True
            st.rerun()
        else:
            st.session_state["failed"] = True
            st.rerun()


def render_audio_challenge(challenge):
    """Render an audio-based OSINT challenge."""
    st.markdown(f"""
    <div style="border:1px solid #FF6600; padding:20px; background:#1a1000; margin:15px 0;">
        <p style="color:#FF6600 !important; font-size:12px; margin-bottom:10px;">SIGNAL INTERCEPTION</p>
        <p style="color:#00FF00 !important; font-size:16px;">
            {challenge["question"]}
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Waveform animation + audio player
    st.components.v1.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        .wave-container {
            display: flex; justify-content: center; align-items: center;
            gap: 3px; padding: 20px; background: #0a0a0a;
            border: 1px solid #00FF00; margin: 10px 0;
        }
        .wave-bar {
            width: 4px; background: #00FF00; border-radius: 2px;
            animation: wave 1.2s ease-in-out infinite;
        }
        @keyframes wave {
            0%, 100% { height: 10px; }
            50% { height: 40px; }
        }
        .wave-label {
            text-align: center; color: #00FFFF; font-family: 'Fira Code', monospace;
            font-size: 12px; margin-top: 8px;
        }
    </style>
    <div class="wave-container">
    """ + "".join(
        f'<div class="wave-bar" style="animation-delay:{i*0.1}s;"></div>'
        for i in range(30)
    ) + """
    </div>
    <div class="wave-label">INTERCEPTED TRANSMISSION — PLAYING...</div>
    """, height=120)

    # Play audio if file exists
    audio_file = challenge.get("file", "")
    if os.path.exists(audio_file):
        st.audio(audio_file)
    else:
        st.markdown("""
        <p style="color:#555 !important; font-size:12px; text-align:center;">
            [AUDIO FILE NOT FOUND — Add audio to assets/ folder]
        </p>
        """, unsafe_allow_html=True)

    answer = st.text_input("Decode transmission:", key=f"osint_audio_{st.session_state['osint_index']}",
                           placeholder="Type your answer...")

    if st.button("DECRYPT", key=f"osint_audio_submit_{st.session_state['osint_index']}"):
        if answer.strip().lower() == challenge["answer"].strip().lower():
            st.session_state["fragments"].append(challenge["fragment"])
            st.session_state["osint_index"] += 1
            st.session_state["fragment_just_recovered"] = True
            st.rerun()
        else:
            st.session_state["failed"] = True
            st.rerun()

# ============================================================
# LEVEL 3 — CRYPTOLOGY
# ============================================================

def render_level_3():
    full_base64 = "".join(st.session_state["fragments"])

    st.markdown("""
    <div style="text-align:center; margin-bottom:10px;">
        <span style="color:#00FFFF; font-size:12px;">SECURITY LAYER 3 OF 3</span>
    </div>
    <h2 style="text-align:center; color:#00FF00 !important; text-shadow: 0 0 10px #00FF00;">
        CRYPTOGRAPHIC DECRYPTION
    </h2>
    <p style="text-align:center; color:#008800 !important; font-size:14px;">
        All fragments recovered. Assemble and decrypt the payload.
    </p>
    """, unsafe_allow_html=True)

    # Fragment assembly animation
    fragments_display = " + ".join([f'<span style="color:#00FFFF;">{f}</span>' for f in st.session_state["fragments"]])
    st.markdown(f"""
    <div style="text-align:center; padding:15px; border:1px solid #00FF00; background:#0a0a0a; margin:15px 0;">
        <p style="color:#888 !important; font-size:12px; margin-bottom:10px;">ASSEMBLED FRAGMENTS:</p>
        <div style="font-size:13px; margin-bottom:15px;">{fragments_display}</div>
        <p style="color:#888 !important; font-size:12px;">COMBINED PAYLOAD:</p>
    </div>
    """, unsafe_allow_html=True)

    # Show the full Base64 string prominently
    st.markdown(f"""
    <div style="text-align:center; padding:25px; border:2px solid #00FF00; background:#001100; margin:15px 0;
                box-shadow: 0 0 20px rgba(0,255,0,0.2);">
        <p style="color:#00FF00 !important; font-size:12px; margin-bottom:10px;">ENCRYPTED PAYLOAD (Base64)</p>
        <h2 style="color:#00FF00 !important; letter-spacing:3px; word-break:break-all; font-size:22px;
                    text-shadow: 0 0 10px #00FF00;">
            {full_base64}
        </h2>
    </div>
    """, unsafe_allow_html=True)

    answer = st.text_input("Enter decoded message:", key="crypto_answer",
                           placeholder="Decrypt the payload...")

    if st.button("DECRYPT PAYLOAD", key="crypto_submit"):
        if answer.strip().lower() == DECODED_MESSAGE.strip().lower():
            advance_level("finale_dark")
            st.rerun()
        else:
            st.session_state["failed"] = True
            st.rerun()

    if st.session_state["failed"]:
        show_access_denied()
        st.session_state["failed"] = False

# ============================================================
# FINALE — DARK SCREEN
# ============================================================

def render_finale_dark():
    st.components.v1.html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        body { background: #000; margin: 0; }
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        @keyframes progress {
            0% { width: 0%; }
            100% { width: 100%; }
        }
        .dark-container {
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            height: 100vh; background: #000;
            font-family: 'Fira Code', monospace;
        }
        .upload-text {
            color: #00FF00; font-size: 22px;
            animation: blink 0.8s infinite;
            margin-bottom: 20px;
        }
        .progress-bar {
            width: 300px; height: 6px;
            background: #111; border: 1px solid #00FF00;
            border-radius: 3px; overflow: hidden;
        }
        .progress-fill {
            height: 100%; background: #00FF00;
            animation: progress 3s ease-in-out forwards;
            box-shadow: 0 0 10px #00FF00;
        }
    </style>
    <div class="dark-container">
        <div class="upload-text">UPLOADING PAYLOAD...</div>
        <div class="progress-bar"><div class="progress-fill"></div></div>
    </div>
    """, height=600)

    time.sleep(4)
    advance_level("finale")
    st.rerun()

# ============================================================
# FINALE — CELEBRATION
# ============================================================

def render_finale():
    st.balloons()
    st.snow()

    # ASCII art + message
    st.components.v1.html(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;700&display=swap');
        body {{ background: #0E1117; margin: 0; }}

        @keyframes fadeInUp {{
            0% {{ transform: translateY(40px); opacity: 0; }}
            100% {{ transform: translateY(0); opacity: 1; }}
        }}

        @keyframes rainbow {{
            0% {{ color: #FF0000; text-shadow: 0 0 20px #FF0000; }}
            16% {{ color: #FF8800; text-shadow: 0 0 20px #FF8800; }}
            33% {{ color: #FFFF00; text-shadow: 0 0 20px #FFFF00; }}
            50% {{ color: #00FF00; text-shadow: 0 0 20px #00FF00; }}
            66% {{ color: #0088FF; text-shadow: 0 0 20px #0088FF; }}
            83% {{ color: #FF00FF; text-shadow: 0 0 20px #FF00FF; }}
            100% {{ color: #FF0000; text-shadow: 0 0 20px #FF0000; }}
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); }}
            50% {{ transform: scale(1.05); }}
        }}

        .finale-container {{
            text-align: center; padding: 30px;
            font-family: 'Fira Code', monospace;
        }}

        .ascii-art {{
            color: #FFD700; font-size: 10px; line-height: 1.1;
            white-space: pre; display: inline-block;
            animation: fadeInUp 1s ease-out;
            text-shadow: 0 0 10px #FFD700;
        }}

        .main-title {{
            font-size: 42px; font-weight: bold;
            animation: rainbow 3s infinite, pulse 2s infinite;
            margin: 25px 0;
        }}

        .sub-message {{
            color: #00FF00; font-size: 18px; line-height: 2;
            animation: fadeInUp 1.5s ease-out;
        }}

        .name {{
            color: #FFD700; font-size: 28px; font-weight: bold;
            text-shadow: 0 0 20px #FFD700;
            animation: fadeInUp 2s ease-out;
        }}
    </style>
    <div class="finale-container">
        <pre class="ascii-art">
 ██▓▓██  ██    ██  ██▓▓██       ██   ██  ██▓▓██
   ██     ██  ██     ██         ██  ██     ██
   ██      ████      ██         █████      ██
   ██       ██       ██         ██  ██     ██
 ██▓▓██    ██      ██▓▓██      ██   ██  ██▓▓██

 ████▓  ████▓  ████  ████▓  ██  ██ ██  ██
 ██  ██ ██  ██ ██    ██  ██ ██  ██ ███ ██
 ██  ██ ██  ██ ██ ▓▓ ██  ██ ██  ██ ██████
 ██  ██ ██  ██ ██  ██ ██  ██ ██  ██ ██ ███
 ████▓  ████▓  ████  ████▓  ████▓  ██  ██
        </pre>

        <div class="main-title">
            &#127874; iYi Ki DOGDUN! &#127874;
        </div>

        <div class="name">{FRIEND_NAME}</div>

        <div class="sub-message">
            <br>
            &#9608; All security layers bypassed.<br>
            &#9608; Payload successfully uploaded.<br>
            &#9608; Birthday protocol activated.<br>
            <br>
            &#127873; Dogum gunun kutlu olsun dostum! &#127873;
        </div>
    </div>
    """, height=650)

    # Confetti canvas animation
    st.components.v1.html("""
    <canvas id="confetti" style="position:fixed;top:0;left:0;width:100vw;height:100vh;pointer-events:none;z-index:99998;"></canvas>
    <script>
    const cvs = document.getElementById('confetti');
    const ctx = cvs.getContext('2d');
    cvs.width = window.innerWidth;
    cvs.height = window.innerHeight;
    const colors = ['#FFD700','#FF6600','#00FF00','#FF00FF','#00FFFF','#FF0000','#FFFFFF'];
    const pieces = Array.from({length:200}, () => ({
        x: Math.random()*cvs.width,
        y: Math.random()*cvs.height - cvs.height,
        w: Math.random()*8+4,
        h: Math.random()*6+2,
        color: colors[Math.floor(Math.random()*colors.length)],
        vy: Math.random()*3+1.5,
        vx: Math.random()*2-1,
        rot: Math.random()*360,
        rotSpeed: Math.random()*6-3,
    }));
    function draw() {
        ctx.clearRect(0,0,cvs.width,cvs.height);
        pieces.forEach(p => {
            ctx.save();
            ctx.translate(p.x + p.w/2, p.y + p.h/2);
            ctx.rotate(p.rot * Math.PI/180);
            ctx.fillStyle = p.color;
            ctx.fillRect(-p.w/2, -p.h/2, p.w, p.h);
            ctx.restore();
            p.y += p.vy;
            p.x += p.vx;
            p.rot += p.rotSpeed;
            if (p.y > cvs.height) { p.y = -20; p.x = Math.random()*cvs.width; }
        });
        requestAnimationFrame(draw);
    }
    draw();
    </script>
    """, height=0)

    # Optional QR code
    qr_path = "assets/qr_code.png"
    if os.path.exists(qr_path):
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center; padding:20px;">
            <p style="color:#FFD700 !important; font-size:16px;">
                &#127873; Hediyeni bulmak icin QR kodu tara:
            </p>
        </div>
        """, unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.image(qr_path, width=200)

# ============================================================
# MAIN ROUTING
# ============================================================

inject_css()

level = st.session_state["level"]

# Check for lockdown state
if st.session_state["lockdown"] and level in (1, 2, 3):
    render_lockdown()
else:
    # Start countdown when entering Level 1 for the first time
    if level == 1 and st.session_state["countdown_start"] is None:
        st.session_state["countdown_start"] = time.time()

    # Show countdown on gameplay levels
    if level in (1, 2, 3):
        render_countdown()

    if level == "boot":
        render_boot()
    elif level == "intro":
        render_intro()
    elif level == 1:
        render_level_1()
    elif level == 2:
        render_level_2()
    elif level == 3:
        render_level_3()
    elif level == "finale_dark":
        render_finale_dark()
    elif level == "finale":
        render_finale()
