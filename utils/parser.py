from pdfminer.high_level import extract_text

def extract_resume_text(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"