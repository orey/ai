#============================================
# File name:      next-word-sem.py
# Author:         Olivier Rey
# Date:           September 2025
# License:        GPL v3
#============================================
#!/usr/bin/env python3
import sys, time, random
sys.path.append('.')


from tools8 import file_tokenizer, myProgressBar, mybreakpoint


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


#---------------------------------------------------------------- 
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


#------------------------------------------------------------------main        
def test():
    testfile = '../content/segond-clean.txt'
    print(f"Tokenizing file '{testfile}'...")
    words = file_tokenizer(testfile, True)
    print("Done")
    g = SimpleGraph("Dictionary")
    feedSimpleGraph(g, words, 1, 1)
    feedSimpleGraph(g, words, 2, 1)
    feedSimpleGraph(g, words, 3, 1)
    feedSimpleGraph(g, words, 4, 1)
    #g.print()
    generatedtext = input("Provide a start phrase: ")
    while True:
        generatedtext += ' ' + g.next(generatedtext)
        print(generatedtext)
        stop = input("Next? ['n' terminates] ")
        if stop == 'n':
            break
    print("Terminated")

    
#------------------------------------------------------------------main
if __name__ == "__main__":
    #test_get_n_last()
    test()
    
