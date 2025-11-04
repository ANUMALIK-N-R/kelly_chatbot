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
st.set_page_config(page_title="Kelly - AI Scientist Poet", page_icon="🧠", layout="wide")

# ============================
# ✅ Custom Chat Style (Teal + Gray)
# ============================
st.markdown("""
<style>
body {
    background-color: #e0f2f1; /* soft teal background */
    font-family: 'Helvetica', sans-serif;
}
.chat-container {
    max-width: 650px;
    margin: auto;
    background-color: #f7f7f7;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0 3px 15px rgba(0,0,0,0.15);
    height: 75vh;
    overflow-y: auto;
}
.user-bubble {
    background-color: #b2dfdb; /* teal bubble */
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    margin: 8px;
    max-width: 75%;
    float: right;
    clear: both;
    color: #004d40;
}
.bot-bubble {
    background-color: #ffffff; /* white bubble for bot */
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    margin: 8px;
    max-width: 75%;
    float: left;
    clear: both;
    color: #263238;
}
.icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    margin: 0 8px;
}
.footer {
    position: fixed;
    bottom: 10px;
    width: 100%;
    text-align: center;
    font-size: 13px;
    color: #4f4f4f;
}
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background-color: #80cbc4;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ============================
# ✅ Header
# ============================
st.markdown("<h2 style='text-align:center; color:#004d40;'>💬 Kelly — The AI Scientist Poet 🤖</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#00695c;'>Ask Kelly about AI, ethics, or algorithms — and she’ll respond in poetic skepticism.</p>", unsafe_allow_html=True)

# ============================
# ✅ Message Memory
# ============================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Kelly, an AI scientist who responds only in poetic form. "
            "Your tone is analytical, skeptical, and professional — questioning broad claims about AI, "
            "highlighting its limitations, and offering evidence-based insights in verse."
        )}
    ]

# ============================
# ✅ Chat Display
# ============================
st.markdown("<div class='chat-container' id='chat-box'>", unsafe_allow_html=True)

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-end; align-items:center;">
            <div class='user-bubble'>{msg["content"]}</div>
            <img src='https://cdn-icons-png.flaticon.com/512/194/194938.png' class='icon'>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex; justify-content:flex-start; align-items:center;">
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712109.png' class='icon'>
            <div class='bot-bubble'>{msg["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ============================
# ✅ Chat Input & Response
# ============================
prompt = st.chat_input("Type your message to Kelly...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # ✅ updated Groq model
        messages=st.session_state.messages,
        temperature=0.7,
        max_tokens=300
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()

# ============================
# ✅ Footer
# ============================
st.markdown("<div class='footer'>Built with 💚 using Streamlit + Groq + LLaMA 3.3</div>", unsafe_allow_html=True)
