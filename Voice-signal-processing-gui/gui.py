import threading
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Scale, Frame, Checkbutton, IntVar, Toplevel
from time import sleep
from numpy import array
import settingsGui


class AudioApp:
    def __init__(self, root) -> None:
        self.root = root
        self.root.geometry("700x450")
        self.root.configure(bg="#180421")
        self.root.resizable(False, False)

        self.ASSETS_PATH = Path(r"assets\frame0")

        self.setup_canvas()
        self.setup_buttons()
        self.setup_images_and_text()
        self.setup_slinders()

        self.denoise = False
        self.mute = False
        self.reset = False
        self.settings = False

        self.button_4_visible = False  # Butonun başlangıçta görünmez olduğunu belirtiyoruz
        # Canvas'a tıklama eventi ekleyelim
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.check = array([None, None], dtype = object)
        

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_canvas(self):
        self.canvas = Canvas(
            self.root,
            bg="#180421",
            height=450,
            width=700,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

    def setup_buttons(self):
        # Create buttons with threads for their commands
        button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        self.button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: threading.Thread(target=self.button_1_clicked).start(),
            relief="flat"
        )
        self.button_1.image = button_image_1  # Keep a reference to avoid garbage collection
        self.button_1.place(x=170.0, y=33.0, width=60.0, height=60.0)

        button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        self.button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: threading.Thread(target=self.button_2_clicked).start(),
            relief="flat"
        )
        self.button_2.image = button_image_2
        self.button_2.place(x=270.0, y=33.0, width=60.0, height=60.0)

        button_image_3 = PhotoImage(file=self.relative_to_assets("button_3.png"))
        self.button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: threading.Thread(target=self.button_3_clicked).start(),
            relief="flat"
        )
        self.button_3.image = button_image_3
        self.button_3.place(x=370.0, y=33.0, width=60.0, height=60.0)

        button_image_4 = PhotoImage(file=self.relative_to_assets("button_4.png"))
        self.button_4 = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: threading.Thread(target=self.button_4_clicked).start(),
            relief="flat"
        )
        self.button_4.image = button_image_4
        self.button_4.place(x=470.0, y=33.0, width=60.0, height=60.0)
        self.button_4.place_forget()  # Butonu gizleyelim

    def on_canvas_click(self, event):
        # Belirli koordinatlara tıklandığında buton 4 görünür olsun
        if 575 <= event.x <= 600 and 63 <= event.y <= 67:  
            if not self.button_4_visible:
                self.button_4.place(x=470.0, y=33.0, width=60.0, height=60.0)
                self.button_4_visible = True

    def setup_slinders(self):
        
        audioLevelFrame = Frame(self.root, bg="#180421")
        audioLevelFrame.place(x=110, y=120)

        ekoLevelFrame = Frame(self.root, bg="#180421")
        ekoLevelFrame.place(x=223, y=120)

        bassLevelFrame = Frame(self.root, bg="#180421")
        bassLevelFrame.place(x=333, y=120)

        tizLevelFrame = Frame(self.root, bg="#180421")
        tizLevelFrame.place(x=443, y=120)

        pitchLevelFrame = Frame(self.root, bg="#180421")
        pitchLevelFrame.place(x=553, y=120)

        self.audioLevelSlider = Scale(
            audioLevelFrame, 
            from_=0, 
            to=100, 
            orient="vertical",
            bg="#180421",
            highlightthickness=0,
            troughcolor="#180421",
            fg="white"
        )
        self.audioLevelSlider.pack()

        self.ekoLevelSlider = Scale(
            ekoLevelFrame, 
            from_=0, 
            to=100, 
            orient="vertical",
            bg="#180421",
            highlightthickness=0,
            troughcolor="#180421",
            fg="white"
        )
        self.ekoLevelSlider.pack()

        self.bassLevelSlider = Scale(
            bassLevelFrame, 
            from_=0, 
            to=100, 
            orient="vertical",
            bg="#180421",
            highlightthickness=0,
            troughcolor="#180421",
            fg="white"
        )
        self.bassLevelSlider.pack()

        self.tizLevelSlider = Scale(
            tizLevelFrame, 
            from_=0, 
            to=100, 
            orient="vertical",
            bg="#180421",
            highlightthickness=0,
            troughcolor="#180421",
            fg="white"
        )
        self.tizLevelSlider.pack()

        self.pitchLevelSlider = Scale(
            pitchLevelFrame, 
            from_=0, 
            to=100, 
            orient="vertical",
            bg="#180421",
            highlightthickness=0,
            troughcolor="#180421",
            fg="white"
        )
        self.pitchLevelSlider.pack()

    def read_slider_values(self, reset = None):
        """This method runs in a separate thread and constantly reads slider values."""
        while True:
            audio_level = self.audioLevelSlider.get()
            eko_level = self.ekoLevelSlider.get()
            bass_level = self.bassLevelSlider.get()
            tiz_level = self.tizLevelSlider.get()
            pitch_level = self.pitchLevelSlider.get()
            
            if reset is False:
                 self.reset = False
            
            sleep(0.1)  # Adjust the interval as needed
            return audio_level, eko_level, bass_level, tiz_level, pitch_level, self.reset, self.denoise, self.settings, self.mute, self.check

    def setup_images_and_text(self):
        
        # Checkbutton değişkenleri
        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()
        self.var4 = IntVar()
        self.var5 = IntVar()
        self.var6 = IntVar()
        self.var7 = IntVar()
        
        image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        self.canvas.create_image(175.0, 400.0, image=image_image_1)
        self.canvas.image_image_1 = image_image_1  # Keep a reference to avoid garbage collection

        image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        self.canvas.create_image(525.0, 400.0, image=image_image_2)
        self.canvas.image_image_2 = image_image_2

        # Adding text to canvas
        self.canvas.create_text(175.0, 318.0, anchor="nw", text="SİNYAL", fill="#FFFFFF", font=("Inter", 20 * -1))
        self.canvas.create_text(505.0, 319.0, anchor="nw", text="FFT", fill="#FFFFFF", font=("Inter", 20 * -1))
        self.canvas.create_text(46.0, 276.0, anchor="nw", text="banyo", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(157.0, 276.0, anchor="nw", text="MAĞARA", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(268.0, 276.0, anchor="nw", text="AKUSTİK", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(379.0, 276.0, anchor="nw", text="ROCK", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(490.0, 276.0, anchor="nw", text="SAHNE", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(601.0, 276.0, anchor="nw", text="STÜDYO", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(653.0, 304.0, anchor="nw", text="SOFT", fill="#FFFFFF", font=("Inter", 10 * -1))

        self.canvas.create_text(102.0, 250.0, anchor="nw", text="SES SEVİYESİ", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(217.0, 250.0, anchor="nw", text="YANKI SEVİYESİ", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(327.0, 250.0, anchor="nw", text="BASS SEVİYESİ", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(437.0, 250.0, anchor="nw", text="TİZ SEVİYESİ", fill="#FFFFFF", font=("Inter", 10 * -1))
        self.canvas.create_text(547.0, 250.0, anchor="nw", text="PITCH SEVİYESİ", fill="#FFFFFF", font=("Inter", 10 * -1))
                
        self.cb1 = Checkbutton(self.root, variable=self.var1, command=lambda: self.check_button_clicked(self.var1, 1), bg="#180421")
        self.canvas.create_window(12.0, 271.0, window=self.cb1, anchor="nw")

        self.cb2 = Checkbutton(self.root, variable=self.var2, command=lambda: self.check_button_clicked(self.var2, 2), bg="#180421")
        self.canvas.create_window(123.0, 271.0, window=self.cb2, anchor="nw")

        self.cb3 = Checkbutton(self.root, variable=self.var3, command=lambda: self.check_button_clicked(self.var3, 3), bg="#180421")
        self.canvas.create_window(234.0, 271.0, window=self.cb3, anchor="nw")

        self.cb4 = Checkbutton(self.root, variable=self.var4, command=lambda: self.check_button_clicked(self.var4, 4), bg="#180421")
        self.canvas.create_window(345.0, 271.0, window=self.cb4, anchor="nw")

        self.cb5 = Checkbutton(self.root, variable=self.var5, command=lambda: self.check_button_clicked(self.var5, 5), bg="#180421")
        self.canvas.create_window(456.0, 271.0, window=self.cb5, anchor="nw")

        self.cb6 = Checkbutton(self.root, variable=self.var6, command=lambda: self.check_button_clicked(self.var6, 6), bg="#180421")
        self.canvas.create_window(567.0, 271.0, window=self.cb6, anchor="nw")

        self.cb7 = Checkbutton(self.root, variable=self.var7, command=lambda: self.check_button_clicked(self.var7, 7), bg="#180421")
        self.canvas.create_window(653.0, 271.0, window=self.cb7, anchor="nw")
        
    def check_button_clicked(self, var, check_num):
        if var.get() == 1:
            #print(f"Checkbutton {check_num} selected")
            self.check[0] = check_num
            self.check[1] = True
        else:
            #print(f"Checkbutton {check_num} deselected")
            self.check[0] = check_num
            self.check[1] = False                
    # Button actions using threads
    def button_1_clicked(self):
        #burası da on off mantığı güzel
        self.denoise = not self.denoise

    def button_2_clicked(self):
        #burada tüm değerlere reset atsın
        self.reset = not self.reset

    def button_3_clicked(self):
        #on off mantığı güzel bura için
        self.mute = not self.mute

    def button_4_clicked(self):
        self.settings = not self.settings
        if self.settings is True:
            window = Tk()#Toplevel()
            settings = settingsGui.AudioSettingsGUI(window)
            print(settings.update_settings())
            window.mainloop()
            
            

'''
def read_slider_values_in_loop(app):
    """A function to read slider values in a while loop with sleep."""
    while True:
        audio_level, eko_level, bass_level, tiz_level, pitch_level, __, __, __, __ = app.read_slider_values()
        #print(f"Thread --- Audio Level: {audio_level}, Echo Level: {eko_level}, Bass Level: {bass_level}, Tiz Level: {tiz_level}, Pitch Level: {pitch_level}")
        sleep(0.1) 

if __name__ == "__main__":
    root = Tk()
    app = AudioApp(root)

    # Start the slider reading in a separate thread
    slider_thread = threading.Thread(target=read_slider_values_in_loop, args=(app,))
    slider_thread.daemon = True  # Set as a daemon thread so it closes with the main program
    slider_thread.start()

    root.mainloop()
'''