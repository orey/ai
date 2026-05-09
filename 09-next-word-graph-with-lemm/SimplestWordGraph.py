from collections import defaultdict
from heapq import nlargest

#============================================= WordGraph
class WordGraph:
    def __init__(self, name="DefaultWordGraph"):
        self.name = name
        self.next_id = 0

        self.labels = {}          # id -> label
        self.ids = {}             # label -> id
        self.ranks = defaultdict(int)
        self.edges = set()
        self.types = {} # id -> [types]

    @staticmethod
    def _edge(a, b):
        if a > b:
            a, b = b, a
        return (a << 32) | b

    def add_node(self, label):
        """
        Add node only if it does not already exist.
        Returns node id.
        """

        id = self.ids.get(label)

        if id is not None:
            return id

        id = self.next_id
        self.next_id += 1

        self.ids[label] = id
        self.labels[id] = label

        return id

    def add_types_to_node(self, label, types):
        id = self.ids.get(label)
        self.types[id] = types        

    def add_edge(self, label_a, label_b):
        """
        Add edge only if it does not already exist.
        Automatically creates missing nodes.
        """

        if label_a == label_b:
            return

        a = self.add_node(label_a)
        b = self.add_node(label_b)

        e = self._edge(a, b)

        if e not in self.edges:
            self.edges.add(e)
            self.ranks[a] += 1
            self.ranks[b] += 1

    def top_ranks(self, n):
        return [
            (self.labels[id], rank)
            for id, rank in nlargest(
                n,
                self.ranks.items(),
                key=lambda x: x[1]
            )
        ]

    def count(self):
        print(f"Graph '{self.name}' contains {len(self.ids)} nodes and {len(self.edges)} edges")
        

#============================================= test
def testWordGraph():
    g = WordGraph()

    g.add_edge("cat", "animal")
    g.add_edge("dog", "animal")
    g.add_edge("cat", "pet")
    g.add_edge("dog", "pet")

    g.add_edge("animal", "cat")   # ignored (same edge)
    g.add_node("cat",["noun"])    # ignored (already exists)
    
    print(g.top_ranks(10))
    print(g)
    g.count()

if __name__ == "__main__":
    testWordGraph()
    
