import streamlit as st
from text_model import generate_guidance, load_mood_questions, evaluate_responses
from auth import save_user_data, load_user_data

#Login check
if "user" not in st.session_state or st.session_state["user"] is None:
    st.query_params["page"] = "Login"
    st.rerun()


# Page config
st.set_page_config(page_title="Mood Selection", layout="centered")

st.title("😃 EMOWELL - Select Your Mood")

st.write("### Please select your mood for today:")


if "selected_mood" not in st.session_state:
    st.session_state.selected_mood = None

def set_mood(mood):
    st.session_state.selected_mood = mood

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
for idx, (emoji, mood_value) in enumerate(moods.items()):
    with cols[idx % 4]:
        # use on_click to set session state so selection persists
        st.button(emoji, key=f"mood-{idx}", on_click=set_mood, args=(mood_value,), use_container_width=True)

selected_mood = st.session_state.selected_mood



# Show next step if mood selected
if selected_mood:

    st.success(f"You selected mood: **{selected_mood}** ✅")
    st.title("🧠 EMOWELL - Choose an Action")

    # Create box-shaped clickable options
    col1, col2 = st.columns(2)

    with col1:
        if st.button("🧘 Get Guidance", key="action-btn-guidance", use_container_width=True):
            st.session_state.last_action = "guidance"
            st.rerun()

    with col2:
        if st.button("📊 Evaluate", key="action-btn-evaluate", use_container_width=True):
            st.session_state.last_action = "evaluate"
            st.rerun()

    #Handle action selection
    action = st.session_state.get("last_action")

    if action == "guidance":
        st.subheader("Guidance")
        note = st.text_area("Optional note (more context helps):", key="guidance_note")
        if st.button("Send", key="send_guidance"):
            if note.strip() or selected_mood:
                with st.spinner("Generating guidance..."):
                    try:
                        response = generate_guidance(user_mood=selected_mood, user_note=note)
                        st.markdown("**🤖 EMOWELL Response:**")
                        st.write(response)
                        # Optionally save per-user
                        try:
                            if "user" in st.session_state and st.session_state["user"]:
                                save_user_data(st.session_state["user"], "last_response", response)
                        except Exception:
                            pass
                    except Exception as e:
                        st.error(f"Guidance generation failed: {e}")
            else:
                st.warning("Please add a note or ensure a mood is selected.")

    elif action == "evaluate":
        st.subheader("Self-evaluation")
        try:
            questions = load_mood_questions(selected_mood)
            st.info(f"Answer the following questions related to **{selected_mood}** mood:")
        except FileNotFoundError:
            st.error(f"No question file found for mood '{selected_mood}'. Please add {selected_mood.lower()}.json in data/")
            st.stop()

        # Display questions inside a form
        with st.form("evaluation_form"):
            user_answers = {}
            for i, q in enumerate(questions):
                # Show question and options
                choice = st.radio(
                    label=q["question"],
                    options=list(q["options"].keys()),
                    key=f"{selected_mood}_{i}",
                    horizontal=True
                )
                # Save user choice -> score
                user_answers[q["question"]] = q["options"][choice]

            submitted = st.form_submit_button("🧩 Evaluate")

        # Handle evaluation
        if submitted:
            try:
                result = evaluate_responses(user_answers)
                st.markdown(f"### 🧾 Your Evaluation Result")
                st.write(f"**Score:** {result['score']}%")
                st.success(result['status'])
                st.info(result['tip'])
            except Exception as e:
                st.error(f"Evaluation failed: {e}")


    # --- Prompt Box Section ---
    st.markdown("<br><hr>", unsafe_allow_html=True)
    st.markdown("### 💬 Enter your Prompt below:")
    prompt = st.text_area("Your message to Mentify Chatbot:", placeholder="Type your feelings, questions, or thoughts here...")

    if st.button("Send"):
        if prompt.strip():
            with st.spinner("Generating response..."):
                try:
                    response = generate_guidance(user_mood=selected_mood or "Neutral", user_note=prompt)
                    st.markdown("**🤖 EMOWELL Response:**")
                    st.write(response)
                except Exception as e:
                    st.error(f"Failed to generate response: {e}")
        else:
            st.warning("Please type something before sending.")

    
