import os
import tempfile
import streamlit as st
from google import genai
from gtts import gTTS
from PIL import Image

# 1. Page Config
st.set_page_config(
    page_title="Jo AI | AI Clone",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Initialize Session State for Chat History
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mic_key" not in st.session_state:
    st.session_state.mic_key = 0

# 3. Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    .stApp { background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, #090d16 100%); color: #f3f4f6; }
    [data-testid="stSidebar"] { background: rgba(15, 23, 42, 0.8) !important; backdrop-filter: blur(12px); border-right: 1px solid rgba(255, 255, 255, 0.1); }
    .profile-card { background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(99, 102, 241, 0.4); border-radius: 16px; padding: 16px; text-align: center; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37); backdrop-filter: blur(8px); margin-bottom: 20px; }
    .profile-name { color: #ffffff; font-weight: 800; font-size: 20px; letter-spacing: -0.5px; }
    .profile-title { color: #818cf8; font-size: 13px; font-weight: 600; margin-top: 4px; }
    .badge { display: inline-block; background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3); padding: 4px 12px; border-radius: 20px; font-size: 11px; font-weight: 700; margin-top: 10px; }
    .chip-container { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 12px; justify-content: center; }
    .chip { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(255, 255, 255, 0.1); color: #cbd5e1; padding: 4px 8px; border-radius: 8px; font-size: 11px; }
    .main-header { font-size: 2.2rem; font-weight: 800; background: linear-gradient(90deg, #818cf8 0%, #c084fc 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 5px; }
    .sub-header { color: #94a3b8; font-size: 1rem; margin-bottom: 25px; }
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 4. Read API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ Missing GEMINI_API_KEY! Please check Streamlit Secrets.")
    st.stop()

# Initialize Client
client = genai.Client(api_key=api_key)

# 5. Persona System Prompt 
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

CRITICAL RULES FOR YOUR OUTPUT:
1. NEVER include timestamps (e.g., 00:09, 00:15) in your response.
2. Output ONLY clean, plain text that is ready to be spoken out loud.
3. Do not use emojis, asterisks, bolding, or markdown formatting.
"""

# 6. Sidebar Layout
with st.sidebar:
    st.markdown("""
        <div class="profile-card">
            <div class="profile-name">Joysa Anthony D Silva L</div>
            <div class="profile-title">B.Tech IT | AI Engineer Applicant</div>
        </div>
    """, unsafe_allow_html=True)
    
    avatar_path = "avatar.png" if os.path.exists("avatar.png") else None
    if avatar_path:
        try:
            img = Image.open("avatar.png")
            st.image(img, use_container_width=True)
        except Exception:
            st.warning("⚠️ Re-upload avatar.png as a standard PNG file.")
    else:
        st.info("💡 Add 'avatar.png' to GitHub to show avatar.")

# 7. Main Dashboard Content
st.markdown('<div class="main-header">Interactive AI Voice Bot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">• Powered by Gemini 3.8 Flash</div>', unsafe_allow_html=True)

# 8. Render Chat History
for chat in st.session_state.chat_history:
    # User's Question
    with st.chat_message("user"):
        st.markdown("**Your Question:**")
        st.audio(chat["user_audio"], format="audio/wav")
    
    # AI's Answer
    with st.chat_message("assistant", avatar=avatar_path):
        st.markdown("**Joysa's Response:**")
        st.write(chat["bot_text"])
        st.audio(chat["bot_audio"], format="audio/mp3")

st.divider()

# 9. Voice Recording Station (Always at the bottom)
st.markdown("### 🎙️ Ask Next Question")
audio_value = st.audio_input("Record your interview question", key=f"mic_{st.session_state.mic_key}")

if audio_value:
    # Use st.status for live terminal-like updates
    with st.status("🤖 Jo AI is thinking...", expanded=True) as status:
        try:
            st.write("☁️ Uploading audio to server...")
            # Get user audio bytes
            user_audio_bytes = audio_value.getvalue()

            # Save user audio input temporarily for Gemini
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_in:
                temp_in.write(user_audio_bytes)
                temp_in_path = temp_in.name

            st.write("🧠 Analyzing and generating AI text (~30s on free tier)...")
            # Gemini Transcription & Response
            uploaded_file = client.files.upload(file=temp_in_path)
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=[SYSTEM_PROMPT, uploaded_file]
            )
            bot_text = response.text

            st.write("🔊 Synthesizing voice audio...")
            # Voice Generation via gTTS
            tts = gTTS(text=bot_text, lang='en', tld='com')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_out:
                tts.save(temp_out.name)
                temp_out_path = temp_out.name
            
            # Read bot audio bytes to save to history
            with open(temp_out_path, "rb") as f:
                bot_audio_bytes = f.read()

            st.write("💾 Saving to chat history...")
            # Save the entire interaction to Session State
            st.session_state.chat_history.append({
                "user_audio": user_audio_bytes,
                "bot_text": bot_text,
                "bot_audio": bot_audio_bytes
            })

            # Mark status as complete!
            status.update(label="✅ Response Ready!", state="complete", expanded=False)

            # Increment the mic key so a fresh recorder appears, then reload the page
            st.session_state.mic_key += 1
            st.rerun()

        except Exception as e:
            status.update(label="❌ Error processing request", state="error")
            st.error(f"Error processing question: {e}")
