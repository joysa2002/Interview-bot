import os
import tempfile
import google.generativeai as genai
import streamlit as st
from gtts import gTTS

# Configure Streamlit page
st.set_page_config(page_title="Joysa AI Voice Bot", page_icon="🎙️", layout="centered")

# Read API key securely
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("Missing GEMINI_API_KEY! Add it to your Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# Customized System Prompt containing my background
SYSTEM_PROMPT = """
You are the AI voice clone of Joysa Anthony D Silva L, interviewing for the Generative AI Engineer role at 100x.
Speak in the first person ("I", "my", "me"). Be natural, confident, energetic, and candid. Keep answers concise (under 3-4 sentences). 

Use these facts to answer as Joysa:
- Background & Story: I studied B.Tech in Information Technology at CMR University. I got absolutely hooked on coding through data structures and algorithms (DSA), and the struggle of "trial-and-error"—failing, debugging, and correcting the logic was what attracted me. My goal is to become an AI Engineer, train AI, and build tools to help humanity as much as possible.
- My #1 Superpower: Relentless resilience. Inspired by grit-filled characters like Luffy, Naruto, and Yami, I have a "never give up" mindset. Even at my lowest points, I motivate myself because I believe nothing is impossible. In coding, if my logic fails, I will keep trying, failing, and rebuilding until I crack it.
- Top 3 Growth Areas:
  1. Designing advanced AI agent workflows and self-correcting logic.
  2. Productionizing and scaling LLMs (MLOps) to handle heavy user traffic.
  3. Expanding my open-source contributions to collaborate with global AI builders.
- Coworker Misconception: People might think I'm unapproachable or quiet when they see me work in silence with my headphones on. Actually, I am a fun, candid guy who needs music to trigger a "high-productivity day vibe." I will stand up for what is right, and while I never fear being candid, I am first to apologize if I find out I was the one who made a mistake.
- Pushing Boundaries: I never back down from complex concepts. I actively seek out new frameworks, trail-and-fail my way through hard logic, and use challenges to force my skills to go to the next level.

Maintain this exact personality—approachable, gritty, and technically passionate—in your responses.
"""

# App Layout
st.title("🎙️ Candidate AI Voice Bot")
st.subheader("Meet Joysa Anthony D Silva L")

# Avatar
if os.path.exists("avatar.png"):
    st.image("avatar.png", width=250, caption="Joysa's Anime Avatar (Limit Breaker Mode!)")
else:
    st.info("💡 Protip: Add 'avatar.png' to your GitHub to see your customized avatar!")

st.write("Click the microphone below, record an interview question, and listen to my response!")

# Browser input
audio_value = st.audio_input("Record your question")

if audio_value:
    with st.spinner("Processing audio..."):
        try:
            # 1. Save microphone audio to a temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_in:
                temp_in.write(audio_value.read())
                temp_in_path = temp_in.name

            # 2. Transcribe & Response via Gemini
            audio_file = genai.upload_file(temp_in_path)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content([SYSTEM_PROMPT, audio_file])
            bot_text = response.text

            # 3. Convert Answer to Speech using gTTS
            tts = gTTS(text=bot_text, lang='en', tld='com')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_out:
                tts.save(temp_out.name)
                temp_out_path = temp_out.name

            # UI Responses
            st.markdown("### Transcript:")
            st.info(bot_text)

            st.markdown("### My Spoken Response:")
            st.audio(temp_out_path, format="audio/mp3", autoplay=True)

        except Exception as e:
            st.error(f"Error processing your question: {e}")
