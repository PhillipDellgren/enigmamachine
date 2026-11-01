# File: EnigmaModel.py

""" This is the starter file for the Enigma project. """

from EnigmaView import EnigmaView
from EnigmaConstants import ALPHABET
from EnigmaConstants import ROTOR_PERMUTATIONS      #Gathers Rotor Permutations
import string
INV_ROTOR_PERMUTATIONS = [
    "UWYGADFPVZBECKMTHXSLRINQOJ", #Inverted permutation for slow rotor
    "AJPCZWRLFBDKOTYUQGENHXMIVS", #Permutation for medium rotor
    "TAGBPCSDQEUFVNZHYIXJWLRKOM", #Permutation for fast rotor
]
REFLECTOR_PERMUTATION = "IXUHFEZDAOMTKQJWNSRLCYPBVG"
#To keep an overview and do the inverted permutations
# Slow rotor mapping
#    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
#    | | | | | | | | | | | | | | | | | | | | | | | | | |
#    E K M F L G D Q V Z N T O W Y H X U S P A I B R C J
#
# Medium rotor mapping - Added by myself
#    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
#    | | | | | | | | | | | | | | | | | | | | | | | | | |
#    A J D K S I R U X B L H W T M C Q G Z N P Y F V O E
#
# Fast rotor mapping - Added by myself
#    A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
#    | | | | | | | | | | | | | | | | | | | | | | | | | |
#    B D F H J L C P R T X V Z N Y E I W G A K M U S Q O



class EnigmaModel:

    def __init__(self):
        """Creates a new EnigmaModel with no views."""
        self._views = [ ]

        #Tracks the state of every key. Are they pressed or not.
        self.keyboard_released = {
        'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False,
        'G': False, 'H': False, 'I': False, 'J': False, 'K': False, 'L': False,
        'M': False, 'N': False, 'O': False, 'P': False, 'Q': False, 'R': False,
        'S': False, 'T': False, 'U': False, 'V': False, 'W': False, 'X': False,
        'Y': False, 'Z': False
        }

        #Each rotor as a seperate object.
        #The parameter used, is each the permutation for each rotor.
        #This is used as a parameter aswell for each object later down, when defining the class.
        #The rotor class' (__init__) see each of the ROTOR_PERMUTATIONS[i]-
        # as the "permutationstr" - which is later to be used as the -
        # self._permutation
        #The EnigmaModel "owns" the rotor objects. Therefore they are defined under this constructor.
        #This means that the model, creates three seperate rotor objects. 
        self._rotors = [
                EnigmaRotor(ROTOR_PERMUTATIONS[0]),     #[0] Slow rotor (Rotor0)
                EnigmaRotor(ROTOR_PERMUTATIONS[1]),     #[1] Medium rotor (Rotor1)
                EnigmaRotor(ROTOR_PERMUTATIONS[2]),     #[2] Fast rotor (Rotor2)
                ]

        #Forces all lamps to shut off, once key is released
        self.encoded_lamp = {
        'A': False, 'B': False, 'C': False, 'D': False, 'E': False, 'F': False,
        'G': False, 'H': False, 'I': False, 'J': False, 'K': False, 'L': False,
        'M': False, 'N': False, 'O': False, 'P': False, 'Q': False, 'R': False,
        'S': False, 'T': False, 'U': False, 'V': False, 'W': False, 'X': False,
        'Y': False, 'Z': False
        }

        # Reflector object defined
        self._reflector = REFLECTOR_PERMUTATION                       

    def add_view(self, view):
        """Adds a view to this model."""
        self._views.append(view)
        

    def update(self):
        """Sends an update request to all the views."""
        for view in self._views:
            view.update()

    #Determines whether or not a key is pressed.
    #Additionally the parameter used, is passed in the if statement to determine which letter is pressed
    def is_key_down(self, letter):
        if self.keyboard_released[letter] == True:
            return True
        else:
            return False
     
    #Determines if the lamp should light up, with the letter parameter passed.
    #The lamp will light up the encoded letter.
    def is_lamp_on(self, letter):
        if self.encoded_lamp[letter] == True:
            return True
        elif self.encoded_lamp[letter] == False:
            return False
        

    def key_pressed(self, letter):
        #--Advance rotor--
        #Even though these variables store the same, as the rotor2, rotor1 or rotor0 later.
        #I wanted to keep it seperate and name this differently, for simplicities sake, which helps my own overview of my code.
        #Yes it would be cleaner in some regard, but for my style, I chose this way.

                                                    #Defining rotors for carry when wrapped.
        fast_rotor = self._rotors[2]                #Defines rotor2(fast) for the carry.
        did_fast_rotor_wrap = fast_rotor.advance()  #Variable for calling advance for rotor2, furthermore retrieves information as to if it is wrapped or not.

        #The above stated code, will advance the rotor and determine if the rotor has wrapped.
        #Now the below code will begin the carry.
        #If True, means it has wrapped. It will begin to do the same thing as above, just with the next rotor. Rotor1(medium)
        if did_fast_rotor_wrap == True:
            medium_rotor = self._rotors[1]
            did_medium_rotor_wrap = medium_rotor.advance()
            
            #Here we go furher, with the same logic. Medium rotor defined, and we advanced it.
            #Below, we see that if it has wrapped, we move on to define and advance rotor0(slow).
            if did_medium_rotor_wrap == True:
                slow_rotor = self._rotors[0]
                slow_rotor.advance()
                #We dont have more rotors after this, so no need to advance a fourth rotor.
        
        """
        Here our key_pressed signal gets processed.
        We begin by passing it through the fast rotor.
        I'm gonna explain this line by line for the fast rotor only, since the same idea applies for all rotors.
        When we reach the reflector, I'll add a few comments.
        PS. I've kept my print statements as them as comments. Just to show how I "traced" the signal".
        It also demonstrates that each signal through each rotor is correct, when comparing it, to the last demo on the page, which allows you-
        to track the signal.
        Feel free to uncomment my print statements to see them.
        """

        self.keyboard_released[letter] = True       #When our key_pressed function is called, we as the first thing, makes sure that the specified key, is set to true in our dictionary.
        letter_index2 = ALPHABET.index(letter)      #We define a variable which holds an integer, for the index of the letter, from the key, that was pressed.
        rotor2 = self._rotors[2]                    #Defines rotor2(fast) to a variable
        encoded_index2 = apply_permutation(letter_index2, rotor2.get_permutation(), rotor2.get_offset()) #This variable saves, the information returned by the apply_permutation function. See line 268 for more information.
        encoded_letter2 = ALPHABET[encoded_index2]  #This variable uses the index of the encoded letter, to find the corresponding letter in the alphabet. 
        """ -----Debug-----
        print(f"__Fast Rotor__")
        print(f"letter_index2: {letter_index2}")
        print(f"encoded_index2: {encoded_index2}")
        print(f"encoded_leter2: {encoded_letter2}")
        print("\n")
        """
        
        #Passing through medium rotor
        letter_index1 = ALPHABET.index(encoded_letter2)
        rotor1 = self._rotors[1]
        encoded_index1 = apply_permutation(letter_index1, rotor1.get_permutation(), rotor1.get_offset())
        encoded_letter1 = ALPHABET[encoded_index1]
        """-----Debug-----
        print(f"__Medium Rotor__")
        print(f"letter_index1: {letter_index1}")
        print(f"encoded_index1: {encoded_index1}")
        print(f"encoded_letter1: {encoded_letter1}")
        print("\n")
        """

        #Passing through the slow rotor
        letter_index0 = ALPHABET.index(encoded_letter1)
        rotor0 = self._rotors[0]
        encoded_index0 = apply_permutation(letter_index0, rotor0.get_permutation(), rotor0.get_offset())
        encoded_letter0 = ALPHABET[encoded_index0]
        """-----Debug-----
        print("__Slow Rotor__")
        print(f"letter_index0: {letter_index0}")
        print(f"encoded_index0: {encoded_index0}")
        print(f"encoded_letter0: {encoded_letter0}")
        print("\n")
        """

        #Passing through the reflector
        letter_index_r = ALPHABET.index(encoded_letter0) #Seen previously, a variable that stores an integer for what the index is for the character returned by encoded_letter0.
        reflector = self._reflector
        reflected = reflector[letter_index_r]
        #Essentially we do the same in the reflector, as the code above. 
        #The change being that we use the reflectors permutation and do not call the apply_permutation function.
        """-----Debug-----
        print("__Reflector__")
        print(f"letter_index_r: {letter_index_r}")
        print(f"reflected: {reflected}")
        print("\n")
        """
        
        #Here the code changes a bit, because it is close to being the same, as when passing the signal up until the reflector.
        #Follow my comments to see, what is going on.
        #Additionally, check EnigmaConstants. My inverted permutations are written there.
        #You will also see I added the alphabet mapping to the keys, to help myself manually rewrite them.

        #From reflector back through slow rotor
        inv_letter_index0 = ALPHABET.index(reflected)                                       #Seen previously, finds the index for the letter we stored in the "reflected" variable.
        inv_perm = INV_ROTOR_PERMUTATIONS[0]                                                #Defines a variable to the inverted permutation for rotor0.
        inv_offset0 = self._rotors[0].get_offset()                                          #Variable which stores an integer, that reads the offset from rotor0. 
        inv_encoded_index0 = apply_permutation(inv_letter_index0, inv_perm, inv_offset0)    #This almost does the same, as to when the signal passed up till the reflector.
                                                                                            #I changed my approach, because I had already three rotor objects. It felt wrong, to create-
                                                                                            #three "new rotors" for inverting them. Then I decided to just manually define the permutation to a variable, and add-
                                                                                            #the offset, from the "original" rotor to a new "inverted variable". Otherwise the offset would de-sync for me.
        inv_encoded_letter0 = ALPHABET[inv_encoded_index0]                                  #Passses the index of the letter and looks up that index in the alphabet and stores it in a variable.
        """-----Debug-----
        print("__Inverse Slow__")
        print(f"inv_letter_index0: {inv_letter_index0}")
        print(f"inv_encoded_index0: {inv_encoded_index0}")
        print(f"inv_encoded_letter0: {inv_encoded_letter0}")
        print("\n")
        """


        #From slow back through medium rotor
        inv_letter_index1 = ALPHABET.index(inv_encoded_letter0)
        inv_perm1 = INV_ROTOR_PERMUTATIONS[1]
        inv_offset1 = self._rotors[1].get_offset()
        inv_encoded_index1 = apply_permutation(inv_letter_index1, inv_perm1, inv_offset1)
        inv_encoded_letter1 = ALPHABET[inv_encoded_index1]
        """-----Debug-----
        print("__Inverse Medium__")-----Debug-----
        print(f"inv_letter_index1: {inv_letter_index1}")
        print(f"inv_encoded_index1: {inv_encoded_index1}")
        print(f"inv_encoded_letter1: {inv_encoded_letter1}")
        print("\n")
        """
        
        #From medium back through fast rotor
        inv_letter_index2 = ALPHABET.index(inv_encoded_letter1)
        inv_perm2 = INV_ROTOR_PERMUTATIONS[2]
        inv_offset2 = self._rotors[2].get_offset()
        inv_encoded_index2 = apply_permutation(inv_letter_index2, inv_perm2, inv_offset2)
        inv_encoded_letter2 = ALPHABET[inv_encoded_index2]
        """-----Debug-----
        print("__Inverse Fast__")
        print(f"inv_letter_index2: {inv_letter_index2}")
        print(f"inv_encoded_index2: {inv_encoded_index2}")
        print(f"inv_encoded_letter2: {inv_encoded_letter2}")
        print("-----------------")
        """

        self.encoded_lamp[inv_encoded_letter2] = True #Lastly here, we set a letter to true in the encoded_lamp dictionary, and pass the letter from the last variable "inv_encoded_letter2"
        self.update()
        

    def key_released(self, letter):                         #This will change the value of the key in the dictionary back to false, when released. And also in the lamp dictionary.
        self.keyboard_released[letter] = False              #Changed value back to false, for the passed letter in the keyboard_released dict.
        for key, values in self.encoded_lamp.items():   
            if values == True:
                self.encoded_lamp[key] = False          #Instead of writing self.encoded_lamp[letter] = False, (which caused the lamp to hang), this will just set all lamps to false again.
                                                        #Otherwise, the lamps would continue to just be lightened up, which should not be the case!
                                                        #I could perhaps have written something else, to check if the key was released and then stop lighting the lamp
                                                        #which ideally would be more correct. But chose this approach instead. Fast and intuitive.
        self.update()
        
        

    def get_rotor_letter(self, index):  #A method which retrived the specified rotors letter. 
       rotor = self._rotors[index]      #self._rotors[index] used, because it passes what rotor is being looked at in the index parameter. This is stored in the variable rotor.
       offset = rotor.get_offset()      #Retrieves the offset for desired rotor.
       letter = ALPHABET[offset]        #Stores which letter should be presented in the rotor window, decided by what offset we are at.
       return letter                    #Returns the variable

    def rotor_clicked(self, index):     #When we want to manually advance the rotor
        self._rotors[index].advance()   #Selects the rotor the same way, as above. Additionally we call the advance function, on the rotor[index] which are selected.
        #print(f"Rotor: {index}, Offset: {self._rotors[index].get_offset()}")
        self.update()

                                                    #Each rotor essentially have a class each, which was defined in the EnigmaModel constructor.
                                                    #This below defines what exactly a rotor is. Each has offset, permutation and can advance.
class EnigmaRotor:                                  

    def __init__(self, permutationstr):             #The constructor for the class. permutationstr, is the parameter from when I defined the object for the constructor in the EnigmaModel.To be exact. The permutation for each rotor.
        self._offset = 0                            #Each rotor object, has a offset.
        self._permutation = permutationstr          #The permutation for each rotor, saved to a variable.

    def get_offset(self):                           #Method that returns the offset for the rotor.
        return self._offset

    def get_permutation(self):                      #A method that returns the permutation for the desired rotor.
        return self._permutation
    
    def advance(self) -> bool:                      #This methods does two things. Advances the offset, and determines if the rotor wrapped.
        self._offset = (self._offset + 1 ) % 26     #Saves the offset value in a variable, and will add 1 for each time its called. Additionally wrapping the value by 26. Because thats the length of the alphabet.
                                                    #This part, is what determines whether or not the rotor does a carry.
        if self._offset % 26 != 0:                  #If our offset mod 26 is not 0. Then we do not carry. If it is, well the rotor has wrapped and we return a true. Which will cause a carry. 
            return False
        else:
            return True
                
        

def apply_permutation(letter_index, permutation, offset):       #Three parameters used. leter_index: index of the letter. Permutation: the permutation for the selected rotor. Offset: Offset value of the rotor.    
    offset_index = (letter_index + offset) % 26                 #Determines the index of the letter with the offset being added mod 26, so its wraps, when the offset gets large enough. Stored in a variable.
    permuted_letter = permutation[offset_index]                 #Looks up the letter in the permutation for a rotor, with the index from the offset_index variable.
    permuted_index = ALPHABET.index(permuted_letter)            #The variable which contains a string being a letter from a permutatin, is then indexed as an integer and saved in the variable "permuted_index".
    new_index = (permuted_index - offset) % 26          #Here I subtract the offset from the permuted_index variable, saved in a variable.
    return new_index                                    #Returns the variable, so when the function is called. It returns an integer, that will tell the index of the permutation, for a rotor with a appleid offset.

def enigma():
    """Runs the Enigma simulator."""
    model = EnigmaModel()
    view = EnigmaView(model)
    model.add_view(view)

# Startup code

if __name__ == "__main__":
    enigma()