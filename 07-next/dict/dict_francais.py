########################################################
# Creation of dataset for French
# O. Rey - rey.olivier@gmail.com
# Creation date: September 2025
# Last update: September 2025
########################################################
# Source: lexique.org
########################################################

import sys
sys.path.append('.')
from rdfdb import string2uri
from rdfdb import RDFDB, IRI, RDF


# ortho - le mot - 0
# phon: les formes phonologiques du mot - 1
# lemme: les lemmes de ce mot - 2
# cgram: les catégories grammaticales de ce mot - 3
# genre: le genre - 4
# nombre: le nombre - 5
# freqlemfilms: la fréquence du lemme selon le corpus de sous-titres (par million d’occurrences) - 6
# freqlemlivres: la fréquence du lemme selon le corpus de livres (par million d’occurrences) - 7
# freqfilms: la fréquence du mot selon le corpus de sous-titres (par million d’occurrences) - 8
# freqlivres: la fréquence du mot selon le corpus de livres (par million d’occurrences) - 9
# infover: modes, temps, et personnes possibles pour les verbes - 10
# nbhomogr: nombre d'homographes - 11
# nbhomoph: nombre d'homophones - 12
# islem: indique si c'est un lemme ou pas - 13
# nblettres: le nombre de lettres - 14
# nbphons: nombre de phonèmes - 15
# cvcv: la structure orthographique - 16
# p-cvcv: la structure phonologique - 17
# voisorth: nombre de voisins orthographiques - 18
# voisphon: nombre de voisins phonologiques - 19
# puorth: point d'unicité orthographique - 20
# puphon: point d'unicité phonologique - 21
# syll: forme phonologique syllabée - 22
# nbsyll: nombre de syllabes - 23
# cv-cv : structure phonologique syllabée - 24
# orthrenv: forme orthograhique inversée - 25
# phonrenv: forme phonologique inversée - 26
# orthosyll: forme orthographique syllabée - 27

CAT_GRAM = "Catégorie grammaticale"
ABBREV = {
"ADJ": "Adjectif",
"ADJ:dem": "Adjectif démonstratif",
"ADJ:ind": "Adjectif indéfini",
"ADJ:int": "Adjectif interrogatif",
"ADJ:num": "Adjectif numérique",
"ADJ:pos": "Adjectif possessif",
"ADV": "Adverbe",
"ART:def": "Article défini",
"ART:inf": "Article indéfini",
"AUX": "Auxiliaire",
"CON": "Conjonction",
"LIA": "Liaison euphonique (l')",
"NOM": "Nom commun",
"ONO": "Onomatopée",
"PRE": "Préposition",
"PRO:dem": "Pronom démonstratif",
"PRO:ind": "Pronom indéfini",
"PRO:int": "Pronom interrogatif",
"PRO:per": "Pronom personnel",
"PRO:pos": "Pronom possessif",
"PRO:rel": "Pronom relatif",
"VER": "Verbe"
}

frns = "https://orey.github.io/rdf/fr_lex"

semdb = RDFB("lexique", [
    frns,
])

def create_lexice_categories(db):
    db.add(IRI(frns, "fr_gram_cat"), RDFS.subPropertyOf, 
    for key,value in ABBREV:
        db.add(IRI(catns, string2uri(key)),


with open("Lexique383.tsv", "r") as f:
    lines = f.readlines()
    for line in lines:
        tab = line.split("\t")
        
        print(tab)
