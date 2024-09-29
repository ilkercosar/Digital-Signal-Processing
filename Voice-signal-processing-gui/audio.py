import sounddevice as sd
import queue
import voiceProcessing
from numpy import all, zeros, array


class AudioStream:
    def __init__(self, samplerate=44100, channels=1) -> None:
        self.samplerate = samplerate
        self.channels = channels
        self.stream = sd.Stream(callback=self.callback, channels=self.channels,
                                 samplerate=self.samplerate, blocksize=25000, latency='low')
        self.data_queue = queue.Queue()  # Ses verisini depolamak için bir kuyruk

        self.is_muted = False  # Mikrofonun açık/kapalı durumunu tutan bir bayrak
        self.processor = voiceProcessing.audio()
        
        # Ses bilgileri
        self.tiz = 0
        self.bass = 0
        self.volume = 0
        self.pitch = 0
        self.eko = 0
        
        self.denoiseSample = 0
        self.denoise = None
        self.check = array([None, None], dtype = object)
        

    def callback(self, indata, outdata, frames, time, status):
        if status:
            print("Hata: ", status)  # Hata durumlarını yazdırır
        # Alınan sesi doğrudan çıkışa yönlendir
        if not self.is_muted:
            try:
            # Ses sinyalini işleme için veriler 
                if self.denoiseSample <50:
                    self.processor.capture_noise_profile(data=indata[:])
                    self.denoiseSample += 1
                
                if self.denoiseSample == 50 and self.denoise == True:
                        denoisedSignal = self.processor.denoise(data=indata) 
                        if denoisedSignal.shape[0] != outdata.shape[0]:
                            denoisedSignal = denoisedSignal[:outdata.shape[0]]
                        outdata[:, 0] = denoisedSignal.squeeze() * self.volume 
                    
                        outdata[:, 0] = self.processor.denoise(data=indata).squeeze() * self.volume
                        
                else:
                    # Ses seviyesini ayarlama
                    outdata[:] = indata * self.volume  # İşlenmeden doğrudan geçiş    
            except Exception as denoiseError:
                print(f"Denoise processer gives an error {denoiseError}")
                
            try:
                # İşlemleri gerçekleştirme
                makeBass = self.processor.LPF(indata[:, 0]) * self.bass if self.bass != 0 else zeros(indata.shape[0])
                makeEko = self.processor.echo(indata[:, 0], self.eko) if self.eko != 0 else zeros(indata.shape[0])
                makeTiz = self.processor.HPF(indata[:, 0]) * self.tiz if self.tiz != 0 else zeros(indata.shape[0])
                makePitch = self.processor.PITCH(data=indata, voice=outdata, pitchLevel=self.pitch) if self.pitch != 0 else zeros(indata.shape[0])
            
                if all(makePitch == 0) and all(makeTiz == 0) and all(makeBass == 0):
                    outdata[:] = indata * self.volume
                else:
                    outdata[:, 0] = (makeBass + makeTiz + makePitch + makeEko) * self.volume
            except Exception as error:
                print(f"Voice processing return an error: {error}")
                outdata[:] = indata * self.volume
                
            try:
                if self.check[1] is True:
                    if self.check[0] == 1:
                        outdata[:, 0] = self.processor.bath(indata[:, 0]) * self.volume
                    elif self.check[0] == 2:
                        outdata[:, 0] = self.processor.cave(indata[:, 0]) * self.volume
                    elif self.check[0] == 3:
                        outdata[:, 0] = self.processor.acoustic(indata[:, 0]) * self.volume
                    elif self.check[0] == 4:
                        outdata[:, 0] = self.processor.rock(indata[:, 0]) * self.volume
                    elif self.check[0] == 5:
                        outdata[:, 0] = self.processor.stage(indata[:, 0]) * self.volume
                    elif self.check[0] == 6:
                        outdata[:, 0] = self.processor.studio(indata[:, 0]) * self.volume
                    elif self.check[0] == 7:
                        outdata[:, 0] = self.processor.soft(indata[:, 0]) * self.volume
                    else:
                        outdata[:] = indata * self.volume
                else:
                    pass
            except Exception as effectError:
                print(f"Effect processer gives an error: {effectError}")
                        
            # Ses verisini kuyruğa ekle
            self.data_queue.put(indata.copy())  # Alınan veriyi kuyruğa ekle
        else:
            outdata.fill(0)  # Mikrofon kapalıysa çıkışı sıfırla

    def start(self):
        """Ses akışını başlat."""
        self.stream.start()

    def stop(self):
        """Ses akışını durdur."""
        self.stream.stop()
        self.stream.close()
        print("Akış durduruldu.")
    
    def get_audio_data(self):
        """Kuyruktan ses verisini alır."""
        try:
            return self.data_queue.get_nowait()  # Kuyruktan veriyi al
        except queue.Empty:
            return None  # Kuyruk boşsa None döndür
        
    def set_mute(self, mute: bool):
        """Mikrofonu aç veya kapat."""
        self.is_muted = mute

    def read_parameters(self, tiz = 0, bass = 0, volume = 0, pitch = 0, eko = 0, denoise = None, check = None):
        self.tiz = tiz
        self.bass = bass
        self.volume = volume
        self.pitch = pitch
        self.eko = eko
        self.denoise = denoise
        self.check = check 