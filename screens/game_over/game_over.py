import tkinter as tk
from database.koneksi import hubungkan_database

class Screen10GameOver(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.parent = parent
        self.controller = controller
        self.sudah_game_over = False

    def populate_data(self, data):

        # BARIS DEBUG UTAMAKU
        print("\n" + "=" * 60)
        print("[DEBUG GAME OVER] DATA YANG DITERIMA DARI SCREEN GAMEPLAY:")
        print(data)
        print("=" * 60 + "\n")


        # SECTION 2: DATA ACQUISITION (DIBUAT SEPENUHNYA DINAMIS UNTUK SEMUA USER)
        username_aktif = data.get("username") or getattr(self.controller, 'username_aktif', None) or getattr(self.controller, 'user_aktif', None)
        if not username_aktif:
            username_aktif = "Guest"

        level_sekarang = data.get("level", 1)
        kata_diterima = data.get("kata", "-")
        sisa_waktu = data.get("sisa_waktu", 0)
        hp_player = data.get("hp_player", 0)
        tebakan_salah = data.get("tebakan_salah", 0)
        koin_hiburan = 20  # Kunci mati 20 poin sesuai request


        # PROSES SANITASI DATA: Memastikan kata_tertebak murni Angka (Integer)
        raw_benar = data.get("kata_tertebak") or data.get("tebakan_benar") or data.get("benar")
        
        # Jika data dari gameplay ternyata kosong/None, set langsung ke 0
        if raw_benar is None:
            kata_tertebak = 0
        else:
            try:
                kata_tertebak = int(raw_benar)
            except (ValueError, TypeError):
                kata_tertebak = 0


        if kata_tertebak >= 3:
            bintang_str = "⭐ ⭐"  
        elif kata_tertebak >= 2:
            bintang_str = "⭐"         
        else:
            bintang_str = "😢"         

        self.sudah_game_over = True

        # Simpan list widget lama sebelum membuat container baru (agar tidak transisi layar putih)
        widget_lama = self.winfo_children()

        # SECTION 4: UI LAYOUT & GRAPHICAL WIDGETS (Menggunakan Container Utama)
        main_container = tk.Frame(self, bg="white")
        main_container.pack(fill="both", expand=True)

        # TOP HEADER BANNER
        banner = tk.Frame(main_container, bg="#E53935", height=65)
        banner.pack(fill="x", pady=(30, 10), padx=20)
        banner.pack_propagate(False)

        lbl_gameover = tk.Label(banner, text="GAME OVER", font=("Arial", 20, "bold"), fg="white", bg="#E53935")
        lbl_gameover.pack(expand=True)

        # TAMPILAN BINTANG HASIL GAME OVER
        lbl_bintang = tk.Label(main_container, text=bintang_str, font=("Arial", 20, "bold"), fg="#FFB300", bg="white")
        lbl_bintang.pack(pady=(10, 5))

        # REVEAL CORRECT ANSWER
        lbl_info = tk.Label(main_container, text="KATA PADA LEVEL INI :", font=("Arial", 11, "bold"), fg="black", bg="white")
        lbl_info.pack(pady=(15, 2))

        lbl_kata_asli = tk.Label(main_container, text=kata_diterima, font=("Arial", 10), fg="black", bg="white", wraplength=340)
        lbl_kata_asli.pack(pady=(0, 20))

        # CENTRAL REWARD VISUALIZER (CONSOLATION PRIZE)
        reward_box = tk.Frame(main_container, bg="white")
        reward_box.pack(fill="x", padx=35, pady=10)

        tk.Label(reward_box, text="REWARD HIBURAN", font=("Arial", 11, "bold"), fg="black", bg="white").pack(pady=(12, 2))

        coin_row = tk.Frame(reward_box, bg="white")
        coin_row.pack(anchor="center", pady=(0, 12))

        lbl_icon = tk.Label(coin_row, text="💰", font=("Arial", 36), fg="#FFB300", bg="white")
        lbl_icon.pack(side="left", padx=(0, 8))

        lbl_text = tk.Label(coin_row, text=f"+{koin_hiburan}", font=("Arial", 36, "bold"), fg="#FFB300", bg="white")
        lbl_text.pack(side="left")

        # MOTIVATIONAL TEXT
        lbl_motivasi = tk.Label(main_container, text="Jangan menyerah!\nAsah strategimu dan coba sekali lagi.", font=("Arial", 11, "italic"), fg="#555555", bg="white", justify="center")
        lbl_motivasi.pack(pady=25)

        # NAVIGATION CONTROL BUTTONS
        btn_frame = tk.Frame(main_container, bg="white")
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=35)

        btn_coba = tk.Button(btn_frame, text="COBA LAGI", font=("Arial", 12, "bold"), bg="#E53935", fg="white", relief="flat", height=2, command=self._action_coba_lagi)
        btn_coba.pack(fill="x", pady=6)

        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu)
        btn_menu.pack(fill="x", pady=6)

        # Hancurkan widget lama secara bersih setelah UI baru selesai digambar di layar
        for widget in widget_lama:
            widget.destroy()

        self.tkraise()
        self.update_idletasks()

        # SECTION 3: DATABASE SYNCHRONIZATION
        self._simpan_game_over_ke_db(
            username_aktif, level_sekarang, koin_hiburan, kata_diterima, sisa_waktu, hp_player, kata_tertebak, tebakan_salah
        )

    def _action_coba_lagi(self):
        self.sudah_game_over = False
        try:
            self.controller.show_frame("Screen5PersiapanPerang")
        except AttributeError:
            print("[PREVIEW] Tombol Coba Lagi Diklik")

    def _action_menu(self):
        self.sudah_game_over = False
        try:
            self.controller.show_frame("MenuPage")
        except AttributeError:
            print("[PREVIEW] Tombol Kembali ke Menu Diklik")

    def _simpan_game_over_ke_db(self, username, level, koin, kata, sisa_waktu, hp, benar, salah):
        if username == "Guest":
            print("[DATABASE] Mode Guest Aktif: Data tidak disimpan ke database.")
            return

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
                    if waktu_bermain < 0 or waktu_bermain > 90:
                        waktu_bermain = 90

                    cursor.execute(query_score, (user_id, level, waktu_bermain, 'GAME OVER', kata, sisa_waktu, hp, benar, salah, koin))
                    db_koneksi.commit()
                    print(f"[DATABASE] Sukses mencatat data LOSE & menambah +{koin} koin hiburan untuk user '{username}' (ID: {user_id})!")
                else:
                    print(f"[DATABASE] User '{username}' tidak ditemukan di database.")
            except Exception as e:
                print(f"[DATABASE] Error saat mencatat data kekalahan: {e}")
            finally:
                cursor.close()
                db_koneksi.close()
        else:
            print("[DATABASE] Gagal terhubung ke database.")