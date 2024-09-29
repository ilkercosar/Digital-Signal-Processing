# Audio processing event
import numpy as np
from scipy.signal import butter, lfilter, resample

class audio:
    def __init__(self) -> None:
        # Örnekleme frekansı ve kanal sayısı
        self.fs = 44100  # 44.1 kHz örnekleme frekansı
        self.channels = 1  # Mono (tek kanal)
        self.noise_profile = None  # Gürültü profilini saklamak için
        self.noise_count = 0  # Gürültü profilini oluşturmak için sinyal sayacı
        self.noise_data_list = []  # İlk birkaç sinyali saklamak için liste
        
        # Eko ayarları
        self.echo_delay = 0.2  # Eko gecikmesi (saniye cinsinden)
        self.echo_buffer = np.zeros(int(self.fs * self.echo_delay))  # Eko tamponu
        self.cuttoffLPF = 200
        self.cuttoffHPF = 3000
        
    def capture_noise_profile(self, data, max_samples=50):
        if self.noise_count < max_samples:
            self.noise_data_list.append(data)
            self.noise_count += 1            
            
            if self.noise_count == max_samples:
                self.noise_profile = np.mean(self.noise_data_list, axis=0)

    def denoise(self, data):
        if self.noise_profile is not None:
            
            if len(data.shape) > 1 and data.shape[1] > 1:
                data = data[:, 0]
            # Gürültü profiline göre sinyali düzelt
            denoised_signal = data - self.noise_profile[:len(data)]
            # Negatif değerleri sıfırlamak veya normalize etmek için
            denoised_signal = np.clip(denoised_signal, -1.0, 1.0)
            return denoised_signal
        else:
            # Gürültü profili yoksa girdiği gibi döndür
            return data
    
    # Bass filtresi (high-pass)
    def LPF(self, data, cutoff=200, fs=44100, order=5):
        cutoff = self.cuttoffLPF
        nyquist = 0.5 * self.fs
        normalCutoff = cutoff / nyquist
        b, a = butter(order, normalCutoff, btype='low', analog=False)
        return lfilter(b, a, data)
    
    # Tiz filtresi (high-pass)
    def HPF(self, data, cutoff=3000, fs=44100, order=5):
        cutoff = self.cuttoffHPF
        nyquist = 0.5 * self.fs
        normalCutoff = cutoff / nyquist
        b, a = butter(order, normalCutoff, btype='high', analog=False)
        return lfilter(b, a, data)
    
    # Sesi kalınlaştırma
    def PITCH(self, data, voice, pitchLevel):
        pitchLevel = max(0.5, min(pitchLevel, 2.0))
        samples = int(len(data) * pitchLevel)
        
        resampled_signal = resample(data[:, 0], samples)

        if len(resampled_signal) > len(voice):
            resampled_signal = resampled_signal[:len(voice)]
        elif len(resampled_signal) < len(voice):
            #resampled_signal = np.pad(resampled_signal, (0, len(voice) - len(resampled_signal)), 'constant')
            resampled_signal = np.pad(resampled_signal, (0, len(voice) - len(resampled_signal)), 'wrap')
            
        resampled_signal = resampled_signal / np.max(np.abs(resampled_signal))

        return resampled_signal 
    
    # Yankı için
    def echo(self, data, ekoVolume):
        # Eko tamponuna mevcut ses verisini ekleyin
        output_signal = np.zeros_like(data)
        ekoVolume = min(1.0, max(ekoVolume / 100.0, 0.0))
        #if ekoVolume != 0:
            #ekoVolume /= 10

        for i in range(len(data)):
            # Mevcut ses verisi
            current_sample = data[i]
            # Eko tamponundan gelen ses verisi
            delayed_sample = self.echo_buffer[i % len(self.echo_buffer)]
        
            # Eko etkisi ekleme
            output_signal[i] = current_sample + (delayed_sample * ekoVolume)

            # Eko tamponuna mevcut ses verisini ekleyin
            self.echo_buffer[i % len(self.echo_buffer)] = current_sample + (delayed_sample * ekoVolume)  # Eko efekti ile ekleme
    
        return output_signal
    
    # Banyo efekti
    def bath(self, data):
        # Düşük frekansları azaltarak yankı ve reverb ekleyelim
        data = self.LPF(data, cutoff=500)  
        return self.echo(data, ekoVolume=70)  

    # Mağara efekti
    def cave(self, data):
        # Düşük ve yüksek frekansları azaltarak derin bir yankı oluştur
        data = self.LPF(data, cutoff=300)  
        data = self.HPF(data, cutoff=2000)  
        return self.echo(data, ekoVolume=80)  

    # Akustik efekti
    def acoustic(self, data):
        # Daha doğal bir ses için hafif yankı
        return self.echo(data, ekoVolume=50)

    # Rock efekti
    def rock(self, data):
        # Tizleri artırmak ve düşük frekansları güçlendirmek
        data = self.HPF(data, cutoff=500)  
        return self.LPF(data, cutoff=150)  

    # Sahne efekti
    def stage(self, data):
        # Genellikle daha fazla eko ve derinlik
        return self.echo(data, ekoVolume=90)

    # Stüdyo efekti
    def studio(self, data):
        # Düşük ve yüksek frekansları iyileştirerek temiz bir ses sağla
        data = self.LPF(data, cutoff=3000)  
        data = self.HPF(data, cutoff=200)  
        return data  

    # Soft efekti
    def soft(self, data):
        # Yumuşak bir ses için hafif filtreleme
        data = self.LPF(data, cutoff=1000)  
        return data  # Yumuşak ses