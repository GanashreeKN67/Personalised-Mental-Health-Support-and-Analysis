
import random
import json
from transformers import pipeline

# ========== Load or define your evaluation question bank ==========
# Example structure; you can load from JSON dataset if available.
QUESTION_BANK = [
    {
        "question": "How often do you feel overwhelmed by daily tasks?",
        "options": {"Rarely": 0, "Sometimes": 1, "Often": 2, "Almost always": 3},
    },
    {
        "question": "How well are you sleeping lately?",
        "options": {"Very well": 0, "Somewhat well": 1, "Poorly": 2, "Very poorly": 3},
    },
    {
        "question": "Do you find it hard to concentrate during work or study?",
        "options": {"Never": 0, "Occasionally": 1, "Frequently": 2, "Always": 3},
    },
]

# ========== Load your LLM for guidance (Llama 2 / local / Hugging Face) ==========
_guidance_model = None

def _get_guidance_model():
    global _guidance_model
    if _guidance_model is None:
        try:
            # Prefer a lightweight generator to avoid long/hanging loads during import
            _guidance_model = pipeline(
                "text-generation",
                model="distilgpt2",
                max_length=200,
                temperature=0.8,
                pad_token_id=50256
            )
        except Exception:
            # final fallback to gpt2
            _guidance_model = pipeline(
                "text-generation",
                model="gpt2",
                max_length=200,
                temperature=0.8,
                pad_token_id=50256
            )
    return _guidance_model
# ============================================================
# 1️⃣ GUIDANCE MODE
# ============================================================

def generate_guidance(user_mood: str, user_note: str = ""):
    """Generate empathetic guidance for the user's mood."""
    prompt = (
        f"The user feels {user_mood}. "
        f"User note: '{user_note}'. "
        f"As a compassionate mental-health assistant, give supportive advice and coping tips."
    )

    model = _get_guidance_model()
    # call with a spinner in the UI (handled in Text.py) — keep generation params here minimal
    out = model(prompt, max_length=200)
    response = out[0].get("generated_text", "").strip()
    # remove the prompt echo if the model repeats it (simple heuristic)
    if response.startswith(prompt):
        response = response[len(prompt):].strip()
    return response
# ============================================================
# 2️⃣ EVALUATION MODE
# ============================================================

import json
import os

def load_mood_questions(mood: str):
    """Load the question set for the selected mood."""
    file_path = os.path.join("data", f"{mood.lower()}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No question file found for mood: {mood}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    questions = []
    for q in data["questions"]:
        opts = q["options"]

        # ✅ If options are list like "Rarely+0", convert to dict {"Rarely":0}
        if isinstance(opts, list):
            option_dict = {}
            for o in opts:
                if "+" in o:
                    text, score = o.split("+")
                    option_dict[text.strip()] = int(score)
                else:
                    option_dict[o.strip()] = 0
            q["options"] = option_dict

        questions.append(q)

    return questions


def evaluate_responses(responses: dict):
    """
    Calculate mental-health score and feedback.
    responses: dict mapping question -> selected score (int)
    """
    total_score = sum(responses.values())
    max_score = len(responses) * 3
    percentage = (total_score / max_score) * 100

    if percentage < 25:
        status = "Excellent mental well-being"
        tip = "Keep maintaining your positive habits and balanced routine!"
    elif percentage < 50:
        status = "Mild stress detected"
        tip = "Practice relaxation and stay socially connected."
    elif percentage < 75:
        status = "Moderate emotional distress"
        tip = "Take breaks, rest well, and consider talking to someone you trust."
    else:
        status = "High emotional stress"
        tip = "Reach out to a counselor or mental health professional for support."

    return {
        "score": round(percentage, 2),
        "status": status,
        "tip": tip
    }

