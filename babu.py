import streamlit as st
import cohere
import eng_to_ipa as ipa
import pyttsx3
import speech_recognition as sr
from difflib import SequenceMatcher
import random

# Initialize Cohere client
co = cohere.Client('3fYNqs63XuqeNPBxmQezmbyWq3LWcFGFFmUKpODr')

# Initialize pyttsx3 TTS engine once, outside any conditional blocks
engine = pyttsx3.init()

# Function to calculate accuracy
def calculate_accuracy(actual, user):
    matcher = SequenceMatcher(None, actual, user)
    match = matcher.find_longest_match(0, len(actual), 0, len(user))
    accuracy = match.size / len(actual)
    return accuracy

# Function to generate score
def generate_score(accuracy):
    if accuracy == 1.0:
        return 10
    elif accuracy >= 0.8:
        return 8
    elif accuracy >= 0.6:
        return 6
    elif accuracy >= 0.4:
        return 4
    elif accuracy >= 0.2:
        return 2
    else:
        return 0

# Function to handle text-to-speech with engine state management
def speak_text(text):
    if not engine.isBusy():
        engine.say(text)
        engine.runAndWait()

# Function to handle speech recognition
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Speak your sentence...")
        audio_data = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio_data)
        return user_input
    except sr.UnknownValueError:
        st.write("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        st.write("Sorry, there was an error with the speech recognition service.")
        return None

# Function to generate sentence based on level
def generate_sentence(level):
    sentences = {
        1: ["I like cats.", "The sun is shining."],
        2: ["She is happy.", "The bird sings."],
        3: ["They are playing outside.", "The flowers bloom."],
        4: ["He likes to read books.", "The dog barks."],
        5: ["The dog barks loudly.", "The sky is blue."],
        6: ["The sky is blue.", "She dances gracefully."],
        7: ["She dances gracefully.", "He plays the guitar."],
        8: ["He plays the guitar.", "The flowers bloom in springs."],
        9: ["The flowers bloom in spring.", "They travel to new places."],
        10: ["They travel to new places.", "The river flows peacefully."]
    }
    return random.choice(sentences[level])

# Streamlit app
def main():
    st.title("SpeechSavvy")

    # Dropdown for selecting level
    level = st.selectbox("Select your level (1-10)", list(range(1, 11)))

    # Initialize test_response and accuracy variables
    test_response = generate_sentence(level)
    correct_pronunciation = ipa.convert(test_response)
    accuracy = None

    # Button to trigger chat response
    if st.button("Start"):
        st.success(test_response)

        # Display the phonetic pronunciation
        st.info("Correct Pronunciation (IPA): " + correct_pronunciation)

        engine.say(test_response)

        # Prompt the user to speak the sentence and recognize speech
        user_input = recognize_speech()
        if user_input is not None:
            st.info("User Input (Speech): " + user_input)

            # Convert the correct pronunciation and user input into lists of words
            correct_words = correct_pronunciation.split()
            user_words = ipa.convert(user_input).split()

            # Compare each word in the correct pronunciation with the corresponding word in the user's input
            for i in range(min(len(correct_words), len(user_words))):
                if correct_words[i] != user_words[i]:
                    st.warning(f"Expected: {correct_words[i]} | Actual: {user_words[i]}")

            # Calculate accuracy based on the whole sentence
            accuracy = calculate_accuracy(correct_pronunciation, ipa.convert(user_input))

    # Display accuracy and score
    if accuracy is not None:
        score = generate_score(accuracy)
        st.info(f"Accuracy: {accuracy:.2f}")
        st.info(f"Score: {score}")

    # Speak the generated sentence if a response is available
    speak_text(test_response)

if __name__ == "__main__":
    main()
