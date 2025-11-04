import streamlit as st
from openai import OpenAI
import uuid

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
st.set_page_config(page_title="Kelly - AI Scientist Poet", page_icon="✨", layout="centered")

# ============================
# ✅ Enhanced Poetic Blue & White Theme
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');
/* (keep your full CSS exactly as before) */
</style>
""", unsafe_allow_html=True)

# ============================
# ✅ Sidebar for Chat Sessions
# ============================
st.sidebar.title("💬 Kelly Chat")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "current_chat" not in st.session_state:
    st.session_state.current_chat = str(uuid.uuid4())

# New Chat
if st.sidebar.button("🆕 New Chat"):
    st.session_state.current_chat = str(uuid.uuid4())
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Kelly, an AI scientist who responds in elegant poetic form. "
            "Write thoughtful verses that fully explore the concept being discussed. "
            "Blend analytical insight with poetic beauty."
        )}
    ]
    st.rerun()

# Previous Chats
st.sidebar.markdown("### 🕓 Previous Chats")
for cid, cdata in st.session_state.chat_history.items():
    if st.sidebar.button(cdata["title"], key=cid):
        st.session_state.current_chat = cid
        st.session_state.messages = cdata["messages"]
        st.rerun()

# ============================
# ✅ Message Memory - POETIC MODE
# ============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Kelly, an AI scientist who responds in elegant poetic form. "
            "Write thoughtful verses that fully explore the concept being discussed. "
            "Blend analytical insight with poetic beauty."
        )}
    ]

# ============================
# ✅ Elegant Header
# ============================
st.markdown("""
<div class='header-container'>
    <h1 class='header-title'>Kelly</h1>
    <div class='decorative-flourish'>
        <div class='flourish-line'></div>
        <span class='flourish-icon'>✨</span>
        <div class='flourish-line'></div>
    </div>
    <p class='header-subtitle'>An AI scientist who speaks in verse, where neural networks meet literary universe</p>
</div>
""", unsafe_allow_html=True)

# ============================
# ✅ Chat Display Container
# ============================
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-messages-container'>", unsafe_allow_html=True)

    for i, msg in enumerate(st.session_state.messages[1:], start=1):
        if msg["role"] == "user":
            # Editable user message
            col1, col2 = st.columns([8, 1])
            with col1:
                st.markdown(f"""
                <div class='message-wrapper user-wrapper'>
                    <div class='message-content user-message'>{msg["content"]}</div>
                    <div class='message-avatar user-avatar'>👤</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✏️", key=f"edit_{i}"):
                    st.session_state.edit_index = i
                    st.session_state.edit_text = msg["content"]
                    st.rerun()

        elif msg["role"] == "assistant":
            # Assistant message with copy button
            col1, col2 = st.columns([8, 1])
            with col1:
                st.markdown(f"""
                <div class='message-wrapper assistant-wrapper'>
                    <div class='message-avatar assistant-avatar'>✨</div>
                    <div class='message-content assistant-message'>{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                copy_button = f"""
                <button onclick="navigator.clipboard.writeText(`{msg["content"]}`)"
                style="background:none;border:none;cursor:pointer;font-size:18px;">📋</button>
                """
                st.markdown(copy_button, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# ✅ Edit Prompt (Inline)
# ============================
if "edit_index" in st.session_state:
    st.markdown("### ✏️ Edit Your Message")
    new_text = st.text_area("Edit prompt:", st.session_state.edit_text)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save"):
            st.session_state.messages[st.session_state.edit_index]["content"] = new_text
            del st.session_state["edit_index"]
            st.rerun()
    with col2:
        if st.button("❌ Cancel"):
            del st.session_state["edit_index"]
            st.rerun()

# ============================
# ✅ Chat Input & Response
# ============================
prompt = st.chat_input("Share your thoughts with Kelly...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages,
        temperature=0.85,
        max_tokens=500
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Save chat title for history
    if st.session_state.current_chat not in st.session_state.chat_history:
        st.session_state.chat_history[st.session_state.current_chat] = {
            "title": prompt[:25] + "...",
            "messages": st.session_state.messages.copy()
        }
    else:
        st.session_state.chat_history[st.session_state.current_chat]["messages"] = st.session_state.messages.copy()

    st.rerun()
