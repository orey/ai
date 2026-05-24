'''
This module contains the prompts.
'''

KEYWORDS_PROMPT ='''Extract the core semantic concepts from the text for use in:
- ontology construction
- semantic graph building
- topic clustering
- graph RAG indexing

Rules:
- Return ONLY valid JSON.
- No markdown.
- Use canonical concept names.
- Prefer technical concepts and domain terms.
- Prefer noun phrases.
- Merge lexical variants and synonyms.
- Ignore filler vocabulary.
- Maximum 15 keywords.
- Score importance from 0 to 1.
- Text is starting after $$$ and finishes before £££

Format:
{
  "keywords": [
    {
      "term": "string",
      "score": float
    }
  ]
}

Text:
$$$
TEXT
£££'''

def generate_keywords_prompt(text):
    return KEYWORDS_PROMPT.replace("TEXT", text)



