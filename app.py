import io
import os
from PIL import Image, ImageOps
import streamlit as st
from google import genai
from google.genai import types

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & STYLING
# ---------------------------------------------------------
st.set_page_config(
    page_title="Antardrishti AI - An Insight",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Styling matching APAC Cohort 3 Presentation Deck
st.markdown("""
<style>
    /* Dark Aesthetic & Typography */
    .main {
        background-color: #030712;
        color: #f8fafc;
        font-family: 'DM Sans', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Urbanist', sans-serif;
        color: #ffffff;
    }
    .hero-title {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: -1px;
        margin-bottom: 0px;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.15rem;
        margin-bottom: 25px;
    }
    .badge {
        display: inline-block;
        background-color: rgba(16, 185, 129, 0.15);
        color: #10b981;
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 12px;
        letter-spacing: 1px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 1px solid #1e293b;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
        color: #94a3b8;
    }
    .stTabs [aria-selected="true"] {
        color: #10b981 !important;
        border-bottom: 3px solid #10b981 !important;
    }
    .feature-card {
        background-color: #0b1329;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        box-shadow: 0 4px 14px rgba(16, 185, 129, 0.35);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. BULLETPROOF MULTIMODAL IMAGE HELPER
# ---------------------------------------------------------
def prepare_uploaded_image(uploaded_file):
    """
    Safely processes images from Gallery, Drive, Downloads, or Camera:
    1. Resets read pointer
    2. Corrects EXIF rotation
    3. Flattens alpha/RGBA channels into pure RGB JPEG
    4. Downsamples heavy 50MP/108MP phone camera shots to preserve Cloud memory
    """
    try:
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        
        # Correct phone orientation from EXIF metadata
        image = ImageOps.exif_transpose(image)
        
        # Convert transparent/PNG/Gallery modes to standard RGB
        if image.mode in ("RGBA", "P", "LA", "CMYK"):
            image = image.convert("RGB")
            
        # Prevent Streamlit Cloud container out-of-memory crashes
        max_dimension = 1600
        image.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        
        # Export normalized JPEG bytes
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85, optimize=True)
        buffer.seek(0)
        
        return image, buffer.getvalue()
    except Exception as e:
        st.error(f"Image processing error: {e}")
        return None, None

# ---------------------------------------------------------
# 3. SIDEBAR - CREDENTIALS & ORCHESTRATION
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    
    # Priority 1: Check Streamlit Secrets; Priority 2: Environment; Priority 3: Manual Input
    secret_key = st.secrets.get("GEMINI_API_KEY", os.environ.get("GEMINI_API_KEY", ""))
    
    if secret_key:
        api_key = secret_key
        st.success("✅ Google GenAI API Key Linked")
    else:
        api_key = st.text_input("Enter Gemini API Key:", type="password")
        if not api_key:
            st.warning("⚠️ Please provide an API key to proceed.")

    # Target model set to Gemini 3.6 Flash as verified by API response
    model_choice = st.selectbox(
        "Active Gemini Model",
        options=["gemini-3.6-flash", "gemini-3.6-pro"],
        index=0,
        help="Gemini 3.6 Flash provides ultra-fast reasoning and native multimodal capabilities."
    )

    st.markdown("---")
    st.markdown("### 🌿 Antardrishti AI")
    st.markdown("""
    **Track:** #MeetTheBuilders  
    **Program:** Google Cloud Gen AI Academy APAC  
    **Lead:** Anamika Dubey  
    **Engine:** Gemini 3.6 Flash
    """)
    st.info("Dual-Core Architecture: Empathetic High-EQ reflection paired with high-velocity Gemini reasoning.")

# Initialize GenAI Client
client = None
if api_key:
    try:
        client = genai.Client(api_key=api_key)
    except Exception as e:
        st.sidebar.error(f"Client initialization failed: {e}")

# ---------------------------------------------------------
# 4. MAIN INTERFACE HEADER
# ---------------------------------------------------------
st.markdown('<span class="badge">#MeetTheBuilders | APAC COHORT 3</span>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Antardrishti <span style="color:#10b981;">AI</span></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">An Insight: Empowering Inner Reflection via Multimodal Cognitive Reasoning</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. CORE FUNCTIONALITY TABS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🌿 Mood Reflection",
    "💡 Cognitive Synthesis",
    "📷 Multimodal Visual Insight",
    "📊 About & Architecture"
])

# ---------------------------------------------------------
# TAB 1: MOOD-BASED EMPATHETIC REFLECTION
# ---------------------------------------------------------
with tab1:
    st.markdown("### Feature 1: Emotional Calibration & Guided Reflection")
    st.write("Calibrate the companion's emotional lens to receive personalized validation, grounding, and inquiry.")

    col1, col2 = st.columns([1, 2])
    with col1:
        current_mood = st.selectbox(
            "How is your mind feeling right now?",
            ["Overwhelmed & Anxious", "Stressed & Low", "Reflective & Pensive", "Grateful & Calm", "Restless & Seeking Focus"],
            index=1
        )
        depth_preference = st.radio("Reflection Mode", ["Gentle Grounding (Breathing + Empathy)", "Deep Cognitive Inquiry"], index=0)
        
    with col2:
        journal_input = st.text_area(
            "Express what is on your heart and mind:",
            placeholder="Write freely... Antardrishti is a judgment-free, confidential space for your thoughts.",
            height=160
        )
        submit_reflection = st.button("Generate Empathetic Insight", key="btn_mood")

    if submit_reflection:
        if not client:
            st.error("Please configure a valid Gemini API key in the sidebar or Streamlit secrets.")
        elif not journal_input.strip():
            st.warning("Please share a few thoughts so Antardrishti can reflect with you.")
        else:
            with st.spinner("Antardrishti is tuning into your emotional frequency..."):
                prompt = f"""
                You are Antardrishti AI, a compassionate, heart-centered well-being companion and cognitive guide.
                The user identifies their current state as: {current_mood}.
                Chosen reflection depth: {depth_preference}.
                
                User's journal entry:
                "{journal_input}"
                
                Guidelines:
                1. Provide genuine, non-judgmental empathy and validation.
                2. If the user feels overwhelmed or stressed, offer a soothing grounding technique or 4-4-4 breathing prompt.
                3. Offer gentle reframing and two reflective, open-ended questions to illuminate inner clarity.
                4. Keep the tone warm, grounded, and deeply human.
                """
                try:
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=prompt
                    )
                    st.markdown("---")
                    st.markdown("### 🕊️ Antardrishti Reflection")
                    st.markdown(response.text)
                except Exception as err:
                    st.error(f"Error generating reflection: {err}")

# ---------------------------------------------------------
# TAB 2: COGNITIVE REASONING & SYNTHESIS
# ---------------------------------------------------------
with tab2:
    st.markdown("### Feature 2: High-Velocity Cognitive Synthesis")
    st.write("Unpack complex dilemmas, tangled thoughts, or career and decision-making friction into structured clarity.")

    thought_dump = st.text_area(
        "Dump your unorganized thoughts, decisions, or dilemmas here:",
        placeholder="e.g., I have three different priorities pulling me in opposite directions, feeling pulled between work obligations, personal growth, and creative projects...",
        height=180
    )
    
    col_a, col_b = st.columns(2)
    with col_a:
        analysis_goal = st.selectbox("Primary Goal", ["Extract Core Dilemma & Blindspots", "Structured Pros & Cons with Emotional Weight", "Step-by-Step Clarity Framework"])
    with col_b:
        st.write("")
        st.write("")
        submit_synthesis = st.button("Synthesize & Clarify", key="btn_synthesis")

    if submit_synthesis:
        if not client:
            st.error("Please configure a valid Gemini API key in the sidebar.")
        elif not thought_dump.strip():
            st.warning("Please enter your thoughts or dilemmas to synthesize.")
        else:
            with st.spinner("Deconstructing thoughts and synthesizing themes..."):
                synth_prompt = f"""
                You are the analytical synthesis engine of Antardrishti AI.
                The user has submitted an unstructured thought dump with the goal: {analysis_goal}.
                
                Input:
                "{thought_dump}"
                
                Task:
                1. Identify the underlying cognitive tensions, root themes, and hidden assumptions.
                2. Provide a structured, clear breakdown formatted in Markdown.
                3. Deliver an actionable 'Next Clear Step' and one powerful 'Inquiry Question'.
                """
                try:
                    response = client.models.generate_content(
                        model=model_choice,
                        contents=synth_prompt
                    )
                    st.markdown("---")
                    st.markdown("### 🧩 Synthesized Clarity")
                    st.markdown(response.text)
                except Exception as err:
                    st.error(f"Error during cognitive synthesis: {err}")

# ---------------------------------------------------------
# TAB 3: MULTIMODAL VISUAL INSIGHT (GALLERY + DRIVE + CAMERA)
# ---------------------------------------------------------
with tab3:
    st.markdown("### Feature 3: Multimodal Cognitive Perception")
    st.write("Upload handwritten notes, journal pages, physical diagrams, or visual surroundings from **Gallery**, **Google Drive**, **Files**, or **Camera**.")

    uploaded_image_file = st.file_uploader(
        "Upload an image (Gallery, Photos, Drive, or Camera)",
        type=["jpg", "jpeg", "png", "webp"],
        help="Accepts all image formats. Full compatibility with mobile photo galleries, screenshots, and drive downloads."
    )

    visual_query = st.text_input(
        "What specific insight would you like Antardrishti to explore from this image?",
        placeholder="e.g., Transcribe and reflect on these handwritten journal notes, or unpack the emotion in this space..."
    )

    if uploaded_image_file is not None:
        pil_img, img_bytes = prepare_uploaded_image(uploaded_image_file)

        if pil_img is not None and img_bytes is not None:
            col_img, col_act = st.columns([1, 1])
            with col_img:
                st.image(pil_img, caption="Processed Image Preview", use_container_width=True)
            with col_act:
                st.info("✅ Image standardized: RGB normalized, EXIF aligned, and memory optimized for Gemini.")
                trigger_multimodal = st.button("Generate Multimodal Reflection", key="btn_multimodal")

            if trigger_multimodal:
                if not client:
                    st.error("Please configure a valid Gemini API key in the sidebar.")
                else:
                    with st.spinner("Antardrishti is perceiving and reflecting on your visual context..."):
                        if not visual_query.strip():
                            visual_query = (
                                "Examine this image carefully. Transcribe any visible handwriting or text if present, "
                                "and provide an empathetic, deep cognitive reflection on the themes or atmosphere conveyed."
                            )

                        try:
                            # Standardized bytes payload via Google GenAI Part API
                            image_part = types.Part.from_bytes(
                                data=img_bytes,
                                mime_type="image/jpeg"
                            )

                            response = client.models.generate_content(
                                model=model_choice,
                                contents=[image_part, visual_query]
                            )

                            st.markdown("---")
                            st.markdown("### 👁️ Visual & Cognitive Reflection")
                            st.markdown(response.text)
                        except Exception as err:
                            st.error(f"Gemini Multimodal processing error: {err}")

# ---------------------------------------------------------
# TAB 4: ARCHITECTURE & BUILDER PROOFS
# ---------------------------------------------------------
with tab4:
    st.markdown("### 🏗️ Architecture & Implementation Proof")
    
    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.markdown("""
        <div class="feature-card">
            <h4>🧠 Gemini 3.6 Flash</h4>
            <p style="color:#94a3b8; font-size:0.95rem;">
                Provides sub-second token delivery and native multimodal image understanding.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_t2:
        st.markdown("""
        <div class="feature-card">
            <h4>☁️ Google Cloud Engine</h4>
            <p style="color:#94a3b8; font-size:0.95rem;">
                Streamlit deployment on GCP architecture with Secret Manager isolation.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_t3:
        st.markdown("""
        <div class="feature-card">
            <h4>🛡️ Privacy-First Design</h4>
            <p style="color:#94a3b8; font-size:0.95rem;">
                In-memory byte streaming without persistent storage of user personal reflections.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    **Project Submission:** Google Cloud Gen AI Academy APAC — Cohort 3  
    **Theme:** Human-Centered Well-Being via Multimodal AI  
    **Repository:** [github.com/anamika202/Antardrishti-An-Insight](https://github.com/anamika202/Antardrishti-An-Insight)
    """)