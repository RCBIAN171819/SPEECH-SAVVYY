from allosaurus.app import read_recognizer
import sounddevice as sd
import soundfile as sf
import tempfile
import numpy as np

# Load your model
model = read_recognizer()

# Function to record audio from microphone
def record_audio(duration, sample_rate=44100, channels=1):
    print("Recording...")
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
    try:
        print("Running inference...")
        phonemes = model.recognize(audio_filename)
        print("Phonemes:", phonemes)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up temporary file
        import os
        os.remove(audio_filename)

# Main function to continuously transcribe phonemes
def main():
    transcribe_phonemes()

if __name__ == "__main__":
    main()