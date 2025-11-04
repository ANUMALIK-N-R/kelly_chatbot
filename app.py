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
# ✅ Professional Chat Style
# ============================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

body {
    background-color: #f8f9fa;
    font-family: 'Inter', sans-serif;
}

.main {
    background-color: #ffffff;
}

.chat-container {
    max-width: 900px;
    margin: 20px auto;
    background-color: #ffffff;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    min-height: 70vh;
    max-height: 70vh;
    overflow-y: auto;
    border: 1px solid #e5e7eb;
}

.message-row {
    display: flex;
    margin-bottom: 20px;
    align-items: flex-start;
}

.user-row {
    justify-content: flex-end;
}

.assistant-row {
    justify-content: flex-start;
}

.message-content {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 8px;
    line-height: 1.6;
    font-size: 15px;
}

.user-message {
    background-color: #2563eb;
    color: #ffffff;
    border-bottom-right-radius: 4px;
}

.assistant-message {
    background-color: #f3f4f6;
    color: #1f2937;
    border-bottom-left-radius: 4px;
    border-left: 3px solid #2563eb;
}

.message-avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    margin: 0 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    flex-shrink: 0;
}

.user-avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.assistant-avatar {
    background: linear-gradient(135deg, #2563eb 0%, #1e40af 100%);
    color: white;
}

.chat-input-container {
    max-width: 900px;
    margin: 20px auto;
    padding: 0 24px;
}

::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #cbd5e1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #94a3b8;
}

.header-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 32px 24px 16px 24px;
    border-bottom: 1px solid #e5e7eb;
    background-color: #ffffff;
}

.stChatInputContainer {
    border-top: 1px solid #e5e7eb;
    padding-top: 16px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# ✅ Header
# ============================
st.markdown("""
<div class='header-container'>
    <h1 style='margin: 0; color: #1f2937; font-size: 28px; font-weight: 600;'>Kelly</h1>
    <p style='margin: 8px 0 0 0; color: #6b7280; font-size: 15px;'>AI Research Assistant — Expert insights on artificial intelligence, machine learning, and technology ethics</p>
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
