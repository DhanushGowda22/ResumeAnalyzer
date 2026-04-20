from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    
    return round(score * 100, 2)