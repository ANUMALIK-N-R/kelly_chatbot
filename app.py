import streamlit as st
from openai import OpenAI
from datetime import datetime
import time
import pyperclip  # to handle copy utility

# ======================
# ✅ Config
# ======================
st.set_page_config(page_title="Kelly Chat", page_icon="💬", layout="wide")

# ======================
# ✅ Groq API client
# ======================
client = OpenAI(
    api_key=st.secrets.get("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1"
)

# ======================
# ✅ Session State
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
            {"role": "system", "content": "You are Kelly, an AI scientist who replies in poetic form."}
        ]
    }

# ======================
# ✅ Sidebar (Chat History)
# ======================
with st.sidebar:
    st.markdown("### 💬 Chats")
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(int(time.time()))
        st.session_state.chats[new_id] = {
            "title": "New Chat",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": [
                {"role": "system", "content": "You are Kelly, an AI scientist who replies in poetic form."}
            ]
        }
        st.session_state.active_chat = new_id
        st.rerun()

    for cid, cdata in sorted(st.session_state.chats.items(),
                             key=lambda x: x[1]["timestamp"],
                             reverse=True):
        label = f"🕓 {cdata['title']} ({cdata['timestamp']})"
        if st.button(label, key=cid, use_container_width=True):
            st.session_state.active_chat = cid
            st.rerun()

# ======================
# ✅ Get Active Chat
# ======================
current_chat = st.session_state.chats[st.session_state.active_chat]

# ======================
# ✅ Chat Display
# ======================
st.markdown("<h2 style='text-align:center;'>💡 Kelly — The Poetic Scientist</h2>", unsafe_allow_html=True)
st.write("---")

for i, msg in enumerate(current_chat["messages"][1:], start=1):  # skip system prompt
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.markdown(msg["content"])
            # --- Copy button like ChatGPT ---
            copy_key = f"copy_btn_{i}"
            copy_script = f"""
            <button id="{copy_key}" style="
                background:none;
                border:1px solid #ccc;
                color:#333;
                border-radius:6px;
                font-size:12px;
                padding:4px 8px;
                margin-top:4px;
                cursor:pointer;
            " onclick="navigator.clipboard.writeText(`{msg["content"].replace('`','\\`')}`)">
                📋 Copy
            </button>
            """
            st.markdown(copy_script, unsafe_allow_html=True)

# ======================
# ✅ Chat Input
# ======================
prompt = st.chat_input("Message Kelly...")

if prompt:
    # Store user message
    current_chat["messages"].append({"role": "user", "content": prompt})
    # Generate reply
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            resp = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=current_chat["messages"],
                temperature=0.8,
                max_tokens=400
            )
            reply = resp.choices[0].message.content
            st.markdown(reply)
            current_chat["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
