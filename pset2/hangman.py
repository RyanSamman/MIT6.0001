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
import re
import random
import string
from collections import Counter

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
	print(len(wordlist), "words loaded.")
	return wordlist



def choose_word(wordlist):
	"""
	wordlist (list): list of words (strings)
	
	Returns a word from wordlist at random
	"""
	return "apple" # random.choice(wordlist)

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
	return all(c in letters_guessed for c in secret_word)



def get_guessed_word(secret_word, letters_guessed):
	'''
	secret_word: string, the word the user is guessing
	letters_guessed: list (of letters), which letters have been guessed so far
	returns: string, comprised of letters, underscores (_), and spaces that represents
	  which letters in secret_word have been guessed so far.
	'''
	return "".join([c if c in letters_guessed else '_' for c in secret_word])



def get_available_letters(letters_guessed):
	'''
	letters_guessed: list (of letters), which letters have been guessed so far
	returns: string (of letters), comprised of letters that represents which letters have not
	  yet been guessed.
	'''
	START_POS = 97 # 97 is 'a' in ASCII
	NUMBER_OF_LETTERS = 26 # 26 letters in the alphabet
	return "".join(chr(i) for i in range(START_POS, START_POS + NUMBER_OF_LETTERS) if chr(i) not in letters_guessed)
	
	

def checkLetter(letter, lettersGuessed):
	if not letter.isalpha():
		return "That is not  valid letter."
	
	if letter in lettersGuessed:
		return "You've already guessed that letter."

	return False

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
	chosenWord = choose_word(wordlist)
	lost = True
	remainingGuesses = 6
	remainingWarnings = 3
	lettersGuessed = []

	print("Welcome to the game Hangman!")
	print(f"I am thinking of a word that is {len(chosenWord)} letters long.")
	print(f"You have {remainingWarnings} warnings left.")

	while (lost := not is_word_guessed(chosenWord, lettersGuessed)) and remainingGuesses > 0:
		
		print("--------------")
		print(f"You have {remainingGuesses} guesses left.")
		print(f"Available letters: {get_available_letters(lettersGuessed)}")
		letter = input("Please guess a letter: ").lower()

		if errorMessge := checkLetter(letter, lettersGuessed):
			if remainingWarnings <= 0:
				remainingGuesses -= 1
				print(f"Oops! {errorMessge} You have no warnings left so you lose one guess: ", end="")
			else:
				remainingWarnings -= 1
				print(f"Oops! {errorMessge} You have {remainingWarnings} warnings left: ", end="")
			print(f" {get_guessed_word(chosenWord, lettersGuessed)}")
			continue
			
		lettersGuessed.append(letter)

		if (letter not in chosenWord):
			remainingGuesses -= 2 if letter in "aeiou" else 1
			print(f"Oops! That letter is not in my word: ", end="")
		else:
			print("Good guess: ", end="")

		print(f"{get_guessed_word(chosenWord, lettersGuessed)}")

	print("--------------")

	if lost:
		print(f"Sorry, you ran out of guesses. The word was {chosenWord}")
		return

	score = len(Counter(chosenWord)) * remainingGuesses
	print("Congratulations, you won!")
	print(f"Your total score for this game is: {score}")


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word: string, other_word: str):
	'''
	my_word: string with _ characters, current guess of secret word
	other_word: string, regular English word
	returns: boolean, True if all the actual letters of my_word match the 
		corresponding letters of other_word, or the letter is the special symbol
		_ , and my_word and other_word are of the same length;
		False otherwise: 
	'''
	
	takenCharacters = f"[^{my_word.replace('_', '')}]"
	regex = f"^{my_word.replace('_', takenCharacters)}$"
	return re.match(regex, other_word) is not None



def show_possible_matches(my_word):
	'''
	my_word: string with _ characters, current guess of secret word
	returns: nothing, but should print out every word in wordlist that matches my_word
			 Keep in mind that in hangman when a letter is guessed, all the positions
			 at which that letter occurs in the secret word are revealed.
			 Therefore, the hidden letter(_ ) cannot be one of the letters in the word
			 that has already been revealed.

	'''
	return [w for w in wordlist if match_with_gaps(my_word, w)]



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
	
	chosenWord = choose_word(wordlist)
	lost = True
	remainingGuesses = 6
	remainingWarnings = 3
	lettersGuessed = []

	print("Welcome to the game Hangman!")
	print(f"I am thinking of a word that is {len(chosenWord)} letters long.")
	print(f"You have {remainingWarnings} warnings left.")

	while (lost := not is_word_guessed(chosenWord, lettersGuessed)) and remainingGuesses > 0:
		
		print("--------------")
		print(f"You have {remainingGuesses} guesses left.")
		print(f"Available letters: {get_available_letters(lettersGuessed)}")
		letter = input("Please guess a letter: ").lower()

		if letter == '*':
			possibleWords = show_possible_matches(get_guessed_word(chosenWord, lettersGuessed))
			print("Possible word matches: ")
			print(*possibleWords)
			continue

		if errorMessge := checkLetter(letter, lettersGuessed):
			if remainingWarnings <= 0:
				remainingGuesses -= 1
				print(f"Oops! {errorMessge} You have no warnings left so you lose one guess: ", end="")
			else:
				remainingWarnings -= 1
				print(f"Oops! {errorMessge} You have {remainingWarnings} warnings left: ", end="")
			print(f" {get_guessed_word(chosenWord, lettersGuessed)}")
			continue
			
		lettersGuessed.append(letter)

		if (letter not in chosenWord):
			remainingGuesses -= 2 if letter in "aeiou" else 1
			print(f"Oops! That letter is not in my word: ", end="")
		else:
			print("Good guess: ", end="")

		print(f"{get_guessed_word(chosenWord, lettersGuessed)}")

	print("--------------")

	if lost:
		print(f"Sorry, you ran out of guesses. The word was {chosenWord}")
		return

	score = len(Counter(chosenWord)) * remainingGuesses
	print("Congratulations, you won!")
	print(f"Your total score for this game is: {score}")



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
	# To test part 2, comment out the pass line above and
	# uncomment the following two lines.
	# x = show_possible_matches("a_pl_")
	# print(x)
	# secret_word = choose_word(wordlist)
	# hangman(secret_word)

###############
	
	# To test part 3 re-comment out the above lines and 
	# uncomment the following two lines. 
	
	secret_word = choose_word(wordlist)
	hangman_with_hints(secret_word)
