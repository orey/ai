import spacy


filepath = "C:\\ct\\c\\GREECE\\01 - Contract PDF 29-08-03\\HELLENIC CONTRACT English version with PRICES.pdf.txt"


def extract_keywords_spacy(text, top_n=10):
    """Extract keywords using spaCy's POS tagging and noun chunks."""
    
    # Process the text
    doc = nlp(text)
    
    # Stopwords list from spaCy
    stopwords = set(nlp.Defaults.stop_words)
    
    keywords = []
    
    # Method 1: Extract noun phrases (noun chunks)
    for chunk in doc.noun_chunks:
        # Filter short chunks and those with only stopwords
        if len(chunk.text.split()) <= 3 and not all(word.text.lower() in stopwords for word in chunk):
            keywords.append(chunk.text.lower())
    
    # Method 2: Extract named entities
    for ent in doc.ents:
        if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT']:  # Common entity types
            keywords.append(ent.text.lower())
    
    # Method 3: Extract adjectives and nouns (content words)
    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and not token.is_stop and len(token.text) > 2:
            keywords.append(token.text.lower())
    
    # Count frequency and get top keywords
    keyword_counts = Counter(keywords)
    top_keywords = keyword_counts.most_common(top_n)
    
    return top_keywords

with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

    nlp = spacy.load("en_core_web_sm")
    keywords = extract_keywords_spacy(text, top_n=25)

    print(keywords)
