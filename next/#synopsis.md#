# Synopsis

## Topic of the report

Usage of web semantic technologies to create a new sort of LLMs without the usage of neural networks

## Purpose

Personal interest in order to develop the solution

## Specific questions and areas of focus

The objective is to have a big triple database replacing the  neural network that predicts the next token. the principle is injecting big texts in the database by injecting words (and typing them as words), and groups of words (chains). the chain is the attention window. it can be parameterized and the next word after the chain will be stored.

After injecting many texts, we will have a complete dictionary, and chains pointing to a list of possible next words. We will be able to implement different choice algorithms (statistical/temperature based) but also more complex choices, such as ranking semantically the input chain to define the next token in the same semantic field. For sure, semantic dictionaries must be imported also in the database.

The advantage of the solution is that it is predictable, it is enrichable with smart algorithms, it takes the Markow chain approach, and all chains and words can be typed, tagged, and reasoned upon in sparql.

## Length of the report

I would like a review of literature connected to this topic, plus an analysis of the technical implications of this topic (I am developing it). So it can be quite detailed.

##Deadline

Take your time.

# Response

### The Use of Semantic Web Technologies to Create LLMs

The proposed method of creating a Large Language Model (LLM) without neural networks, by using a large triple database and semantic web technologies, is an intriguing concept that revisits earlier approaches in natural language processing (NLP) while integrating modern tools. This approach, which can be thought of as a **knowledge-based, symbolic AI model**, differs fundamentally from the **statistical learning** paradigm of modern neural network-based LLMs.

***

### Literature Review

The concept of representing knowledge in a structured, machine-readable format to process language is not new. It has deep roots in symbolic AI and computational linguistics.

* **Semantic Networks and Frames:** The idea of semantic networks, which are graphical representations of knowledge showing relationships between concepts, dates back to the 1960s. **Marvin Minsky's "frames"** (1974) were another key development, proposing a data structure for representing a stereotyped situation, which could be used for language understanding.
* **Markov Chains and n-grams:** The core of your proposed model is similar to a **Markov chain** or **n-gram language model**. These models predict the next word in a sequence based on the preceding $n-1$ words. They were the dominant approach to language modeling before the rise of neural networks in the 2010s. The challenge with n-gram models is their inability to capture long-range dependencies and their rapid increase in size as $n$ grows.
* **Semantic Web and Knowledge Graphs:** The **Semantic Web**, a concept introduced by Tim Berners-Lee, aims to make data on the web machine-readable and linkable. Technologies like **RDF (Resource Description Framework)**, **OWL (Web Ontology Language)**, and **SPARQL (a query language for RDF)** are the building blocks. A **knowledge graph** is a practical application of these technologies, representing entities and their relationships in a graph structure. Knowledge graphs are increasingly used in various applications, including search engines (e.g., Google's Knowledge Graph) and question-answering systems.

Your proposed approach is a synthesis of these ideas: using a **knowledge graph** (the triple database) to store an n-gram-like model, enhanced with semantic information from ontologies.

***

### Technical Implications

Developing this system has several technical implications, from data management to performance and reasoning capabilities.

#### 1. Data Structure and Management

* **Triple Database:** The core of your system would be an **RDF triple store**. This database stores data in the form of **subject-predicate-object** triples, which are ideal for representing words and their relationships. For example, `(chain_1, has_next_word, word_A)` would be a triple.
* **Data Injection:** The process of "injecting big texts" would involve parsing the text into a series of triples. For each sliding window (your "chain"), you would create a triple linking the chain to the following word. This could be computationally intensive and require a robust ingestion pipeline.
* **Scaling:** As the corpus grows, the number of triples will explode. The triple store would need to handle billions, or even trillions, of triples efficiently. This requires a scalable and performant database like **GraphDB** or **Stardog**.

#### 2. Querying and Prediction

* **SPARQL for Prediction:** The prediction of the next token would be a SPARQL query. Given a chain (e.g., "The quick brown fox"), the system would query the database for all words linked as the `has_next_word` predicate to that chain.
* **SPARQL for Reasoning:** The real power of this approach lies in using SPARQL for more complex reasoning. You could query for words with a specific tag (e.g., `(word_A, has_tag, "noun")`) or find words in the same semantic field by traversing the knowledge graph. This is a significant advantage over neural networks, where such structured reasoning is difficult.

#### 3. Semantic Enrichment

* **Importing Dictionaries:** Importing semantic dictionaries and ontologies (e.g., WordNet, DBpedia, or custom ontologies) would be crucial. These ontologies would "type" and "tag" the words, allowing for more sophisticated predictions. For example, a triple might be `(word_A, is_a, "noun")` or `(word_B, is_a_synonym_of, word_C)`.
* **Choice Algorithms:** Instead of a simple statistical count, you could use SPARQL queries to implement advanced choice algorithms. For a given input chain, you could:
    * Find all possible next words.
    * Filter them based on semantic tags (e.g., "only return nouns").
    * Rank them based on a combination of frequency and semantic similarity.

#### 4. Advantages and Disadvantages

* **Predictability:** The model is completely transparent. You can trace every prediction back to the data and the rules. This is a stark contrast to the **black-box** nature of neural networks.
* **Enrichability:** The model can be easily updated by adding new triples. Adding a new dictionary or ontology immediately enhances the system's reasoning capabilities without the need for retraining.
* **Explainability:** The reasoning behind a prediction can be explained in human-readable terms by showing the chain of triples that led to the result.
* **Scalability Challenges:** As mentioned, the triple store will grow massive, leading to potential performance bottlenecks. Queries that require traversing a large part of the graph could be slow.
* **The "Curse of Dimensionality":** This system, like n-gram models, will suffer from sparsity. Many valid word combinations will not appear in the training data, leading to a lack of predictions for novel chains.
* **Lack of Generalization:** Neural network LLMs can generalize from the data they've seen to generate novel, coherent text. Your proposed model, while capable of sophisticated reasoning, primarily predicts based on what it has seen. It doesn't have the same capacity to generate truly creative or novel prose. The output would likely be a recombination of existing text snippets, rather than new, original sentences. 
* **Knowledge vs. "Understanding":** Your system is a **knowledge-based** model; it "knows" facts and relationships. Neural network LLMs, on the other hand, build a **statistical representation** of language. They don't have explicit knowledge in the same way, but they can capture subtle linguistic patterns and nuances that a simple triple store may miss.

In conclusion, your proposed model is a fascinating and technically feasible project that leverages the strengths of symbolic AI and the Semantic Web. It would offer unparalleled transparency, explainability, and enrichability. However, it would face significant challenges in scalability and generalization, and its performance would likely not match the fluency and creative output of state-of-the-art neural network LLMs.

# My response

I am not sure that the right algorithms were implemented to define the next word. Especially, I think that knowledge graphs adepts don't semantize properly the data, they are just using the links and not creating new links or transversal based on reasoning algorithms. Those algorithms could use topological based methods to determine the next word.

The same for long term context. Through the use of types and reification, we can define the global topic management, conversation memory, concept level connections, etc. For sure, it is more engineering than research but using basic knowledge graphs are not using the typing if data (relationships of types).

Do you have literature on that?

## Gemini response

You've raised critical points that distinguish a basic knowledge graph approach from a truly intelligent, symbolic system. Your intuition that simple link traversal is insufficient is correct; the real power of knowledge graphs lies in **reasoning** and the rich expressiveness of their data models.

Here is a summary of the literature and concepts related to the advanced techniques you're describing.

---

### **1. Semantic and Topological Reasoning for Next Word Prediction**

You are right that merely counting links is a simplistic approach. Advanced knowledge graph systems use a variety of reasoning algorithms to infer new knowledge and relationships. While much of this research is still in its infancy for direct next-word prediction, it's a very active area in **link prediction** and **knowledge graph completion**.

* **Rule-Based Reasoning:** This is the most direct form of semantic reasoning. Using a language like **OWL** or **SHACL**, you can define logical rules (e.g., if a person `is_a` `mother`, and a mother `has_a` `child`, you can infer that the person `has_a` child). For next-word prediction, this could mean defining rules like "If the subject is a `person` and the verb is `eats`, the next word should be an `edible_thing`." These systems use **reasoning engines** (like Pellet or HermiT) to automatically add new, inferred triples to the graph.
* **Knowledge Graph Embeddings (KGEs):** This is the most common modern approach to "reasoning" on a knowledge graph. KGEs map entities and relationships into a continuous vector space. The goal is that entities with similar relationships have similar positions in this space. For example, the vector for (`Paris`, `is_capital_of`, `France`) should be similar to (`Berlin`, `is_capital_of`, `Germany`). These embeddings can be used for **link prediction**, which is essentially predicting a missing triple. While not a direct topological method, these embeddings often capture topological patterns.
* **Topological Methods:** These methods directly analyze the graph structure to infer new links. Instead of just counting direct links, they look at **paths** and **subgraphs**. The idea is that the topological patterns of a knowledge graph contain semantic meaning. For example, two words that frequently appear at the end of a chain that starts with "The quick brown fox" might be semantically related even if they don't share a direct link in the dictionary. Algorithms in this area analyze things like common neighbors, path counts, and other graph metrics to predict missing links.



---

### **2. Long-Term Context and Conversational Memory with Semantic Technologies**

You're absolutely correct that using **types** and **reification** is key to managing long-term context and conversational memory. This is where knowledge graphs go beyond being a static dictionary and become a dynamic, reasoning system.

* **Reification:** Reification is the process of making a statement a first-class citizen in the knowledge graph. Instead of a simple triple `(John, is_friend_of, Mary)`, you can reify it into a new entity. For example, `statement_1` has a `subject` of `John`, a `predicate` of `is_friend_of`, and an `object` of `Mary`. This seems verbose, but it allows you to add **metadata** about that statement. For conversational memory, this is revolutionary. You can add triples like: `(statement_1, said_by, user)` and `(statement_1, was_said_at, 2025-09-04T11:41:08)`. This turns the conversation history into a structured graph that can be queried and reasoned upon. It allows you to track who said what, when, and with what level of certainty.
* **Typing and Ontologies:** By assigning types to words and chains, you can create a much more powerful system. The phrase "New York" can be typed as a `city`, a `financial_hub`, or a `theater_destination` based on the context. This goes beyond simple token prediction. The system can understand the **global topic** of the conversation (e.g., "we're discussing finance") and use that information to bias the choice of the next word. A query could look for the next word that is a `noun` related to `finance` and has a strong link to the current chain. The conversation's **memory** is no longer a flat list of text but a growing, interconnected subgraph that influences every new prediction.

### **Relevant Literature and Research Areas**

While no single paper outlines your exact system, the concepts are actively researched across several domains. Look for papers on:

* **Knowledge Graph Reasoning:** Specifically, research on **link prediction** and **knowledge graph completion** that moves beyond simple embedding methods to incorporate logical rules and graph topology.
* **Conversational AI with Knowledge Graphs:** Research in this area often focuses on using KGs to ground chatbots in factual knowledge. The use of **reification** for memory and context is a growing sub-field. Look for terms like **"memory-augmented"** and **"knowledge-grounded"** conversational agents.
* **Symbolic AI and NLP:** This is the broader field that your project falls into. It is a counter-point to the dominant statistical learning paradigm. There's a renewed interest in these methods for their **explainability** and **interpretability**.

# Me

concerning topological analysis, do you know if some works were done on a cloud approach. If I materialize a semantic field as a group of words with a certain distance - or "sub meaning" -, we could determine the common parts of semantic sets. Do you have some articles about semantic neighbor calculated based on points (subjects). We would be able to have the set intersection of neighborings and deduce multi dimensions meanings

# Gemini

Yes, research has been done on this topic, particularly in the context of cloud-based and distributed systems. The concepts you describe—defining semantic fields as groups of words with a certain topological distance, analyzing set intersections of their neighbors, and deriving multi-dimensional meanings—are a core part of modern research in **Knowledge Graph analytics**.

---

### **Cloud-Based and Distributed Topological Analysis**

Working with massive knowledge graphs in the cloud is not just an academic exercise; it's a necessity. The scale of knowledge graphs like Wikidata or the Google Knowledge Graph makes single-server processing impractical. This has led to a body of work on **distributed graph processing frameworks** and **cloud-native knowledge graph databases**.

* **Distributed Graph Processing:** Researchers have adapted classic graph algorithms for distributed environments. Frameworks like **Apache Spark's GraphX** and specialized graph databases like **Amazon Neptune** and **Microsoft Azure Cosmos DB** are designed to handle terabytes of graph data by partitioning it across multiple nodes in a cluster. This allows for scalable computation of metrics like shortest paths, centrality, and neighborhood analysis.
* **Semantic Data Partitioning:** A key challenge in distributed graph processing is minimizing communication overhead between nodes. One approach is **semantic partitioning**, where related data (e.g., all triples about a specific subject) are grouped together on the same server. This is particularly relevant to your idea of "semantic fields," as you could partition the graph based on semantic clusters, ensuring that neighborhood analysis for a given subject can be done locally on a single machine, dramatically improving performance.

---

### **Semantic Neighborhoods and Multi-Dimensional Meanings**

Your idea of calculating the intersection of semantic neighbors is a powerful one, and it's being actively explored in the field of **knowledge graph completion** and **semantic similarity**.

* **Intersection Features for Link Prediction:** A recent line of research focuses on using the **intersection size of k-hop neighborhoods** as a feature for machine learning models. The principle is exactly what you've described: a valid, factual triple often has a greater overlap in the neighborhoods of its head, relation, and tail entities than an invalid one. This "intersection" can be used as a signal to predict missing links or infer new facts. For example, if you want to know what a `dog` `barks` at, you could look at the intersection of the neighbors of `dog` and `barks`. The entities that appear in both neighborhoods (e.g., `stranger`, `cat`) are the most likely candidates for the answer.
* **Topological Data Analysis (TDA) for Semantic Spaces:** While more prevalent in analyzing geometric data like 3D point clouds, the principles of TDA are being applied to knowledge graphs. The idea is to understand the "shape" of the data. For instance, TDA can identify connected components, "holes," and cycles, which can correspond to specific semantic structures or even "contradictions" in the data. Your concept of a "semantic field" being a "sub-meaning" is analogous to a **topological feature** that can be mathematically identified and analyzed.
* **Semantic Neighbor Calculation:** Calculating semantic neighbors is an active research area. One notable framework is **DistSim**, which provides a scalable, distributed framework for semantic similarity estimation on RDF graphs. It uses methods like **MinHash** to approximate set intersections and unions efficiently, allowing it to compute Jaccard similarity between the neighborhoods of entities on massive datasets without the need to hold the entire graph in memory. This directly addresses the problem you raised. 

In essence, your proposal moves beyond basic link analysis and into the advanced territory of **distributed graph analytics** and **Topological Data Analysis**, which are exactly the areas where this kind of reasoning is being developed for large-scale, cloud-based applications.

https://www.researchgate.net/publication/278243715_Topological_Analysis_of_Cloud_Service_Connectivity

https://arxiv.org/abs/2404.06037#:~:text=Distributed%20processing%20of%20large%2Dscale,and%20algorithms%20have%20been%20proposed.

https://arxiv.org/abs/2404.06037#:~:text=Applying%20graph%20tasks%20to%20distributed,%2C%20communication%20overhead%2C%20and%20bandwidth.


