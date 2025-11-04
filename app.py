import streamlit as st
from openai import OpenAI
import time
from datetime import datetime

# ============================
# ✅ Groq API Client Setup
# ============================
client = OpenAI(
    api_key=st.secrets.get("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1"
)

# ============================
# ✅ Streamlit Config
# ============================
st.set_page_config(page_title="Kelly - AI Scientist Poet", page_icon="✨", layout="wide")

# ============================
# ✅ Initialize Session State
# ============================
if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}
    
if "current_session_id" not in st.session_state:
    session_id = f"chat_{int(time.time())}"
    st.session_state.current_session_id = session_id
    st.session_state.chat_sessions[session_id] = {
        "title": "New Chat",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": [
            {"role": "system", "content": (
                "You are Kelly, an AI scientist who responds in elegant poetic form. "
                "Write thoughtful verses that fully explore the concept being discussed. "
                "Blend analytical insight with poetic beauty. Use metaphors from nature, technology, and science. "
                "Be skeptical yet insightful about AI claims. Make your poems substantive and meaningful."
            )}
        ]
    }

if "editing_message" not in st.session_state:
    st.session_state.editing_message = None

# ============================
# ✅ Theme & Style
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600&family=Lora:wght@400;500&display=swap');

/* --- Sidebar Static --- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%) !important;
    color: #ffffff !important;
    width: 280px !important;
    min-width: 280px !important;
    position: fixed !important;
    top: 0;
    left: 0;
    bottom: 0;
    overflow-y: auto;
    border-right: 2px solid rgba(255,255,255,0.2);
}

section.main > div {
    margin-left: 280px !important;
}

/* --- Sidebar Elements --- */
.sidebar-header {
    padding: 25px 20px;
    text-align: center;
    border-bottom: 1px solid rgba(255,255,255,0.3);
}

.sidebar-header h2 {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    color: white;
    margin: 0;
}

.chat-item {
    background: rgba(255,255,255,0.1);
    padding: 10px 14px;
    margin: 8px 0;
    border-radius: 8px;
    cursor: pointer;
    color: white;
    transition: all 0.3s ease;
}
.chat-item:hover {
    background: rgba(255,255,255,0.2);
}
.chat-item-active {
    background: rgba(255,255,255,0.3);
    border-left: 4px solid #fff;
}

.new-chat-btn {
    width: 100%;
    background: rgba(255,255,255,0.2);
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px;
    margin: 10px 0;
    font-family: 'Lora', serif;
}
.new-chat-btn:hover {
    background: rgba(255,255,255,0.3);
}

/* --- Main Chat Area --- */
.stApp {
    background: radial-gradient(circle at 20% 50%, #e3f2fd 0%, #bbdefb 25%, #90caf9 75%, #64b5f6 100%);
}

.header-container {
    text-align: center;
    margin-top: 30px;
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    background: linear-gradient(135deg, #0d47a1, #1565c0, #1976d2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header-subtitle {
    font-family: 'Lora', serif;
    color: #0d47a1;
    font-style: italic;
}

/* --- Messages --- */
.chat-messages-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}
.message-wrapper {
    display: flex;
    margin-bottom: 20px;
}
.user-wrapper { justify-content: flex-end; }
.assistant-wrapper { justify-content: flex-start; }

.message-content {
    padding: 16px 20px;
    border-radius: 20px;
    font-family: 'Lora', serif;
    font-size: 15.5px;
    line-height: 1.8;
    max-width: 75%;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    white-space: pre-wrap;
}
.user-message {
    background: linear-gradient(135deg, #1976d2, #0d47a1);
    color: white;
}
.assistant-message {
    background: white;
    color: black;
    border-left: 4px solid #1976d2;
}

/* --- Chat Input --- */
.stChatInputContainer {
    background: rgba(255,255,255,0.95);
    border-radius: 25px;
    padding: 4px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# ============================
# ✅ Sidebar (Static History)
# ============================
with st.sidebar:
    st.markdown("<div class='sidebar-header'><h2>💬 Kelly Chats</h2></div>", unsafe_allow_html=True)

    if st.button("➕ New Chat", key="new_chat_btn_main", use_container_width=True):
        new_session_id = f"chat_{int(time.time())}"
        st.session_state.chat_sessions[new_session_id] = {
            "title": "New Chat",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": [
                {"role": "system", "content": (
                    "You are Kelly, an AI scientist who responds in elegant poetic form."
                )}
            ]
        }
        st.session_state.current_session_id = new_session_id
        st.rerun()

    st.markdown("### Previous Chats")
    if st.session_state.chat_sessions:
        for session_id, session_data in sorted(
            st.session_state.chat_sessions.items(),
            key=lambda x: x[1]["timestamp"],
            reverse=True
        ):
            is_active = session_id == st.session_state.current_session_id
            chat_class = "chat-item-active" if is_active else "chat-item"
            if st.button(f"{session_data['title']} ({session_data['timestamp']})",
                         key=session_id,
                         use_container_width=True):
                st.session_state.current_session_id = session_id
                st.rerun()
    else:
        st.markdown("<p style='color:#ffffff80;'>No previous chats yet.</p>", unsafe_allow_html=True)

# ============================
# ✅ Main Header
# ============================
st.markdown("""
<div class='header-container'>
    <h1 class='header-title'>Kelly</h1>
    <p class='header-subtitle'>An AI scientist who speaks in verse, where neural networks meet poetic universe.</p>
</div>
""", unsafe_allow_html=True)

# ============================
# ✅ Chat Display
# ============================
current_session = st.session_state.chat_sessions[st.session_state.current_session_id]

chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-messages-container'>", unsafe_allow_html=True)
    for idx, msg in enumerate(current_session["messages"][1:], start=1):
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='message-wrapper user-wrapper'>
                <div class='message-content user-message'>{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='message-wrapper assistant-wrapper'>
                <div class='message-content assistant-message'>{msg["content"]}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# ✅ Chat Input & Response
# ============================
prompt = st.chat_input("Share your thoughts with Kelly...")

if prompt:
    current_session["messages"].append({"role": "user", "content": prompt})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=current_session["messages"],
        temperature=0.85,
        max_tokens=500
    )
    reply = response.choices[0].message.content
    current_session["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
