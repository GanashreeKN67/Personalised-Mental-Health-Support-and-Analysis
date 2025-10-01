# app.py
import streamlit as st
from model_utils import transcribe_audio, analyze_text_emotion, analyze_face_emotion, ocr_image, speak_text
from PIL import Image


st.set_page_config(page_title='MH Assistant Prototype', layout='centered')
st.title('Personalized Mental Health Assistant — Prototype')


st.markdown('Upload audio, an image, or type text. The assistant will analyze and reply with supportive guidance.')


mode = st.radio('Input mode', ['Text', 'Audio - Upload / Record', 'Image - Face / Document'])


if mode == 'Text':
    user_text = st.text_area('Write how you feel (or copy/paste):')
    if st.button('Analyze Text') and user_text.strip():
        emo = analyze_text_emotion(user_text)
        st.write('Emotion analysis:', emo)
        reply = f"I hear that you're feeling {emo.get('label')} (score {emo.get('score'):.2f}). Here are a few suggestions: \n - Try a 4-4-4 breathing exercise\n - Write for 5 minutes about what you're feeling\n - Reach out to a trusted friend"
        st.info(reply)
        if st.button('Speak reply'):
            speak_text(reply)


# ...existing code...

if mode == 'Audio - Upload / Record':
    st.write("Choose an audio source:")
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



if mode == 'Image - Face / Document':
    st.write("Choose an image source:")
    img_file = st.file_uploader('Upload image (selfie or document)', type=['png','jpg','jpeg'])
    cam_img = st.camera_input("Or take a photo")

    image = None
    if img_file is not None:
        image = Image.open(img_file).convert('RGB')
        st.image(image, caption='Uploaded')
        img_source = img_file
    elif cam_img is not None:
        image = Image.open(cam_img).convert('RGB')
        st.image(image, caption='Camera Photo')
        img_source = cam_img

    if image is not None and st.button('Analyze Image'):
        with st.spinner('Running face emotion + OCR...'):
            face_res = analyze_face_emotion(img_source)
            ocr_text = ocr_image(img_source)
        st.write('Face emotion result:')
        st.write(face_res)
        st.write('OCR extracted text (if any):')
        st.text(ocr_text)
        reply = 'I detected ' + face_res.get('dominant_emotion', 'unknown') + ". If this is tied to a physical symptom or medication question, please consult a professional. Otherwise consider a short relaxation exercise."
        st.info(reply)
        if st.button('Speak reply'):
            speak_text(reply)


