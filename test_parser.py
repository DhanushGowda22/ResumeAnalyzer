from utils.parser import extract_resume_text
from utils.preprocess import preprocess_text, extract_skills
from utils.similarity import compute_similarity

# Load skills
with open("data/skills.txt") as f:
    skills_list = f.read().splitlines()


file_path = "sample_resume.pdf"

# Resume
resume_text = extract_resume_text(file_path)
resume_clean = preprocess_text(resume_text)

# Job Description
jd = """
Looking for a Machine Learning Engineer with experience in Python, 
Deep Learning, NLP, and Scikit-learn. 
Experience with FastAPI and deployment is a plus.
"""

jd_clean = preprocess_text(jd)

# Similarity
score = compute_similarity(resume_clean, jd_clean)

# Skills extraction
resume_skills = extract_skills(resume_clean, skills_list)
jd_skills = extract_skills(jd_clean, skills_list)

# Missing skills
missing_skills = list(set(jd_skills) - set(resume_skills))

print("MATCH SCORE:", score, "%")
print("\nResume Skills:", resume_skills)
print("\nJD Skills:", jd_skills)
print("\nMissing Skills:", missing_skills)