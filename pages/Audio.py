import streamlit as st
from audio_sentiment_model import analyze_audio
import tempfile

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
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(audio_source.read())
        file_path = tmp_file.name

    st.audio(file_path)

    if st.button("🧠 Analyze Audio"):
        with st.spinner("Processing audio..."):
            result = analyze_audio(file_path)

        st.subheader("🗣️ Transcription")
        st.write(result["transcription"])

        st.subheader("💬 Sentiment")
        st.write(f"**{result['sentiment']}** ({result['score']*100:.1f}%)")

        st.subheader("🤖 Response")
        st.success(result["response"])

