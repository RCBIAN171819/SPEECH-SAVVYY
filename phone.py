import pyaudio
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

def record_audio(seconds=5, fs=22050):
    chunk = 1024
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)
    frames = []
    print("Recording...")
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    p.terminate()
    return b''.join(frames)

def detect_syllables(audio_data, fs=22050, threshold=0.05):
    y, sr = librosa.load(io.BytesIO(audio_data), sr=fs)
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    
    # Calculate energy for each frame
    energy = librosa.feature.rms(y=y)
    
    # Smooth the energy curve
    energy_smoothed = np.convolve(energy[0], np.ones(10)/10, mode='same')
    
    # Find peaks in the energy curve
    peaks = np.where(energy_smoothed > threshold)[0]
    
    # Convert frame indices to time
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)
    peak_times = librosa.frames_to_time(peaks, sr=sr)
    
    # Plot the waveform and energy curve for visualization
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    librosa.display.waveshow(y, sr=sr)
    plt.vlines(onset_times, -1, 1, color='r', linestyle='-', label='Onsets')
    plt.legend()
    plt.title('Waveform with Syllable Onsets')
    
    plt.subplot(2, 1, 2)
    plt.plot(librosa.times_like(energy_smoothed), energy_smoothed, label='Smoothed Energy')
    plt.plot(librosa.times_like(energy[0]), energy[0], alpha=0.5, label='Energy')
    plt.vlines(peak_times, 0, 1, color='g', linestyle='-', label='Syllable Peaks')
    plt.legend()
    plt.title('Energy Curve')
    plt.tight_layout()
    plt.show()

# Example usage
audio_data = record_audio()
detect_syllables(audio_data)
