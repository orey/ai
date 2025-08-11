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
from tools7 import RDFStore, Literal, URIRef, RDF, RDFS, BNode, XSD


#size of the keys for every token, each token being a word
PADDING_SIZE = 5

PUNCTUATION = [".",",",";",":","!","?","'",'"',"-","(",")","—"]

#semantic constants
DOMAIN = "https://orey.github.io/ai/"

TOKEN = URIRef(DOMAIN + "TOKEN")
SEQUENCE = URIRef(DOMAIN + "SEQUENCE")
RANK = URIRef(DOMAIN + "RANK") # rank of sequence


#------------------------------------------------------------------SemDict
class SemWordDict():
    '''
    SemWordDict keeps the old dict representation but creates on top
    a semantic graph
    '''
    def __init__(self, name):
        '''
        creates a dict with
        dict key : word
        dict value : [
               string padded of integer_representation (auto-increment counter),
               nb_occurences of the word in the texts that were provided
            ]
        This dict is used for troubleshooting only, the real data being in the
        graph.
        '''
        # count is the number of words, not the number of triples
        self.dic = {}
        self.count = 0
        # create the graph
        self.name = name
        self.graph = RDFStore(name)
        # initialize the types
        self.graph.add((TOKEN, RDFS.subClassOf, RDFS.Class))
        self.graph.add((SEQUENCE, RDFS.subClassOf, RDFS.Class))
        self.graph.add((RANK, RDFS.subPropertyOf, RDF.Property))

    def add_words(self, words, verbose = False):
        '''
        words : array of words
        returns the array of tokens corresponding to words
        '''
        tokenized_words = []
        for word in words:
            if word in self.dic:
                # adding a new occurence
                rep = self.dic[word][0]
                tokenized_words.append(rep)
                occ = self.dic[word][1]
                self.dic[word] = [rep, occ+1]
            else:
                # adding the word in dic
                rep = ("{:0"+ str(PADDING_SIZE)+"d}").format(self.count+1)
                tokenized_words.append(rep)
                self.dic[word] = [rep, 1]
                self.count +=1
                # adding the word in the graph
                s = URIRef(DOMAIN + rep)
                if word in PUNCTUATION:
                    self.graph.add((s, RDF.type, ))
        if verbose:
            print(self)
        return tokenized_words       





#------------------------------------------------------------------main
if __name__ == "__main__":
    words = file_tokenizer('./content/segond-clean.txt', True)
    dic = SemDict()
