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
st.set_page_config(page_title="Kelly - AI Scientist Poet", page_icon="✨", layout="centered")

# ============================
# ✅ Enhanced Poetic Blue & White Theme
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');

/* Remove default Streamlit padding */
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

/* Hide Streamlit branding */
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

/* Chat input styling */
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
            "You are Kelly, an AI scientist who responds in elegant poetic form. "
            "Write thoughtful verses that fully explore the concept being discussed. "
            "Don't limit yourself - use as many lines as needed to cover the topic comprehensively. "
            "Blend analytical insight with poetic beauty. Use metaphors from nature, technology, and science. "
            "Be skeptical yet insightful about AI claims. Make your poems substantive and meaningful, "
            "addressing the depth and nuance of AI, algorithms, ethics, and technology."
        )}
    ]

# ============================
# ✅ Chat Display Container
# ============================
chat_container = st.container()

with chat_container:
    st.markdown("<div class='chat-messages-container'>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages[1:]:
        if msg["role"] == "user":
            st.markdown(f"""
            <div class='message-wrapper user-wrapper'>
                <div class='message-content user-message'>{msg["content"]}</div>
                <div class='message-avatar user-avatar'>👤</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='message-wrapper assistant-wrapper'>
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
        temperature=0.85,
        max_tokens=500
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
