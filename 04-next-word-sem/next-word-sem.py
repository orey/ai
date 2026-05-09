#============================================
# File name:      next-word-sem.py
# Author:         Olivier Rey
# Date:           July 2025
# License:        GPL v3
#============================================
#!/usr/bin/env python3

#from rdflib import Graph, Literal, URIRef, RDF, RDFS, BNode, XSD

import sys, time
sys.path.append('.')

from tools8 import file_tokenizer, imprint, Timer, myProgressBar, mybreakpoint
#RDFStore
#from rdflib import Literal, URIRef, RDF, RDFS, XSD, BNode, Seq

from rdfdb import IRI, BlankNode, TextLiteral, IntLiteral, RDFDB, RDFS, RDF, XSD


#size of the keys for every token, each token being a word
PADDING_SIZE = 5

PUNCTUATION = [".",",",";",":","!","?","'",'"',"-","(",")","—"]

WORD = 1
SEQUENCE = 2

TESTDOM = "https://orey.github.io/ai/bible#"

#---------------------------------------------------------------- Semantic constants
class Sem():
    # static members
    Domain = "https://orey.github.io/ai/"
    Identifiable = IRI(Domain, "Identifiable")
    Word = IRI(Domain, "Word")
    Sequence = IRI(Domain, "Sequence")
    Rank = IRI(Domain, "Rank") # rank of sequence
    Punctuation = IRI(Domain, "Punctuation")
    InstancesInDict = IRI(Domain, "InstancesInDict")
    FollowedBy = IRI(Domain, "FollowedBy")

    # Static method
    def init_graph_grammar(graph):
        '''
        graph is a RDFStore (from tools)
        '''
        #=== Initialize the grammar
        #--- Identifiable is the root of words and sequences
        graph.add(Sem.Identifiable, RDFS.subClassOf, RDFS.Class)
        #--- Token: ID or a "word"
        graph.add(Sem.Word, RDFS.subClassOf, Sem.Identifiable)
        #--- Sequence: list of tokens
        graph.add(Sem.Sequence, RDFS.subClassOf, Sem.Identifiable)
        graph.add(Sem.Sequence, RDFS.subClassOf, RDF.Seq) # The _1, _2, etc. will be used
        #--- Rank: The number of tokens of a sequence
        graph.add(Sem.Rank, RDFS.subPropertyOf, RDF.Property)
        graph.add(Sem.Rank, RDFS.domain, Sem.Sequence)
        graph.add(Sem.Rank, RDFS.range, XSD.integer)
        #--- Punctuation
        graph.add(Sem.Punctuation, RDFS.subClassOf, Sem.Word)
        #--- InstancesInDict
        graph.add(Sem.InstancesInDict, RDFS.subPropertyOf, RDF.Property)
        graph.add(Sem.InstancesInDict, RDFS.domain, Sem.Sequence)
        graph.add(Sem.InstancesInDict, RDFS.range, XSD.integer)
        #--- FollowedBy
        graph.add(Sem.FollowedBy, RDFS.subPropertyOf, RDF.Property)
        graph.add(Sem.FollowedBy, RDFS.domain, Sem.Identifiable)
        graph.add(Sem.FollowedBy, RDFS.range, Sem.Identifiable)
        

    
#------------------------------------------------------------------SemDict
class SemDict():
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
        #self.graph = RDFStore(name)
        self.graph = RDFDB(name, [TESTDOM])
        # initialize the grammar
        Sem.init_graph_grammar(self.graph)


    def add_word(self, word, thetype=WORD, language="en", verbose=False):
        rep = ""
        if word in self.dic:
            # adding a new occurence
            rep = self.dic[word][0]
            occ = self.dic[word][1]
            self.dic[word] = [rep, occ+1]
            #--- Graph addition ---
            # token is already in graph but we have one more instance
            s = IRI(Sem.Domain, rep)
            self.graph.remove(s, Sem.InstancesInDict, IntLiteral(occ))
            self.graph.add(s, Sem.InstancesInDict, IntLiteral(occ+1))
            if verbose: imprint("-",end="") #new occurence
        else:
            # adding the word in dic
            rep = ("{:0"+ str(PADDING_SIZE)+"d}").format(self.count+1)
            self.dic[word] = [rep, 1]
            self.count +=1
            #--- Graph addition ---
            # adding the token with the word as value in the graph
            s = IRI(Sem.Domain, rep)
            self.graph.add(s, RDF.value, TextLiteral(word, language))
            # type the token properly
            # we could define more type like verbs, adjectives, pronouns and
            # have semantic rules applying
            if word in PUNCTUATION:
                self.graph.add(s, RDF.type, Sem.Punctuation)
            else:
                if thetype == WORD:
                    self.graph.add(s, RDF.type, Sem.Word)
                else:
                    self.graph.add(s, RDF.type, Sem.Sequence)
            # this is the first instance
            self.graph.add(s, Sem.InstancesInDict, IntLiteral(1))
            self.graph.add(s, Sem.Rank, IntLiteral(1))
            if verbose: imprint("n",end="") #new word
        return rep
    
        
    def add_words(self, words, language="en", verbose=False):
        """
        words : array of words
        returns the array of tokens corresponding to words
        """
        tokenized_words = []
        siz = len(words)
        if verbose: imprint(f"Length of the array of tokens: {siz}")
        pb = myProgressBar(siz)
        i = 0
        for word in words:
            pb.set(i)
            i+=1
            tokenized_words.append(self.add_word(word, WORD, language, verbose))
        if verbose:
            imprint(f"\nDictionary containing {self.count} words and punctuation")
        return tokenized_words

    
    def add_sequence(self, before, after, language="en", verbose=False):
        '''
        Before and after are sequences that are linked together. The SemDict is not here
        to calculate the sequences but to record them and their links.
        '''
        # treat 'before'
        bef = " ".join(before)
        befrep = self.add_word(bef, SEQUENCE, language, verbose)
        befs = IRI(Sem.Domain, befrep)
        objs = []
        #for word in before:
        #    wordid = self.add_word(word, WORD, language, verbose)
        #    objs.append(IRI(Sem.Domain, wordid))
        #befcont = Seq(self.graph.store, befs, objs)
        self.graph.add(befs, Sem.Rank, IntLiteral(len(before)))
        # treat 'after'
        aft = " ".join(after)
        aftrep = self.add_word(aft, SEQUENCE, language, verbose)
        afts = IRI(Sem.Domain, aftrep)
        objs = []
        #for word in after:
        #    wordid = self.add_word(word, WORD, language, verbose)
        #    objs.append(IRI(Sem.Domain, wordid))
        #aftcont = Seq(self.graph.store, afts, objs)
        self.graph.add(afts, Sem.Rank, IntLiteral(len(after)))
        # treat the link between before and after
        self.graph.add(befs, Sem.FollowedBy, afts)         

    
    def dump(self):
        self.graph.dump()
        

def scan(words, befores, afters, dic):
    thelength = len(words)
    wind = befores + afters
    lastindex = thelength - wind
    p = myProgressBar(lastindex+1)
    mybreakpoint(lastindex+1)
    batch = 0
    for i in range(lastindex+1):
        before = words[i : i+befores]
        after = words[i+befores: i+befores+afters]
        dic.add_sequence(before,after)
        batch += 1
        if batch == 60000:
            p.set(i, "Bunch of 30000 reached. Pausing 7 seconds")
            time.sleep(10)
            batch = 0
        else:
            p.set(i)


        
def test():    
    print("Tokenizing file...")
    words = file_tokenizer('./content/segond-clean.txt', True)
    #words = file_tokenizer('./content/the-verdict.txt', False)
    print("Done")
    dic = SemDict("BibleSegond")
    #dic = SemDict("Verdict")
    print("Adding words to dic + creating individual triplets")
    tim = Timer("Add words in dic")
    tokens = dic.add_words(words, "fr", False)
    #tokens = dic.add_words(words, "en", False)
    tim.stop()
    print("Done")
    print("Before scan")
    tom = Timer("scan")
    scan(words, 4, 3, dic)
    print("\nAfter scan")
    dic.dump()

#------------------------------------------------------------------main
if __name__ == "__main__":
    test()
        
