# model_utils.py
import whisper
from transformers import pipeline
from deepface import DeepFace
import easyocr
import tempfile
from PIL import Image
import pyttsx3
import io


# load models lazily
_whisper_model = None
_text_pipe = None
_ocr_reader = None
_tts_engine = None





def get_whisper():
    global _whisper_model
    if _whisper_model is None:
        _whisper_model = whisper.load_model('base')
    return _whisper_model




def transcribe_audio(file_obj):
    # file_obj: streamlit UploadedFile or file-like
    model = get_whisper()
    # save to temp file
    tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    data = file_obj.read()
    tmp.write(data)
    tmp.flush()
    res = model.transcribe(tmp.name)
    return res.get('text','')





def load_image_models():
    global _face_emotion_model, _ocr_reader
    if _face_emotion_model is None:
        _face_emotion_model = pipeline("image-classification", model="dima806/facial_emotions_image_detection")
    if _ocr_reader is None:
        _ocr_reader = easyocr.Reader(["en"], gpu=False)
    return _face_emotion_model, _ocr_reader




def ocr_image(image):
    """Extract visible text from image using EasyOCR."""
    _, reader = load_image_models()
    if hasattr(image, "read"):  # Streamlit UploadedFile
        data = image.read()
        img = Image.open(io.BytesIO(data)).convert("RGB")
        tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        img.save(tmp.name)
        result = reader.readtext(tmp.name, detail=0)
    else:
        result = reader.readtext(image, detail=0)
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

# AUDIO TRANSCRIBE AND

# Load Whisper for speech-to-text
asr_model = whisper.load_model("base")  # "tiny", "base", "small", etc.

# Load sentiment analysis model
sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment",
    return_all_scores=True
)

# Load text generation model (small local one for example)
response_generator = pipeline(
    "text-generation",
    model="gpt2",
    max_length=60
)

def analyze_audio(file_path):
    """Takes an audio file, transcribes, analyzes sentiment, and generates response."""
    
    # 1️⃣ Transcribe audio
    print("Transcribing...")
    transcription = asr_model.transcribe(file_path)
    text = transcription["text"].strip()

    # 2️⃣ Sentiment analysis
    print("Analyzing sentiment...")
    sentiment_scores = sentiment_model(text)[0]
    # Sort by score
    sentiment_scores.sort(key=lambda x: x['score'], reverse=True)
    top_sentiment = sentiment_scores[0]

    sentiment_label = top_sentiment["label"]
    sentiment_score = top_sentiment["score"]

    # 3️⃣ Generate empathetic response
    print("Generating response...")
    prompt = f"User said: '{text}'. The sentiment is {sentiment_label}. Reply empathetically."
    response = response_generator(prompt)[0]["generated_text"]

    return {
        "transcription": text,
        "sentiment": sentiment_label,
        "score": round(float(sentiment_score), 3),
        "response": response
    }
