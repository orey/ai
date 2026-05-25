'''
**Orchestrator module**

This module provides the global logic of orchestration to feed an optimized RDF database.

* Date: May 2026
* Author: O. Rey
* email: rey.olivier@gmail.com
'''

#--------------------------------- global imports
import json, os

#--------------------------------- local imports
import sys
sys.path.append('.')

from tools10 import interrupt, sha256_fingerprint, ensureFile, footprint_sha1

from chunker import chunk_text
from prompts import generate_keywords_prompt
from openai_api_server import AI_Session, QWEN3_6, clean_output
from rdfdb import RDFDB, IRI, format_IRI_name, TextLiteral, RDF

MODEL = QWEN3_6

#--------------------------------- constants
SOURCE = "C:\\c\\oreyboulot-NHI"

TEST_LIMIT = 100


#--------------------------------- semantic web constants
NS = "https://orey.github.io/ai/keywords#"

class INDEX:
    # types
    fingerprint = IRI(NS,"fingerprint")
    filetype = IRI(NS,"filetype")
    # relations
    fingerprint_of = IRI(NS,"fingerprint_of")
    keyword_in = IRI(NS,"keyword_in")
    

#------------------------------------------------------------ treat_docx_file
def treat_file(session, namespace, f):
    '''
    A file has several chunks
    f is the full name of the file
    '''
    # defining the keywords for the document
    keywords = {} # keyword, nb of time it appears
    if not f.endswith(".txt"):
        return False
    dbfilename = f.replace(".txt",".ttl")
    if ensureFile(dbfilename):
        print(f"File already exists : {dbfilename}")
        return True
    print(f"Processing file: {f}")
    #fingerprint = IRI(NS,sha256_fingerprint(f))
    # going simpler and faster
    fingerprint = IRI(NS,footprint_sha1(f))
    # when the db will be dumped, a .ttl extension will be added
    rdfdb = RDFDB(dbfilename,[namespace])
    rdfdb.add(
        fingerprint,
        RDF.type,
        INDEX.fingerprint
    )
    justfile = f.split("\\")[-1]
    rdfdb.add(
        fingerprint,
        INDEX.fingerprint_of,
        TextLiteral(justfile)
    )
    
    with open(os.path.join(f), "r", encoding="utf-8") as thefile:
        # 1. Open the file and read the content
        content = thefile.read()
        # 2. Chunk it
        chunks = chunk_text(content, overlap=2)
        count = 0
        print("--- Chunks: ", end="", flush=True)
        for c in chunks:
            count += 1
            print(str(count) + ", ", end="", flush=True)
            # 3. ask the LLM
            params = [
                "You are a helpful assistant, always answering in json format.",
                generate_keywords_prompt(c),
                ""
            ]
            response = session.ask(*params, streaming=False, verbose=False)
            #print(f"\n---\n{response}\n---\n")
            # 4. get the keywords and record them
            clean = ""
            try:
                clean = clean_output(MODEL, response)
                kw = json.loads(clean)
            except JSONDecodeError as e:
                print(f"Error in JSON decoding for file {f}, chunk number {count}")
                interrupt(clean)
                continue
            for k in kw["keywords"]:
                if k not in keywords:
                    keywords[k] = 1
                else:
                    num = keywords[k]
                    keywords[k] += 1
    # 5. We have the keywords for the document
    #$$$
    print("\n--- Adding keywords to the semantic database")
    for k in keywords:
        rdfdb.add(
            IRI(NS, format_IRI_name(k)),
            INDEX.keyword_in,
            fingerprint
        )
        rdfdb.add(
            IRI(NS, format_IRI_name(k)),
            RDF.value,
            TextLiteral(k)
        )
    rdfdb.dump(extension="")
    print(f"TTL file generated: {dbfilename}")
    

#-------------------------------------------------------- main
def main(test=False):
    session = AI_Session("test")
    count = 0
    end = False
    for root, dirs, files in os.walk(SOURCE):
        if end:
            break
        for f in files:
            if f.endswith(".txt"):
                count += 1
                treat_file(
                    session,
                    NS,
                    os.path.join(root,f)
                )
                if test and count >= TEST_LIMIT:
                    end = True
                    break
    db.dump()


#============================================================entry point
if __name__ == "__main__":
    main(True)





