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

    # New Chat Button
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

    # Display Chat History
    for cid, chat_data in sorted(
        st.session_state.chats.items(),
        key=lambda x: x[1]["timestamp"],
        reverse=True
    ):
        label = f"💭 {chat_data['title']} ({chat_data['timestamp']})"
        if st.button(label, key=cid, use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

# ======================
# ✅ Get Current Chat
# ======================
current_chat = st.session_state.chats[st.session_state.active_chat]

# ======================
# ✅ Custom CSS Styling (ChatGPT style)
# ======================
st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
    }
    .stApp {
        background-color: #f9fafb;
    }
    .stChatMessage {
        margin-bottom: 1rem;
    }
    .chat-message-user {
        background-color: #dcf8c6;
        color: #000;
        padding: 10px 16px;
        border-radius: 12px;
        max-width: 80%;
        margin-left: auto;
        margin-right: 8px;
    }
    .chat-message-assistant {
        background-color: #ffffff;
        color: #000;
        padding: 10px 16px;
        border-radius: 12px;
        max-width: 80%;
        margin-right: auto;
        margin-left: 8px;
        border: 1px solid #e0e0e0;
    }
    .copy-btn {
        border: 1px solid #ccc;
        background-color: transparent;
        color: #333;
        font-size: 12px;
        border-radius: 6px;
        padding: 3px 8px;
        cursor: pointer;
        margin-top: 4px;
        transition: all 0.2s ease;
    }
    .copy-btn:hover {
        background-color: #e0e0e0;
    }
    .stChatInput {
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ======================
# ✅ Chat Display
# ======================
st.markdown("<h2 style='text-align:center;'>✨ Kelly — The Poetic Scientist</h2>", unsafe_allow_html=True)
st.write("---")

for i, msg in enumerate(current_chat["messages"][1:], start=1):  # skip system message
    if msg["role"] == "user":
        st.markdown(f"<div class='chat-message-user'>{msg['content']}</div>", unsafe_allow_html=True)
    elif msg["role"] == "assistant":
        st.markdown(f"<div class='chat-message-assistant'>{msg['content']}</div>", unsafe_allow_html=True)
        # Copy button
        st.markdown(f"""
            <button class='copy-btn' onclick="navigator.clipboard.writeText(`{msg['content'].replace('`','\\`')}`)">
                📋 Copy
            </button>
        """, unsafe_allow_html=True)

# ======================
# ✅ Chat Input
# ======================
prompt = st.chat_input("Message Kelly...")

if prompt:
    # Store user message
    current_chat["messages"].append({"role": "user", "content": prompt})

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Kelly is composing..."):
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=current_chat["messages"],
                temperature=0.8,
                max_tokens=400
            )
            reply = response.choices[0].message.content

            st.markdown(f"<div class='chat-message-assistant'>{reply}</div>", unsafe_allow_html=True)
            st.markdown(f"""
                <button class='copy-btn' onclick="navigator.clipboard.writeText(`{reply.replace('`','\\`')}`)">
                    📋 Copy
                </button>
            """, unsafe_allow_html=True)

            current_chat["messages"].append({"role": "assistant", "content": reply})
            current_chat["title"] = prompt[:30] + "..." if len(prompt) > 30 else prompt

    st.rerun()
