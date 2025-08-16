########################################################
# RDF DB for AI tests
# O. Rey - August 2025
########################################################

import sys, time
sys.path.append('.')
from tools8 import mybreakpoint


#====================================================================== URI
class URI():
    def __init__(self, namespace: str, value: str):
        self.namespace = namespace
        self.value = value

    def to_str(self) -> str:
        return f"<{self.namespace}{self.value}>"

#====================================================================== BlankNode
class BlankNode():
    def __init__(self, namespace: str, value: str):
        self.namespace = namespace
        self.value = value
        
    def to_str(self) -> str:
        return f"<{self.namespace}{self.value}>"


#====================================================================== TextLiteral
class TextLiteral():
    def __init__(self, namespace: str, value: str, language="en"):
        self.namespace = namespace
        self.value = value
        self.language = language

    def to_str(self) -> str:
        return f"\"{self.value}\"@{self.language}"

#====================================================================== IntLiteral
class IntLiteral():
    def __init__(self, namespace: str, value: int):
        self.namespace = namespace
        self.value = value
        
    def to_str(self) -> str:
        return f"{self.value}"
    
    

#====================================================================== RDFDB
class RDFDB():
    '''
    Simple RDF DB with turtle notation in mind
    '''
    def __init__(self, name, namespaces):
        '''
        namespaces is an array of URI roots finishing by / or #
        will give birth to turtle header
        @prefix ns1: <https://orey.github.io/ai/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        '''
        self.name = name
        self.namespaces = {
            "https://orey.github.io/ai/control#": "ctl:",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf:",
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
            "http://www.w3.org/2001/XMLSchema#": "xsd:"
        }
        i = 0
        # creating aliases for unknown namespaces
        for n in namespaces:
            i += 1
            self.namespaces[n] = f"ns{i}:"
        # DB is a tree (made with dicts) similar to turtle representation
        # { "ns1:s1" : { "ns2:p1" : {"ns3:o1" : 1, "ns3:o2" : 4, ...}, ... }, ...  }
        # Warning: the last dict contains the number of occurences found
        # sb contains only aliases of namespaces unless the namespace has no alias
        self.db = {}


    def build_rep(self, uri):
        urirep = ""
        if uri.namespace in self.namespaces:
            urirep = self.namespaces[uri.namespace] + uri.value
        else:
            urirep = uri.namespace + uri.value
        return urirep
        
        
    def add(self, s, p, o, verbose=False) -> bool:
        if isinstance(s, IntLiteral) or isinstance(s, TextLiteral):
            print("Literal cannot be subject of a RDF triple")
            return False
        if isinstance(p, IntLiteral) or isinstance(p, TextLiteral):
            print("Literal cannot be predicate of a RDF triple")
            return False
        # s should be a URI - the BlankNode case is not implemented
        if not isinstance(s,URI):
            print("Subject should be a URI")
            return False
        if isinstance(p,IntLiteral) or isinstance(p, TextLiteral) or isinstance(p, BlankNode):
            print("Predicate should be a URI")
            return False
        if isinstance(o, BlankNode):
            print("Object cannot be a BlankNode")
            return False
        # do we know the namespace?
        sub = self.build_rep(s)
        pred = self.build_rep(p)
        obj = ""
        if isinstance(o, URI):
            obj = build_rep(o)
        else:
            #Literal
            obj =o.to_str()
        # we have the three members, now we put them in DB
        if s in self.db:
            if p in self.db[s]:
                if o in self.db[s][p]:
                    self.db[s][p][o] += 1
                else:
                    self.db[s][p][o] = 1
            else:
                self.db[s][p] = {o : 1}
        else:
            self.db[s] = {p : {o : 1}}
        return True


    def dump(self):
        with open(self.name + ".ttl", "w", encoding="utf-8") as f:
            for n in self.namespaces:
                f.write(f"@prefix {self.namespaces[n]} <{n}> .\n\n")
            f.write("\n")
            str = ""
            for s in self.db:
                str = s
                ps = list(self.db[s].keys()) # array of predicates
                mybreakpoint(ps)
                lenps = len(ps)
                if lenps == 1:
                    # we are on the line of the subject
                    str += " " + ps[0] + str_for_objects( self.db[s][ps[0]], True)
                else:
                    for j in range(lenps):
                        if j == 0:
                            # we are on the line of the subject
                            str += " " + ps[0] + str_for_objects( self.db[s][ps[0]], False)
                        elif j == lenps-1:
                            # we are on the last pred line and there were others before
                            str += "    " + ps[j] + str_for_objects( self.db[s][ps[j]], True)
                        else:
                            str += "    " + ps[j] + str_for_objects( self.db[s][ps[j]], False)
                f.write(str + "\n")

                        
def str_for_objects(dic, lastP=False):
    '''
    dic = {o1 : nb1, o2, nb2, ...}
    '''
    str = ""
    keys = list(dic.keys())
    # one object + we are on the line on the last predicate
    if len(dic) == 1 and lastP:
        return " " + dic[keys[0]] + " .\n"
    # on bject + we are on the line on the predicate
    if len(dic) == 1:
        return " " + dic[keys[0]] + " ;\n"
    for i in range(len(keys)):
        if i == 0:
            # we are on the line of the predicate
            str += " " + dic[keys[0]] + " ,\n"
        elif i == len(keys) -1:
            # we are on the last line
            if lastP:
                str += "        " + dic[keys[i]] + " .\n"
            else:
                str += "        " + dic[keys[i]] + " ;\n"
        else:
            str += "        " + dic[keys[i]] + " ,\n"
            



def test():
    '''
    ns1:20506 a ns1:Word ;
    rdf:value "chrysoprase"@fr ;
    ns1:InstancesInDict 1 ;
    ns1:Rank 1 .
    '''
    domain = "https://test.com/blurp#"
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    db = RDFDB("test",[domain])
    a = URI(domain,"20506")
    mybreakpoint(isinstance(a, URI))
    db.add(URI(domain,"20506"), URI(rdf, "value"), TextLiteral(domain, "chrysoprase", "fr"))
    db.add(URI(domain,"20506"), URI(domain, "InstancesInDict"), IntLiteral(domain, 4))
    db.add(URI(domain,"20506"), URI(domain, "InstancesInDict"), IntLiteral(domain, 2))
    mybreakpoint(db.db)
    db.dump()


            

if __name__ == "__main__":
    test()
    


