#============================================
# File name:      next-word-sem.py
# Author:         Olivier Rey
# Date:           September 2025
# License:        GPL v3
#============================================
#!/usr/bin/env python3
import sys, time, random
import spacy # used for lemmification

sys.path.append('.')
from tools8 import file_tokenizer, myProgressBar, mybreakpoint, generateName, ADD_SPACE_AROUND, interrupt


def get_n_last(tex, n):
    '''
    tex is a text with words separated by space
    returns an array of string from the longest to the shortest
    '''
    tab = tex.split(" ")
    pivot = 0
    if len(tab) < n:
        pivot = len(tab)
    else:
        pivot = n
    returnarr = []
    for i in range(pivot,0,-1):
        returnarr.append(" ".join(tab[-i:]))
    return returnarr
    
def test_get_n_last():
    print(get_n_last("test", 1))
    print(get_n_last("test1 test2", 1))
    print(get_n_last("test1 test2", 2))
    print(get_n_last("test1 test2 test3", 2))
    print(get_n_last("test1 test2 test3 test4", 3))
    print(get_n_last("test1 test2 test3 test4", 5))


#---------------------------------------------------------------- SimpleGraph
class SimpleGraph:
    '''
    The simplest memory graph based on voisinages:
    {text_source_node: {text_target_node: nb_of occurrence, etc.}, etc.}
    The word separator is the space.
    '''
    #- - - - - - - - - - - - - 
    def __init__(self, name):
        self.name = name
        self.g = {}
        self.maxinput = 0 #max length of in the input
        #the output length is supposed to be "1" because
        #we are getting the next word

    #- - - - - - - - - - - - - 
    def add(self, node1, node2):
        '''
        nodes are supposed to be strings
        '''
        #---1 analyze if node has more than one word
        # and record the longuest chains length
        temp1 = len(node1.split(' '))
        if temp1 > self.maxinput:
            self.maxinput = temp1
        #---2 add in dict
        if node1 in self.g:
            voiz = self.g[node1]
            if node2 in voiz:
                voiz[node2] += 1
            else:
                voiz[node2] = 1
        else:
            self.g[node1] = {node2 : 1}
            
    #- - - - - - - - - - - - - 
    def print(self):
        print(self.g)
        
    #- - - - - - - - - - - - - 
    def next(self, key):
        mymin = min(self.maxinput, len(key.split(' ')))
        series = get_n_last(key, mymin)
        nextw = ""
        for before in series:
            if before in self.g:
                #return algo_highest_first_one(self.g[before])
                return algo_probas(self.g[before])
        #--- we try every combination and there is no match
        return ""

    
#---------------------------------------------------------------- algo_probas
def algo_probas(theedges):
    '''
    Takes a list of edges
    {node1:weight1, node2:weight2,etc.}
    '''
    weights = 0
    for e in theedges:
        weights += theedges[e]
    baseproba = 1 / weights
    probas = {}
    cumul = 0
    #the aim is to have cumulated probas up to 1
    for e in theedges:
        cumul += theedges[e]*baseproba
        probas[e] = cumul
    run = random.random()
    for e in probas:
        if run > probas[e]:
            continue
        else:
            #it is this one
            return e
    

#---------------------------------------------------------------- algo_highest_first_one
def algo_highest_first_one(theedges):
    '''
    Takes a list of edges
    {node1:weight1, node2:weight2,etc.}
    This algo is bad because it always takes the first one
    in cases where we have {node1:1, node2,1, node3:1, etc.}
    The result is that it can loop again and again
    '''
    highest = 0
    nextword = ""
    for e in theedges:
        if theedges[e] > highest:
            highest = theedges[e]
            nextword = e
    return nextword

            
#---------------------------------------------------------------- feedSimpleGraph
def feedSimpleGraph(g, words, befores, afters):
    print(f"Feeding graph with pattern {befores}/{afters}")
    thelength = len(words)
    wind = befores + afters
    lastindex = thelength - wind
    #p = myProgressBar(lastindex+1)
    batch = 0
    for i in range(lastindex+1):
        before = ' '.join(words[i : i+befores])
        after = ' '.join(words[i+befores: i+befores+afters])
        g.add(before,after)
    print("Graph contains " + '{:,}'.format(len(g.g)) + " entries")


#---------------------------------------------------------------- feedThesaurus
class MyThesaurus:
    '''
    Using 
    '''
    def __init__(self, name):
        self.name = name
        self.dict = {} # {"manger" : ["VERB", count], ...}
        print("Loading 'fr_core_news_md'")
        self.nlp = spacy.load("fr_core_news_md")

    def add(self, word):
        doc = self.nlp(word)
        if len(doc) !=1:
            print(f"Warning: {word} is generating a lemmification with more than one element")
            print(doc)
        token = doc[0]
        if token.lemma_ in self.dict:
            carac = self.dict[token.lemma_]
            carac[1] += 1
        else:
            self.dict[token.lemma_] = [token.pos_, 1]
            

def feedSimpleThesaurus(t, words):
    for word in words:
        if word not in ADD_SPACE_AROUND:
            t.add(word)

    
#---------------------------------------------------------------- load and prompt
def load_and_prompt(name, files, windowlimit):
    g = SimpleGraph(name)
    t = MyThesaurus(name)
    for f in files:
        print(f"Tokenizing file '{f}'...")
        words = file_tokenizer(f, True) # problem to solve: apostrophe + special guillemets
        interrupt(words)
        for i in range(windowlimit):
            feedSimpleGraph(g, words, i+1, 1)
            feedSimpleThesaurus(t, words)
    interrupt(t)
    generatedtext = input("Provide a start phrase: ")
    while True:
        generatedtext += ' ' + g.next(generatedtext)
        print(generatedtext)
        stop = input("Next? ['n' terminates] ")
        if stop == 'n':
            break
    outputfilename = generateName(name + ".txt")
    with open(outputfilename, "w") as output:
        output.write(generatedtext)
        print(f"{outputfilename} file generated")


#------------------------------------------------------------------main        
def test():
    #load_and_prompt("Segond",
    #                ['../content/segond-clean.txt'],
    #                4)
    load_and_prompt("Proust",
                    [
                        "../content/Proust-1-DuCoteDeChezSwann.txt",
                        "../content/Proust-2-1-AL'OmbreDesJeunesFillesEnFleur.txt",
                        "../content/Proust-2-2-AL'OmbreDesJeunesFillesEnFleur.txt",
                        "../content/Proust-2-3-AL'OmbreDesJeunesFillesEnFleur.txt",
                        "../content/Proust-3-1-LeCoteDesGuermantes.txt",
                        "../content/Proust-3-2-LeCoteDesGuermantes.txt",
                        "../content/Proust-3-3-LeCoteDesGuermantes.txt",
                        "../content/Proust-4-1-SodomeEtGomorrhe.txt",
                        "../content/Proust-4-2-SodomeEtGomorrhe.txt",
                        "../content/Proust-5-LaPrisionniere.txt",
                        "../content/Proust-6-1-AlbertineDisparue.txt",
                        "../content/Proust-6-2-AlbertineDisparue.txt",
                        "../content/Proust-7-1-LeTempsRetrouve.txt",
                        "../content/Proust-7-2-LeTempsRetrouve.txt"
                    ],
                    6)



#------------------------------------------------------------------test of spacy
def test_spacy():
    nlp = spacy.load("fr_core_news_md")

    text = "Ils mangeaient des pommes mais n'avaient pas de sous"

    doc = nlp(text)

    for token in doc:
        print(token.text, token.lemma_, token.pos_)
    
#------------------------------------------------------------------main
if __name__ == "__main__":
    #test_get_n_last()
    test_spacy()
    interrupt("Continuer le test")
    test()
    
