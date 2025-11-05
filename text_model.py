# text_model.py
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# --- Load environment variables ---
load_dotenv()

# --- Configure Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("❌ Gemini API key not found. Please add it to your .env file as GEMINI_API_KEY=<your_key>")

genai.configure(api_key=GEMINI_API_KEY)

print(genai.list_models())

# --- Load the Gemini model ---
gemini_model = genai.GenerativeModel("gemini-2.5-flash")  # you can also use "gemini-1.5-flash" for faster responses


# ============================================================
# 🧩 CBT THERAPY PROMPTS
# ============================================================
CBT_PROMPTS = {
    "anger": (
        "The user feels angry. As a CBT therapist, help them recognize triggers, validate their emotion, "
        "and suggest healthy coping strategies to release frustration. User note: '{user_note}'."
    ),
    "anxiety": (
        "The user feels anxious. As a CBT therapist, guide them to challenge irrational worries, focus on breathing, "
        "and use grounding techniques. User note: '{user_note}'."
    ),
    "bipolar": (
        "The user reports mood swings linked to bipolar experiences. Help them track triggers, maintain stability, "
        "and establish routines. User note: '{user_note}'."
    ),
    "depression": (
        "The user feels depressed or hopeless. Offer CBT-based help by identifying negative thinking, encouraging "
        "self-compassion, and suggesting small positive actions. User note: '{user_note}'."
    ),
    "fear": (
        "The user is feeling fearful. As a CBT therapist, explore what triggers the fear, challenge exaggerated thoughts, "
        "and guide them toward gradual exposure. User note: '{user_note}'."
    ),
    "self harm": (
        "The user expresses self-harm thoughts. As a CBT therapist, respond with empathy, prioritize safety, "
        "and suggest alternatives like journaling, mindfulness, or calling a friend. User note: '{user_note}'."
    ),
    "insomnia": (
        "The user struggles with insomnia. Apply CBT-I principles: challenge sleep-related worries, establish routine, "
        "and use relaxation techniques. User note: '{user_note}'."
    ),
    "loneliness": (
        "The user feels lonely. As a CBT therapist, validate their emotions and encourage social reconnection, hobbies, "
        "and reframing negative beliefs. User note: '{user_note}'."
    ),
    "panic attack": (
        "The user is having a panic attack. Provide CBT-based guidance: slow breathing, grounding, and cognitive reframing. "
        "Remind them that panic symptoms are temporary. User note: '{user_note}'."
    ),
    "paranoia": (
        "The user feels paranoid. As a CBT therapist, gently explore the evidence behind thoughts, teach grounding, "
        "and promote self-awareness. User note: '{user_note}'."
    ),
    "phobia": (
        "The user reports a phobia. Use CBT exposure and gradual desensitization. Encourage step-by-step confidence building. "
        "User note: '{user_note}'."
    ),
    "psychosis": (
        "The user reports psychotic-like experiences. As a CBT therapist, remain calm and empathetic. "
        "Help them distinguish between perceptions and thoughts, ensuring emotional safety. User note: '{user_note}'."
    ),
    "schizophrenia": (
        "The user mentions schizophrenia-related experiences. Encourage self-awareness, structure, and supportive routines. "
        "Use CBT to manage distressing thoughts. User note: '{user_note}'."
    ),
    "self confidence": (
        "The user struggles with self-confidence. Use CBT techniques to challenge self-critical thoughts and reinforce strengths. "
        "Encourage small achievements and affirmations. User note: '{user_note}'."
    ),
    "hearing voices": (
        "The user hears voices. As a CBT therapist, respond compassionately. Help them externalize voices, question their control, "
        "and practice grounding. User note: '{user_note}'."
    ),
    "weight loss": (
        "The user is focused on weight loss. Use CBT to promote body positivity, self-acceptance, and healthy behavior change. "
        "User note: '{user_note}'."
    )
}


# ============================================================
# 🧘‍♀️ GUIDANCE GENERATION (Gemini Only)
# ============================================================

def generate_guidance(user_mood: str, user_note: str = ""):
    """
    Generate empathetic CBT-guided response for the user's mood using Google Gemini.
    """
    mood = user_mood.lower()

    prompt = (
        f"You are a compassionate CBT therapist. "
        f"Your goal is to help the user using evidence-based CBT techniques. "
        f"User mood: {user_mood}. "
        f"User note: '{user_note}'. "
        "1. Validate the user's feelings.\n"
        "2. Identify and challenge negative thoughts.\n"
        "3. Suggest practical CBT coping strategies (e.g., journaling, thought records, behavioral experiments).\n"
        "4. Encourage small, achievable actions.\n"
        "5. End with a supportive, hopeful message.\n"
        "Avoid medical diagnosis. Do not give generic advice. Focus on CBT methods only.\n"
        "Example response for sadness: 'It's understandable to feel sad sometimes. Let's explore what thoughts are contributing to your sadness. Can you identify any negative beliefs? Try writing them down and challenging their accuracy. Consider engaging in a small activity you enjoy, even if it's brief. Remember, these feelings are temporary and you have the strength to cope.'\n"
    )

    try:
        response = gemini_model.generate_content(prompt)
        return response.text.strip() if response and response.text else "I'm here to help, but I couldn't generate a response right now."
    except Exception as e:
        return f"Error while generating response from Gemini: {e}"


# ============================================================
# 🧩 EVALUATION LOGIC (optional - keep from your old code)
# ============================================================

def load_mood_questions(mood: str):
    """Load questions for mood evaluation."""
    file_path = os.path.join("data", f"{mood.lower()}.json")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No question file found for mood: {mood}")
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["questions"]


def evaluate_responses(responses: dict):
    """Simple scoring logic for mood evaluation."""
    total_score = sum(responses.values())
    max_score = len(responses) * 3
    percentage = (total_score / max_score) * 100

    if percentage < 25:
        status = "Excellent mental well-being"
        tip = "Keep maintaining your positive habits and balanced routine!"
    elif percentage < 50:
        status = "Mild stress detected"
        tip = "Try relaxation techniques or talk with a close friend."
    elif percentage < 75:
        status = "Moderate emotional distress"
        tip = "Take breaks, rest well, and try journaling your thoughts."
    else:
        status = "High emotional stress"
        tip = "Reach out to a counselor or mental health professional."

    return {"score": round(percentage, 2), "status": status, "tip": tip}
