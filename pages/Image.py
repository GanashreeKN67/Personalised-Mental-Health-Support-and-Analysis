# ===== image.py =====

import streamlit as st
from PIL import Image
from image_emotion_detection import analyze_image, ocr_image, speak_text
# Page setup
st.set_page_config(page_title="Image Emotion Detection", layout="centered")

st.title("📸 Emotion Detection & CBT Therapy Guidance")
st.markdown("Upload or capture an image to detect emotions and receive CBT-based support.")

# Upload or camera capture
img_file = st.file_uploader("📤 Upload an image", type=["jpg", "jpeg", "png"])
cam_img = st.camera_input("📷 Or take a photo")

image = None
if img_file:
    image = Image.open(img_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_container_width=True)
elif cam_img:
    image = Image.open(cam_img).convert("RGB")
    st.image(image, caption="Captured Photo", use_container_width=True)

# Process image
if image is not None and st.button("🔍 Analyze Image"):
    with st.spinner("Analyzing your image..."):
        face_result = analyze_image(image)
        ocr_text = ocr_image(image)

    st.subheader("🧠 Detected Emotion")
    st.write(f"**Emotion:** {face_result['emotion']} ({face_result['confidence']}% confidence)")

    st.subheader("📝 OCR Extracted Text")
    st.text(ocr_text)

    st.markdown("### 💬 CBT-Guided Response:")
    st.success(face_result["response"])

    
