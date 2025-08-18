# Notes

## Design options

See the semantic model in the `graphml` file. The grammar of the graph is in the static class `Sem`.

The objective is to feed a semantic graph with:

* The words and punctuation:
    * They are represented by a token 
    * This could be extended with a real semantic typing of verbs, adjectives, pronouns, etc. in the future;
* The sequences that are treated as words.

## How to count the number of triples in the followed_by relationship?

### Reify the relation as a resource

Instead of storing the edge as a plain triple, turn it into a node (a "statement resource") with properties:

```
:A :follows [
    a :FollowRelation ;
    :to :B ;
    :count 4
] ;
:follows [
    a :FollowRelation ;
    :to :C ;
    :count 1
] .
```

This way:

You can attach metadata (:count) about the relation itself.

Querying is simple:

```
SELECT ?target ?count WHERE {
  :A :follows [ :to ?target ; :count ?count ] .
}
```

Scales well, doesn’t clutter the ontology with extra properties.

## Impact on rdfdb

The memory storage of rdfdb is mirroring this design:

```
{ A : { follows : { B : 4, C : 1}}}
```

Indeed the `follows` relation in this sample is no more a semantic `follows`, it is a semantic `owns`.

```
:A :owns [
    a :FollowRelation ;
    :to :B ;
    :count 4
] ;
:owns [
    a :FollowRelation ;
    :to :C ;
    :count 1
] .
```

Epanded:

```
:A :follows _:b1 .
_:b1 a :FollowRelation .
_:b1 :to :B .
_:b1 :count 4 .

:A :follows _:b2 .
_:b2 a :FollowRelation .
_:b2 :to :C .
_:b2 :count 1 .
```

### Usage of rdf*

```
<< :A :follows :B >> :count 4 .
```

This is the equivalent of :

```
_:stmt a rdf:Statement ;
       rdf:subject   :A ;
       rdf:predicate :follows ;
       rdf:object    :B ;
       :count        4 .
```

