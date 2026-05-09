/*-----------------------------------------------------
Author: O. Rey
email: rey.olivier@gmail.com
Date: March 18 2019
Neighborhood request calculation
License: Apache 2
-------------------------------------------------------
This section is an implementation of the standard
http://rdf.js.org/

Some liberty was taken with the standard that is pushing
for the use of the DataFactory, making it difficult to use
directly the various class structures.
Our interpretation of the standard makes it possible to
use the classes inside the standard, not only through
the factory, and so to have libraries, manipulating those
objects.
This requirement is mandatory if we consider that each
single object, in order to be displayed as a graph,
will need to have an ID => false.
In order to represent them, we have also the obligation of
making them unique, which implies class customization 
or subclassing.
------------------------------------------------------*/

//var uuidv4 = require('uuid/v4');

const DEFAULT_GRAPH = "DEFAULT";

const NAMED_NODE = "NamedNode";
const BLANK_NODE = "BlankNode";
const LITERAL    = "Literal";
const VARIABLE   = "Variable";
const GRAPH      = "DefaultGraph";

/**
 * Root class of the hierarchy
 */
class Term {
    constructor(termType, value) {
        if (termType.constructor.name != "String")
            throw new TypeError("termType should be a String. Provided type: " +
                                termType.constructor.name);
        this.termType = termType;
        if (value.constructor.name != "String")
            throw new TypeError("value should be a String. Provided type: " +
                                value.constructor.name);
        this.value = value;
//	this.id = uuidv4();
    }
    equals(t){
        if ((t.termType == this.termType) && (t.value == this.value))
            return true;
        else
            return false;
    }
    to_str(){
        return "== Term == Termtype: " + this.termType + " | Value: " + this.value;
    }
    get_rdf_object(){
        if (this.termType == NAMED_NODE)
            return new NamedNode(this.value);
        else if (this.termType == BLANK_NODE)
            return new BlankNode(this.value);
        else if (this.termType == LITERAL)
            return new Literal(this.value);
        else if (this.termType == VARIABLE)
            return new Variable(this.value);
        else
            throw new TypeError("Unknown term type: " + termType);
    }
}

// Liberty with the standard, the object is directly buildable
// because I need it.
class NamedNode extends Term{
    constructor(value){
        super(NAMED_NODE, value);
    }
    to_str(){
        return "<" + this.value + ">";
    }
}

// Liberty with the standard, the object is directly buildable
// because I need it.
class BlankNode extends Term{
    constructor(value){
        super(BLANK_NODE, value);
    }
    to_str(){
        return "<" + this.value + ">";
    }
}

// Interpretation of the standard
class Literal extends Term{
    constructor(value, languageOrDatatype = "en"){
        super(LITERAL, value);
        let ltype = languageOrDatatype.constructor.name;
        if (ltype == "String") {
            this.language = languageOrDatatype;
            this.datatype = null;
        }
        else if (ltype == "NamedNode"){
            this.language = "";
            this.datatype = languageOrDatatype;
        }
        else {
            throw new TypeError(
                "languageOrDataType should be a String or a NamedNode. Provided: "
                    + ltype);
        }
    }
    equals(t){
        // Interpretation of the standard
        if ((t.termType == this.termType) && (t.value == this.value) &&
            (t.language == this.language) && this.datatype.equals(t.datatype))
            return true;
        else
            return false;
    }
    to_str(){
        return '"' + this.value + '"';
    }
}

class Variable extends Term{
    constructor(value){
        super(VARIABLE, value);
    }
    to_str(){
        return "[" + this.value + "]";
    }
}

class DefaultGraph extends Term{
    constructor(value = "default"){
        super(GRAPH, value);
    }
    to_str(){
        //return "(" + this.value + ")";
        return this.value;
    }
}

class Quad {
    constructor(subject, predicate, object, graph){
        if ((!subject instanceof Term) ||
            (!predicate instanceof Term) ||
            (!object instanceof Term) ||
            (!graph  instanceof Term))
            throw new TypeError("Arguments of Quad constructor must all be of type Term");
        this.subject = subject;
        this.predicate = predicate;
        this.object = object;
        this.graph = graph;
    }
    equals(q){
        if (this.subject.equals(q.subject) && this.predicate.equals(q.predicate) &&
            this.object.equals(q.object) && this.graph.equals(q.graph))
            return true;
        else
            return false;
    }
    to_str(){
        return this.graph.to_str() + " | " +
            this.subject.to_str() + " " +
            this.predicate.to_str() + " " +
            this.object.to_str() + " .";
    }
    get_graph(){
        return this.graph;
    }
    get_subject(){
        return this.subject;
    }
    get_predicate(){
        return this.predicate;
    }
    get_object(){
        return this.object;
    }
}

// Interpretation of the standard
// This factory is not so easy to use because it does not reveal the real
// types of objects.
class DataFactory{
    namedNode(value){
        return new NamedNode(value);
    }
    blankNode(value = ""){
        return new BlankNode(value);
    }
    literal(value, languageOrDatatype){
        return new Literal(value, languageOrDataType);
    }
    //Optional method
    variable(value){
        return new Variable(value);
    }
    // The standard method has no parameter, which is weird. Taking
    // liberty with the standard.
    defaultGraph(value = ""){
        return new DefaultGraph(value);
    }
    quad(subject, predicate, object, graph=null){
        if (graph == null)
            return new Quad(subject, predicate, object, new DefaultGraph("DEFAULT"));
        else
            return new Quad(subject, predicate, object, graph);
    }
}


/*-----------------------------------------------------
Tests
To run on the console:
$ node -e "var a = require('./rdfjs.js');a.test()"
------------------------------------------------------*/
function test(){
    q = new Quad(new NamedNode("dc:toto"), new NamedNode("a"),
                 new Literal("Rouboudou", "en"), new DefaultGraph("books"));
    console.log(q.to_str());
}

/*----------------------------------------------------------
Exports
----------------------------------------------------------*/
module.exports = {
    Term : Term,
    NamedNode : NamedNode,
    BlankNode : BlankNode,
    Literal : Literal,
    Variable : Variable,
    DefaultGraph : DefaultGraph,
    Quad : Quad,
    DataFactory : DataFactory,
    test : test,
    NAMED_NODE : NAMED_NODE,
    BLANK_NODE :BLANK_NODE,
    LITERAL : LITERAL,
    VARIABLE : VARIABLE
}

