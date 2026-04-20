import re
import spacy

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    # Lowercase
    text = text.lower()
    
    # Remove special characters
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    
    # Process with spaCy
    doc = nlp(text)
    
    # Lemmatization + remove stopwords
    tokens = [token.lemma_ for token in doc if not token.is_stop]
    
    return " ".join(tokens)