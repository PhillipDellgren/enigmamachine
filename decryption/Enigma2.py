from EnigmaModel import *
from EnigmaConstants import *
import doctest

## -- Helper functions --

# Carry over function for each full rotation of the previous rotor
def carry_over(rotor: list) -> list:
     if rotor[2] == 25:
        rotor[2] = 0
        if rotor[1] == 25:
             rotor[1] = 0
             rotor[0] += 1
        else:
             rotor[1] += 1
     else: rotor[2] += 1
     return rotor

# Rotor conversion from integers in a list to a 3-letter string
def convert_rotor_to_str (rotor_list: list) -> str:
    '''
    Docstring for convert_rotor_to_str:
    Takes a list of integers, only op to 3 elements, and convert it to an alphabet string(alphabet positions).
    
    :param rotor_list: Description
    :type rotor_list: list
    :return: Description
    :rtype: str
    '''
    output_str = ""
    for i in rotor_list:
        output_str = output_str + ALPHABET[i]
    return output_str 

# Opposite conversion from 3-letter string to integers
def convert_rotor_to_int(rotor_str: str) -> list:
     rotor_list = []
     for letter in rotor_str:
          rotor_list.append(ALPHABET.find(letter))
     return rotor_list

# -- Project Code --´# Encrypt function
def encrypt(rotors: str, message: str) -> str:
    rotorList = [ # Creates rotors indexed 0-2
        EnigmaRotor(), EnigmaRotor(), EnigmaRotor()
        ]
    
    rotorOffsets = convert_rotor_to_int(rotors)

    message = "".join(message.split()) # Removes spaces and whitespace from the input string
    message = message.upper() # Ensures uppercase for the entire string
    
    for i in range(0,3): #Sets each rotors offset according to the argument "message" passed in
        rotorList[i].offset = rotorOffsets[i]

    messageOut = ""

    for f in range(len(message)): # Carry over without the use of the helper function
        if rotorList[2].advance(): # Advances rotor, if True is returned, it advances the next rotor
            if rotorList[1].advance():
                rotorList[0].advance()

        letter = message[f]

        # Encryption forwards
        for i in reversed(range(0,3)):
                letter = rotorList[i].apply_permutation(ALPHABET.index(letter), rotorList[i].get_permutation(i), rotorList[i].get_offset()) 

        # Reflection
        letter = REFLECTOR_PERMUTATION[ALPHABET.index(letter)]
        
        # Encryption backwards
        for i in range(0,3):
            letter = rotorList[i].apply_permutation(ALPHABET.index(letter), rotorList[i].invert_key(i), rotorList[i].get_offset())
        messageOut += letter
        
    return messageOut

def find_rotors(message: str, cipher: str)-> str: 
    # Removes spaces and ensures capital letters only
    message = message.replace(" ","").upper()
    cipher = cipher.replace(" ","").upper()

    # Ensures initial rotor offset of 0 on all rotors
    rotor_offset = [0, 0, 0]

    while rotor_offset[0] < 26: # This while loop ensures that we don't go beyond rotor setting ZZZ (from AAA-ZZZ)
        rotor_str = convert_rotor_to_str(rotor_offset)
        encrypted = encrypt(rotor_str, message)

        if encrypted == cipher: # Returns the rotor settings if the encrypted message is the same as the cipher. Otherwise, advances to the next rotor setting.
            return  rotor_str
          
        rotor_offset = carry_over(rotor_offset)

def decrypt(cipher: str)-> str:
    # Creates a list containing ~10.000 of the most common english words
    word_list = []

    for line in open('word10k.txt'): # Adds each line as a seperate element in a list
        word = line.strip()
        if len(word) > 1: # Discards words which are only one character
            word_list.append(word.upper())

    word_list = sorted(word_list, key=len, reverse=True) # The list is sorted by length, from longest to shortest (and then alphabetically if same length, still reversed)

    cipher.replace(" ","").upper() # Ensures no spaces, and all capital letters
    rotor_offset = [0, 0, 0]
    sentence_length = len(cipher)
    best_guess = 0

    while rotor_offset[0] < 26: # Stops the loop and returns the best guess when all options have been attempted. Also initializes some variables for use with each settings
        rotor_str = convert_rotor_to_str(rotor_offset)
        encrypted = encrypt(rotor_str, cipher)
        decrypted_msg = str(encrypted)
        chars = 0

        for word in word_list: # Every word in the word list is checked against the encryption. Matching characters are counted, and matching words are removed from the encrypted string
            if word in encrypted:
                chars += len(word) * encrypted.count(word)
                encrypted = encrypted.replace(word," ")
        if chars != 0: # If at least one character (word) is found, then the accuracy is calculated, and if it is more accurate than the previous (or is the first) guess, it is saved.
            if best_guess < (chars / sentence_length) * 100:
                best_guess = (chars / sentence_length) * 100  
                best_guess_rotor, best_guess_msg = rotor_str, decrypted_msg
                if best_guess == 100:
                    break
          
        rotor_offset = carry_over(rotor_offset)
    
    return (f"The best guess rotor = {best_guess_rotor}, The best guess message {best_guess_msg}, the best guess accuracy {best_guess}") # Returns the final guess, with an accuracy percentage.