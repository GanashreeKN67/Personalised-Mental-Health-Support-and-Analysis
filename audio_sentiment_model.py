# ===== audio_sentiment_model.py =====
import numpy as np
import librosa
import tensorflow as tf
import joblib
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv() 
# --- Configure Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key not found. Add it to your .env file as GEMINI_API_KEY=<your_key>")

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # or "gemini-1.5-flash" for faster output

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




# Load your trained model (adjust path as needed)
MODEL_PATH = "models/speech_emotion_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Optionally load label encoder if you saved one
LABEL_ENCODER_PATH = "models/label_encoder.pkl"
try:
    label_encoder = joblib.load(LABEL_ENCODER_PATH)
except Exception:
    label_encoder = None

# --- FEATURE EXTRACTION ---
def extract_features(file_path, mfcc=True, chroma=True, mel=True):
    """Extract MFCC, Chroma, and Mel features from audio file."""
    X, sample_rate = librosa.load(file_path, res_type="kaiser_fast", duration=3, offset=0.5)
    result = np.array([])
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
        result = np.hstack((result, mfccs))
    if chroma:
        stft = np.abs(librosa.stft(X))
        chroma_features = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
        result = np.hstack((result, chroma_features))
    if mel:
        mel_features = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
        result = np.hstack((result, mel_features))
    return result



# --- PREDICTION FUNCTION ---
def analyze_audio(file_path):
    """Use the trained model to predict emotion and CBT guidance."""
    try:
        features = extract_features(file_path)
        features = np.expand_dims(features, axis=0)
        prediction = model.predict(features)
        predicted_index = np.argmax(prediction)
        
        if label_encoder:
            emotion = label_encoder.inverse_transform([predicted_index])[0]
        else:
            # fallback emotion list (modify to match your dataset)
            emotion_classes = ["angry", "calm", "fearful", "happy", "sad", "surprised", "neutral"]
            emotion = emotion_classes[predicted_index]

        confidence = round(float(np.max(prediction)) * 100, 2)
        top_emotion = emotion[0]['label'].lower()

        # Step 2: Build CBT-based therapeutic prompt
        base_prompt = CBT_PROMPTS.get(
            top_emotion,
            f"The user’s detected emotion is {top_emotion}. Provide CBT-based empathetic guidance."
        )
        prompt = f"Detected emotion: {top_emotion}. {base_prompt} Use practical CBT steps and empathetic language."

        # Step 3: Generate response from Gemini
        response = gemini_model.generate_content(prompt)


        return {
            "transcription": "N/A",
            "sentiment": emotion,
            "score": confidence / 100,
            "response": response.text.strip() if response and response.text else "No response generated."
        }

    except Exception as e:
        return {"error": str(e)}

