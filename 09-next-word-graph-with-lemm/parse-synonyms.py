import sys

sys.path.append('.')
from SimplestWordGraph import WordGraph
from tools8 import interrupt, Timer


THESAURUS = "../thesaurus/th_fr_FR_v2.dat"



def main():
    treatment = Timer("Synonyms")
    wg = WordGraph()
    with open(THESAURUS, "r",encoding='utf-8') as f:
        lines = [line.rstrip() for line in f]
        nblines = len(lines)
        nbwords = (nblines -1) / 2
        print(f"{nbwords} found in file")
        count = 0
        i = 1
        while count < nbwords:
            #interrupt(lines[i])
            # each synonym is defined by 2 lines
            wordlinetokens = lines[i].split('|')
            if len(wordlinetokens) != 2:
                print(f"Error, expected word line and found: '{lines[i]}'")
                sys.exit()
            nbsignific = int(wordlinetokens[1])
            for k in range(1, nbsignific + 1):
                synlinetokens = lines[i+k].split('|')
                types = synlinetokens[0].replace('(','').replace(')','').split(' ')
                wg.add_node(wordlinetokens[0])
                wg.add_types_to_node(wordlinetokens[0],types)
                nb = len(synlinetokens)
                for j in range(1,nb):
                    wg.add_edge(wordlinetokens[0],synlinetokens[j])
            i = i + nbsignific + 1
            count += 1
            if i == len(lines):
                break
            else:
                print(lines[i][0],end="")
    print("")
    treatment.stop()
    wg.count()
    print(wg.top_ranks(100))
            



if __name__ == "__main__":
    main()
