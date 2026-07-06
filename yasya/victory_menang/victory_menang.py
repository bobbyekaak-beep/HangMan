# victory_menang.py
import tkinter as tk

class Screen9Victory(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F6")
        self.parent = parent
        
    def populate_data(self, data):
        # Bersihkan widget lama agar tidak menumpuk saat bermain ulang
        for widget in self.winfo_children():
            widget.destroy()
            
        # Mengambil data dari hasil permainan
        kata = data.get("kata", "HARIMAU")
        sisa_waktu = data.get("sisa_waktu", 75)   
        hp_player = data.get("hp_player", 80)     
        tebakan_benar = data.get("tebakan_benar", 7)

        # BANNER ATAS
        banner = tk.Frame(self, bg="#4CAF50", height=65)
        banner.pack(fill="x", pady=(40, 15), padx=20)
        banner.pack_propagate(False)
        lbl_victory = tk.Label(banner, text="VICTORY!", font=("Arial", 22, "bold"), fg="white", bg="#4CAF50")
        lbl_victory.pack(expand=True)

        # DETAIL KATA RAHASIA 
        lbl_kata = tk.Label(self, text=f"KATA: {kata}", font=("Arial", 16, "bold"), fg="black", bg="#F0F4F6")
        lbl_kata.pack(pady=10)

        # BOX REWARD UTAMA 
        reward_box = tk.Frame(self, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        reward_box.pack(fill="x", padx=35, pady=15)
        
        tk.Label(reward_box, text="REWARD LUAR BIASA", font=("Arial", 10, "bold"), fg="black", bg="white").pack(pady=(12, 2))
        tk.Label(reward_box, text="💰 +150", font=("Arial", 28, "bold"), fg="#FFB300", bg="white").pack(pady=(0, 12))

        # SKOR BONUS 
        stats_frame = tk.Frame(self, bg="#F0F4F6")
        stats_frame.pack(fill="x", padx=45, pady=15)

        m, s = divmod(sisa_waktu, 60)
        
        items = [
            ("⏱️", "#4CAF50", 14, "Sisa Waktu", f"{m:02d}:{s:02d}", "+70 Pts"),   
            ("❤️", "#E53935", 14, "Sisa HP Kamu", f"{hp_player}/100", "+60 Pts"), 
            ("🎯", "#FFB300", 18, "Tebakan Benar", f"{tebakan_benar} Huruf", "+20 Pts") 
        ]

        for icon, icon_col, icon_size, label_teks, label_val, label_bonus in items:
            row = tk.Frame(stats_frame, bg="#F0F4F6")
            row.pack(fill="x", pady=6)
            
            tk.Label(row, text=icon, font=("Arial", icon_size), fg=icon_col, bg="#F0F4F6").pack(side="left", padx=(0, 8))
            
            tk.Label(row, text=label_teks, font=("Arial", 11, "bold"), fg="black", bg="#F0F4F6").pack(side="left")
            
            tk.Label(row, text=label_bonus, font=("Arial", 11, "bold"), fg="#4CAF50", bg="#F0F4F6").pack(side="right")
            
            tk.Label(row, text=label_val, font=("Arial", 11), fg="#333333", bg="#F0F4F6").pack(side="right", padx=20)

        # TOMBOL AKSI 
        btn_frame = tk.Frame(self, bg="#F0F4F6")
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=45)

        btn_lanjut = tk.Button(btn_frame, text="LANJUT LEVEL", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", height=2, command=self._action_lanjut)
        btn_lanjut.pack(fill="x", pady=6)

        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu)
        btn_menu.pack(fill="x", pady=6)

    def _action_lanjut(self):
        try:
            self.parent.switch_screen("game")
        except AttributeError:
            print("[PREVIEW] Tombol Lanjut Level Diklik")

    def _action_menu(self):
        try:
            self.parent.switch_screen("menu")
        except AttributeError:
            print("[PREVIEW] Tombol Kembali ke Menu Diklik")


#  PENGETESAN TAMPILAN 
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Preview Halaman Victory")
    root.geometry("400x700")
    root.resizable(False, False)
    root.configure(bg="#F0F4F6")

    data_dummy = {
        "kata": "HARIMAU",
        "sisa_waktu": 75,
        "hp_player": 80,
        "tebakan_benar": 7
    }

    app = Screen9Victory(root)
    app.pack(fill="both", expand=True)
    app.populate_data(data_dummy)
    root.mainloop()