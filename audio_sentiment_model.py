
# AUDIO TRANSCRIBE AND SENTIMENT ANALYSIS

import torch
import whisper
from transformers import pipeline
import os

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
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    print(f"Analyzing: {file_path}")
    transcription = asr_model.transcribe(file_path)

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
