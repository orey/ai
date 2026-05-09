########################################################
# RDF Turtle DB for AI tests
# O. Rey - rey.olivier@gmail.com
# Creation date: August 2025
# Last update: September 2025
########################################################

import sys, time

sys.path.append('.')
from tools9 import mybreakpoint

#------------------------------------------------------- Management of French chars in URI

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

#------------------------------------------------------- string2uri
def string2uri(s):
    '''
    This function converts whatever string in URI.
    Tested with English and French languages.
    '''
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


#------------------- tests_string2uri
def tests_string2uri():
    t = u"Le frère de cette personne qu'Octave a épousée. Il croit que le dessein que vous avez de mettre votre fille à la place que tient sa sœur est ce qui pousse le plus fort à faire rompre leur mariage ; et, dans cette pensée, il a résolu hautement de décharger son désespoir sur vous et vous ôter la vie pour venger son honneur. Tous ses amis, gens d'épée comme lui, vous cherchent de tous les côtés, et demandent de vos nouvelles. J'ai vu même deçà et delà, des soldats de sa compagnie qui interrogent ceux qu'ils trouvent, et occupent par pelotons toutes les avenues de votre maison. De sorte que vous ne sauriez aller chez vous, vous ne sauriez faire un pas ni à droit, ni à gauche, que vous ne tombiez dans leurs mains."
    print(string2uri(t))

    with open("./texts/Proust-Swann.txt", "r", encoding="utf-8") as f:
        t = f.read()
        print(string2uri(t[1:]))


#====================================================================== IRI
class IRI():
    def __init__(self, namespace: str, value: str):
        self.namespace = namespace
        self.value = value

    def __str_(self):
        return f"<{self.namespace}{self.value}>"

#====================================================================== BlankNode
class BlankNode():
    def __init__(self, namespace: str):
        self.namespace = namespace
        
    def __str__(self):
        return f"<{self.namespace}_>"

#======================================================================
# Literals have no namespace
#====================================================================== TextLiteral
class TextLiteral():
    def __init__(self, value: str, language="en"):
        self.value = value.replace('"', "")
        self.language = language

    def __str__(self):
        return f'"{self.value}"@{self.language}'

#====================================================================== IntLiteral
class IntLiteral():
    def __init__(self, value: int):
        self.value = value
    

#==================================== Major namespaces used in the programs (to be completed)
class Namespace():
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    RDFS = "http://www.w3.org/2000/01/rdf-schema#"
    XSD = "http://www.w3.org/2001/XMLSchema#"


#====================================================================== RDF namespace
class RDF():
    type = IRI(Namespace.RDF, "type")
    Property = IRI(Namespace.RDF, "Property")
    Seq = IRI(Namespace.RDF, "Seq")
    value = IRI(Namespace.RDF, "Value")

    
#====================================================================== RDFS namespace
class RDFS():
    subClassOf = IRI(Namespace.RDFS, "subClassOf")
    Class = IRI(Namespace.RDFS, "Class")
    subPropertyOf = IRI(Namespace.RDFS, "subPropertyOf")
    domain = IRI(Namespace.RDFS, "domain")
    range = IRI(Namespace.RDFS, "range")


#==================================================================== XSD namespace
class XSD():
    integer = IRI(Namespace.XSD, "integer")
        

#====================================================================== RDFDB
class RDFDB():
    '''
    Simple RDF DB with turtle notation in mind
    '''
    def __init__(self, name, namespaces = []):
        '''
        namespaces is an array of IRI roots finishing by / or #
        will give birth to turtle header
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        '''
        self.name = name
        self.namespaces = {
            Namespace.RDF: "rdf:",
            Namespace.RDFS: "rdfs:",
            Namespace.XSD: "xsd:"
        }
        self.index = 0
        # creating aliases for unknown namespaces
        for n in namespaces:
            self.index += 1
            self.namespaces[n] = f"ns{self.index}:"
        # DB is a tree (made with dicts) similar to turtle representation
        # { "ns1:s1" : { "ns2:p1" : {"ns3:o1" : 1, "ns3:o2" : 4, ...}, ... }, ...  }
        # Warning: the last dict contains the number of occurences found
        # sb contains only aliases of namespaces unless the namespace has no alias
        self.db = {}


    def get_domain_alias(self, iri):
        if not iri.namespace in self.namespaces:
            self.index += 1
            self.namespaces[iri.namespace] = f"ns{self.index}:"
        return self.namespaces[iri.namespace]
        

    def add(self, s, p, o, verbose=False) -> bool:
        if isinstance(s, IntLiteral) or isinstance(s, TextLiteral):
            print("Literal cannot be subject of a RDF triple")
            return False
        if isinstance(p, IntLiteral) or isinstance(p, TextLiteral):
            print("Literal cannot be predicate of a RDF triple")
            return False
        # s should be a IRI - the BlankNode case is not implemented
        if not isinstance(s,IRI):
            print("Subject should be a IRI")
            return False
        if isinstance(p,IntLiteral) or isinstance(p, TextLiteral) or isinstance(p, BlankNode):
            print("Predicate should be a IRI")
            return False
        if isinstance(o, BlankNode):
            print("Object cannot be a BlankNode")
            return False
        # do we know the namespace?
        sub = self.get_domain_alias(s) + s.value
        pred = self.get_domain_alias(p) + p.value
        obj = ""
        if isinstance(o, IRI):
            obj = self.get_domain_alias(o) + o.value
        else:
            if isinstance(o, TextLiteral):
                obj = str(o)
            else:
                obj = o.value
        # we have the three members, now we put them in DB
        if sub in self.db:
            if pred in self.db[sub]:
                if obj in self.db[sub][pred]:
                    self.db[sub][pred][obj] += 1
                else:
                    self.db[sub][pred][obj] = 1
            else:
                self.db[sub][pred] = {obj : 1}
        else:
            self.db[sub] = {pred : {obj : 1}}
        return True

    
    def remove(self, s, p, o, verbose=False) -> bool:
        if not s.namespace in self.namespaces:
            print(f"Subject namespace '{s.namespace}' unknown in RDFDB")
            return False
        key1 = self.namespaces[s.namespace] + s.value
        if key1 not in self.db:
            print(f"Suject '{key1}' unknown in RDFDB")
            return False
        if not p.namespace in self.namespaces:
            print(f"Predicate namespace '{p.namespace}' unknown in RDFDB")
            return False
        key2 = self.namespaces[p.namespace] + p.value
        if key2 not in self.db[key1]:
            print(f"Predicate '{key1}' unknown in RDFDB")
            return False
        if isinstance(o, IRI):
            if o.namespace not in self.namespaces:
                print(f"Object namespace '{o.namespace}' unknown in RDFDB")
                return False
            key3 = self.namespaces[o.namespace] + o.value
        else:
            # o is a Literal
            key3 = str(o) if isinstance(o, TextLiteral) else o.value
        if key3 not in self.db[key1][key2]:
            print(f"Object '{key1}' unknown in RDFDB")
            return False
        if len(self.db[key1][key2]) != 1:
            # easy, one object t remove
            del self.db[key1][key2][key3]
            return True
        else:
            # that means that the predicate dict can also be deleted
            # can we delete the subject also?
            if len(self.db[key1]) == 1:
                #we must delete everything
                del self.db[key1]
                return True
            else:
                #there are several predicates attached to the same subject
                del self.db[key1][key2]
                return True
        
    def dump(self):
        with open(self.name + ".ttl", "w", encoding="utf-8") as f:
            for n in self.namespaces:
                f.write(f"@prefix {self.namespaces[n]} <{n}> .\n")
            f.write("\n")
            stri = ""
            for s in self.db:
                stri = s
                ps = list(self.db[s].keys()) # array of predicates
                lenps = len(ps)
                if lenps == 1:
                    # we are on the line of the subject
                    stri += " " + ps[0] + str_for_objects( self.db[s][ps[0]], True)
                else:
                    for j in range(lenps):
                        if j == 0:
                            # we are on the line of the subject
                            stri += " " + ps[0] + str_for_objects( self.db[s][ps[0]], False)
                        elif j == lenps-1:
                            # we are on the last pred line and there were others before
                            stri += "    " + ps[j] + str_for_objects( self.db[s][ps[j]], True)
                        else:
                            stri += "    " + ps[j] + str_for_objects( self.db[s][ps[j]], False)
                f.write(stri + "\n")

                
#----------------------------------------------------------- str_for_objects
def str_for_objects(dic, lastP=False):
    '''
    dic = {o1 : nb1, o2, nb2, ...}
    '''
    stri = ""
    keys = list(dic.keys())
    # one object + we are on the line on the last predicate
    if len(dic) == 1 and lastP:
        return f" {keys[0]} .\n"
    # on bject + we are on the line on the predicate
    if len(dic) == 1:
        return " " + str(keys[0]) + " ;\n"
    for i in range(len(keys)):
        if i == 0:
            # we are on the line of the predicate
            stri += " " + str(keys[0]) + " ,\n"
        elif i == len(keys) -1:
            # we are on the last line
            if lastP:
                stri += "        " + str(keys[i]) + " .\n"
            else:
                stri += "        " + str(keys[i]) + " ;\n"
        else:
            stri += "        " + str(keys[i]) + " ,\n"
    return stri
            


#----------------------------------------------------------- test
def test():
    '''
    ns1:20506 a ns1:Word ;
    rdf:value "chrysoprase"@fr ;
    ns1:InstancesInDict 1 ;
    ns1:Rank 1 .
    '''
    namespace = "https://test.com/blurp#"
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    db = RDFDB("test",[namespace])
    a = IRI(namespace,"20506")
    db.add(IRI(namespace,"20506"), IRI(rdf, "value"), TextLiteral("chrysoprase", "fr"))
    db.add(IRI(namespace,"20506"), IRI(namespace, "InstancesInDict"), IntLiteral(4))
    db.add(IRI(namespace,"20506"), IRI(namespace, "InstancesInDict"), IntLiteral(2))
    db.add(IRI(namespace,"44444"), IRI(rdf, "value"), TextLiteral("johnny go", "en"))
    db.add(IRI(namespace,"44444"), IRI(namespace, "FollowedBy"), IRI(namespace, "55555"))
    db.add(IRI(namespace,"79797"), IRI(namespace, "LooksAt"), IRI(namespace, "TOTO"))
    db.add(IRI("http://test-namespace.com/","79797"), IRI(namespace, "LooksAt"), IRI(namespace, "TOTO"))
    mybreakpoint(f"Dump of memory DB\n {db.db}")

    # tests of deletion
    db.remove(IRI(namespace,"20506"), IRI(namespace, "InstancesInDict"), IntLiteral(2))
    mybreakpoint(f"After deleting just one object in s=20506\n {db.db}")
    db.add(IRI(namespace,"20506"), IRI(namespace, "InstancesInDict"), IntLiteral(2))
    mybreakpoint(f"After recreating the object\n {db.db}")
    db.remove(IRI(namespace,"44444"), IRI(rdf, "value"), TextLiteral("johnny go", "en"))
    mybreakpoint(f"After deleting just one object in s=44444\n {db.db}")
    db.add(IRI(namespace,"44444"), IRI(rdf, "value"), TextLiteral("johnny go", "en"))
    mybreakpoint(f"After recreating the object\n {db.db}")
    db.remove(IRI("http://test-namespace.com/","79797"), IRI(namespace, "LooksAt"), IRI(namespace, "TOTO"))
    mybreakpoint(f"After deleting just one object in s=79797\n {db.db}")
    db.add(IRI("http://test-namespace.com/","79797"), IRI(namespace, "LooksAt"), IRI(namespace, "TOTO"))
    db.dump()

    
#======================================================== main
if __name__ == "__main__":
    tests_string2uri()
    test()
    


