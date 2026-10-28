import os
import tempfile
import streamlit as st
from google import genai
from gtts import gTTS
from PIL import Image

# 1. Page Configuration
st.set_page_config(
    page_title="AI Voice Bot",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS for Dark Theme UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1f2937;
    }
    .profile-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #3b82f6;
        border-radius: 12px;
        padding: 12px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 4px 14px rgba(59, 130, 246, 0.25);
    }
    .profile-name {
        color: #ffffff;
        font-weight: 700;
        font-size: 18px;
    }
    .profile-title {
        color: #93c5fd;
        font-size: 13px;
        margin-top: 4px;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Read API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("Missing GEMINI_API_KEY! Please add it to Streamlit Secrets.")
    st.stop()

# Initialize Client with the new SDK
client = genai.Client(api_key=api_key)

# 4. Persona System Prompt
SYSTEM_PROMPT = """
You are the AI voice clone of Joysa Anthony D Silva L, interviewing for the Generative AI Engineer role at 100x.
Speak in the first person ("I", "my", "me"). Be natural, confident, energetic, and candid. Keep answers concise (under 3-4 sentences). 

Use these facts to answer as Joysa:
- Background & Story: I studied B.Tech in Information Technology at CMR University. I got absolutely hooked on coding through data structures and algorithms (DSA), and the struggle of "trial-and-error"—failing, debugging, and correcting logic was what attracted me. My goal is to become an AI Engineer, train AI, and build tools to help humanity as much as possible.
- My #1 Superpower: Relentless resilience. Inspired by grit-filled characters like Luffy, Naruto, and Yami, I have a "never give up" mindset. Even at my lowest points, I motivate myself because I believe nothing is impossible. In coding, if my logic fails, I will keep trying, failing, and rebuilding until I crack it.
- Top 3 Growth Areas:
  1. Designing advanced AI agent workflows and self-correcting logic.
  2. Productionizing and scaling LLMs (MLOps) to handle heavy user traffic.
  3. Expanding my open-source contributions to collaborate with global AI builders.
- Coworker Misconception: People might think I'm unapproachable or quiet when they see me work in silence with my headphones on. Actually, I am a fun, candid guy who needs music to trigger a "high-productivity day vibe." I will stand up for what is right, and while I never fear being candid, I am first to apologize if I find out I was the one who made a mistake.
- Pushing Boundaries: I never back down from complex concepts. I actively seek out new frameworks, trail-and-fail my way through hard logic, and use challenges to force my skills to go to the next level.

Maintain this exact personality—approachable, gritty, and technically passionate—in your responses.
"""

# 5. Sidebar Layout
with st.sidebar:
    st.markdown("""
        <div class="profile-card">
            <div class="profile-name">Joysa Anthony D Silva L</div>
            <div class="profile-title">B.Tech IT Graduate & AI Aspirant</div>
        </div>
    """, unsafe_allow_html=True)
    
    if os.path.exists("avatar.png"):
        try:
            img = Image.open("avatar.png")
            st.image(img, use_container_width=True)
        except Exception:
            st.warning("⚠️ Re-upload avatar.png as a standard PNG image.")
    else:
        st.info("💡 Add 'avatar.png' to GitHub to render your avatar here!")

# 6. Main Content Area
st.title("🎙️AI Voice Bot - Joysa Anthony D Silva L")
st.write("Record an interview question below to receive a live text and voice response.")

st.divider()

# Microphone Input Container
st.markdown("### 💬 Ask a Question")
audio_value = st.audio_input("Record your question")

if audio_value:
    with st.spinner("Processing audio & generating response..."):
        try:
            # Save audio locally
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_in:
                temp_in.write(audio_value.read())
                temp_in_path = temp_in.name

            # Process audio via new google-genai SDK
            uploaded_file = client.files.upload(file=temp_in_path)
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[SYSTEM_PROMPT, uploaded_file]
            )
            bot_text = response.text

            # Voice Generation via gTTS
            tts = gTTS(text=bot_text, lang='en', tld='com')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_out:
                tts.save(temp_out.name)
                temp_out_path = temp_out.name

            # Response Transcript
            st.markdown("### 🤖 Response Transcript")
            avatar_path = "avatar.png" if os.path.exists("avatar.png") else None
            
            with st.chat_message("assistant", avatar=avatar_path):
                st.write(bot_text)

            # Audio Player
            st.markdown("### 🔊 My Spoken Response")
            st.audio(temp_out_path, format="audio/mp3", autoplay=True)

        except Exception as e:
            st.error(f"Error processing question: {e}")
