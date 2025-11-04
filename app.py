import streamlit as st
from openai import OpenAI


# You can set GROQ_API_KEY as a Streamlit secret or environment variable
client = OpenAI(
    api_key=st.secrets.get("GROQ_API_KEY", ""),
    base_url="https://api.groq.com/openai/v1"
)


st.set_page_config(page_title="Kelly - AI Scientist Poet", page_icon="🧠", layout="wide")


st.markdown("""
<style>
body {
    background-color: #ece5dd;
    font-family: 'Helvetica', sans-serif;
}
.chat-container {
    max-width: 600px;
    margin: auto;
    background-color: #e5ddd5;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
    height: 75vh;
    overflow-y: auto;
}
.user-bubble {
    background-color: #dcf8c6;
    padding: 10px 15px;
    border-radius: 15px 15px 0 15px;
    margin: 5px;
    max-width: 80%;
    float: right;
    clear: both;
}
.bot-bubble {
    background-color: white;
    padding: 10px 15px;
    border-radius: 15px 15px 15px 0;
    margin: 5px;
    max-width: 80%;
    float: left;
    clear: both;
}
.icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    margin: 0 8px;
}
.footer {
    position: fixed;
    bottom: 10px;
    width: 100%;
    text-align: center;
    font-size: 13px;
    color: gray;
}
</style>
""", unsafe_allow_html=True)


st.markdown("<h2 style='text-align:center; color:#075e54;'>💬 Kelly — The AI Scientist Poet 🤖</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Ask Kelly about AI, ethics, or algorithms — and she’ll reply in skeptical, evidence-based poetry.</p>", unsafe_allow_html=True)


if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": (
            "You are Kelly, an AI scientist who responds in the form of a poem. "
            "Your poems should be analytical, skeptical, and professional in tone. "
            "Each response should question broad claims about AI, highlight limitations, "
            "and offer practical, evidence-based insights. "
            "Always respond only in poetic form, not prose."
        )}
    ]


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


prompt = st.chat_input("Type your message to Kelly...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        model="whisper-large-v3-turbo",
        messages=st.session_state.messages,
        temperature=0.7,
        max_tokens=300
    )

    reply = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.rerun()


st.markdown("<div class='footer'>Built with 💚 using Streamlit + Groq + LLaMA 3</div>", unsafe_allow_html=True)
