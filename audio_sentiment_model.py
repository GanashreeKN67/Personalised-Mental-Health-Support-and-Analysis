
# AUDIO TRANSCRIBE AND SENTIMENT ANALYSIS

import torchaudio
from transformers import pipeline
from transformers import pipeline as hf_pipeline
import torch
import streamlit as st

asr_model = pipeline(
    "automatic-speech-recognition",
    model="facebook/wav2vec2-base-960h"
)


def analyze_audio(file_path):
    
    waveform, sample_rate = torchaudio.load(file_path)

    language_code = st.selectbox("Choose language:", ["en", "hi", "ta", "te", "kn"])
    result = asr_model(
        {"array": waveform.squeeze().numpy(), "sampling_rate": sample_rate},
        generate_kwargs={"language": language_code}
    )

    # Hugging Face pipeline expects raw waveform + sampling rate
    result = asr_model({"array": waveform.squeeze().numpy(), "sampling_rate": sample_rate },generate_kwargs={"language": "en"})
    text = result["text"].strip()

    # The rest of your sentiment + response pipeline remains same
    
    sentiment_model = hf_pipeline(
        "sentiment-analysis",
        model="cardiffnlp/twitter-roberta-base-sentiment",
        return_all_scores=True
    )
    response_gen = hf_pipeline("text-generation", model="gpt2", max_length=80, pad_token_id=50256)

    sentiment_scores = sentiment_model(text)[0]
    sentiment_scores.sort(key=lambda x: x['score'], reverse=True)
    top = sentiment_scores[0]
    label, score = top["label"], top["score"]

    prompt = f"User said: '{text}'. The sentiment is {label}. Reply empathetically."
    response = response_gen(prompt)[0]["generated_text"]

    return {
        "transcription": text,
        "sentiment": label,
        "score": round(float(score), 3),
        "response": response
    }
 
''' # AUDIO TRANSCRIBE AND SENTIMENT ANALYSIS
# ---------------------------------------
# This version uses Hugging Face's Speech-to-Text model for transcription
# No FFmpeg or Whisper needed!

import os
import torch
from transformers import pipeline

# ====== LOAD MODELS ======

# 🎤 1. Speech-to-Text (Hugging Face ASR)
asr_model = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny",   # or "facebook/wav2vec2-base-960h"
)

# 💬 2. Sentiment Analysis
sentiment_model = pipeline(
    "sentiment-analysis",
    model="cardiffnlp/twitter-roberta-base-sentiment",
    return_all_scores=True
)

# 🤖 3. Response Generation
response_generator = pipeline(
    "text-generation",
    model="gpt2",
    max_length=80,
    pad_token_id=50256
)


# ====== MAIN FUNCTION ======

def analyze_audio(file_path):
    """Transcribe, analyze sentiment, and generate empathetic response."""

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    print(f"\n🔍 Analyzing audio: {file_path}")

    # 1️⃣ Transcribe using Hugging Face model
    print("🎧 Transcribing with Hugging Face ASR model...")
    result = asr_model(file_path)
    text = result["text"].strip()

    # 2️⃣ Sentiment analysis
    print("💬 Analyzing sentiment...")
    sentiment_scores = sentiment_model(text)[0]
    sentiment_scores.sort(key=lambda x: x["score"], reverse=True)
    top_sentiment = sentiment_scores[0]
    sentiment_label = top_sentiment["label"]
    sentiment_score = top_sentiment["score"]

    # 3️⃣ Generate empathetic response
    print("🤖 Generating response...")
    prompt = f"User said: '{text}'. The sentiment is {sentiment_label}. Reply empathetically."
    response = response_generator(prompt)[0]["generated_text"]

    return {
        "transcription": text,
        "sentiment": sentiment_label,
        "score": round(float(sentiment_score), 3),
        "response": response
    }
'''