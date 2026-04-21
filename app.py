import streamlit as st
from utils.parser import extract_resume_text
from utils.preprocess import preprocess_text, extract_skills
from utils.similarity import compute_similarity

# Load skills
with open("data/skills.txt") as f:
    skills_list = f.read().splitlines()

st.set_page_config(page_title="Resume Scanner", layout="centered")

st.title("📄 Resume Scanner using NLP")

# Upload resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job description input
jd = st.text_area("Paste Job Description")

if uploaded_file and jd:

    # Save uploaded file temporarily
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    # Extract and preprocess
    resume_text = extract_resume_text("temp.pdf")
    resume_clean = preprocess_text(resume_text)
    jd_clean = preprocess_text(jd)

    # Similarity score
    score = compute_similarity(resume_clean, jd_clean)

    # Extract skills
    resume_skills = extract_skills(resume_clean, skills_list)
    jd_skills = extract_skills(jd_clean, skills_list)

    # Missing skills
    missing = list(set(jd_skills) - set(resume_skills))

    # Skill match score
    matched_skills = set(resume_skills) & set(jd_skills)

    if len(jd_skills) > 0:
        skill_score = (len(matched_skills) / len(jd_skills)) * 100
    else:
        skill_score = 0

    # ===== DISPLAY RESULTS =====

    st.subheader(" Results")

    st.subheader(f"Text Similarity Score: {score:.2f}%")
    st.subheader(f"Skill Match Score: {skill_score:.2f}%")

    # Progress bar for skill match
    st.progress(int(skill_score))

    st.markdown("---")

    st.write("**Resume Skills:**")
    st.write(resume_skills)

    st.write("**JD Skills:**")
    st.write(jd_skills)

    st.write("**Missing Skills:**")
    st.write(missing)