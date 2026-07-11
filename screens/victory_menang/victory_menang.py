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
        # Kunci pengaman awal
        self.sudah_sukses_menang = False

    def populate_data(self, data):
        # Bersihkan data/ambil data dulu untuk pengecekan awal
        sisa_waktu = int(data.get("sisa_waktu", 0))
        hp_player = int(data.get("hp_player", 0))

        # Jika HP sudah 0 atau waktu sudah habis, paksa ke Game Over, jangan tampilkan Victory!
        if hp_player <= 0 or sisa_waktu <= 0:
            print(f"[PENGAMAN] Deteksi Victory Palsu! HP={hp_player}, Waktu={sisa_waktu}. Dialihkan ke Game Over.")
            if hasattr(self.controller, "show_frame"):
                self.controller.show_frame("Screen10GameOver", data=data)
                return

        if self.sudah_sukses_menang:
            self.tkraise()
            return
            
        self.sudah_sukses_menang = True

        for widget in self.winfo_children():
            widget.destroy()

        # SECTION 2: DATA ACQUISITION
        level_sekarang = int(data.get("level", 1))
        self.level_sekarang = level_sekarang
        kata_diterima = str(data.get("kata", ""))
        tebakan_salah = int(data.get("tebakan_salah", 0))

        if kata_diterima:
            total_kata_level = len([k for k in kata_diterima.split(",") if k.strip()])
        else:
            total_kata_level = int(data.get("total_kata_level", 0))
            
        if total_kata_level <= 0:
            total_kata_level = 1
            
        kata_tertebak = total_kata_level

        # SECTION 3: REVISI CORE GAME LOGIC (KECEPATAN & KETEPATAN)
        rasio_waktu = sisa_waktu / 90
        rasio_hp = hp_player / 100
        skor_performa = (rasio_waktu * 0.5) + (rasio_hp * 0.5)
        
        if skor_performa >= 0.80:
            teks_bintang = "⭐ ⭐ ⭐"
        elif skor_performa >= 0.45:
            teks_bintang = "⭐ ⭐"
        else:
            teks_bintang = "⭐"

        poin_tebakan = kata_tertebak * 25
        poin_waktu = sisa_waktu * 1
        poin_hp = hp_player * 1
        koin_didapat = poin_tebakan + poin_waktu + poin_hp

        # SECTION 4: DATABASE SYNCHRONIZATION
        self._simpan_victory_reward_ke_db(
            self.controller, level_sekarang, koin_didapat, kata_diterima, sisa_waktu, hp_player, kata_tertebak, tebakan_salah
        )

        # SECTION 5: UI LAYOUT
        warna_banner = "#4CAF50"
        banner = tk.Frame(self, bg=warna_banner, height=65)
        banner.pack(fill="x", pady=(30, 5), padx=20)
        banner.pack_propagate(False)

        lbl_victory = tk.Label(banner, text="VICTORY!", font=("Arial", 24, "bold"), fg="white", bg=warna_banner)
        lbl_victory.pack(expand=True)

        lbl_bintang = tk.Label(self, text=teks_bintang, font=("Arial", 26), fg="#FFB300", bg="white")
        lbl_bintang.pack(pady=(5, 5))

        lbl_judul_kata = tk.Label(self, text="KATA PADA LEVEL INI :", font=("Arial", 11, "bold"), fg="black", bg="white")
        lbl_judul_kata.pack(pady=(2, 0))

        lbl_isi_kata = tk.Label(self, text=kata_diterima, font=("Arial", 10), fg="#555555", bg="white", wraplength=340)
        lbl_isi_kata.pack(pady=(2, 10))

        reward_box = tk.Frame(self, bg="white")
        reward_box.pack(fill="x", padx=35, pady=5)
        tk.Label(reward_box, text="REWARD LUAR BIASA", font=("Arial", 10, "bold"), fg="black", bg="white").pack(pady=(12, 2))

        coin_row = tk.Frame(reward_box, bg="white")
        coin_row.pack(anchor="center", pady=(0, 12))

        lbl_icon = tk.Label(coin_row, text="💰", font=("Arial", 32), fg="#FFB300", bg="white")
        lbl_icon.pack(side="left", padx=(0, 8))

        lbl_koin = tk.Label(coin_row, text=f"+{koin_didapat}", font=("Arial", 32, "bold"), fg="#FFB300", bg="white")
        lbl_koin.pack(side="left")

        stats_frame = tk.Frame(self, bg="white")
        stats_frame.pack(fill="x", padx=45, pady=15)
        m, s = divmod(sisa_waktu, 60)
        items = [
            ("⏱️", "#4CAF50", 14, "Sisa Waktu", f"{m:02d}:{s:02d}", f"+{poin_waktu} Pts"),
            ("❤️", "#E53935", 14, "Sisa HP Kamu", f"{hp_player}/100", f"+{poin_hp} Pts"),
            ("🎯", "#FFB300", 14, "Tebakan Benar", f"{kata_tertebak}/{total_kata_level}", f"+{poin_tebakan} Pts")
        ]
        for icon, icon_col, icon_size, label_teks, label_val, label_bonus in items:
            row = tk.Frame(stats_frame, bg="white")
            row.pack(fill="x", pady=8)

            tk.Label(row, text=icon, font=("Arial", icon_size), fg=icon_col, bg="white").pack(side="left", padx=(0, 8))

            tk.Label(row, text=label_teks, font=("Arial", 11, "bold"), fg="black", bg="white").pack(side="left")

            tk.Label(row, text=label_bonus, font=("Arial", 11, "bold"), fg="#4CAF50", bg="white").pack(side="right")

            tk.Label(row, text=label_val, font=("Arial", 11), fg="#333333", bg="white").pack(side="right", padx=20)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=30)

        btn_lanjut = tk.Button(btn_frame, text="LANJUT LEVEL", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", height=2, command=self._action_lanjut)
        btn_lanjut.pack(fill="x", pady=6)
        
        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu)
        btn_menu.pack(fill="x", pady=6)

    # SECTION 6: NAVIGATION HANDLERS (CONTROLLERS)
    def _action_lanjut(self):
        self.sudah_sukses_menang = False
        
        daftar_level = [
            "Screen6Gameplay", 
            "Screen7GameplayLevel2", 
            "Screen8GameplayLevel3", 
        ]
        
        try:
           
            if self.level_sekarang < len(daftar_level):
                next_screen = daftar_level[self.level_sekarang]
                self.controller.show_frame(next_screen)
            else:
                # Jika level sudah habis tamat, balikkan ke Menu
                print("[GAME] Semua level telah diselesaikan!")
                self.controller.show_frame("MenuPage")
        except Exception as e:
            print(f"[NAVIGASI] Error pindah level: {e}")
            self.controller.show_frame("MenuPage")

    def _action_menu(self):
        self.sudah_sukses_menang = False
        try:
            self.controller.show_frame("MenuPage")
        except AttributeError:
            print("[PREVIEW] Tombol Kembali ke Menu Diklik")

    # SECTION 7: BACKEND DATABASE TRANSACTIONS
    def _simpan_victory_reward_ke_db(self, controller, level, koin, kata, sisa_waktu, hp, benar, salah):
        if controller is None or not hasattr(controller, 'user_aktif') or controller.user_aktif is None:
            print("[DATABASE] Menjalankan Mode Preview: Database dilewati karena tidak ada session user aktif.")
            return
            
        user_id = controller.user_aktif["id"]
        db_koneksi = hubungkan_database()
        if db_koneksi is not None:
            try:
                cursor = db_koneksi.cursor()
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
                print(f"[DATABASE] Sukses mencatat skor VICTORY & menambah +{koin} koin untuk User ID: {user_id}!")
            except Exception as e:
                print(f"[DATABASE] Error saat mencatat data kemenangan: {e}")
            finally:
                cursor.close()
                db_koneksi.close()
        else:
            print("[DATABASE] Gagal terhubung ke database.")