import tkinter as tk 
from database.koneksi import hubungkan_database 

LEVELS = [
    "Screen7GameplayLevel2",
    "Screen8GameplayLevel3",
]

class Screen9Victory(tk.Frame): 
    def __init__(self, parent, controller): 
        super().__init__(parent, bg="white") 
        self.parent = parent 
        self.controller = controller

    def populate_data(self, data): 
        # Bersihkan widget lama jika fungsi dipanggil ulang agar tidak menumpuk 
        for widget in self.winfo_children(): 
            widget.destroy() 
            
        # SECTION 2: DATA ACQUISITION (MULTI-USER & PROGRESS) 
        username_aktif = data.get("username", "mama") 
        level_sekarang = data.get("level", 1)
        self.level_sekarang = level_sekarang
        kata_diterima = data.get("kata", "HARIMAU, KANCIL, GAJAH") 
        sisa_waktu = data.get("sisa_waktu", 75) 
        hp_player = data.get("hp_player", 80) 
        kata_tertebak = data.get("kata_tertebak", 3) 
        total_kata_level = data.get("total_kata_level", 4) 
        tebakan_salah = data.get("tebakan_salah", 0) 
        
        if total_kata_level <= 0: 
            total_kata_level = 1 
            
        # SECTION 3: CORE GAME LOGIC (RATING & REWARD CALCULATIONS) 
        rasio_sukses = kata_tertebak / total_kata_level 
        if kata_tertebak == total_kata_level and kata_tertebak > 0: 
            teks_bintang = "⭐ ⭐ ⭐" 
        elif rasio_sukses >= 0.50: 
            teks_bintang = "⭐ ⭐" 
        else: 
            teks_bintang = "⭐" 
            
        poin_tebakan = kata_tertebak * 25 
        poin_waktu = sisa_waktu * 1 
        poin_hp = hp_player * 1 
        koin_didapat = poin_tebakan + poin_waktu + poin_hp 
        
        # SECTION 4: DATABASE SYNCHRONIZATION (MULTI-USER EVENT) 
        self._simpan_victory_reward_ke_db( 
            username_aktif, level_sekarang, koin_didapat, kata_diterima, 
            sisa_waktu, hp_player, kata_tertebak, tebakan_salah 
        ) 
        
        # SECTION 5: UI LAYOUT #  TOP HEADER BANNER 
        warna_banner = "#4CAF50" 
        banner = tk.Frame(self, bg=warna_banner, height=65) 
        banner.pack(fill="x", pady=(30, 5), padx=20) 
        banner.pack_propagate(False) 
        
        lbl_victory = tk.Label(banner, text="VICTORY!", font=("Arial", 24, "bold"), fg="white", bg=warna_banner) 
        lbl_victory.pack(expand=True) 
        
        # RATINGS CONTENT
        lbl_bintang = tk.Label(self, text=teks_bintang, font=("Arial", 26), fg="#FFB300", bg="white") 
        lbl_bintang.pack(pady=(5, 5)) 
        
        lbl_judul_kata = tk.Label(self, text="KATA PADA LEVEL INI :", font=("Arial", 11, "bold"), fg="black", bg="white") 
        lbl_judul_kata.pack(pady=(2, 0)) 
        
        lbl_isi_kata = tk.Label(self, text=kata_diterima, font=("Arial", 10), fg="#555555", bg="white", wraplength=340) 
        lbl_isi_kata.pack(pady=(2, 10)) 
        
        # CENTRAL REWARD VISUALIZER
        reward_box = tk.Frame(self, bg="white") 
        reward_box.pack(fill="x", padx=35, pady=5) 
        
        tk.Label(reward_box, text="REWARD LUAR BIASA", font=("Arial", 10, "bold"), fg="black", bg="white").pack(pady=(12, 2)) 
        
        coin_row = tk.Frame(reward_box, bg="white")
        coin_row.pack(anchor="center", pady=(0, 12))
        
        lbl_icon = tk.Label(coin_row, text="💰", font=("Arial", 32), fg="#FFB300", bg="white")
        lbl_icon.pack(side="left", padx=(0, 8))
        
        lbl_koin = tk.Label(coin_row, text=f"+{koin_didapat}", font=("Arial", 32, "bold"), fg="#FFB300", bg="white") 
        lbl_koin.pack(side="left") 
        
        # DETAILED STATISTICS SCOREBOARD 
        stats_frame = tk.Frame(self, bg="white") 
        stats_frame.pack(fill="x", padx=45, pady=15) 
        
        m, s = divmod(sisa_waktu, 60) 
        items = [ 
            ("⏱️", "#4CAF50", 14, "Sisa Waktu", f"{m:02d}:{s:02d}", f"+{poin_waktu} Pts"), 
            ("❤️", "#E53935", 14, "Sisa HP Kamu", f"{hp_player}/100", f"+{poin_hp} Pts"), 
            ("🎯", "#FFB300", 14, "Tebakan Benar", f"{kata_tertebak}/{total_kata_level} Kata", f"+{poin_tebakan} Pts") 
        ] 
        
        for icon, icon_col, icon_size, label_teks, label_val, label_bonus in items: 
            row = tk.Frame(stats_frame, bg="white") 
            row.pack(fill="x", pady=8) 
            tk.Label(row, text=icon, font=("Arial", icon_size), fg=icon_col, bg="white").pack(side="left", padx=(0, 8)) 
            tk.Label(row, text=label_teks, font=("Arial", 11, "bold"), fg="black", bg="white").pack(side="left") 
            tk.Label(row, text=label_bonus, font=("Arial", 11, "bold"), fg="#4CAF50", bg="white").pack(side="right") 
            tk.Label(row, text=label_val, font=("Arial", 11), fg="#333333", bg="white").pack(side="right", padx=20) 
            
        # NAVIGATION CONTROL BUTTONS 
        btn_frame = tk.Frame(self, bg="white") 
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=30) 
        
        btn_lanjut = tk.Button(btn_frame, text="LANJUT LEVEL", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", height=2, command=self._action_lanjut) 
        btn_lanjut.pack(fill="x", pady=6) 
        
        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu) 
        btn_menu.pack(fill="x", pady=6) 

    # SECTION 6: NAVIGATION HANDLERS (CONTROLLERS) 
    def _action_lanjut(self):
        try:
            next_screen = LEVELS[self.level_sekarang - 1]
            self.controller.show_frame(next_screen)
        except (IndexError, AttributeError):
            self.controller.show_frame("MenuPage")

    def _action_menu(self):
        try:
            self.controller.show_frame("MenuPage")
        except AttributeError:
            print("[PREVIEW] Tombol Kembali ke Menu Diklik")

    # SECTION 7: BACKEND DATABASE TRANSACTIONS (MySQL) 
    def _simpan_victory_reward_ke_db(self, username, level, koin, kata, sisa_waktu, hp, benar, salah): 
        db_koneksi = hubungkan_database() 
        if db_koneksi is not None: 
            try: 
                cursor = db_koneksi.cursor() 
                query_user = "SELECT id FROM users WHERE username = %s" 
                cursor.execute(query_user, (username,)) 
                user_data = cursor.fetchone() 
                if user_data is not None: 
                    user_id = user_data[0] 
                    if koin > 0: 
                        query_koin = "UPDATE users SET coins = coins + %s WHERE id = %s" 
                        cursor.execute(query_koin, (koin, user_id)) 
                    query_score = """ 
                        INSERT INTO scores (user_id, level_reached, waktu_bermain, status_game, kata_rahasia, sisa_waktu, hp_player, tebakan_benar, tebakan_salah, koin_didapat) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                    """ 
                    waktu_bermain = 90 - sisa_waktu 
                    if waktu_bermain < 0: 
                        waktu_bermain = 0 
                    cursor.execute(query_score, (user_id, level, waktu_bermain, 'VICTORY', kata, sisa_waktu, hp, benar, salah, koin)) 
                    db_koneksi.commit() 
                    print(f"[DATABASE] Sukses mencatat skor & menambah +{koin} koin untuk user '{username}' (ID: {user_id})!") 
                else: 
                    print(f"[DATABASE] User '{username}' tidak ditemukan di database.") 
            except Exception as e: 
                print(f"[DATABASE] Error saat mencatat data: {e}") 
            finally: 
                cursor.close() 
                db_koneksi.close() 
        else: 
            print("[DATABASE] Gagal terhubung ke database.") 

# TESTING 
if __name__ == "__main__": 
    root = tk.Tk() 
    root.title("Victory") 
    root.geometry("400x700") 
    root.resizable(False, False) 
    root.configure(bg="white") 
    
    data_dummy = { 
        "username": "mama", 
        "level": 1, 
        "kata": "HARIMAU, GAJAH, ELANG, KANCIL, MERPATI", 
        "total_kata_level": 5, 
        "kata_tertebak": 4, 
        "sisa_waktu": 75, 
        "hp_player": 80, 
        "tebakan_salah": 2 
    } 
    app = Screen9Victory(root) 
    app.pack(fill="both", expand=True) 
    app.populate_data(data_dummy) 
    root.mainloop()