# game_over.py
import tkinter as tk

class Screen10GameOver(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F6")
        self.parent = parent
        
    def populate_data(self, data):
        for widget in self.winfo_children():
            widget.destroy()
            
        kata = data.get("kata", "HARIMAU")

        # BANNER ATAS (GAME OVER) 
        banner = tk.Frame(self, bg="#E53935", height=65)
        banner.pack(fill="x", pady=(40, 15), padx=20)
        banner.pack_propagate(False)
        lbl_gameover = tk.Label(banner, text="GAME OVER", font=("Arial", 20, "bold"), fg="white", bg="#E53935")
        lbl_gameover.pack(expand=True)

        # PENUNJUK KATA YANG BENAR 
        lbl_info = tk.Label(self, text="KATA YANG BENAR :", font=("Arial", 11, "bold"), fg="black", bg="#F0F4F6")
        lbl_info.pack(pady=(25, 2))
        lbl_kata_asli = tk.Label(self, text=kata, font=("Arial", 22, "bold"), fg="#E53935", bg="#F0F4F6")
        lbl_kata_asli.pack(pady=(0, 25))

        # BOX REWARD MINIMAL (HADIAH HIBURAN) 
        reward_box = tk.Frame(self, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        reward_box.pack(fill="x", padx=35, pady=10)
        
        tk.Label(reward_box, text="REWARD HIBURAN", font=("Arial", 10, "bold"), fg="black", bg="white").pack(pady=(12, 2))
        tk.Label(reward_box, text="💰 +20", font=("Arial", 26, "bold"), fg="#FFB300", bg="white").pack(pady=(0, 12))

        # KALIMAT MOTIVASI 
        lbl_motivasi = tk.Label(self, text="Jangan menyerah!\nAsah strategimu dan coba sekali lagi.", font=("Arial", 11, "italic"), fg="#555555", bg="#F0F4F6", justify="center")
        lbl_motivasi.pack(pady=35)

        # TOMBOL AKSI BAWAH 
        btn_frame = tk.Frame(self, bg="#F0F4F6")
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=45)

        btn_coba = tk.Button(btn_frame, text="COBA LAGI", font=("Arial", 12, "bold"), bg="#E53935", fg="white", relief="flat", height=2, command=self._action_coba_lagi)
        btn_coba.pack(fill="x", pady=6)

        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu)
        btn_menu.pack(fill="x", pady=6)

    def _action_coba_lagi(self):
        try:
            self.parent.switch_screen("game")
        except AttributeError:
            print("[PREVIEW] Tombol Coba Lagi Diklik")

    def _action_menu(self):
        try:
            self.parent.switch_screen("menu")
        except AttributeError:
            print("[PREVIEW] Tombol Kembali ke Menu Diklik")


#  PENGETESAN TAMPILAN
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Preview Halaman Game Over")
    root.geometry("400x700")
    root.resizable(False, False)
    root.configure(bg="#F0F4F6")

    data_dummy_kalah = {
        "kata": "HARIMAU"
    }

    app = Screen10GameOver(root)
    app.pack(fill="both", expand=True)
    app.populate_data(data_dummy_kalah)
    root.mainloop()