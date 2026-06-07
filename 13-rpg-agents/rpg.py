'''
Simple RPG system
'''
import math, random

#-------------------------------------------------- roll
def roll(nb, faces, pip=0, verbose=False):
    acc = 0
    for i in range(nb):
        temp = random.randint(1, faces)
        if verbose: print(f"Roll number {i+1}: {temp}")
        acc += temp
    acc += pip
    if verbose: print(f"Result: {acc}")
    return acc


#-------------------------------------------------- Character
class Character:
    PHYSICAL = 0
    MENTAL = 1
    AVERAGE = 2
    def __init__(self, name, physical, mental):
        self.name = name
        self.physical = physical
        self.mental = mental
        self.average = math.floor((physical + mental) /2)
    def __repr__(self):
        return f"{self.name} | PHYSICAL: {self.physical} | AVERAGE: {self.average} | MENTAL: {self.mental}"

    
#-------------------------------------------------- Character
class Player:
    def __init__(self, name, character):
        self.name = name
        self.character = character
    def test(self, what, difficulty=0, verbose=False):
        r = roll(1, 20)
        if verbose: print(f"1d20: {r}")
        if what == Character.PHYSICAL:
            if r <= self.character.physical:
                return True
            else:
                return False
        elif what == Character.MENTAL:
            if r <= self.character.mental:
                return True
            else:
                return False
        else:
            if r <= self.character.average:
                return True
            else:
                return False

            
           







    

#-------------------------------------------------- Character
def test():
    roll(2, 6, 3, True)
    roll(3, 6, 1, True)
    # Split 24 points between physical and mental
    conan = Character("Conan", 15, 9)
    print(conan)
    difficulty = 2
    john = Player("john", conan)
    print(f"Physical test: {"Passed" if john.test(Character.PHYSICAL, difficulty, True) else "Failed"}")
    print(f"Mental test: {"Passed" if john.test(Character.MENTAL, difficulty, True) else "Failed"}")
    print(f"Average test: {"Passed" if john.test(Character.AVERAGE, difficulty, True) else "Failed"}")
    

if __name__ == "__main__":
    test()
