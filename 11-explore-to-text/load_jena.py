'''
This script scans a tree of folder to find turtle files and
load them into a running Jena dataset
'''

import os
from SPARQLWrapper import SPARQLWrapper
import requests

FUSEKI_URL = "http://localhost:3030/oreyboulot/data"

SOURCE = "C:\\c\\oreyboulot-NHI"

for root, dirs, files in os.walk(SOURCE):
    for fname in files:
        if fname.endswith(".ttl"):
            fpath = os.path.join(root, fname)
            print(f"Loading: {fpath}")
            with open(fpath, "rb") as f:
                r = requests.post(
                    FUSEKI_URL,
                    data=f.read(),
                    headers={"Content-Type": "text/turtle"}
                )
                print(f"  Status: {r.status_code}")
