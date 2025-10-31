# app.py
import streamlit as st
from audio_sentiment_model import analyze_audio
import streamlit as st
from auth import register_user, authenticate_user

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
#st.set_page_config(page_title="Login", layout="centered")


if "user" not in st.session_state:
    st.session_state["user"] = None

st.title("Sign in / Register")

tab1, tab2 = st.tabs(["Sign in", "Register"])
with tab1:
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Sign in"):
        if authenticate_user(username, password):
            st.session_state["user"] = username
            st.success("Signed in")
            st.query_params["page"] = "D:\Personalised-Mental-Health-Analysis-and-Support\app.py" 
            st.rerun()
        else:
            st.error("Invalid credentials")

with tab2:
    r_username = st.text_input("Choose username", key="reg_username")
    r_password = st.text_input("Choose password", type="password", key="reg_password")
    if st.button("Register"):
        ok = register_user(r_username, r_password)
        if ok:
            st.success("User registered — please sign in")
        else:
            st.error("Username taken")

st.markdown(custom_css, unsafe_allow_html=True)

#mode = st.radio('Input mode', ['Text', 'Audio - Upload / Record', 'Image - Face / Document'])

if st.session_state["user"]:
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
        width: 10px !important;
        height: 20px !important;
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

