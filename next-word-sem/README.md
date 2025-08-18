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

### Impact on rdfdb

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

## Execution

`BibleSegond.ttl` se charge correctement dans Jena. Le fichier n'est pas dans github mais peut être reconstitué en faisant:

```
python next-word-sem-v2.py
```

Nombre de triples dans Jena : 4 187 258. Mais ce chiffre est trompeur car le cas de test fait un scan 4, 3 du texte (4 mots avant liés avec des suites de 3 mots après). On pourrait juste prédire le mot suivant.

## TODO

* Revoir le code de tokenization car problème sur les `"`.
* Protéger les classes IRI et Literal de RDFDB similairement à ce qui a été fait dans `csv2rdf`.
* Implémenter le `count` en mode annotation rdf*. Cela servira pour l'algo de next word quand ce dernier tournera sur base de données Jena, car dans le cas de la base de données mémoire, aucun besoin de RDF\*..
* Implémenter le générateur de texte. Dans un premier temps, il peut être basé sur les structures mémoire de la base. Dans un second temps, le faire sur la base.
* Travailler la notion de dimension sémantique dans le cadre du choix de la suite. Les LLMs le font. Il faudrait loader un dictionnaire analogique dans le corpus et travailler sur base des dimensions sémantiques proposées.
