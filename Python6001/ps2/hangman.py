# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
from re import A
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    _correctCount = 0
    _guessed = False

    for i in range(len(letters_guessed)):
      if letters_guessed[i] in secret_word:
        #counts how many of the specific letter is within the secret word and adds it to the count
        _count = secret_word.count(letters_guessed[i])
        _correctCount+=_count
      if len(secret_word)==_correctCount:
        _guessed = True
        break
    return _guessed

def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # create an array of secret word length
    _userProgress = [" _ "] * len(secret_word)
    _correctGuess = False
    
    for i in range(len(_userProgress)):
      if letters_guessed[len(letters_guessed)-1] in secret_word:
        _correctGuess = True
      for j in range(len(letters_guessed)):
        if secret_word[i] == letters_guessed[j]:
          _userProgress[i] = " "+letters_guessed[j]+" "
    return "".join(_userProgress), _correctGuess

def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    _alphabet = string.ascii_lowercase
    for i in range(len(letters_guessed)):
      if letters_guessed[i] in _alphabet:
        _alphabet = _alphabet.replace(letters_guessed[i], "")
    return _alphabet

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    _progress = False
    _nbGuess = 6
    _nbWarning = 3
    _wordCount = len(secret_word)
    _guessArray = []
    _uniqueLetters = []
    _lettersAvail = get_available_letters(_guessArray)  

    #get the total # of unique letters for the total score
    for i, letters in enumerate(secret_word):
      if not letters in _uniqueLetters:
        _uniqueLetters.append(letters)

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %d letters long" %_wordCount)
    print(f"You have {_nbWarning} warning(s) left")
    print("---------------------------")

    while _nbGuess > 0:
      print("You have %d guesses left" %_nbGuess)
      print(f"Available letters: {_lettersAvail}")
      _alreadyExist = False
      _hasWarning = False
      _userGuess = str.lower(input("Please guess a letter: "))
      #Inputs checks
      if not _userGuess.isalpha() or len(_userGuess) > 1:
        _nbWarning-=1
        _hasWarning = True

      if _userGuess in _guessArray:
        if not _hasWarning:
          _hasWarning = True
          _nbWarning-=1
        _alreadyExist = True
        _isCorrect = False 
      else:
        _guessArray.append(_userGuess)
        _guessedLetters, _isCorrect = get_guessed_word(secret_word, _guessArray)

      if _isCorrect:
        print(f"Good guess: {_guessedLetters}")
      else:
        if _hasWarning and _alreadyExist:
          print(f"Oops! You've already guessed that letter. You have {'no' if _nbWarning < 1 else _nbWarning} warning(s) left: {_guessedLetters}")
        elif _hasWarning:
          print(f"Oops! That is not a valid letter. You have {'no' if _nbWarning < 1 else _nbWarning} warning(s) left: {_guessedLetters}")
        else:
          print(f"Oops! That letter is not in my word: {_guessedLetters}")
      
      _lettersAvail = get_available_letters(_guessArray)
      _progress = is_word_guessed(secret_word, _guessArray)
      
      # if all letters are guessed correctly
      if _progress:
        _total_score = _nbGuess*len(_uniqueLetters)
        print("Congratulations! You won!")
        print(f"Your total score for this game is: {_total_score}")
        break
      print("---------------------------")

      if _nbWarning <1 or (_nbWarning>0 and _hasWarning==False):
        if not _isCorrect and _hasWarning:
          _nbGuess -= 1
        elif not _isCorrect: 
          _nbGuess -= 2 if _userGuess in "aeiou" else 1

    if not _progress:
      print(f"Sorry you ran out of guesses. The word was {secret_word}")

# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------

# # sorts and counts how many letter are in a particular string
# def sorting(_word):
#   _sortingArray = []
#   _matchArray = []

#   # for i in range(len(_word)):
#   #   if not _word[i] in _sortingArray and _word[i] != "_":
#   #     _letters = str(_word[i])
#   #     _letterCount = str(_word.count(_word[i]))
#   #     _sortingArray.append(_letters)
#   #     _matchArray.append(_letterCount)
#   #     # ensures both array are of same size so it they can be cross compared -- ONLY for the users input 
#   #   if _word[i] == "_" and _word[i-1] != "_":
#   #     _sortingArray.append(_word[i])
#   #     _matchArray.append(0)

#   _matchArray = list(zip(_sortingArray, _matchArray))

#   return _matchArray


def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    _isMatch = False

    if len(my_word) != len(other_word):
      return False
    
    for i in range(len(my_word)):
      if my_word[i] == other_word[i]:
        _isMatch = True #if a letter is at the same index return true
      if (my_word[i] != "_" and my_word[i] != other_word[i]):
        _isMatch = False
        break
  
      #check if its the same letter in a row
      # print(other_word[i])
  
      if (other_word[i] == other_word[i-1]):
        if (my_word[i] != "_" and my_word[i-1] == "_") or (my_word[i] == "_" and my_word[i-1] != "_"):
          _isMatch = False
          break
    return _isMatch

def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    #removes all spaces and underscores
    _userProgress = my_word.replace(" ", "")
    _letterPos = [x for x in _userProgress]

    _alphabet = string.ascii_lowercase
    _words = ""
    low = 0
    high = len(wordlist)
    guess_rate = (low+high)//2


    for i in range(len(_letterPos)):
      if not _letterPos[i] == "_":
        # bisection search - around 15 steps log2(50000) no need to break the loop as it will 100% find a match
        # search for words with x letters
        while len(wordlist[guess_rate]) != len(_letterPos):
          if len(_letterPos) > len(wordlist[guess_rate]):
            low = guess_rate
          else: 
            high = guess_rate
          guess_rate = (low+high)//2

        _index = _alphabet.index(wordlist[guess_rate][0])
        _wordIndex = _alphabet.index(_letterPos[i]) # gives the users guessed letters
        _iteration = guess_rate
        #check which letter of the alphabet this corresponds to, and iterate until we get a match
        while _wordIndex != _index:
          _index = _alphabet.index(wordlist[_iteration][0])
          if _index - _wordIndex > 0:
            _iteration-=abs(_index - _wordIndex) #the further it is the more words it jumps over
          else: 
            _iteration+=abs(_index - _wordIndex)
        steps = _iteration

        #check all the words that are similar to the users guess as long as it's the same length
        while len(wordlist[steps]) == len(_letterPos):

          _matches = match_with_gaps(_letterPos, wordlist[steps])
 
          if _matches:
            if not wordlist[steps] in _words:
              _words += wordlist[steps] + " "
          steps+=1
        
        #check both sides of the array
        steps = _iteration
        while len(wordlist[steps]) == len(_letterPos):

          _matches = match_with_gaps(_letterPos, wordlist[steps])
          if _matches:
            if not wordlist[steps] in _words:
              _words += wordlist[steps] + " "
          steps-=1

    #if still no match 
    if len(_words) < 1:
      _words = "No matches found"
    return _words

def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    _progress = False
    _nbGuess = 6
    _nbWarning = 3
    _wordCount = len(secret_word)
    _guessArray = []
    _uniqueLetters = []
    _guessedLetters = []
    _lettersAvail = get_available_letters(_guessArray)  
    #get the total # of unique letters for the total score
    for i, letters in enumerate(secret_word):
      if not letters in _uniqueLetters:
        _uniqueLetters.append(letters)

    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is %d letters long" %_wordCount)
    print(f"You have {_nbWarning} warning(s) left")
    print("---------------------------")

    while _nbGuess > 0:
      print("You have %d guesses left" %_nbGuess)
      print(f"Available letters: {_lettersAvail}")
      _alreadyExist = False
      _hasWarning = False
      _needHint = False

      _userGuess = str.lower(input("Please guess a letter: "))
      
      #Inputs checks
      if _userGuess == "*":
        _needHint = True

      if (not _userGuess.isalpha() or len(_userGuess) > 1) and _needHint == False:
        _nbWarning-=1
        _hasWarning = True

      if _needHint == False:
        if (_userGuess in _guessArray):
          if not _hasWarning:
            _hasWarning = True
            _nbWarning-=1
          _alreadyExist = True
          _isCorrect = False 
        else:
          _guessArray.append(_userGuess)
          _guessedLetters, _isCorrect = get_guessed_word(secret_word, _guessArray)

      #check if guess is correct or not
      if _needHint == False:
        if _isCorrect and _userGuess != "":
          print(f"Good guess: {_guessedLetters}")
        else:
          if _hasWarning and _alreadyExist:
            print(f"Oops! You've already guessed that letter. You have {'no' if _nbWarning < 1 else _nbWarning} warning(s) left: {_guessedLetters}")
          elif _hasWarning:
            print(f"Oops! That is not a valid letter. You have {'no' if _nbWarning < 1 else _nbWarning} warning(s) left: {_guessedLetters}")
          else:
            print(f"Oops! That letter is not in my word: {_guessedLetters}")
      else:
        if _guessedLetters:
          #checks if at least one letter has been guessed          
          print("Possible word matches are: " + show_possible_matches(_guessedLetters))
        else:
          print("Please guess at least one letter before asking for a hint :)")
      
      _lettersAvail = get_available_letters(_guessArray)
      _progress = is_word_guessed(secret_word, _guessArray)
      
      # if all letters are guessed correctly
      if _progress:
        _total_score = _nbGuess*len(_uniqueLetters)
        print("Congratulations! You won!")
        print(f"Your total score for this game is: {_total_score}")
        break
      print("---------------------------")

      if _nbWarning <1 or (_nbWarning>0 and _hasWarning==False) and _needHint == False:
        if not _isCorrect and _hasWarning:
          _nbGuess -= 1
        elif not _isCorrect: 
          _nbGuess -= 2 if _userGuess in "aeiou" else 1

    if not _progress:
      print(f"Sorry you ran out of guesses. The word was {secret_word}")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)
