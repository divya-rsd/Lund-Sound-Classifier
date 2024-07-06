import numpy as np
import pywt
import pywt.data
import scipy.io.wavfile as wavfile
sample_rate, noisy_signal = wavfile.read('71.wav')

wavelet = 'haar'
level = 3
threshold_mode = 'hard'
coeffs = pywt.wavedec(noisy_signal, wavelet, level=level)

threshold_value = np.std(coeffs[-1]) * np.sqrt(2 * np.log(len(noisy_signal)))

coeffs = [pywt.threshold(c, threshold_value, mode=threshold_mode) for c in coeffs]

denoised_signal = pywt.waverec(coeffs, wavelet)

wavfile.write('denoised_71.wav', sample_rate, denoised_signal.astype(np.int16))