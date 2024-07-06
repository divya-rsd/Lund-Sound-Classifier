import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

def spectral_subtraction(input_file, noise_file, output_file):
   
    fs, audio_data = wavfile.read(input_file)
    fs_noise, noise_data = wavfile.read(noise_file)
    
    if len(audio_data.shape) == 2:
        audio_data = np.mean(audio_data, axis=1)
    if len(noise_data.shape) == 2:
        noise_data = np.mean(noise_data, axis=1)
    
    spectrum_audio = np.fft.fft(audio_data)
    spectrum_noise = np.fft.fft(noise_data)
    
    magnitude_audio = np.abs(spectrum_audio)
    phase_audio = np.angle(spectrum_audio)
    magnitude_noise = np.abs(spectrum_noise)
    phase_noise = np.angle(spectrum_noise)
    
    noise_magnitude = magnitude_noise
    
    enhanced_magnitude = np.maximum(magnitude_audio - noise_magnitude, 0)  
    enhanced_spectrum = enhanced_magnitude * np.exp(1j * phase_audio)
    
    enhanced_audio = np.fft.ifft(enhanced_spectrum).real.astype('int16')
    
    wavfile.write(output_file, fs, enhanced_audio)

def remove_beats(input_file, output_file):
    noise_file = "beats.wav"

    spectral_subtraction(input_file, noise_file, output_file)
