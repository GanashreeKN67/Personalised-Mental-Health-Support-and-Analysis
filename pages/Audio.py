import streamlit as st
from model_utils import transcribe_audio, analyze_text_emotion, analyze_face_emotion, ocr_image, speak_text
from PIL import Image

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
    with st.spinner('Transcribing...'):
        transcript = transcribe_audio(audio_source)
    st.write('Transcript:')
    st.write(transcript)
    emo = analyze_text_emotion(transcript)
    st.write('Emotion (from text):', emo)
    reply = f"Transcript emotion: {emo.get('label')} ({emo.get('score'):.2f}). Suggested coping: grounding exercise, short walk, hydrate, or contact help if overwhelmed."
    st.info(reply)
    if st.button('Speak reply (audio)'):
        speak_text(reply)

