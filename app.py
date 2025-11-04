import streamlit as st
from openai import OpenAI

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
# ✅ Enhanced Poetic Blue & White Theme
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

body {
    background: radial-gradient(circle at 20% 50%, #e1f5fe 0%, #b3e5fc 25%, #81d4fa 50%, #4fc3f7 75%, #29b6f6 100%);
    font-family: 'Lora', serif;
}

.main {
    background: transparent;
}

.stApp {
    background: radial-gradient(circle at 20% 50%, #e1f5fe 0%, #b3e5fc 25%, #81d4fa 50%, #4fc3f7 75%, #29b6f6 100%);
}

.header-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 50px 20px 30px 20px;
    text-align: center;
    position: relative;
}

.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 64px;
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
    50% { transform: translateY(-8px); }
}

.header-subtitle {
    font-family: 'Lora', serif;
    font-size: 20px;
    color: #0d47a1;
    margin: 20px auto 0 auto;
    font-style: italic;
    opacity: 0.9;
    max-width: 600px;
    line-height: 1.6;
}

.decorative-flourish {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 25px 0;
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

.chat-container {
    max-width: 800px;
    margin: 20px auto;
    padding: 0 20px;
    min-height: 55vh;
    max-height: 55vh;
    overflow-y: auto;
}

.message-row {
    display: flex;
    margin-bottom: 28px;
    align-items: flex-start;
    animation: messageSlide 0.5s ease-out;
}

@keyframes messageSlide {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-row {
    justify-content: flex-end;
}

.assistant-row {
    justify-content: flex-start;
}

.message-content {
    max-width: 70%;
    padding: 18px 24px;
    border-radius: 24px;
    line-height: 1.8;
    font-size: 16px;
    font-family: 'Lora', serif;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
    position: relative;
}

.user-message {
    background: linear-gradient(135deg, rgba(25, 118, 210, 0.95) 0%, rgba(21, 101, 192, 0.95) 100%);
    color: #ffffff;
    border-bottom-right-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.assistant-message {
    background: rgba(255, 255, 255, 0.98);
    color: #0d47a1;
    border-bottom-left-radius: 8px;
    border-left: 4px solid #1976d2;
    font-style: italic;
    box-shadow: 0 8px 32px rgba(13, 71, 161, 0.15);
}

.message-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    margin: 0 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
    flex-shrink: 0;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    border: 3px solid rgba(255, 255, 255, 0.9);
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

::-webkit-scrollbar {
    width: 12px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.4);
    border-radius: 10px;
    margin: 10px 0;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, #64b5f6 0%, #42a5f5 50%, #2196f3 100%);
    border-radius: 10px;
    border: 2px solid rgba(255, 255, 255, 0.3);
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, #42a5f5 0%, #2196f3 50%, #1976d2 100%);
}

.stChatInputContainer {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 30px;
    padding: 10px;
    backdrop-filter: blur(15px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
    border: 2px solid rgba(255, 255, 255, 0.5);
}

.floating-particles {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}

.particle {
    position: absolute;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    animation: float 20s infinite ease-in-out;
}
</style>
""", unsafe_allow_html=True)

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
# ✅ Message Memory - POETIC MODE
# ============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Kelly, an AI scientist who responds in short, elegant poetic form. "
            "Write 3-6 lines of verse that are analytical yet beautiful, skeptical yet insightful. "
            "Use metaphors from nature, technology, and science. Keep your poems brief and impactful. "
            "Focus on clarity while maintaining poetic rhythm. Address AI, algorithms, and technology "
            "with both wonder and critical thought. Make each response feel like a crafted haiku or short verse."
        )}
    ]

# ============================
# ✅ Chat Display
# ============================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='message-row user-row'>
            <div class='message-content user-message'>{msg["content"]}</div>
            <div class='message-avatar user-avatar'>👤</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class='message-row assistant-row'>
            <div class='message-avatar assistant-avatar'>✨</div>
            <div class='message-content assistant-message'>{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ============================
# ✅ Chat Input & Response
# ============================
prompt = st.chat_input("Share your thoughts with Kelly...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages,
        temperature=0.8,
        max_tokens=250
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
