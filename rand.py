import random

# Sample list of words with their IPA representations
word_ipa_data = [
    {"word": "apple", "ipa": "/ˈæpəl/"},
    {"word": "banana", "ipa": "/bəˈnænə/"},
    {"word": "orange", "ipa": "/ˈɔːrɪndʒ/"},
    {"word": "grape", "ipa": "/ɡreɪp/"},
    {"word": "pineapple", "ipa": "/ˈpaɪnˌæpl/"},
    {"word": "watermelon", "ipa": "/ˈwɔːtəˌmɛlən/"},
    {"word": "kiwi", "ipa": "/ˈkiːwi/"},
    {"word": "strawberry", "ipa": "/ˈstrɔːb(ə)ri/"},
    {"word": "blueberry", "ipa": "/ˈbluːb(ə)ri/"},
    {"word": "mango", "ipa": "/ˈmæŋɡəʊ/"}
]

# Function to generate a random row from the sample data
def generate_random_row():
    word_info = random.choice(word_ipa_data)
    return {"word": word_info["word"], "ipa": word_info["ipa"]}

# Generate a random row
random_row = generate_random_row()

# Print the random row
print("Word:", random_row["word"])
rand_ipa = (random_row["ipa"])
print(rand_ipa)
