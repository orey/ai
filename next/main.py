########################################################
# AI based on semantic web
# O. Rey - rey.olivier@gmail.com
# Creation date: September 2025
# Last update:
########################################################

import sys
sys.path.append('.')
from tools9 import mybreakpoint

from tokenizer import file_tokenizer
from rdfdb import string2uri





if __name__ == "__main__":
    for f in ["./texts/Proust-Swann.txt",
              "./texts/Bible-Segond.txt",
              "./texts/kjv.txt",
              "./texts/kjv-cleaned.txt"]:
        st = file_tokenizer(f)
        mybreakpoint(st)
        for elem in st:
            uri = string2uri(elem)
            print(uri, end=" - ")
        mybreakpoint("Paused to examine the result")
