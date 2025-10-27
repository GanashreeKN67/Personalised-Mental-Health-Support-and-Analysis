# app.py
import streamlit as st
from audio_sentiment_model import analyze_audio


from model_utils import transcribe_audio, analyze_text_emotion, analyze_face_emotion, ocr_image, speak_text
from PIL import Image

if "user" not in st.session_state or st.session_state["user"] is None:
    st.query_params["page"] = "Login"
    st.rerun()


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
        st.switch_page('pages/Text.py')  # Navigates to Mood Selection page
with col2:
    if st.button('AUDIO (🗣️)'):
        st.switch_page('pages/Audio.py')     # Replace with your audio page filename
with col3:
    if st.button('IMAGE (📷)'):
        st.switch_page('pages/Image.py')  

#Logout button
# Add this before your button (once per page)
st.markdown("""
    <style>
    .logout-btn button {
        width: 20px !important;
        height: 60px !important;
        font-size: 22px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Wrap your button in a container with the custom class
with st.container():
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state["user"] = None
        st.query_params["page"] = "Login"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

