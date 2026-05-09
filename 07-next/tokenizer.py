########################################################
# Tokenizer tool
# O. Rey - rey.olivier@gmail.com
# Creation date: August 2025
# Last update: September 2025
########################################################
import unidecode
from tools9 import mybreakpoint


#-----------------------------------------------------------------------my_tokenizer
REPLACE = [
    ("\n", " "),
    ("_" , " "),
    ("”" , "'"), #warning: " is not acceptable as Literal in a triple
    ("‘" , "'"),
    ("“" , "'"), #no "
    ("[" , "" ),
    ("]" , "" )
]

ADD_SPACE_AROUND = [".",",",";",":","!","?","'","-","(",")","—"] #no "

def my_tokenizer(text, toascii = False, tolower = False, verbose = False):
    '''
    This tokenizer was tested for English and French. It is simple and is quite robust.
    (benchmarks made on the Bible). It preserves accents and is word based.
    Returns an array of tokens in the order of the text.
    '''
    if toascii:
        text = unidecode.unidecode(text)
        if verbose: print("Converted to ASCII")
    if tolower:
        text = text.lower()
        if verbose: print("Text in lower case")
    for before, after in REPLACE:
        text = text.replace(before, after)
        if verbose: print(f"{before} was replaced by {after}")
    for char in ADD_SPACE_AROUND:
        text = text.replace(char," " + char + " ")
        if verbose: print("Created spaces around << " + char + " >>")
    return [x for x in text.split(" ") if x] #removing empty strings


#-----------------------------------------------------------------------file_tokenizer
def file_tokenizer(f,
                   enc = "utf-8",
                   toascii=False,
                   tolower = False,
                   verbose = False,
                   removeFirstChar=False):
    '''
    More basic stuff but working quite well
    '''
    with open(f, 'r', ) as g:
        text = g.read()[(1 if removeFirstChar else 0):] #removing first char \ufeff
        if verbose: print("Text read")
        return my_tokenizer(text, toascii, tolower, verbose)



def tests():
    for f in ["./texts/Proust-Swann.txt",
              "./texts/Bible-Segond.txt",
              "./texts/kjv.txt",
              "./texts/kjv-cleaned.txt"]:
        st = file_tokenizer(f)
        print(st)
        mybreakpoint("Paused to examine the result")     

    
if __name__ == "__main__":
    tests()
