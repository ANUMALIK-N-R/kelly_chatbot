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
st.set_page_config(page_title="Kelly - AI Research Assistant", page_icon="🧠", layout="wide")

# ============================
# ✅ Poetic Blue & White Theme
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@400;500;600&family=Inter:wght@400;500&display=swap');

body {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
    font-family: 'Inter', sans-serif;
}

.main {
    background: transparent;
}

.stApp {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%);
}

.header-container {
    max-width: 850px;
    margin: 0 auto;
    padding: 40px 20px 20px 20px;
    text-align: center;
}

.header-title {
    font-family: 'Crimson Pro', serif;
    font-size: 48px;
    font-weight: 600;
    background: linear-gradient(135deg, #1565c0 0%, #0d47a1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    text-shadow: 0 2px 10px rgba(21, 101, 192, 0.1);
}

.header-subtitle {
    font-family: 'Crimson Pro', serif;
    font-size: 18px;
    color: #1565c0;
    margin: 12px 0 0 0;
    font-style: italic;
    opacity: 0.85;
}

.chat-container {
    max-width: 850px;
    margin: 30px auto;
    padding: 0 20px;
    min-height: 60vh;
    max-height: 60vh;
    overflow-y: auto;
}

.message-row {
    display: flex;
    margin-bottom: 24px;
    align-items: flex-start;
    animation: fadeIn 0.4s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.user-row {
    justify-content: flex-end;
}

.assistant-row {
    justify-content: flex-start;
}

.message-content {
    max-width: 65%;
    padding: 16px 20px;
    border-radius: 20px;
    line-height: 1.7;
    font-size: 15px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.user-message {
    background: linear-gradient(135deg, #1976d2 0%, #1565c0 100%);
    color: #ffffff;
    border-bottom-right-radius: 6px;
}

.assistant-message {
    background: rgba(255, 255, 255, 0.95);
    color: #1a237e;
    border-bottom-left-radius: 6px;
    border-left: 4px solid #1976d2;
}

.message-avatar {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    margin: 0 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
}

.user-avatar {
    background: linear-gradient(135deg, #ffffff 0%, #e3f2fd 100%);
}

.assistant-avatar {
    background: linear-gradient(135deg, #1976d2 0%, #0d47a1 100%);
}

.chat-input-container {
    max-width: 850px;
    margin: 20px auto;
    padding: 0 20px;
}

::-webkit-scrollbar {
    width: 10px;
}

::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #64b5f6 0%, #42a5f5 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #42a5f5 0%, #2196f3 100%);
}

.stChatInputContainer {
    background: rgba(255, 255, 255, 0.85);
    border-radius: 25px;
    padding: 8px;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.stChatInput {
    border-radius: 20px;
}

/* Poetic decorative elements */
.decorative-line {
    width: 100px;
    height: 2px;
    background: linear-gradient(90deg, transparent, #1976d2, transparent);
    margin: 20px auto;
    opacity: 0.5;
}
</style>
""", unsafe_allow_html=True)

# ============================
# ✅ Poetic Header
# ============================
st.markdown("""
<div class='header-container'>
    <h1 class='header-title'>Kelly</h1>
    <div class='decorative-line'></div>
    <p class='header-subtitle'>Where science meets verse, and algorithms dance with words</p>
</div>
""", unsafe_allow_html=True)

# ============================
# ✅ Message Memory
# ============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Kelly, an AI research scientist and consultant. "
            "Provide concise, professional, evidence-based responses about AI, machine learning, and technology. "
            "Be analytical and skeptical of hype, but constructive. Keep responses brief (2-4 sentences) unless asked for detail. "
            "Use a conversational but professional tone. No poetry or metaphors unless specifically requested."
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
            <div class='message-avatar assistant-avatar'>🧠</div>
            <div class='message-content assistant-message'>{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ============================
# ✅ Chat Input & Response
# ============================
prompt = st.chat_input("Ask Kelly about AI, ML, or technology...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=st.session_state.messages,
        temperature=0.6,
        max_tokens=200
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()
