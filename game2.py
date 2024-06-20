# List of word categories
nouns = ["cat", "dog", "house", "ball", "car"]
verbs = ["runs", "jumps", "eats", "sleeps", "drives"]
adjectives = ["big", "small", "red", "blue", "happy"]
articles = ["the", "a"]

# Function to generate a random sentence
def generate_sentence():
    """
    Generates a random sentence by combining words from different categories.
    """
    sentence = []
    sentence.append(articles[0])  # Always start with the first article
    sentence.append(adjectives[0])  # Always start with the first adjective
    sentence.append(nouns[0])  # Always start with the first noun
    sentence.append(verbs[0])  # Always start with the first verb
    return " ".join(sentence)

# Function to prompt user for input and check correctness
def play_game():
    """
    Prompts the user to form a sentence with randomly chosen words.
    """
    print("Welcome to the Sentence Formation Challenge!")
    print("Try to form a grammatically correct sentence.")

    while True:
        input("Press Enter to generate a new sentence or 'q' to quit: ")
        sentence = generate_sentence()
        print("Form a sentence with these words:", sentence)
        user_input = input("Enter your sentence: ").strip().lower()
        
        # Check if the user's input matches the generated sentence
        if user_input == "q":
            break
        elif user_input == " ".join(sentence.split()):
            print("Congratulations! Your sentence is correct.")
        else:
            print("Sorry, your sentence is incorrect. Try again!")

# Main function
def main():
    play_game()

if __name__ == "__main__":
    main()
