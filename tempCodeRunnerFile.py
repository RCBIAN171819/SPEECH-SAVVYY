import random
import g2p_en
import pyttsx3

# Function to generate random words for a given grade level range
def generate_random_words(grade_level_range):
    # Sample word list for demonstration purposes
    word_list = {
        '4th': ['apple', 'bicycle', 'elephant', 'giraffe', 'kangaroo'],
        '5th': ['computer', 'mountain', 'umbrella', 'piano', 'restaurant'],
        '6th': ['chemistry', 'hospital', 'library', 'volcano', 'astronomy'],
        '7th': ['chocolate', 'environment', 'mathematics', 'universe', 'vegetable']
    }
    return random.choice(word_list[grade_level_range])

# Function to generate alternate pronunciations for a given word
def generate_alternate_pronunciations(word):
    # Initialize the g2p object
    g2p = g2p_en.G2p()

    # Generate the phonetic representation for the word
    phonetic_representation = g2p(word)

    # Generate alternate pronunciations by replacing one phoneme with a similar one
    alternate_pronunciations = []
    for _ in range(2):  # Generate 2 alternate pronunciations
        alternate_phonetic_representation = list(phonetic_representation)
        # Randomly select a position to replace a phoneme
        position = random.randint(0, len(phonetic_representation) - 1)
        # Replace the phoneme with a random one
        alternate_phonetic_representation[position] = random.choice('abcdefghijklmnopqrstuvwxyz')
        alternate_pronunciations.append(''.join(alternate_phonetic_representation))
    alternate_pronunciations.append(phonetic_representation)  # Add the correct pronunciation
    random.shuffle(alternate_pronunciations)  # Shuffle the pronunciations
    return alternate_pronunciations

# Function to speak out the word with Indian accent
def speak_word(word):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    # Set properties for Indian English accent
    engine.setProperty('voice', 'english+f1')
    # Speak out the word
    engine.say(word)
    engine.runAndWait()

# Function to present the word and alternate pronunciations to the user
def present_word_and_alternates(word, alternate_pronunciations):
    print("Listen to the word:")
    speak_word(word)
    print("Choose the correct pronunciation:")
    for index, pronunciation in enumerate(alternate_pronunciations):
        print(f"{index+1}. {pronunciation}")
        # Speak out the alternate pronunciation
        speak_word(pronunciation)

# Function to validate the user's choice
def validate_choice(correct_index, user_choice):
    return correct_index == user_choice - 1

# Main game loop
def main():
    print("Welcome to the Pronunciation Game!")
    grade_level_range = input("Enter the grade level range (e.g., 4th, 5th, 6th, 7th): ")
    word = generate_random_words(grade_level_range)
    alternate_pronunciations = generate_alternate_pronunciations(word)
    present_word_and_alternates(word, alternate_pronunciations)
    correct_index = alternate_pronunciations.index(word)
    user_choice = int(input("Enter your choice (1, 2, or 3): "))
    if validate_choice(correct_index, user_choice):
        print("Congratulations! You chose the correct pronunciation.")
    else:
        print("Sorry, the correct pronunciation was not chosen.")

if __name__ == "__main__":
    main()