from utils.parser import extract_resume_text
from utils.preprocess import preprocess_text

file_path = "sample_resume.pdf"

text = extract_resume_text(file_path)

clean_text = preprocess_text(text)

print("----- RAW TEXT -----")
print(text[:500])

print("\n----- CLEAN TEXT -----")
print(clean_text[:500])