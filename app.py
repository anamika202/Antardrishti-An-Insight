import streamlit as st
from google import genai

st.set_page_config(
    page_title="Antardrishti AI",
    page_icon="👁️",
    layout="centered"
)

st.title("👁️ Antardrishti AI")
st.caption("Empowering Inner Reflection, Cognitive Insights & Accessible Intelligence")

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key configure nahi hai! Streamlit Cloud Settings > Secrets me GEMINI_API_KEY add karein.")
    st.stop()

client = genai.Client(api_key=api_key)

mode = st.radio(
    "Select Mode:",
    ["🧘 Empathetic Mood Reflection", "📝 Text & Reasoning Analysis", "🖼️ Multimodal / Image Insight"],
    horizontal=False
)

if mode == "🧘 Empathetic Mood Reflection":
    st.subheader("Personal Reflective Journal")
    mood = st.selectbox(
        "Aap kaisa feel kar rahe hain? (Select Current Mood):",
        ["Calm / Shanti", "Overwhelmed / Pareshan", "Thoughtful / Chintan", "Energetic / Utsahi", "Anxious / Bechain", "Grateful / Aabhari"]
    )
    reflection_text = st.text_area("Apne vichar ya journal entry yahan likhiye:", placeholder="Aaj kaisa raha din? Kya chal raha hai dimag mein...")
    
    if st.button("Generate Empathetic Insight", type="primary"):
        if not reflection_text.strip():
            st.warning("Kripya apni reflection likhiye.")
        else:
            with st.spinner("Reflecting deeply with empathy..."):
                try:
                    system_prompt = (
                        f"You are Antardrishti, an empathetic, supportive, and non-judgmental reflective guide. "
                        f"The user's current mood is '{mood}'. "
                        f"Analyze the user's reflection, validate their emotions with warmth and emotional intelligence (EQ), "
                        f"and offer a gentle, practical perspective or a thoughtful question for self-growth."
                    )
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=[system_prompt, reflection_text]
                    )
                    st.success("Reflection Complete")
                    st.markdown("### 🌿 Antardrishti Insight:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

elif mode == "📝 Text & Reasoning Analysis":
    st.subheader("Cognitive Reasoning & Inquiry")
    user_prompt = st.text_area("Enter context, inquiry, or document summary:", placeholder="Type here...")
    
    if st.button("Generate Insight", type="primary"):
        if not user_prompt.strip():
            st.warning("Kripya input provide karein.")
        else:
            with st.spinner("Analyzing with Gemini..."):
                try:
                    response = client.models.generate_content(
                        model="gemini-3.6-flash",
                        contents=user_prompt
                    )
                    st.success("Analysis Complete")
                    st.markdown("### Output Insight:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

elif mode == "🖼️ Multimodal / Image Insight":
    st.subheader("Multimodal Perception")
    uploaded_file = st.file_uploader("Upload an image for analysis:", type=["jpg", "jpeg", "png"])
    image_prompt = st.text_input("Prompt for image:", value="Analyze this image and describe its key elements clearly.")
    
    if uploaded_file and st.button("Analyze Image", type="primary"):
        with st.spinner("Processing visual data..."):
            try:
                import PIL.Image
                img = PIL.Image.open(uploaded_file)
                st.image(img, caption="Uploaded Image", use_container_width=True)
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=[img, image_prompt]
                )
                st.success("Visual Analysis Complete")
                st.markdown("### Output Insight:")
                st.write(response.text)
            except Exception as e:
                st.error(f"Error: {e}")



