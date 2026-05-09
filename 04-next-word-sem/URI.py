# URI.py

import sys

uri_reserved = [':', '/', '?', '#', '[', ']', '@', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=']

others = [ u'’', u'"', u'«', u'»', u'—', u'™', u'“', u'”', u'•', '%', '‘' ]

ascii = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
         'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z',
         '0','1','2','3','4','5','6','7','8','9',
         '-','.','_']

francais = {
    u'à':'~a0~', u'â':'~a1~', u'ä':'~a2~',
    u'À':'~A0~', u'Â':'~A1~', u'Ä':'~A2~',
    u'é':'~e0~', u'è':'~e1~', u'ê':'~e2~', u'ë':'~e3~',
    u'É':'~E0~', u'È':'~E1~', u'Ê':'~E2~', u'Ë':'~E3~',
    u'î':'~i0~', u'ï':'~i1~',
    u'Î':'~I0~', u'Ï':'~I1~',
    u'ô':'~o0~', u'ö':'~o1~',
    u'Ô':'~O0~', u"Ö":'~O1~',
    u'û':'~u0~', u'ù':'~u1~', u'ü':'~u2~',
    u'Û':'~U0~', u'Ù':'~U1~', u'Ü':'~U2~',
    u'œ':'~oe~', u'Œ':'~OE~',
    u'æ':'~ae~', u'Æ':'~AE~',
    u'ç':'~c0~', u'Ç':'~c1~'
}

special = [ '\n' ]




def string2uri(s):
    uri= ""
    for c in s:
        if c == ' ':
            uri += '_'
            continue
        if c in uri_reserved or c in special or c in others:
            uri += '_'
            continue
        if c in ascii:
            uri += c
            continue
        if c in francais.keys():
            uri += francais[c]
            continue
        print(c.encode("utf-8"))
        val = input(f"Unknown char '{c}'. Do you want to continue? [n = exit] ")
        if val == 'n':
            sys.exit()
    return uri


def tests():
    t = u"Le frère de cette personne qu'Octave a épousée. Il croit que le dessein que vous avez de mettre votre fille à la place que tient sa sœur est ce qui pousse le plus fort à faire rompre leur mariage ; et, dans cette pensée, il a résolu hautement de décharger son désespoir sur vous et vous ôter la vie pour venger son honneur. Tous ses amis, gens d'épée comme lui, vous cherchent de tous les côtés, et demandent de vos nouvelles. J'ai vu même deçà et delà, des soldats de sa compagnie qui interrogent ceux qu'ils trouvent, et occupent par pelotons toutes les avenues de votre maison. De sorte que vous ne sauriez aller chez vous, vous ne sauriez faire un pas ni à droit, ni à gauche, que vous ne tombiez dans leurs mains."
    print(string2uri(t))

    with open("Proust-Swann.txt", "r", encoding="utf-8") as f:
        t = f.read()
        print(string2uri(t[1:]))


    '﻿'
    
if __name__ == "__main__":
    tests()
