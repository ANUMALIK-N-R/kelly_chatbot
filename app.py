import streamlit as st
from openai import OpenAI
from datetime import datetime
import time

# ======================
# ✅ Streamlit Page Config
# ======================
st.set_page_config(
    page_title="Kelly - The AI Scientist Poet",
    page_icon="✨",
    layout="wide"
)

# ======================
# ✅ Groq API Client
# ======================
client = OpenAI(
    api_key=st.secrets.get("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1"
)

# ======================
# ✅ Session State Setup
# ======================
if "chats" not in st.session_state:
    st.session_state.chats = {}

if "active_chat" not in st.session_state:
    chat_id = str(int(time.time()))
    st.session_state.active_chat = chat_id
    st.session_state.chats[chat_id] = {
        "title": "New Chat",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Kelly, an AI scientist who replies only in poetic form — "
                    "skeptical, analytical, and evidence-based. Every response should "
                    "be a professional poem questioning AI claims and offering thoughtful, "
                    "practical insight backed by reasoning."
                )
            }
        ]
    }

# ======================
# ✅ Sidebar - Chat History
# ======================
with st.sidebar:
    st.markdown("### 💬 Chat History")

    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(int(time.time()))
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are Kelly, an AI scientist who replies only in poetic form — "
                        "skeptical, analytical, and evidence-based."
                    )
                }
            ]
        }
        st.session_state.active_chat = new_id
        st.rerun()

    for cid, chat_data in sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1]["timestamp"],
        reverse=True
    ):
        label = f"{chat_data['title']} ({chat_data['timestamp']})"
        if st.button(label, key=cid, use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

# ======================
# ✅ Get Current Chat
# ======================
current_chat = st.session_state.chats[st.session_state.active_chat]

# ======================
# ✅ Custom CSS Styling
# ======================
st.markdown("""
<style>
    body {
        background-color: #e3f2fd;
    }
    .stApp {
        background-color: #e3f2fd;
    }

    h2.kelly-title {
        text-align: center;
        color: #0d47a1;
        font-weight: 800;
        font-size: 2.5rem;
        letter-spacing: 1px;
        margin-top: 10px;
        margin-bottom: 5px;
        font-family: 'Playfair Display', serif;
    }

    .subtitle {
        text-align: center;
        font-size: 15px;
        font-style: italic;
        color: #1565c0;
        margin-bottom: 25px;
    }

    .chat-container {
        background-color: #bbdefb;
        padding: 30px 20px;
        border-radius: 16px;
        max-width: 950px;
        margin: 0 auto;
        box-shadow: 0 4px 12px rgba(13, 71, 161, 0.2);
    }

    .chat-message-user {
        background-color: #1976d2;
        color: #ffffff;
        padding: 12px 18px;
        border-radius: 16px;
        max-width: 80%;
        margin-left: auto;
        margin-right: 8px;
        margin-top: 20px;
        line-height: 1.6;
    }

    .chat-message-assistant {
        background-color: #ffffff;
        color: #0d47a1;
        padding: 12px 18px;
        border-radius: 16px;
        max-width: 80%;
        margin-right: auto;
        margin-left: 8px;
        border: 1px solid #bbdefb;
        line-height: 1.7;
        margin-top: 20px;
    }

    .copy-btn {
        border: 1px solid #90caf9;
        background-color: #e3f2fd;
        color: #0d47a1;
        font-size: 12px;
        border-radius: 8px;
        padding: 3px 8px;
        cursor: pointer;
        margin-top: 5px;
        margin-left: 8px;
        transition: all 0.2s ease;
    }

    .copy-btn:hover {
        background-color: #bbdefb;
    }

    .stChatInput {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# ✅ Header
# ======================
st.markdown("<h2 class='kelly-title'>Kelly</h2>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The AI Scientist who speaks in skeptical verse</p>", unsafe_allow_html=True)

# ======================
# ✅ Chat Display
# ======================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for i, msg in enumerate(current_chat["messages"][1:], start=1):
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-message-user'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-message-assistant'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <button class='copy-btn' onclick="navigator.clipboard.writeText(`{msg['content'].replace('`','\\`')}`)">
                📋 Copy
            </button>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ======================
# ✅ Chat Input
# ======================
prompt = st.chat_input("Speak to Kelly...")

if prompt:
    # Add user message
    current_chat["messages"].append({"role": "user", "content": prompt})

    # Generate AI poetic response
    with st.spinner("Kelly is composing thoughtful verse..."):
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=current_chat["messages"],
            temperature=0.8,
            max_tokens=400
        )

        reply = response.choices[0].message.content

        current_chat["messages"].append({"role": "assistant", "content": reply})
        current_chat["title"] = prompt[:30] + "..." if len(prompt) > 30 else prompt

    st.rerun()
