########################################################
# RDF Turtle DB for AI tests
# O. Rey - August 2025
########################################################

import sys, time
sys.path.append('.')
from tools8 import mybreakpoint

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
    

#====================================================================== Major namespaces (to be completed)
class Namespace():
    RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    RDFS = "http://www.w3.org/2000/01/rdf-schema#"
    XSD = "http://www.w3.org/2001/XMLSchema#"


class RDF():
    type = IRI(Namespace.RDF, "type")
    Property = IRI(Namespace.RDF, "Property")
    Seq = IRI(Namespace.RDF, "Seq")
    value = IRI(Namespace.RDF, "Value")


class RDFS():
    subClassOf = IRI(Namespace.RDFS, "subClassOf")
    Class = IRI(Namespace.RDFS, "Class")
    subPropertyOf = IRI(Namespace.RDFS, "subPropertyOf")
    domain = IRI(Namespace.RDFS, "domain")
    range = IRI(Namespace.RDFS, "range")

    
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


            

if __name__ == "__main__":
    test()
    


