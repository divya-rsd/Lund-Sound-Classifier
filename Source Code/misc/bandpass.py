import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def butter_bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

def amplify_frequency_range(input_path, output_path, lowcut, highcut, gain=2.0):
    # Load the input audio file
    fs, input_signal = wavfile.read(input_path)

    # Apply bandpass filter to isolate the desired frequency range
    filtered_signal = butter_bandpass_filter(input_signal, lowcut, highcut, fs)

    # Amplify the filtered frequency range
    amplified_signal = filtered_signal * gain

    amplified_signal[np.isinf(amplified_signal)] = np.nan

    # Save the amplified audio to a new file
    wavfile.write(output_path, fs, amplified_signal.astype(np.int16))

if __name__ == "__main__":
    # Specify the paths for the input and output audio files
    input_file = "recording.wav"
    output_file = "amp.wav"

    # Specify the frequency range to amplify (in Hz)
    lowcut = 20
    highcut = 100

    # Specify the gain factor (adjust as needed)
    gain_factor = 2.0

    # Apply frequency range amplification
    amplify_frequency_range(input_file, output_file, lowcut, highcut, gain_factor)
