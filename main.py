import tkinter as tk
from screens.page_splash.splash_view import SplashPage
from screens.page_login.login_view import LoginPage
from screens.page_menu.menu_view import MenuPage
from screens.page_pilih_level.pilih_level_view import PilihLevelApp
from screens.page_toko.toko_view import TokoView
from screens.page_papan_peringkat.papan_peringkat_view import LeaderboardView
from screens.page_misi_pemain_baru.misi_pemain_baru_view import MisiHarianApp
from screens.persiapan.persiapan import Screen5PersiapanPerang
from screens.page_game.level1ui import Screen6Gameplay
from screens.page_game.level2ui import Screen7GameplayLevel2
from screens.page_game.level3ui import Screen8GameplayLevel3
from screens.victory_menang.victory_menang import Screen9Victory
from screens.game_over.game_over import Screen10GameOver
from screens.page_game.misiharianui import ScreenDailyMission

DAFTAR_HALAMAN = [
    SplashPage, LoginPage, MenuPage, PilihLevelApp, TokoView, LeaderboardView,
    MisiHarianApp, Screen5PersiapanPerang, Screen6Gameplay, Screen7GameplayLevel2,
    Screen8GameplayLevel3, Screen9Victory, Screen10GameOver, ScreenDailyMission
    ]
class HangmanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Word Quest")
        self.geometry("400x700") 
        self.configure(bg="white")
        self.resizable(False, False) # Kunci ukuran layar agar tidak berantakan

        self.user_aktif = None

        self.container = tk.Frame(self, bg="white")
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        
        # Memasukkan semua halaman ke dalam memori aplikasi
        for F in DAFTAR_HALAMAN:
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Tumpuk semua halaman di titik yang sama
            frame.grid(row=0, column=0, sticky="nsew")

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Tampilkan splash screen saat pertama kali dibuka
        self.show_frame("SplashPage")

    def show_frame(self, page_name, data=None):
        frame = self.frames[page_name]
        if data is not None and hasattr(frame, "populate_data"):
            frame.populate_data(data)
        frame.tkraise() # Angkat halaman yang dipilih ke urutan paling atas

    def set_hasil_game(self, **kwargs):
        self.hasil_terakhir = kwargs
        # Otomatis pindah ke halaman menang atau kalah sambil membawa data nilai
        if kwargs.get("mode") == "victory":
            self.show_frame("Screen9Victory", data=self.hasil_terakhir)
        else:
            self.show_frame("Screen10GameOver", data=self.hasil_terakhir)

    def go_back(self):
        # Perintah ini akan membawa user kembali ke Menu Utama
        self.show_frame("MenuPage")

    def buka_misi(self):
        self.show_frame("MisiHarianApp")

if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()