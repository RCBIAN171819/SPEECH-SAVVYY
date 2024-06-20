import random
import g2p_en
import pyttsx3

# Sample word list for demonstration purposes
word_lists = {
    '4th': ['apple', 'bicycle', 'elephant', 'giraffe', 'kangaroo'],
    '5th': ['computer', 'mountain', 'umbrella', 'piano', 'restaurant'],
    '6th': ['chemistry', 'hospital', 'library', 'volcano', 'astronomy'],
    '7th': ['chocolate', 'environment', 'mathematics', 'universe', 'vegetable']
}

# Function to generate alternate pronunciations for a given word
def generate_alternate_pronunciations(word):
    # Initialize the g2p object
    g2p = g2p_en.G2p()

    # Generate the correct phonetic representation for the word
    correct_phonetic_representation = g2p(word)

    # Generate two incorrect pronunciations by changing the stress pattern
    incorrect_pronunciations = []
    for _ in range(2):
        # Randomly choose a stress pattern for each phoneme (0 for unstressed, 1 for stressed)
        stress_pattern = ''.join([random.choice(['0', '1']) for _ in range(len(correct_phonetic_representation))])
        # Construct the incorrect pronunciation by appending stress pattern to each phoneme
        incorrect_pronunciation = ''.join([ph + stress for ph, stress in zip(correct_phonetic_representation, stress_pattern)])
        incorrect_pronunciations.append(incorrect_pronunciation)

    return correct_phonetic_representation, incorrect_pronunciations

# Function to speak out the word with Indian accent
def speak_word(word):
    # Initialize the text-to-speech engine
    engine = pyttsx3.init()
    # Set properties for Indian English accent (**without saving audio**)
    engine.setProperty('voice', 'english+f1')
    # Speak out the word
    engine.say(word)
    engine.runAndWait()

# Function to present the word and alternate pronunciations to the user
def present_word_and_alternates(word, correct_pronunciation, incorrect_pronunciations):
    print("Listen to the word:")
    speak_word(word)
    print("Choose the correct pronunciation:")
    options = [correct_pronunciation] + incorrect_pronunciations
    random.shuffle(options)
    for index, pronunciation in enumerate(options):
        print(f"{index+1}. {pronunciation}")
        # Speak out the pronunciation (without saving)
        speak_word(word)

# Function to validate the user's choice
def validate_choice(correct_index, user_choice):
    return correct_index == user_choice

# Main game loop
def main():
    print("Welcome to the Pronunciation Game!")
    grade_level = input("Enter the grade level (4th, 5th, 6th, 7th): ")
    if grade_level in word_lists:
        word = random.choice(word_lists[grade_level])
        correct_pronunciation, incorrect_pronunciations = generate_alternate_pronunciations(word)
        present_word_and_alternates(word, word, incorrect_pronunciations)
        correct_index = 1  # Correct pronunciation is always the first option
        try:
            user_choice = int(input("Enter your choice (1, 2, or 3): "))
            if validate_choice(correct_index, user_choice):
                print("Congratulations! You chose the correct pronunciation.")
            else:
                print("Sorry, the correct pronunciation was not chosen.")
                print("The correct pronunciation is:", word)
        except ValueError:
            print("Invalid input. Please enter a number (1, 2, or 3).")
    else:
        print("Invalid grade level. Please enter a valid grade level.")

if __name__ == "__main__":
    main()
