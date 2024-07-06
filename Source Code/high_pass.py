import scipy.signal as signal
import noisereduce as nr
import librosa
import soundfile as sf
import numpy as np

def remove_heartbeats(audio_file):
    # Load the audio file
    audio_data, sr = librosa.load("static/" + audio_file[:-4] + "_reduced_noise.wav")

    # Define the cutoff frequency for the high-pass filter
    cutoff_frequency = 200  # Adjust as needed

    # Design a high-pass Butterworth filter
    b, a = signal.butter(N=4, Wn=cutoff_frequency / (0.5 * sr), btype='high', analog=False)

    # Apply the high-pass filter to the data
    filtered_signal = signal.filtfilt(b, a, audio_data)

    # Save the filtered audio to a new file
    sf.write(f'static/{audio_file[:-4]}_without_hb.wav', filtered_signal, sr)

    return f"{audio_file[:-4]}_without_hb.wav"

