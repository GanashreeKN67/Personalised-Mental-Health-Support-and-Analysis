import streamlit as st

# Page config
st.set_page_config(page_title="Mood Selection", layout="centered")

st.title("😃 EMOWELL - Select Your Mood")

st.write("### Please select your mood for today:")
st.markdown("""
    <style>
    .option-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 30px;
        margin-top: 40px;
    }

    .box {
        display: inline-block;
        background-color: #f0f4ff;
        border: 2px solid #4A90E2;
        border-radius: 15px;
        width: 120px;
        height: 120px;
        text-align: center;
        font-size: 40px;
        line-height: 240px;
        margin: 10px;
        transition: all 0.3s ease;
    }

    .box:hover {
        background-color: #4A90E2;
        color: white;
        cursor: pointer;
        transform: scale(1.08);
    }

    .action-box {
        background-color: #f5f7fa;
        border: 2px solid #4a90e2;
        border-radius: 15px;
        width: 220px;
        height: 100px;
        text-align: center;
        color: #333;
        font-size: 20px;
        font-weight: 600;
        line-height: 100px;
        margin: 10px;
        transition: all 0.3s ease;
    }

    .action-box:hover {
        background-color: #4A90E2;
        color: white;
        cursor: pointer;
        transform: scale(1.05);
    }

    .prompt-box {
        margin-top: 50px;
        background-color: #ffffff;
        border: 2px solid #ccc;
        border-radius: 10px;
        padding: 20px;
        text-align: left;
        font-size: 16px;
    }
            
    </style>
    """, unsafe_allow_html=True)

# List of moods with emojis
moods = {
    "😡 ANGER": "Anger",
    "😰 ANXIETY": "Anxiety",
    "😵 BIPOLAR": "Bipolar",
    "😞 DEPRESSION": "Depression",
    "😨 FEAR": "Fear",
    "🩸 SELF HARM": "Self Harm",
    "😴 INSOMIA": "Insomnia",
    "😔 LONELINESS": "Loneliness",
    "😱 PANIC ATTACK": "Panic Attack",
    "😶‍🌫️ PARANOIA": "Paranoia",
    "😖 PHOBIA": "Phobia",
    "😵‍💫 PSYCHOSIS": "Psychosis",
    "🧩 SCHIZOPHRENIA": "Schizophrenia",
    "💪 SELF CONFIDENCE": "Self Confidence",
    "🗣️ HEARING VOICES": "Hearing Voices",
    "⚖️ WEIGHT LOSS": "Weight Loss",
}


cols = st.columns(4)
selected_mood = None
for idx, (emoji, mood_value) in enumerate(moods.items()):
    with cols[idx % 4]:
        if st.button(emoji, use_container_width=True):
            selected_mood = mood_value



# Show next step if mood selected
if selected_mood:

    st.success(f"You selected mood: **{selected_mood}** ✅")

    st.title("🧠 EMOWELL - Choose an Action")

    # Create box-shaped clickable options
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧘 Get Guidance", key="action-btn-guidance", use_container_width=True):
            st.success("You selected: Get Guidance")

    with col2:
        if st.button("📊 Evaluate", key="action-btn-evaluate", use_container_width=True):
            st.success("You selected: Evaluate")

    # --- Prompt Box Section ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("### 💬 Enter your Prompt below:")
    prompt = st.text_area("Your message to Mentify Chatbot:", placeholder="Type your feelings, questions, or thoughts here...")

    if st.button("Send"):
        if prompt.strip():
            st.info(f"🤖 Mentify's Response: Analyzing your message — '{prompt}'")
        else:
            st.warning("Please type something before sending.")

    
