import customtkinter as ctk
import importlib

ctk.set_appearance_mode("light")

class HangmanGodzillaApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Word Quest")
        self.geometry("390x720")
        self.resizable(False, False)

        # === GLOBAL STATE GAME ===
        self.player_name    = "PlayerOne"
        self.koin           = 1250
        self.level_terbuka  = 6
        self.bintang_level  = {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 0}

        self.inventory = {
            "💡 Petunjuk Huruf": 2,
            "🕒 Tambah Waktu":   2,
            "❤️ Pulihkan HP":    3,
        }

        self.leaderboard_data = [
            ("ApexPredator", 4500),
            ("GojiraFans",   3800),
            ("PlayerOne",    2450),
            ("KingKong99",   2100),
            ("KaijuHunter",  1500),
        ]

        # === DATA HASIL GAME — diisi gameplay, dibaca victory/gameover ===
        self.hasil_terakhir = {
            "kata":          "",
            "skor":          0,
            "sisa_waktu":    0,
            "hp_player":     0,
            "tebakan_benar": 0,
            "tebakan_salah": 0,
            "huruf_ditebak": set(),
            "mode":          "victory",
        }

        self.current_frame = None
        self.switch_screen("screen1_splash")

    # ── Dipanggil screen6_gameplay SEBELUM switch ke victory/gameover ──
    def set_hasil_game(self, kata, skor, sisa_waktu,
                       hp_player, tebakan_benar,
                       tebakan_salah=0, huruf_ditebak=None,
                       mode="victory"):
        self.hasil_terakhir = {
            "kata":          kata,
            "skor":          skor,
            "sisa_waktu":    sisa_waktu,
            "hp_player":     hp_player,
            "tebakan_benar": tebakan_benar,
            "tebakan_salah": tebakan_salah,
            "huruf_ditebak": huruf_ditebak if huruf_ditebak is not None else set(),
            "mode":          mode,   # "victory" atau "defeat"
        }

    def switch_screen(self, screen_name):
        if self.current_frame is not None:
            self.current_frame.destroy()

        module       = importlib.import_module(screen_name)
        class_name   = "".join([w.capitalize() for w in screen_name.split("_")])
        screen_class = getattr(module, class_name)

        self.current_frame = screen_class(self)
        self.current_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = HangmanGodzillaApp()
    app.mainloop()
