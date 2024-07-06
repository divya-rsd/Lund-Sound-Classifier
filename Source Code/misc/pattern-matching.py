import numpy as np
import librosa
from sklearn.metrics.pairwise import cosine_similarity

overlap = 0.25

def compare_ref(reference_audio, recorded_audio):
# Load and preprocess the first audio signal (replace 'audio1.wav' with your audio file path)
    audio_signal1, sample_rate1 = librosa.load(reference_audio+".wav", sr=None)
    duration1 = librosa.get_duration(y=audio_signal1, sr=sample_rate1)
    # shorter audio

    # Load and preprocess the second audio signal (replace 'audio2.wav' with your audio file path)
    audio_signal2, sample_rate2 = librosa.load(recorded_audio, sr=None)
    duration2 = librosa.get_duration(y=audio_signal2, sr=sample_rate2)

    m = 0
    n = duration1

    max_similarity = 0
    max_segment = [0,0]

    while True:
        start_sample = int(m * sample_rate2)
        end_sample = int(n * sample_rate2)

        extracted_audio = audio_signal2[start_sample:end_sample]

        # Compute the Mel spectrogram for the first audio signal
        mel_spectrogram1 = librosa.feature.melspectrogram(y=audio_signal1, sr=sample_rate1)

        # Compute the Mel spectrogram for the second audio signal
        mel_spectrogram2 = librosa.feature.melspectrogram(y=extracted_audio, sr=sample_rate2)

        # Ensure that both Mel spectrograms have the same number of time frames (if not, adjust as needed)
        min_frames = min(mel_spectrogram1.shape[1], mel_spectrogram2.shape[1])
        mel_spectrogram1 = mel_spectrogram1[:, :min_frames]
        mel_spectrogram2 = mel_spectrogram2[:, :min_frames]

        # Flatten the Mel spectrograms into 1D vectors for comparison
        vector1 = mel_spectrogram1.reshape(-1)
        vector2 = mel_spectrogram2.reshape(-1)

        # Compute cosine similarity between the two vectors
        similarity_score = cosine_similarity(vector1.reshape(1, -1), vector2.reshape(1, -1))

        if similarity_score[0][0] >= max_similarity:
            max_similarity = similarity_score[0][0]
            max_segment = [m, n]

        m += overlap
        n += overlap
        
        if n >= duration2:
            break

    max_segment[0] = max_segment[0].__round__(2)
    max_segment[1] = max_segment[1].__round__(2)
    print("--------------------------------------------")
    print(f"Cosine Similarity ({reference_audio}): {max_similarity}")
    print(f"Max segment: {max_segment}")

audio_file = "pnemonia.wav"

compare_ref("../crackle-fine", audio_file)
compare_ref("../crackle-coarse", audio_file)
compare_ref("../rhonchi", audio_file)
compare_ref("../wheeze", audio_file)
compare_ref("../bronchial", audio_file)
compare_ref("../vesicular", audio_file)
print("--------------------------------------------")
