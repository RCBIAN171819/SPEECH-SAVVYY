import streamlit as st
import cohere
import eng_to_ipa as ipa
import pyttsx3
from difflib import SequenceMatcher

# Initialize Cohere client
co = cohere.Client('3fYNqs63XuqeNPBxmQezmbyWq3LWcFGFFmUKpODr')

# Initialize pyttsx3 TTS engine
engine = pyttsx3.init()

# Streamlit app
def main():
    st.title("SpeechSavvy")

    # Dropdown for selecting level
    level = st.selectbox("Select your level (1-10)", list(range(1, 11)))

    # Button to trigger chat response
    if st.button("Start"):
        test_response = "I like cats."
        st.success(test_response)

        # Extract phonetic pronunciation
        phonetic_pronunciation = ipa.convert(test_response)

        # Display the phonetic pronunciation
        st.info("Phonetic Pronunciation (IPA): " + phonetic_pronunciation)

        user_input = "aɪ laɪk kɑts"
        st.info("User Input Phonetic Pronunciation (IPA): " + user_input)

        # Compare user input with actual phonetics
        matcher = SequenceMatcher(None, phonetic_pronunciation, user_input)
        differences = matcher.get_opcodes()

        # Collect errors
        errors = []
        for tag, i1, i2, j1, j2 in differences:
            if tag == 'replace':
                errors.append((phonetic_pronunciation[i1:i2], user_input[j1:j2]))

        # Display errors
        if errors:
            st.warning("Pronunciation Errors:")
            for error in errors:
                st.write(f"Expected: {error[0]} | Actual: {error[1]}")
        else:
            st.success("No Pronunciation Errors Detected.")

        # Use pyttsx3 to speak the generated sentence
        engine.say(test_response)
        engine.runAndWait()
        engine.endLoop()

if __name__ == "__main__":
    main()
