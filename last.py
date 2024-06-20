import streamlit as st
import cohere
import eng_to_ipa as ipa
import pyttsx3
import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np
from allosaurus.app import read_recognizer
from difflib import SequenceMatcher
import random

# Initialize Cohere client
co = cohere.Client('3fYNqs63XuqeNPBxmQezmbyWq3LWcFGFFmUKpODr')

# Initialize pyttsx3 TTS engine once, outside any conditional blocks
engine = pyttsx3.init()

# Load your model
model = read_recognizer()

# Function to record audio from microphone
def record_audio(duration, sample_rate=44100, channels=1):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()  # Wait for recording to finish
    return audio_data, sample_rate

# Function to save recorded audio to a temporary WAV file
def save_temp_wav(audio_data, sample_rate):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        filename = tmp_file.name
        sf.write(tmp_file.name, audio_data, sample_rate)
    return filename

# Function to transcribe phonemes from microphone input
def transcribe_phonemes(duration=5):
    audio_data, sample_rate = record_audio(duration)
    audio_filename = save_temp_wav(audio_data, sample_rate)
    st.write("Running inference...")
    phonemes = model.recognize(audio_filename)
    st.write("Phonemes:", phonemes)
    import os
    os.remove(audio_filename)
    return phonemes
    # Clean up temporary file
    
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



# Function to generate sentence based on level
def generate_sentence(level):
    sentences = {
    1: ["I like cats.", "The sun is shining.", "She is happy.", "The bird sings."],
    2: ["They are playing outside.", "The flowers bloom.", "He likes to read books.", "The dog barks."],
    3: ["The dog barks loudly.", "The sky is blue.", "She dances gracefully.", "He plays the guitar."],
    4: ["The flowers bloom in spring.", "They travel to new places.", "The river flows peacefully.", "The wind whispers softly."],
    5: ["The child runs joyfully.", "The stars twinkle at night.", "The mountain stands majestically.", "The ocean waves crash against the shore."],
    6: ["The protagonist faces internal conflict.", "The scientist conducts experiments rigorously.", "The artist expresses emotions through brush strokes.", "The philosopher ponders the nature of reality."],
    7: ["The detective solves the mysterious case.", "The author employs vivid imagery in the narrative.", "The composer orchestrates a symphony of sound.", "The mathematician proves the theorem logically."],
    8: ["The politician delivers a compelling speech.", "The historian analyzes primary sources critically.", "The engineer designs innovative solutions.", "The linguist studies languages intricately."],
    9: ["The psychiatrist examines mental health disorders.", "The biologist investigates cellular mechanisms.", "The economist evaluates market trends.", "The sociologist studies societal structures."],
    10: ["The lawyer argues cases persuasively in court.", "The surgeon performs intricate procedures with precision.", "The architect designs sustainable buildings.", "The journalist investigates corruption in politics."]
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

        # Transcribe phonemes from user's speech
        user_phonemes = transcribe_phonemes()

        # Prompt the user to speak the sentence and recognize speech
        user_input = user_phonemes
        if user_input is not None:
            st.info("User Input (Phonemes): " + user_input)

            # Convert the correct pronunciation and user input into lists of words
            correct_words = correct_pronunciation.split()
            user_words = user_input.split()

            # Compare each word in the correct pronunciation with the corresponding word in the user's input
            for i in range(min(len(correct_words), len(user_words))):
                if correct_words[i] != user_words[i]:
                    st.warning(f"Expected: {correct_words[i]} | Actual: {user_words[i]}")

            # Calculate accuracy based on the whole sentence
            accuracy = co.chat(
                message=f"Compare these two strings: {correct_pronunciation} and {user_phonemes}, these two strings are the correct and my pronounciation of setences transcribed into ipa, compare them and give me a report. Give me a score on one to ten based on how close my pronounciation is to the actual one.",
                temperature=0.3
            )

    # Display accuracy and score
    if accuracy is not None:
        # score = generate_score(accuracy)
        st.info(f"Accuracy: {accuracy.text}")
        # st.info(f"Score: {score}")

    # Speak the generated sentence if a response is available
    speak_text(test_response)

if __name__ == "__main__":
    main()
