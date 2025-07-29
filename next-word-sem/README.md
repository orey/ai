# Notes

The major design difference with the previous design is that the dictionary encapsulates the full RDF database. Because in RDF there is not difference between a single word:

```
dict:12122 a dict:word ;
           value .
```

and a chain of tokens in the common sense of the term:

```
win:12345-23454-66543 a win:window ;
                      win:size 3 ;
                      win:next dict:12122 ;
                      win:next
                        
```
