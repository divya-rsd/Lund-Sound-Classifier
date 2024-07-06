import noisereduce as nr
import librosa
import soundfile as sf
import os

def amplify_sound(input_file, output_file, amplification_db=5):

  data, samplerate = sf.read(input_file)

  data = data * amplification_db

  sf.write(output_file, data, samplerate)

def noise_reduce(audio_file):
    
    audio_data, sr = librosa.load(fr"static/{audio_file}")
    
    reduced_noise = nr.reduce_noise(y=audio_data, y_noise=audio_data, sr=sr)

    red_file = fr"{audio_file[:-4]}_reduced_noise.wav"
    sf.write(f"static/{red_file}", reduced_noise, sr)

    amplify_sound(f"static/{red_file}", f"static/{red_file}")
    
    return red_file
