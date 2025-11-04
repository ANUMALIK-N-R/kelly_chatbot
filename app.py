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
                "Don't limit yourself - use as many lines as needed to cover the topic comprehensively. "
                "Blend analytical insight with poetic beauty. Use metaphors from nature, technology, and science. "
                "Be skeptical yet insightful about AI claims. Make your poems substantive and meaningful, "
                "addressing the depth and nuance of AI, algorithms, ethics, and technology."
            )}
        ]
    }

if "editing_message" not in st.session_state:
    st.session_state.editing_message = None

# ============================
# ✅ Enhanced Poetic Blue & White Theme with Sidebar
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

/* Sidebar styling */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #e3f2fd 0%, #bbdefb 100%);
    border-right: 2px solid rgba(25, 118, 210, 0.2);
}

[data-testid="stSidebar"] .block-container {
    padding-top: 2rem;
}

.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    color: #0d47a1;
    margin-bottom: 20px;
    text-align: center;
}

.chat-item {
    background: rgba(255, 255, 255, 0.7);
    padding: 12px;
    margin: 8px 0;
    border-radius: 12px;
    border-left: 3px solid #1976d2;
    cursor: pointer;
    transition: all 0.3s ease;
}

.chat-item:hover {
    background: rgba(255, 255, 255, 0.95);
    transform: translateX(5px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.chat-item-active {
    background: rgba(25, 118, 210, 0.15);
    border-left: 4px solid #0d47a1;
}

/* Main content area */
.main > div {
    padding-top: 2rem;
    padding-bottom: 0rem;
}

.main {
    background: radial-gradient(circle at 20% 50%, #e1f5fe 0%, #b3e5fc 25%, #81d4fa 50%, #4fc3f7 75%, #29b6f6 100%);
}

.stApp {
    background: radial-gradient(circle at 20% 50%, #e1f5fe 0%, #b3e5fc 25%, #81d4fa 50%, #4fc3f7 75%, #29b6f6 100%);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.header-container {
    max-width: 900px;
    margin: 0 auto 20px auto;
    padding: 30px 20px 20px 20px;
    text-align: center;
}

.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 56px;
    font-weight: 700;
    background: linear-gradient(135deg, #0d47a1 0%, #1565c0 50%, #1976d2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: 2px;
    text-shadow: 0 4px 20px rgba(13, 71, 161, 0.2);
    animation: titleFloat 3s ease-in-out infinite;
}

@keyframes titleFloat {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-6px); }
}

.header-subtitle {
    font-family: 'Lora', serif;
    font-size: 18px;
    color: #0d47a1;
    margin: 15px auto 0 auto;
    font-style: italic;
    opacity: 0.9;
    max-width: 600px;
    line-height: 1.6;
}

.decorative-flourish {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 20px 0 10px 0;
    gap: 15px;
}

.flourish-line {
    width: 80px;
    height: 1.5px;
    background: linear-gradient(90deg, transparent, #1976d2, transparent);
    opacity: 0.6;
}

.flourish-icon {
    font-size: 20px;
    color: #1976d2;
    animation: sparkle 2s ease-in-out infinite;
}

@keyframes sparkle {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.2); }
}

.chat-messages-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
}

.message-wrapper {
    display: flex;
    margin-bottom: 24px;
    animation: messageSlide 0.5s ease-out;
    position: relative;
    align-items: flex-start;
}

@keyframes messageSlide {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-wrapper {
    justify-content: flex-end;
}

.assistant-wrapper {
    justify-content: flex-start;
}

.message-content {
    max-width: 75%;
    padding: 16px 20px;
    border-radius: 20px;
    line-height: 1.8;
    font-size: 15.5px;
    font-family: 'Lora', serif;
    backdrop-filter: blur(12px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    white-space: pre-wrap;
    word-wrap: break-word;
    position: relative;
}

.user-message {
    background: linear-gradient(135deg, rgba(25, 118, 210, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%);
    color: #ffffff;
    border-bottom-right-radius: 6px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    margin-left: auto;
}

.assistant-message {
    background: rgba(255, 255, 255, 0.98);
    color: #0d47a1;
    border-bottom-left-radius: 6px;
    border-left: 4px solid #1976d2;
    font-style: italic;
    box-shadow: 0 4px 16px rgba(13, 71, 161, 0.12);
}

.message-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 0 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.9);
}

.user-avatar {
    background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
}

.assistant-avatar {
    background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
    animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.05); }
}

.stChatFloatingInputContainer {
    bottom: 20px;
    padding: 0 20px;
    background: transparent;
}

.stChatInputContainer {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 28px;
    padding: 4px;
    backdrop-filter: blur(15px);
    box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12);
    border: 2px solid rgba(255, 255, 255, 0.6);
    max-width: 900px;
    margin: 0 auto;
}

.stChatInput textarea {
    border-radius: 24px;
    font-family: 'Lora', serif;
    font-size: 15px;
}

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #64b5f6 0%, #42a5f5 50%, #2196f3 100%);
    border-radius: 10px;
    border: 2px solid rgba(255, 255, 255, 0.3);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #42a5f5 0%, #2196f3 50%, #1976d2 100%);
}

/* Button styling */
.stButton > button {
    border-radius: 8px;
    font-family: 'Lora', serif;
}
</style>
""", unsafe_allow_html=True)

# ============================
# ✅ Sidebar - Chat History
# ============================
# ============================
# ✅ Sidebar - Chat History (Black & White Minimal)
# ============================
# ============================
# ✅ Sidebar - Collapsible Chat History (Dark Mode)
# ============================

# --- Main Style Overrides ---
st.markdown("""
<style>
/* --- Global Styling --- */
.stApp {
    background: #f7f7f7;
}
.stMarkdown, .stText, .stWrite, .stCaption, .stChatMessage, .element-container {
    color: #000000 !important; /* ✅ Make all chat text black */
}

/* --- Sidebar Styling --- */
[data-testid="stSidebar"] {
    background: #000000 !important;
    color: #ffffff !important;
    border-right: 2px solid #222;
}

.sidebar-title {
    font-family: 'Playfair Display', serif;
    font-size: 24px;
    font-weight: 700;
    color: #ffffff !important;
    text-align: center;
    margin-bottom: 25px;
}

.chat-item {
    background: rgba(255, 255, 255, 0.1);
    padding: 12px;
    margin: 8px 0;
    border-radius: 10px;
    border-left: 3px solid #ffffff;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #ffffff;
}

.chat-item:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateX(5px);
}

.chat-item-active {
    background: rgba(255, 255, 255, 0.25);
    border-left: 4px solid #ffffff;
}

.stButton > button {
    color: #ffffff !important;
    background: #111111 !important;
    border: 1px solid #444 !important;
    border-radius: 6px;
    font-family: 'Lora', serif;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    background: #333333 !important;
    border-color: #666 !important;
}

.block-container p, .block-container span, .block-container div {
    color: #000000 !important;
}
</style>
""", unsafe_allow_html=True)


# --- Sidebar Toggle ---
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

col1, col2 = st.columns([0.1, 0.9])
with col1:
    toggle_btn = st.button("📂" if not st.session_state.show_sidebar else "❌", help="Toggle chat history sidebar")

if toggle_btn:
    st.session_state.show_sidebar = not st.session_state.show_sidebar
    st.rerun()

# --- Sidebar Content ---
if st.session_state.show_sidebar:
    with st.sidebar:
        st.markdown("<div class='sidebar-title'>Chat History</div>", unsafe_allow_html=True)
        
        if st.button("➕ New Chat", use_container_width=True):
            new_session_id = f"chat_{int(time.time())}"
            st.session_state.chat_sessions[new_session_id] = {
                "title": "New Chat",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "messages": [
                    {"role": "system", "content": (
                        "You are Kelly, an AI scientist who responds in elegant poetic form. "
                        "Write thoughtful verses that fully explore the concept being discussed. "
                        "Don't limit yourself - use as many lines as needed to cover the topic comprehensively. "
                        "Blend analytical insight with poetic beauty. Use metaphors from nature, technology, and science. "
                        "Be skeptical yet insightful about AI claims. Make your poems substantive and meaningful, "
                        "addressing the depth and nuance of AI, algorithms, ethics, and technology."
                    )}
                ]
            }
            st.session_state.current_session_id = new_session_id
            st.session_state.editing_message = None
            st.rerun()

        st.markdown("---")
        st.markdown("### Previous Chats")

        sorted_sessions = sorted(
            st.session_state.chat_sessions.items(),
            key=lambda x: x[1]["timestamp"],
            reverse=True
        )

        for session_id, session_data in sorted_sessions:
            is_active = session_id == st.session_state.current_session_id
            btn_label = session_data['title'][:25] + ("..." if len(session_data['title']) > 25 else "")
            
            button_type = "primary" if is_active else "secondary"
            if st.button(
                btn_label,
                key=f"chat_{session_id}",
                use_container_width=True,
                type=button_type
            ):
                st.session_state.current_session_id = session_id
                st.session_state.editing_message = None
                st.rerun()

            if st.button("🗑️", key=f"delete_{session_id}", help="Delete chat"):
                if len(st.session_state.chat_sessions) > 1:
                    del st.session_state.chat_sessions[session_id]
                    if st.session_state.current_session_id == session_id:
                        st.session_state.current_session_id = list(st.session_state.chat_sessions.keys())[0]
                    st.rerun()
            
            st.caption(f"📅 {session_data['timestamp']}")


# ============================
# ✅ Get Current Session
# ============================
current_session = st.session_state.chat_sessions[st.session_state.current_session_id]

# Update session title based on first user message
if len(current_session["messages"]) > 1 and current_session["title"] == "New Chat":
    first_user_msg = next((msg for msg in current_session["messages"] if msg["role"] == "user"), None)
    if first_user_msg:
        current_session["title"] = first_user_msg["content"][:30]

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
    
    for idx, msg in enumerate(current_session["messages"][1:], start=1):
        if msg["role"] == "user":
            col1, col2, col3 = st.columns([6, 1, 1])
            with col1:
                st.markdown(f"""
                <div class='message-wrapper user-wrapper'>
                    <div class='message-content user-message'>{msg["content"]}</div>
                    <div class='message-avatar user-avatar'>👤</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("✏️", key=f"edit_{idx}", help="Edit message"):
                    st.session_state.editing_message = idx
                    st.rerun()
        else:
            col1, col2 = st.columns([6, 1])
            with col1:
                st.markdown(f"""
                <div class='message-wrapper assistant-wrapper'>
                    <div class='message-avatar assistant-avatar'>✨</div>
                    <div class='message-content assistant-message'>{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("📋", key=f"copy_{idx}", help="Copy to clipboard"):
                    st.code(msg["content"], language=None)
                    st.success("Response shown above - copy manually")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================
# ✅ Edit Message Interface
# ============================
if st.session_state.editing_message is not None:
    edit_idx = st.session_state.editing_message
    original_msg = current_session["messages"][edit_idx]["content"]
    
    st.markdown("---")
    st.markdown("### ✏️ Edit Your Message")
    
    edited_text = st.text_area("Edit your message:", value=original_msg, height=100)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save & Regenerate", use_container_width=True):
            # Update the message
            current_session["messages"][edit_idx]["content"] = edited_text
            
            # Remove all messages after the edited one
            current_session["messages"] = current_session["messages"][:edit_idx + 1]
            
            # Generate new response
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=current_session["messages"],
                temperature=0.85,
                max_tokens=500
            )
            
            reply = response.choices[0].message.content
            current_session["messages"].append({"role": "assistant", "content": reply})
            
            st.session_state.editing_message = None
            st.rerun()
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.session_state.editing_message = None
            st.rerun()

# ============================
# ✅ Chat Input & Response
# ============================
if st.session_state.editing_message is None:
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
