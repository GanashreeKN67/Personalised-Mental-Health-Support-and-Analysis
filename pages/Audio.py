import streamlit as st
import os
import shutil 
from audio_sentiment_model import analyze_audio
import tempfile
from auth import save_user_data, load_user_data

#Login check
if "user" not in st.session_state or st.session_state["user"] is None:
    st.query_params["page"] = "Login"
    st.rerun()


# Page config
st.title("Choose an Audio Source:") 
audio_file = st.file_uploader('Upload audio (wav/mp3)', type=['wav','mp3','m4a'])
mic_audio = st.audio_input("Or record audio")  # Streamlit >= 1.32

audio_source = None
if audio_file is not None:
    st.audio(audio_file)
    audio_source = audio_file
elif mic_audio is not None:
    st.audio(mic_audio)
    audio_source = mic_audio

if audio_source is not None:
    # require login
    if "user" not in st.session_state or st.session_state["user"] is None:
        st.warning("Please sign in to upload or analyze audio.")
    else:
        user = st.session_state["user"]
        user_dir = os.path.join("user_data", user, "audio")
        os.makedirs(user_dir, exist_ok=True)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_source.read())
            local_path = tmp_file.name

        dest = os.path.join(user_dir, os.path.basename(local_path))
        shutil.copyfile(local_path, dest)  # <-- copy instead of move
        os.remove(local_path)              # <-- delete temp file
        st.success(f"Saved audio to {dest}")

        if st.button("🧠 Analyze Audio"):
            with st.spinner("Processing audio..."):
                result = analyze_audio(dest)

            if "transcription" in result:
                st.subheader("🗣️ Transcription")
                st.write(result["transcription"])
                save_user_data(user, "last_audio_transcription", result["transcription"])

                st.subheader("💬 Sentiment")
                st.write(f"**{result['sentiment']}** ({result['score']*100:.1f}%)")

                st.subheader("🤖 Response")
                st.success(result["response"])
                save_user_data(user, "last_audio_response", result["response"])
            else:
                st.error(result.get("error", "Audio analysis failed."))


