# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import enum
import string
import random

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing 
    the list of words to load    
    
    Returns: a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.
    
    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    wordlist = load_words(WORDLIST_FILENAME)

    def __init__(self, text):
        '''
        Initializes a Message object
                
        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        
        self.message = text
        self.valid_words = []
        cleanMsg = self.message.split()

        for i, word in enumerate(cleanMsg):
            self.valid_words.append(is_word(self.wordlist, word))
    
    def __str__(self):
        return f'Here is the message: {self.message} and valid word is: {self.valid_words}'

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class
        
        Returns: self.message_text
        '''
        return self.message

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.
        
        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.        
        
        shift (integer): the amount by which to shift every letter of the 
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to 
                 another letter (string). 
        '''
 
        dict = {}
        alphabet = string.ascii_lowercase
        #changes the entire sentence to lower case
        lowMsg = self.message.lower()

        for count, letter in enumerate(lowMsg):
            # ignores special characters
            if letter not in alphabet:
                continue
            index = alphabet.index(letter)
            # prevents the index to go beyond the 26th letter and loops back 
            if(index+shift>len(alphabet)-1):
                index = index+shift-26
            else:
                index = index+shift
            dict[letter] = alphabet[index]

        return dict   
        

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift        
        
        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        cipher  = ""
        alphabet = string.ascii_lowercase
        dict = self.build_shift_dict(shift)

        for i in self.message:
            #manages capital and special characters
            if i not in alphabet and i.lower() not in alphabet:
                cipher += i
            else:
                if i.isupper():
                    cipher += dict[i.lower()].upper()
                else:
                    cipher += dict[i]
        return cipher

# test = Message("Hello")
# print(test.build_shift_dict(4))
# print(test.apply_shift(4))

class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object        
        
        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = Message.build_shift_dict(self, self.shift)
        self.message_text_encrypted = Message.apply_shift(self, self.shift)
        
    def __str__(self):
        return f'Here is the message: {self.message} and valid word is: {self.valid_words}. Shifted by {self.shift}. {self.get_encryption_dict} -> {self.get_message_text_encrypted}'

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class
        
        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class
        
        Returns: a COPY of self.encryption_dict
        '''
        return self.encryption_dict

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class
        
        Returns: self.message_text_encrypted
        '''
        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other 
        attributes determined by shift.        
        
        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''
        self.shift = shift

# test2 = PlaintextMessage("hello", 4)
# print(test2.get_message_text_encrypted())

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object
                
        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        Message.__init__(self, text)
        
    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value 
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create 
        the maximum number of valid words, you may choose any of those shifts 
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        allSolutions = []
        validList = [0]
        for s in range(0,26):
            #resets after each loop
            decrypted_word = ""
            decryptedMsg = ""
            validCount = 0
            solutions = []
            decrypted_word = self.apply_shift(s)
            decrypted_word = decrypted_word.split()

            for i, word in enumerate(decrypted_word):
                if is_word(self.wordlist, word):
                    validCount += 1
                if i+1 == len(decrypted_word):
                    decryptedMsg += word
                else:
                    decryptedMsg += word + " "
            #remove previous solutions if one with more solution appears
            if max(validList) < validCount and len(allSolutions) > 1:
                allSolutions.clear()
            validList.append(validCount)

            if max(validList) == validCount and validCount != 0:
                solutions.append(decryptedMsg)  
                solutions.append(s)  
                allSolutions.append(solutions)
        #if more than one solutions get a random one
        rdmIndex = random.randint(0, len(allSolutions)-1)
        return allSolutions[rdmIndex][1], allSolutions[rdmIndex][0] 

# test3 = CiphertextMessage("Xoqy Tzcfsm amhvwqoz qvofoqhsf.")
# test3 = CiphertextMessage("dbs")
# test3 = CiphertextMessage("qfsohsr")
# print(test3.decrypt_message())

if __name__ == '__main__':

#    #Example test case (PlaintextMessage)
#    plaintext = PlaintextMessage('hello', 2)
#    print('Expected Output: jgnnq')
#    print('Actual Output:', plaintext.get_message_text_encrypted())
#
#    #Example test case (CiphertextMessage)
#    ciphertext = CiphertextMessage('jgnnq')
#    print('Expected Output:', (24, 'hello'))
#    print('Actual Output:', ciphertext.decrypt_message())

    # plaintext = PlaintextMessage('hello', 2)
    # print('Expected Output: jgnnq')
    # print('Actual Output:', plaintext.get_message_text_encrypted())

    # ciphertext = CiphertextMessage('jgnnq')
    # print('Expected Output:', (24, 'hello'))
    # print('Actual Output:', ciphertext.decrypt_message())

    decryptedTxt = CiphertextMessage(get_story_string())
    print(decryptedTxt.decrypt_message())
