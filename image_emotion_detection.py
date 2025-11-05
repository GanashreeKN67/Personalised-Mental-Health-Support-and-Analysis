# image_detection_model.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from transformers import pipeline
from PIL import Image
import pyttsx3
import io
import easyocr
import tempfile

# Load environment variables
load_dotenv()

# --- Configure Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key not found. Add it to your .env file as GEMINI_API_KEY=<your_key>")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-1.5-flash" for faster output

# --- Load Hugging Face emotion detection model ---
#emotion_detector = pipeline("image-classification", model="dima806/facial_emotions_image_detection")

# ============================================================
# 🧩 CBT PROMPTS FOR THERAPEUTIC RESPONSES
# ============================================================

CBT_PROMPTS = {
    "anger": (
        "The user looks angry. As a CBT therapist, help them explore what triggered this anger, "
        "recognize physical signs of tension, and find ways to calm down safely. "
        "Offer strategies to express emotions constructively."
    ),
    "sad": (
        "The user appears sad. Offer CBT-based empathy, validate their feelings, and suggest small actions "
        "that promote hope — like journaling, reaching out to loved ones, or self-compassion."
    ),
    "happy": (
        "The user looks happy. Reinforce positive behavior and emotional awareness. "
        "Encourage gratitude and reflection on what contributes to their well-being."
    ),
    "surprise": (
        "The user seems surprised. Provide a CBT-style reflection: explore what caused this surprise and "
        "whether it is positive or stressful. Help them process it calmly."
    ),
    "fear": (
        "The user looks fearful. Offer CBT grounding guidance: recognize what feels threatening, "
        "challenge catastrophic thoughts, and focus on safety and breathing."
    ),
    "neutral": (
        "The user appears neutral or calm. Encourage mindfulness and reflection. "
        "Ask how they’re feeling inside — not just what’s visible."
    ),
    "disgust": (
        "The user shows disgust. As a CBT therapist, explore what caused this reaction, "
        "help them identify triggering thoughts, and guide toward balanced evaluation."
    ),
    "contempt": (
        "The user shows contempt. Offer CBT support by reflecting on interpersonal thoughts, "
        "empathy exercises, and emotional regulation strategies."
    )
}

_face_emotion_model = None
_ocr_reader = None

def load_image_models():
    global _face_emotion_model, _ocr_reader
    if _face_emotion_model is None:
        _face_emotion_model = pipeline("image-classification", model="dima806/facial_emotions_image_detection")
    if _ocr_reader is None:
        _ocr_reader = easyocr.Reader(["en"], gpu=False)
    return _face_emotion_model, _ocr_reader




import numpy as np

def ocr_image(image):
    """Extract visible text from image using EasyOCR."""
    _, reader = load_image_models()
    if hasattr(image, "read"):  # Streamlit UploadedFile
        data = image.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        img_np = np.array(img)
        result = reader.readtext(img_np, detail=0)
    elif isinstance(image, Image.Image):  # PIL Image
        img_np = np.array(image.convert("RGB"))
        result = reader.readtext(img_np, detail=0)
    elif isinstance(image, str) and os.path.exists(image):  # File path
        result = reader.readtext(image, detail=0)
    else:
        raise ValueError("Invalid input type for OCR. Must be file path, UploadedFile, or PIL Image.")
    return "\n".join(result) if result else "No visible text detected."





def get_tts_engine():
    global _tts_engine
    if _tts_engine is None:
        _tts_engine = pyttsx3.init()
        _tts_engine.setProperty('rate', 150)
    return _tts_engine




def speak_text(text):
    engine = get_tts_engine()
    engine.say(text)
    engine.runAndWait()




# ============================================================
# 🧠 EMOTION DETECTION + GEMINI RESPONSE
# ============================================================

def analyze_image(image_input):
    """
    Detects facial emotion from image and generates a CBT-guided Gemini response.
    """
    try:

        # Ensure model is loaded
        load_image_models()

        # Convert input to supported format
        if isinstance(image_input, str) and os.path.exists(image_input):
            # File path
            img_for_model = image_input
        elif hasattr(image_input, "read"):  # Streamlit UploadedFile
            data = image_input.read()
            img = Image.open(io.BytesIO(data)).convert("RGB")
            img_for_model = img
        elif isinstance(image_input, Image.Image):
            img_for_model = image_input
        else:
            raise ValueError("Unsupported image input type.")
        
        # Step 1: Detect emotion
        results = _face_emotion_model(img_for_model)

        # Get top emotion
        top_emotion = results[0]['label'].lower()
        confidence = results[0]['score']

        # Step 2: Build CBT-based therapeutic prompt
        base_prompt = CBT_PROMPTS.get(
            top_emotion,
            f"The user’s detected emotion is {top_emotion}. Provide CBT-based empathetic guidance."
        )

        prompt = f"Detected emotion: {top_emotion}. {base_prompt} Use practical CBT steps and empathetic language."

        # Step 3: Generate response from Gemini
        response = gemini_model.generate_content(prompt)

        return {
            "emotion": top_emotion.capitalize(),
            "confidence": round(float(confidence) * 100, 2),
            "response": response.text.strip() if response and response.text else "No response generated."
        }

    except Exception as e:
        return {"emotion": None, "confidence": 0, "response": f"Error analyzing image: {e}"}
