########################################################
# RDF DB for AI tests
# O. Rey - August 2025
########################################################

URI = "URI"
BLANK_NODE   = "BLANK_NODE"
TEXT_LITERAL = "TEXT_LITERAL"
INT_LITERAL  = "INT_LITERAL"


#====================================================================== Term
class Term():
    def __init__(self, namespace: str, value: str):
        self.namespace = namespace
        self.value = value
        self.type = None


#====================================================================== URI
class URI(Term):
    def __init__(self, namespace: str, value: str):
        super().__init__(namespace, value)
        super().type = URI
        

    def to_str(self) -> str:
        return f"<{self.namespace}{self.value}>"

#====================================================================== BlankNode
class BlankNode():
    def __init__(self, namespace: str, value: str):
        super().__init__(namespace, "_")
        super().type = BLANK_NODE
        
    def to_str(self) -> str:
        return f"<{self.namespace}{self.value}>"


#====================================================================== TextLiteral
class TextLiteral():
    def __init__(self, namespace: str, value: str, language="en"):
        super().__init__(namespace,value)
        self.language = language
        super().type = TEXT_LITERAL        

    def to_str(self) -> str:
        return f"\"{self.value}\"@{self.language}"

#====================================================================== IntLiteral
class IntLiteral():
    def __init__(self, namespace: str, value: str):
        self.namespace = namespace
        self.value = value
        super().type = INT_LITERAL
        
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
            self.namespace[n] = "ns" + i + ":"
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
        
        
    def add(self, s, p, o, verbose) -> bool:
        if type(s) in ["IntLiteral", "TextLiteral"]:
            print("Literal cannot be subject of a RDF triple")
            return False
        if type(p) in ["IntLiteral", "TextLiteral"]:
            print("Literal cannot be predicate of a RDF triple")
            return False
        # s should be a URI - the BlankNode case is not implemented
        if type(s) != "URI":
            print("Subject should be a URI")
            return False
        if type(p) in  ["IntLiteral", "TextLiteral", "BlankNode"]:
            print("Predicate should be a URI")
            return False
        if type(o) == "BlankNode":
            print("Object cannot be a BlankNode")
            return False
        # do we know the namespace?
        sub = build_rep(s)
        pred = build_rep(p)
        obj = ""
        if type(o) == "URI":
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
                f.write(f"@prefix {self.namespaces[n]} <{n}> .\n")
            f.write("\n")
            str = ""
            for s in self.db:
                str = s + 
                for p in self.db[s]:
                    for o in self.db[s][p]:


if __name__ == "__main__":
    test = URI("namespace", "/value")
    toto = 


