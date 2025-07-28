#============================================
# File name:      next-word-sem.py
# Author:         Olivier Rey
# Date:           July 2025
# License:        GPL v3
#============================================
#!/usr/bin/env python3

#from rdflib import Graph, Literal, URIRef, RDF, RDFS, BNode, XSD

import sys
sys.path.append('.')
from tools7 import RDFStore


#------------------------------------------------------------------SemDict
class SemDict():
    '''
    SemDict does not need any numeric representation
    '''
    def __init__(self, name):
        super().__init__(name)
        





#------------------------------------------------------------------main
if __name__ == "__main__":
    words = file_tokenizer('./content/segond-clean.txt', True)
    dic = SemDict()
