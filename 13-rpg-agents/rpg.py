'''
Simple RPG system
'''
import math, random

import sys
sys.path.append('.')
from ollama_connector import ask_llm
from pcs import ROLE_JOE, ROLE_ALICE, BACKGROUND_CONAN, BACKROUND_SARTIA

#-------------------------------------------------- Rules
RULES = '''# Rules of the table top roleplaying game

## Stats

Your Player Character (PC) has 3 stats: Physical, Mental and Average (whiwh is the average of the 2 other stats).

Depending on the tasks that the GM will ask, you will call a tool name "check" to throw 1d20 (see Form2 below). The objective is to have a result that is inferior or equal to the stat the GM will mention.

## Interaction

You can interact with all the NPC (Non Playing Characters) and with other PCs, like asking questions, etc. ou take decisions for the character you are managing conforming to its psychology and objectives.

## Answers and tool use

When you are asked, use exclusively one of the two following json forms:

### Form1: Talking

Form1 is as follows: {"type": "discussion", "from" : "character", "to" : "character", "message": "the message you want to pass"}

Note: the message can be addressed to the GM, to a specific player (to be to be called by his/her name) or to "all".

### Form 2: Using a tool

Form2 is as follows: {"type": "check", "attribute": "physical", "value": "15"}

You can expect a response of "True" if the d20 was inferior or equal to the value and "False" otherwise. Tell the GM the result of your check and let him narrate the outcome.
'''


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
    def __init__(self, name, physical, mental, background):
        self.name = name
        self.physical = physical
        self.mental = mental
        self.average = math.floor((physical + mental) /2)
        self.background = background
        self.history = [background]
        
    def __repr__(self):
        return f"{self.name} | PHYSICAL: {self.physical} | AVERAGE: {self.average} | MENTAL: {self.mental}\nBACKGROUND: {self.background}"

    def update_history(self, event):
        """Add to character's memory"""
        self.history.append(f"{event}")

    
#-------------------------------------------------- Character
class Player:
    def __init__(self, name, role, character):
        self.name = name
        self.role = role
        self.character = character
        self.context = [
            RULES,
            str(self.character)
        ]

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

    def receive_gm_input(self, input_text):
        # 1 - Creating the global context
        print(self.context)
        globcontext = "\n".join(self.context) + '\n' + input_text
        response = ask_llm(self.role, globcontext)
        if response.contains("check"):
            print(f"Acheck was required by {self.name}: {response}")
            # simulate the check
            globcontext += "True"
            response = ask_llm(self.role, globcontext)
        self.context.append(f"{input_text}")
        self.context.append(f"{self.character.name}: {response}")
        return response
               

#--------------------------------------------------------run_game
def run_game():
    # 1 - create characters
    conan = Character("Conan", 15, 9, BACKGROUND_CONAN)
    sartia = Character("Sartia", 10, 14, BACKROUND_SARTIA)

    # 2 - Create player agents and assign characters
    joe = Player("Joe", ROLE_JOE, conan)
    alice = Player("Alice", ROLE_ALICE, sartia)

    # 3 - Initialize the capture of the context
    exchanges = [] # array of arrays [ "gm: blah", "joe: bleh", "alice: bluh", ...]

    msg = "GM says: You are in the small town of Roudza. You heard that Hexel Flunk has a piece of clue about where could be the first lieutenant of General Chronos. What do you do?"

    exchanges.append(msg)
    print(msg)
    stop = False
    while not stop:
        response = joe.receive_gm_input(msg)
        a = input(response)
        
#-------------------------------------------------- test
def test():
    roll(2, 6, 3, True)
    roll(3, 6, 1, True)
    # Split 24 points between physical and mental
    comment = '''
    conan = Character("Conan", 15, 9)
    print(conan)
    difficulty = 2
    john = Player("john",
    ''You are playing a barbarian named Conan.
                  You more often use physical confrontation than reflexion but you know how to be smart sometimes. You are a very proud person and very true in your feelings that you may sometimes express a bit brutally.''
                  conan)
    print(f"Physical test: {"Passed" if john.test(Character.PHYSICAL, difficulty, True) else "Failed"}")
    print(f"Mental test: {"Passed" if john.test(Character.MENTAL, difficulty, True) else "Failed"}")
    print(f"Average test: {"Passed" if john.test(Character.AVERAGE, difficulty, True) else "Failed"}")'''
    

if __name__ == "__main__":
    test()
    run_game()
