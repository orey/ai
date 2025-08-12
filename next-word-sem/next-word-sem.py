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

#---------------------------------------------------------------- Semantic constants
class Sem():
    # static members
    Domain = "https://orey.github.io/ai/"
    Identifiable = URIRef(DOMAIN + "Identifiable")
    Token = URIRef(DOMAIN + "Token")
    Sequence = URIRef(DOMAIN + "Sequence")
    Rank = URIRef(DOMAIN + "Rank") # rank of sequence
    Punctuation = URIRef(DOMAIN + "Punctuation")
    InstancesInDict = URIRef(DOMAIN + "InstancesInDict")

    # Static method
    def init_graph_grammar(graph):
        '''
        graph is a RDFStore (from tools)
        '''
        #=== Initialize the grammar
        #--- Identifiable is the root of tokens and sequences
        graph.add((Sem.Identifiable, RDFS.subClassOf, RDFS.Class))
        #--- Token: ID or a "word"
        graph.add((Sem.Token, RDFS.subClassOf, Sem.Identifiable))
        #--- Sequence: list of tokens
        graph.add((Sem.Sequence, RDFS.subClassOf, Sem.Identifiable))
        graph.add((Sem.Sequence, RDFS.subClassOf, RDF.Seq)) # The _1, _2, etc. will be used
        #--- Rank: The number of tokens of a sequence
        graph.add((Sem.Rank, RDFS.subPropertyOf, RDF.Property))
        graph.add((Sem.Rank, RDFS.domain, Sem.Sequence))
        graph.add((Sem.Rank, RDFS.range, XSD.integer))
        #--- Punctuation
        graph.add((Sem.Punctuation, RDFS.subClassOf, RDFS.Token))
        #--- InstancesInDict
        graph.add((Sem.InstancesInDict, RDFS.subPropertyOf, RDF.Property))
        graph.add((Sem.InstancesInDict, RDFS.domain, Sem.Sequence))
        graph.add((Sem.InstancesInDict, RDFS.range, XSD.integer))
        

    
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
        # initialize the grammar
        Sem.init_graph_grammar(self.graph)
        
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
                s = URIRef(Sem.Domain + rep)
                # the value is always the same
                self.graph.add((s, RDF.value, word))
                # the type is not
                if word in PUNCTUATION:
                    self.graph.add((s, RDF.type, Sem.Punctuation))
                else:
                    self.graph.add((s, RDF.type, Sem.Token))
                # to be added, the number of instances could be added
                # reprendre ici
        if verbose:
            print(self)
        return tokenized_words       





#------------------------------------------------------------------main
if __name__ == "__main__":
    words = file_tokenizer('./content/segond-clean.txt', True)
    dic = SemDict()
