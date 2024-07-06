import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
import os

def mel(audio_file):
    # Load the audio file
    y, sr = librosa.load("static/"+ audio_file, sr=None)

    # Generate the Mel spectrogram
    mel_spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)

    # Convert to decibels for visualization (optional but common)
    mel_spectrogram_db = librosa.power_to_db(mel_spectrogram, ref=np.max)

    # Display the Mel spectrogram (optional)
    plt.figure(figsize=(10, 6))
    librosa.display.specshow(mel_spectrogram_db, x_axis='time', y_axis='mel')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Mel Spectrogram')
    plt.tight_layout()

    # Save the Mel spectrogram as an image
    image_file = f"static/mel_spectrogram_{audio_file[:-4]}.png"
    plt.savefig(image_file)

    return image_file

mel("audio_without_hb.wav")