import tkinter as tk
from page_splash.splash_view import SplashPage
from page_login.login_view import LoginPage
from page_menu.menu_view import MenuPage

class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Word Quest")
        self.geometry("400x700") 
        self.configure(bg="white")
        self.resizable(False, False) # Kunci ukuran layar agar tidak berantakan

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        
        # Memasukkan semua halaman ke dalam memori aplikasi
        for F in (SplashPage, LoginPage, MenuPage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Tumpuk semua halaman di titik yang sama
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Tampilkan splash screen saat pertama kali dibuka
        self.show_frame("SplashPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise() # Angkat halaman yang dipilih ke urutan paling atas

if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()