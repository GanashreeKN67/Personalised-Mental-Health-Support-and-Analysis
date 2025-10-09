import streamlit as st
from model_utils import transcribe_audio, analyze_text_emotion, analyze_face_emotion, ocr_image, speak_text
from PIL import Image

# Page config
st.set_page_config(page_title="Mood Selection", layout="centered")

st.title("Choose an Image Source:")

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