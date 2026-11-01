# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaConstants import ROTOR_PERMUTATIONS, ALPHABET, REFLECTOR_PERMUTATION

class EnigmaRotor:
    def __init__(self):
        self.offset = 0 # Sets the initial offset to 0, equivalent to the letter A in the window

    def get_permutation(self, index):
        return ROTOR_PERMUTATIONS[index] # Gets the permutation from the EnigmaConstants.py file, which is imported at the top of the file
    
    def invert_key(self, rotor_index):
        self.inverse_permutation = "" # Inverts the permutation, such that previously if A->B, it is now B->A, for the entire permutation.
        for i in ALPHABET:
            self.inverse_permutation += ALPHABET[ROTOR_PERMUTATIONS[rotor_index].index(i)]
        return self.inverse_permutation 

    def get_offset(self):
        return self.offset % 26 # Ensures that the offset is flipped
            
    def advance(self):
        if self.offset >= 25: # Flips the offset back to 0, once it reaches the end of the alphabet, or adds one if it is not the end of the alphabet
            self.offset = 0
            return True
        else:
            self.offset += 1
            return False

    def apply_permutation(self, index, permutation, offset):
        offsetIndex = (index + offset) % 26 # Finds the index of the letter, with the offset applied
        permChar = permutation[offsetIndex] # Finds the character in the permutation that corresponds with the letter of the alphabet, with offset included
        return ALPHABET[(ALPHABET.index(permChar) - offset) % 26] # Returns the value, with the offset subtracted

class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self._views = [ ]
        self.lettersdown = { # Tracks which letters are currently held down, which also applies the red outline to letters.
            "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False, "H": False, "I": False, "J": False,
            "K": False, "L": False, "M": False, "N": False, "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False,
            "U": False, "V": False, "W": False, "X": False, "Y": False, "Z": False
        }
        self.lampsOn = { # Tracks which lamps are currently turned on, using a dictionary with letters as keys, and booleans as values.
            "A": False, "B": False, "C": False, "D": False, "E": False, "F": False, "G": False, "H": False, "I": False, "J": False,
            "K": False, "L": False, "M": False, "N": False, "O": False, "P": False, "Q": False, "R": False, "S": False, "T": False,
            "U": False, "V": False, "W": False, "X": False, "Y": False, "Z": False
        }
        self.rotors = [ # Initializes 3 rotors: slow, medium and fast which can later be called by index
            EnigmaRotor(), EnigmaRotor(), EnigmaRotor()
        ] 

    def add_view(self, view):
        """Adds a view to this model."""
        self._views.append(view)

    def update(self):
        """Sends an update request to all the views."""
        for view in self._views:
            view.update()

    def is_key_down(self, letter):
        if self.lettersdown[letter]:
            return True
        else: return False # Uses the lettersdown dictionary to check if a letter is currently held down

    def is_lamp_on(self, letter):
        if self.lampsOn[letter]:
            return True
        else: return False # Uses the lampsOn dictionary to check which lamps should be on, after the encryption.

    def key_pressed(self, letter):
        self.lettersdown[letter] = True # Applies red outline to pressed letter
        if self.rotors[2].advance(): # Advances rotors. If True is returned, meaning it has "flipped" back to 0, then the next rotor will advance.
            if self.rotors[1].advance():
                self.rotors[0].advance()

        # Encryption forward
        for i in reversed(range(0,3)):
                letter = self.rotors[i].apply_permutation(ALPHABET.index(letter), self.rotors[i].get_permutation(i), self.rotors[i].get_offset())

        # Reflection
        letter = REFLECTOR_PERMUTATION[ALPHABET.index(letter)]
        
        # Encryption backwards
        for i in range(0,3):
            letter = self.rotors[i].apply_permutation(ALPHABET.index(letter), self.rotors[i].invert_key(i), self.rotors[i].get_offset())
        
        self.lampsOn[letter] = True # Sets the value for the encrypted letter on the lampsOn
        
        self.update()

    def key_released(self, letter):
        self.lettersdown[letter] = False
        for i in ALPHABET:
            self.lampsOn[i] = False # Runs through the entire alphabet, making sure all lamps are off, when the key is released.

        self.update()

    def get_rotor_letter(self, index):
        return ALPHABET[self.rotors[index].get_offset()] # Uses alphabet from EnigmaConstants to get the letter corresponding to the current offset of the rotor.

    def rotor_clicked(self, index):
        self.rotors[index].advance() # Advances rotor when the rotor is clicked directly.
        self.update()  
        
def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()
