import os
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
import re


def extract_keywords_from_file(filepath, top_n=50):
    """Extract top N keywords from a single text file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return []

    # Simple tokenizer: lowercase, remove non-alpha chars, split on whitespace
    words = re.findall(r'\b[a-z]+\b', text.lower())

    if not words:
        return []

    # Use TF-IDF to score keywords
    vectorizer = TfidfVectorizer(
        max_features=top_n * 3,  # keep a buffer for filtering
        stop_words='english',     # remove common English stop words
        min_df=0.95,
        max_df=1               # ignore overly common words
    )

    try:
        tfidf_matrix = vectorizer.fit_transform([' '.join(words)])
        feature_names = vectorizer.get_feature_names_out()

        # Get top N keywords by TF-IDF score
        scores = tfidf_matrix.toarray()[0]
        top_indices = scores.argsort()[::-1][:top_n]
        keywords = [(feature_names[i], float(scores[i])) for i in top_indices if scores[i] > 0]

        return [kw[0] for kw in keywords]
    except Exception as e:
        print(f"Exception raised: {e}")
        return []



def main():
    # Example usage
    directory = 'C:\\ct\\c\\'  # Change to your directory path
    top_n = 50       # Number of keywords per file

    f_k = {} # {id1: [file : [kw1, kw2, ...]], ... }
    global_keywords = {} # {kw1 : 12, kw2 : 45, ... }
    index = {} # {kw1: [id1,id2,], ...}

    count = 0
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt"):
                print(f"Treating: , id = {count}, {file}", flush=True)
                filepath = os.path.join(root, file)
                keywords = extract_keywords_from_file(filepath, top_n)
                # 1. record file id, file and keywords
                f_k[count] = [file, keywords]
                # 2. count keywords
                for k in keywords:
                    if k in global_keywords:
                        global_keywords[k] += 1
                    else:
                        global_keywords[k] = 1
                # 3 create the index
                for k in keywords:
                    if k in index:
                        index[k].append(count)
                    else:
                        index[k] = [count]
                # 4.go to next file
                count += 1
    print(f"Nb of files treated: {count}, nb of files in f_k: {len(f_k)}")
    print(f"Nb of global keywords: {len(global_keywords)}")
    print(f"Index\n{index}")
    


if __name__ == '__main__':
    main()
    
