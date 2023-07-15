import cv2
import numpy as np
import scipy.signal as signal

input_image = cv2.imread('YOUR IMAGE', cv2.IMREAD_GRAYSCALE)

fft_image = np.fft.fft2(input_image)
fft_shift = np.fft.fftshift(fft_image)
magnitude_spectrum = 20 * np.log(np.abs(fft_shift))

nyquist_freq = 0.5
cutoff_freq = 0.1  
numtaps = 1024  
b = signal.firwin(numtaps, cutoff_freq/nyquist_freq)

filtered_spectrum = np.zeros_like(magnitude_spectrum)
for i in range(magnitude_spectrum.shape[0]):
    filtered_spectrum[i,:] = signal.convolve(magnitude_spectrum[i,:], b, mode='same')

filtered_shift = fft_shift * np.exp(1j * np.angle(fft_shift))
filtered_image = np.fft.ifft2(np.fft.ifftshift(filtered_shift)).real

cv2.imwrite('FILTERINMAGE.png', filtered_image)
