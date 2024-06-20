import streamlit as st
import cohere
import eng_to_ipa as ipa
import pyttsx3

# Initialize Cohere client
co = cohere.Client('3fYNqs63XuqeNPBxmQezmbyWq3LWcFGFFmUKpODr')

# Streamlit app
def main():
    st.title("SpeechSavvy")
    sentences = []

    # Initialize pyttsx3 TTS engine
    engine = pyttsx3.init()

    # Dropdown for selecting level
    level = st.selectbox("Select your level (1-10)", list(range(1, 11)))

    # Dropdown for selecting accent
    accent = st.selectbox("Select accent", ["American", "British", "Indian", "Australian"])

    # Map accent names to voice IDs
    accent_to_voice_id = {
        "American": "com.apple.speech.synthesis.voice.Alex",
        "British": "com.apple.speech.synthesis.voice.Daniel",
        "Indian": "com.apple.speech.synthesis.voice.Victoria",
        "Australian": "com.apple.speech.synthesis.voice.karen"
    }

    # Button to trigger chat response
    if st.button("Start"):
        # Send message to Cohere
        response = co.chat(
            message=f"Give me an English sentence, like the ones which can be found in a {level}th grader's English textbook.",
            preamble="Respond only with the sentence and nothing else. Do not include anything else in your reply other than the required sentence."
        )

        # Display the generated English sentence
        st.success(response.text)

        # Extract phonetic pronunciation
        phonetic_pronunciation = ipa.convert(response.text)

        # Display the phonetic pronunciation
        st.info("Phonetic Pronunciation (IPA): " + phonetic_pronunciation)

        # Append the sentence to the list
        sentences.append((response.text, accent_to_voice_id[accent]))

    # Speak all the sentences with the selected accent
    if sentences:
        for sentence, selected_voice_id in sentences:
            engine.setProperty('voice', selected_voice_id)
            engine.say(sentence)
            engine.runAndWait()  # Speak the sentence

if __name__ == "__main__":
    main()





    