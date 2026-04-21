import streamlit as st
from utils.parser import extract_resume_text
from utils.preprocess import preprocess_text, extract_skills
from utils.similarity import compute_similarity

st.markdown("""
<style>
.big-font {
    font-size:22px !important;
    font-weight:600;
}
.score-box {
    padding:15px;
    border-radius:10px;
    background-color:#1f2937;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# Load skills
with open("data/skills.txt") as f:
    skills_list = f.read().splitlines()

st.set_page_config(page_title="Resume Scanner", layout="centered")

st.title("📄 AI-Powered Resume Analyzer (ATS Scoring System)")

# Upload_resume
uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

# Job_description input
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

    # ===== ATS SCORE =====
    ats_score = (0.6 * skill_score) + (0.4 * score)

    # ===== DISPLAY RESULTS =====
    st.subheader("Results")

    # ATS SCORE (MAIN)
    st.markdown("## ATS Score")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.markdown(
            f"<h1 style='margin:0'>{ats_score:.2f}%</h1>"
            f"<p style='color:gray; margin:0'>Score</p>",
            unsafe_allow_html=True
        )

    # FULL WIDTH BAR BELOW (not inside column)
    st.progress(int(ats_score))

    # Interpretation
    if ats_score >= 80:
        st.success("Strong match! High chances of shortlist")
    elif ats_score >= 60:
        st.warning("Good match, but can be improved")
    else:
        st.error("Low match. Resume needs improvement")

    # Breakdown scores
    st.subheader(f"Content Relevance: {score:.2f}%")
    st.subheader(f"Skill Match: {skill_score:.2f}%")

    st.markdown("---")
    st.subheader("Keyword Frequency in Resume")

    keyword_counts = {skill: resume_clean.count(skill) for skill in jd_skills}

    st.write(keyword_counts)


    st.markdown("---")

    # Skills display
    st.write("**Resume Skills:**")
    st.write(resume_skills)

    st.write("**JD Skills:**")
    st.write(jd_skills)

    st.markdown("---")

    if missing:
        st.error("⚠️ Missing Skills")
        st.write(missing)

        st.info("Suggestions to improve your resume:")
        for skill in missing:
            st.write(f"- Add projects or experience related to **{skill}**")
    else:
        st.success("Your resume matches all key job skills!")

    st.markdown("---")
    st.subheader(" Resume Improvement Tips")

    if score < 50:
        st.write("- Use more keywords from the job description")
        st.write("- Align your experience with required skills")
        st.write("- Add measurable achievements")
    elif score < 75:
        st.write("- Improve wording using job description terms")
        st.write("- Highlight relevant projects")
    else:
        st.write("- Strong resume! Fine-tune formatting for ATS")