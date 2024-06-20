import cohere
import eng_to_ipa as ipa

# Initialize Cohere client with your API key
co = cohere.Client('wxGyAk4AmZJ9AazVQYV9QC1eCX7zi1YQkzcA1ZLW')

# Ask the user for an English sentence
user_input = input("Give me an English sentence, like the ones which can be found in a 6th grader's English textbook: ")

# Start a chat session with Cohere, providing the user input as message
response = co.chat(
    message=user_input,
    preamble="Respond only with the sentence and nothing else."
)

# Get the input sentence from the response
input_sentence = response.text.strip()

# Convert the input sentence to phonetic pronunciation in IPA format
phonetic_pronunciation = ipa.convert(input_sentence)

print("Input sentence:", input_sentence)
print("Phonetic pronunciation:", phonetic_pronunciation)
