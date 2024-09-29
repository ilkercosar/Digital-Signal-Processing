from tkinter import Tk, Label, Entry, Button, messagebox

class AudioSettingsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Settings")

        # Örnekleme frekansı ve kanal sayısı
        self.fs = 44100
        self.channels = 1
        
        # Filtre kesme frekansları
        self.cuttoffLPF = 200
        self.cuttoffHPF = 3000
        
        # Eko gecikmesi
        self.echo_delay = 0.2

        # GUI elemanlarını oluştur
        self.create_widgets()
        
        self.updateFlag = False

    def create_widgets(self):
        # Örnekleme frekansı girişi
        Label(self.root, text="Sampling Frequency (fs)").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.fs_entry = Entry(self.root, width=10)
        self.fs_entry.grid(row=0, column=1, padx=10, pady=5)
        self.fs_entry.insert(0, str(self.fs))

        # Kanal sayısı girişi
        Label(self.root, text="Channels").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.channels_entry = Entry(self.root, width=10)
        self.channels_entry.grid(row=1, column=1, padx=10, pady=5)
        self.channels_entry.insert(0, str(self.channels))

        # Low Pass Filter kesme frekansı girişi
        Label(self.root, text="LPF Cutoff Frequency").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.lpf_entry = Entry(self.root, width=10)
        self.lpf_entry.grid(row=2, column=1, padx=10, pady=5)
        self.lpf_entry.insert(0, str(self.cuttoffLPF))

        # High Pass Filter kesme frekansı girişi
        Label(self.root, text="HPF Cutoff Frequency").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.hpf_entry = Entry(self.root, width=10)
        self.hpf_entry.grid(row=3, column=1, padx=10, pady=5)
        self.hpf_entry.insert(0, str(self.cuttoffHPF))

        # Eko gecikmesi girişi
        Label(self.root, text="Echo Delay").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.echo_entry = Entry(self.root, width=10)
        self.echo_entry.grid(row=4, column=1, padx=10, pady=5)
        self.echo_entry.insert(0, str(self.echo_delay))

        # Ayarları güncelle butonu
        self.update_button = Button(self.root, text="Update Settings", command=self.update_settings)
        self.update_button.grid(row=5, columnspan=2, pady=10)

    def update_settings(self):
        try:
            # Değerleri giriş alanlarından al ve güncelle
            self.fs = int(self.fs_entry.get())
            self.channels = int(self.channels_entry.get())
            self.cuttoffLPF = float(self.lpf_entry.get())
            self.cuttoffHPF = float(self.hpf_entry.get())
            self.echo_delay = float(self.echo_entry.get())
            # Güncelleme başarılı mesajı
            messagebox.showinfo("Settings Updated", "Settings have been updated successfully!")
            self.updateFlag = True

            
        except ValueError:
            # Hata mesajı
            messagebox.showerror("Error", "Invalid input. Please enter correct values.")
            self.fs = None
            self.channels =  None
            self.cuttoffLPF =  None
            self.cuttoffHPF =  None
            self.echo_delay =  None
            self.updateFlag = False
    
    
    def getParams(self):
        return self.fs, self.channels, self.cuttoffLPF, self.cuttoffHPF, self.echo_delay if self.updateFlag == True else False
    

''' 
if __name__ == "__main__":
    root = Tk()
    app = AudioSettingsGUI(root)
    app.window.protocol("WM_DELETE_WINDOW", app.clearBackend())
    root.mainloop()
'''