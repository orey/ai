from unidecode import unidecode
import sys, random, inspect

ADD_SPACE_AROUND = [".",",",";",":","!","?","'",'"',"-","(",")","—"]
REPLACE = [
    ("\n", " "),
    ("_" , " "),
    ("”" , '"'),
    ("‘" , "'"),
    ("“" , '"'),
    ("[" , "" ),
    ("]" , "" )
]

PADDING_SIZE = 5
NOT_FOUND = "NOT_FOUND"

#----------------------------------------------------------------------breakpoint
def breakpoint(obj=None):
    prefix = "Breakpoint"
    #print(inspect.stack()[0][3]) => breakpoint
    print(f"{prefix} in {inspect.stack()[1][3]}")
    if obj: print(f"{prefix}: {obj}")
    a = input(f"{prefix}: Do you want to continue? ('n' will stop) ")
    if a == "n":
        print(f"{prefix}:Goodbye")
        sys.exit()
    

#-----------------------------------------------------------------------file_tokenizer
def file_tokenizer(f, keep_accents=False, verbose = False):
    '''
    More basic stuff but working quite well
    '''
    with open(f) as g:
        text = g.read()[1:] #removing first char \ufeff
        if verbose: print("Text read")
        return my_tokenizer(text, keep_accents, verbose)

#-----------------------------------------------------------------------my_tokenizer
def my_tokenizer(text, keep_accents = False, verbose = False):
    if not keep_accents:
        text = unidecode(text)
        if verbose: print("Accents removed")
    text = text.lower()
    if verbose: print("Text in lower case")
    for before, after in REPLACE:
        text = text.replace(before, after)
        if verbose: print(f"{before} was replaced by {after}")
    for char in ADD_SPACE_AROUND:
        text = text.replace(char," " + char + " ")
        if verbose: print("Created spaces around << " + char + " >>")
    return [x for x in text.split(" ") if x] #removing empty strings


#-----------------------------------------------------------------------build_dict    
class WordDict:
    '''
    The dict maintains a dictionary that is the images of all the provided text
    Sequentially, all words are assigned a token. The number of occurrences
    of words is counted.
    The dict enables to parse text and get back an array of tokens.
    '''
    def __init__(self):
        '''
        creates a dict with
        dict key : word
        dict value : [
               string padded of integer_representation (auto-increment counter),
               nb_occurences of the word in the texts that were provided
            ]
        '''
        self.dic = {}
        self.count = 0
        
    def add_words(self, words, verbose= False):
        '''
        words : array of words
        returns the array of tokens
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
        if verbose:
            print(self)
        return tokenized_words

    def print(self, print_elems=False):
        st = ""
        if print_elems:
            temp = dict(sorted(self.dic.items()))
            for elem in temp:
                st += f"{elem} ({temp[elem][1]}) | "
        st += f"\nDictionary length is {len(self.dic)}\n"
        print(st)

    def decode(self, st):
        st_elems = []
        for i in range(int(len(st)/PADDING_SIZE)):
            numrep = st[i*PADDING_SIZE:(i*PADDING_SIZE)+PADDING_SIZE]
            mystr = ""
            found = False
            for k,v in self.dic.items():
                if found:
                    break
                else:
                    if v[0] == numrep:
                        mystr = k
                        found = True
            st_elems.append(mystr)
        return st_elems

    def dump(self, filename):
        with open(filename, "w") as f:
            f.write(f"{self.dic}")
    
#-----------------------------------------------------------------------build_dict
class NextToken():
    '''
    next_tokens est un dic avec
    key: concaténation des id des tokens, chacun paddé sur 4 char avec leading 0
    value: [
      [padded_token_id, nb_occurence],
      [padded_token_id, nb_occurence],
      etc.
    ]
    Pas besoin du dic, NextToken travaille seulement sur les tokens
    '''
    def __init__(self, window_size):
        self.nex = {}
        self.dic = dic
        self.window = window_size

    def scan(self, tokens, verbose=False):
        for i in range(len(tokens)-self.window):
            # getting the real words
            attention = tokens[i : i+self.window]
            next_t = tokens[i+self.window]
            # converting the key and value to nums based on dic
            key = ""
            for elem in attention:
                key += elem
            value = next_t
            # manage count
            if key not in self.nex:
                self.nex[key] = [[value, 1]]
            else:
                if verbose: print(f"***** We have one! ***** Attention: {attention}, next token: '{next_t}'")
                # do we have already the value?
                alternates = self.nex[key]
                #breakpoint(f"BEFORE - Alternates: {alternates} - Value: {value}")
                exist = False
                for e in alternates:
                    if e[0] == value:
                        exist = True
                        if verbose: print("Value already exists")
                        e[1] += 1
                if not exist:
                    alternates.append([value, 1])
                self.nex[key] = alternates
                #breakpoint(f"AFTER - Alternates: {alternates}")
        print(f"NextToken instance - Window size: {str(self.window)}, Nb of elements: {len(self.nex)}")
        return True

    def print(self, dic):
        outstr = ""
        for key, value in self.nex.items():
            #showing only singular items
            if len(value) != 1:
                outstr = f"Key: {key} - Value: {value} |"
                for word in dic.decode(key):
                    outstr += f" {word}"
                for elem in value:
                    outstr += f" | {dic.decode(elem[0])[0]} ({str(elem[1])})"
                print(outstr)

    def get_next(self, key, temperature=0):
        '''
        low temperature is apparition proba based
        high temperature is equiprobable
        '''
        if key in self.nex:
            #what token is most probable
            value = self.nex[key]
            occur = 0
            # value : [ [token1, occ1], [token2, occ2], etc. ]
            print(f"choice between {len(value)}")
            for i in range(len(value)):
                occur += value[i][1]
            proba = []
            cumul = 0
            if temperature < 50:
                for elem in value:
                    cumul += elem[1]
                    proba.append(cumul/occur)
            else:
                # solutions that equiprobable
                for elem in value:
                    cumul += 1/len(value)
                    proba.append(cumul)
            #breakpoint(f"Value: {value}, Probas: {proba}")
            rand = random.uniform(0,1)
            theindex = 0
            for i in range(len(proba)):
                if rand < proba[i]:
                    theindex = i
                    break;
            return value[theindex][0]
        else:
            return NOT_FOUND


#------------------------------------------------------------------concatenate_arrays
def concatenate_arrays(arr1, arr2):
    for elem in arr2:
        arr1.append(elem)
    return arr1
                

#------------------------------------------------------------------prompt
def prompt(dic, nextlist, keep_accents=False, temperature = 0, verbose = False):
    '''
    tokens est la structure qui contient tout le texte sous forme de tokens
    '''
    tokens = []
    while True:
        #breakpoint(f"BEGIN {tokens}")
        resp = input("Your input ('end' terminates) > ")
        window = 0
        if resp == "end":
            sys.exit()

        if (resp == "" or resp == None) and (len(tokens) == 0):
            print("No tokens were provided, you have to enter a query.")
            continue
        else:
            #1. we tokenize the command
            command = my_tokenizer(resp, keep_accents, verbose)
            #breakpoint(command)

            # warning: dic keeps memory of the user prompts and records the unknown words
            # typed in the prompt
            #2. we add it to the current tokens (maybe empty the first time)
            concatenate_arrays(tokens, dic.add_words(command))
            #breakpoint(tokens)

            #3. looping though the NextToken instance
            next_token=""
            found = False
            for nex in nextlist:
                window = nex.window
                thewindow = window
                #breakpoint(f"Window size = {window}")

                #4. keeping the last "window" size of the tokens to find a match
                kept = tokens[-window:]
                #breakpoint(f"Verbose: Tokens of the user input: {tokens}, kept: {kept}")

                #5. Building the key
                key = ''.join(kept)
                next_token = nex.get_next(key, temperature)
                #breakpoint(f"Key: {key}, Next: {next_token}")

                if next_token == NOT_FOUND:
                    #breakpoint(f"Verbose: For key={key}, next token not found")
                    continue
                else:
                    found = True
                    tokens.append(next_token)
                    #breakpoint(f"Next: {next_token}, Tokens: {tokens}")
                    break
            if not found:
                nextuser = input("The next token was not found. Propose one: > ")
                command2 = my_tokenizer(nextuser, keep_accents, verbose)
                concatenate_arrays(tokens, dic.add_words(command2))
                thewindow = 0
            print(f"Resulting context: {' '.join(dic.decode(''.join(tokens)))} ({str(thewindow)})")
                
    
#------------------------------------------------------------------main
if __name__ == "__main__":
    #test()
    #tokens = mytokenizer('./content/the-verdict.txt')
    #words = file_tokenizer('./content/russian-folk-tales.txt',False, True)
    #words = file_tokenizer('./content/kjv-cleaned.txt')
    words = file_tokenizer('./content/segond-clean.txt', True)
    dic = WordDict()
    tokens = dic.add_words(words)
    dic.print()
    #dic.dump("dict-segond.txt")
    #breakpoint()
    #print(tokens)
    #breakpoint()
    attention_windows = [5, 4, 3]
    attentions = []
    temp = None
    for att in attention_windows:
        print(f"Creating attention window of size {att}")
        temp = NextToken(att)
        temp.scan(tokens)
        attentions.append(temp)
        print("Done")
    print("-"*20)
    prompt(dic, attentions, True, 75, False)
    
