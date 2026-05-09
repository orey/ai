import re
from collections import defaultdict, Counter
import random

class MarkovChainTextGenerator:
    def __init__(self, text, window_sizes=[1, 2, 3, 4, 5, 6]):
        self.text = text.lower()  # Convert to lowercase for case-insensitivity
        self.window_sizes = window_sizes
        self.model = defaultdict(list)
        self.build_model()
        
    def preprocess_text(self):
        # Clean and tokenize text
        text = re.sub(r'[^a-z\s]', '', self.text)  # Remove punctuation
        words = text.split()
        return words
    
    def build_model(self):
        words = self.preprocess_text()
        for n in self.window_sizes:
            # Create n-grams (windows) and record next words
            for i in range(len(words) - n):
                window = tuple(words[i:i+n])
                next_word = words[i+n]
                self.model[window].append(next_word)
        
    def generate_text(self, seed_phrase="", length=50):
        if not seed_phrase:
            seed_phrase = random.choice(self.model.keys())
        
        # Start with seed phrase
        words = list(seed_phrase)
        current_window = tuple(words[-self.window_sizes[0]:])
        
        # Generate text
        for _ in range(length):
            # Find the best matching window
            best_match = None
            max_prob = 0
            
            for window_size in self.window_sizes:
                if len(words) >= window_size:
                    candidate = tuple(words[-window_size:])
                    count = self.model.get(candidate, Counter())
                    
                    if count:
                        # Calculate probability of each next word
                        total = sum(count.values())
                        if total > 0:
                            probs = {word: count/total for word, count in count.items()}
                            next_word = self.select_weighted_random(probs)
                            return words + [next_word]
                        else:
                            # If no next words available, use most frequent word
                            if best_match is None or len(count) > 0:
                                best_match = candidate
                                max_prob = total
            
            if best_match is None:
                # If no matches found, use most frequent word overall
                all_words = Counter(self.preprocess_text())
                most_common = all_words.most_common(1)[0][0]
                words.append(most_common)
            else:
                # Use the most frequent next word from the best match
                count = self.model.get(best_match, Counter())
                if count:
                    next_word = max(count.keys(), key=count.get)
                else:
                    next_word = self.select_weighted_random(Counter(self.model.get(tuple(), Counter())))
                words.append(next_word)
        
        return words
    
    def select_weighted_random(self, distribution):
        # Choose a word based on weighted probability
        r = random.random() * sum(distribution.values())
        cumulative = 0
        for word, prob in distribution.items():
            cumulative += prob
            if r <= cumulative:
                return word
        return next(iter(distribution.keys()))
    
    def print_text(self, seed_phrase="", length=50):
        generated_text = self.generate_text(seed_phrase, length)
        print(" ".join(generated_text))

# Example usage
if __name__ == "__main__":
    # Sample text - replace with your own text
    sample_text = """
    The quick brown fox jumps over the lazy dog. 
    This is a sample text for demonstrating the Markov chain text generator.
    The longer the text, the better the results. 
    This sentence is longer than the previous one. 
    We're testing the ability to generate coherent text.
    Another sentence to see how well this works.
    Machine learning is fascinating. 
    Natural language processing is a subfield of linguistics.
    We're building a Markov chain model that predicts the next word.
    The model uses various window sizes to capture different contexts.
    This is a great way to generate creative text.
    """
    
    generator = MarkovChainTextGenerator(sample_text)
    
    # Generate text with different seed phrases
    print("Generated text with seed: 'machine learning'")
    generator.print_text(seed_phrase=("machine learning"), length=20)
    
    print("\nGenerated text with seed: 'the'")
    generator.print_text(seed_phrase=("the",), length=20)
    
    print("\nGenerated text with seed: 'this is'")
    generator.print = lambda seed_phrase, length: generator.print_text(seed_phrase, length)
    generator.print_text(seed_phrase=("this is",), length=20)
    
    print("\nGenerated text with random seed")
    generator.print_text(seed_phrase=None, length=30)
    
