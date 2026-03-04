import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# 1. INITIAL SETUP
load_dotenv()
# RIGHT: Put the NAME of the variable from your .env file
api_key = os.getenv("GEMINI_API_KEY")

# Page Configuration
st.set_page_config(page_title="AI Career Mentor", page_icon="🎓", layout="centered")

# 2. API CONFIGURATION & MODEL PICKER
if api_key:
    genai.configure(api_key=api_key)
    
    # This block automatically finds a model that works for your key
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # Prefer flash if available, otherwise pick the first compatible one
        model_id = 'models/gemini-1.5-flash' if 'models/gemini-1.5-flash' in available_models else available_models[0]
        model = genai.GenerativeModel(model_id)
    except Exception as e:
        st.error(f"Could not initialize model: {e}")
else:
    st.error("API Key not found. Please check your .env file.")

# 3. USER INTERFACE
st.title("🎓 Smart Career Mentor")
st.markdown("""
    Welcome! This AI-powered tool analyzes your current skills and creates a 
    **30-day roadmap** to help you land your dream job.
""")

with st.container():
    st.subheader("Your Profile")
    col1, col2 = st.columns(2)
    
    with col1:
        skills = st.text_area("Current Skills", placeholder="e.g., Python, SQL, Laravel, HTML", height=100)
    with col2:
        target = st.text_input("Target Job Role", placeholder="e.g., Data Scientist, Backend Engineer")
        experience = st.selectbox("Experience Level", ["Student/Fresh Grad", "Junior (1-2 years)", "Mid-level", "Senior"])

# 4. THE LOGIC
if st.button("Generate My Roadmap", type="primary"):
    if not skills or not target:
        st.warning("Please enter both your skills and your target role.")
    else:
        with st.spinner(f"Consulting {model_id}..."):
            try:
                # Optimized Prompt Engineering
                prompt = f"""
                You are an expert Career Coach and Senior Technical Recruiter.
                
                User Context:
                - Current Skills: {skills}
                - Target Role: {target}
                - Experience Level: {experience}
                
                Please provide a detailed career roadmap in Markdown format:
                1. **Gap Analysis**: What are the top 3 technical skills they are missing?
                2. **Project Idea**: Suggest one unique portfolio project that uses their current skills AND the missing skills.
                3. **30-Day Learning Plan**: A week-by-week breakdown of what to study.
                4. **Interview Tip**: One specific technical concept they should master for this role.
                """
                
                response = model.generate_content(prompt)
                
                st.markdown("---")
                st.success("Roadmap Generated!")
                st.markdown(response.text)
                
                # Option to download/copy
                st.download_button("Download Roadmap as Text", response.text, file_name="career_roadmap.txt")
                
            except Exception as e:
                st.error(f"An error occurred during generation: {e}")

# 5. FOOTER
st.markdown("---")
st.caption("Powered by Gemini AI | Built with Streamlit")