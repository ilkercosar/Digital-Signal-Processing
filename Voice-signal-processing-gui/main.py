import gui
from tkinter import Tk
import threading
from time import sleep
import audio
from numpy import array

class AudioAppManager:
    def __init__(self, root) -> None:
        """Init all libraries and functions"""
        self.root = root
        self.app = gui.AudioApp(self.root)
        self.audio_stream = audio.AudioStream()

        self.reset = None
        self.audio_level = 0
        self.eko_level = 0
        self.bass_level = 0
        self.tiz_level = 0
        self.pitch_level = 0
        self.check = array([None, None], dtype = object)

    def read_values_in_loop(self):
        """A function to read values in a while loop with sleep."""
        while True:
            self.audio_level, self.eko_level, self.bass_level, self.tiz_level, self.pitch_level, self.reset, denoise, settings, mute, self.check = self.app.read_slider_values(reset=self.reset)
            self.audio_stream.read_parameters(tiz=self.tiz_level, bass=self.bass_level,volume=self.audio_level, pitch=self.pitch_level, eko=self.eko_level, denoise=denoise, check=self.check)
            if self.reset is True:
                print("Sisteme reset attı")
                self.reset = False

            if mute is True:
                self.audio_stream.set_mute(mute=True)
            else:
                self.audio_stream.set_mute(mute=False)
                
            sleep(0.1)

    def get_voice_data(self):
        """Stream audio data in a separate thread."""
        try:
            stream_thread = threading.Thread(target=self.audio_stream.start)
            stream_thread.start()
            
            while True:
                pass
        except KeyboardInterrupt:
            print("Çıkış yapılıyor...")
        finally:
            self.audio_stream.stop()

    def start(self):
        """Uygulamayı başlatmak için gerekli iş parçacıklarını çalıştır."""
        # Sliders reading in a separate thread
        slider_thread = threading.Thread(target=self.read_values_in_loop)
        slider_thread.daemon = True  # Set as a daemon thread so it closes with the main program
        slider_thread.start()

        # Voice data collection in a separate thread
        voice_thread = threading.Thread(target=self.get_voice_data)
        voice_thread.daemon = True  # Set as a daemon thread so it closes with the main program
        voice_thread.start()

if __name__ == "__main__":
    root = Tk()
    root.title("Ses Uygulaması")

    # AudioAppManager instance oluştur
    manager = AudioAppManager(root)

    # İşlemleri başlat
    manager.start()

    # GUI'yi başlat
    root.mainloop()
