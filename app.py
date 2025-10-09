# app.py
import streamlit as st

from model_utils import transcribe_audio, analyze_text_emotion, analyze_face_emotion, ocr_image, speak_text
from PIL import Image


st.set_page_config(page_title='MH Assistant Prototype', layout='centered')
st.title('Personalized Mental Health Assistant — Prototype')


st.markdown('Upload audio, an image, or text. The assistant will analyze and reply with supportive guidance.')
custom_css = """
<style>
div.stButton > button:first-child {
    height: 100px; /* Example height */
    width: 200px;  /* Example width */
    font-size: 40px; /* Optional: adjust font size */
}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

#mode = st.radio('Input mode', ['Text', 'Audio - Upload / Record', 'Image - Face / Document'])
st.markdown('Choose your input mode:')

col1, col2, col3 = st.columns(3)
with col1:
    if st.button('TEXT (📝)'):
        st.switch_page('pages/mood_selection.py')  # Navigates to Mood Selection page
with col2:
    if st.button('AUDIO (🗣️)'):
        st.switch_page('pages/audio_input.py')     # Replace with your audio page filename
with col3:
    if st.button('IMAGE (📷)'):
        st.switch_page('pages/image_input.py')  




