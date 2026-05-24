import os
import sys
sys.path.append('.')
from tools10 import interrupt

MAX_CHAR = 4000

DOCX_SAMPLE = ".\\data\\source.docx.txt"
SOURCE = "C:\\c\\oreyboulot-NHI"


#------------------------------------------------- chunk_text
def chunk_text(text, max_chars=MAX_CHAR, overlap=1):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    chunks = []
    current = []

    current_size = 0

    for para in paragraphs:
        if current_size + len(para) > max_chars and current:
            chunks.append("\n\n".join(current))

            current = current[-overlap:] if overlap else []
            current_size = sum(len(x) for x in current)

        current.append(para)
        current_size += len(para)

    if current:
        chunks.append("\n\n".join(current))

    return chunks


#------------------------------------------------- sample of complex loop
def explore_and_chunk():
     for root, dirs, files in os.walk(SOURCE):
         for f in files:
             if f.endswith(".docx.txt"):
                 with open(os.path.join(root,f), "r", encoding="utf-8") as f:
                     content = f.read()
                     chunks = chunk_text(content, overlap=2)
                     for c in chunks:
                         print(f"--\n{c}\n")
                     interrupt("end")

                     
#------------------------------------------------- simple_test
def simple_test():
    with open(DOCX_SAMPLE, "r", encoding="utf-8") as f:
        content = f.read()
        chunks = chunk_text(content, overlap=2)
        for c in chunks:
            print(f"--\n{c}\n")

            
#------------------------------------------------- main
def main():
    simple_test()
    explore_and_chunk()


#================================================= entry point
if __name__ == "__main__":
    main()
