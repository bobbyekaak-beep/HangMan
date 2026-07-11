import tkinter as tk
from database.koneksi import hubungkan_database
from logic.level_config import LEVEL_CONFIG, TIME_ATTACK_CONFIG
from audio.sound_manager import putar_sfx, normalkan_musik_latar, hentikan_semua_sfx

class Screen10GameOver(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.parent = parent
        self.controller = controller
        self.sudah_game_over = False

    def populate_data(self, data):
        if self.sudah_game_over:
            self.tkraise()
            return

        self.sudah_game_over = True

        normalkan_musik_latar()
        hentikan_semua_sfx()
        putar_sfx("defeat.mp3")

        for widget in self.winfo_children():
            widget.destroy()

        user_aktif = getattr(self.controller, "user_aktif", None)
        username_dari_controller = user_aktif.get("username") if isinstance(user_aktif, dict) else None
        username_aktif = data.get("username") or username_dari_controller or "Guest"

        level_sekarang = int(data.get("level", 1))
        self.level_sekarang = level_sekarang
        kata_diterima = str(data.get("kata", "-"))
        sisa_waktu = max(0, int(data.get("sisa_waktu", 0)))
        hp_player = max(0, int(data.get("hp_player", 0)))
        tebakan_salah = int(data.get("tebakan_salah", 0))
        koin_hiburan = 20

        raw_benar = data.get("kata_tertebak")
        if raw_benar is None:
            raw_benar = data.get("tebakan_benar")
        if raw_benar is None:
            raw_benar = data.get("benar")

        if raw_benar is None:
            kata_tertebak = 0
        else:
            try:
                kata_tertebak = int(raw_benar)
            except (ValueError, TypeError):
                kata_tertebak = 0

        self._simpan_game_over_ke_db(
            username_aktif, level_sekarang, koin_hiburan, kata_diterima, sisa_waktu, hp_player, kata_tertebak, tebakan_salah
        )

        warna_banner = "#E53935"
        banner = tk.Frame(self, bg=warna_banner, height=65)
        banner.pack(fill="x", pady=(30, 15), padx=20)
        banner.pack_propagate(False)

        lbl_gameover = tk.Label(banner, text="GAME OVER", font=("Arial", 24, "bold"), fg="white", bg=warna_banner)
        lbl_gameover.pack(expand=True)

        lbl_judul_kata = tk.Label(self, text="KATA PADA LEVEL INI :", font=("Arial", 11, "bold"), fg="black", bg="white")
        lbl_judul_kata.pack(pady=(35, 0))
        lbl_isi_kata = tk.Label(self, text=kata_diterima, font=("Arial", 10), fg="#555555", bg="white", wraplength=340)
        lbl_isi_kata.pack(pady=(2, 15))

        reward_box = tk.Frame(self, bg="white")
        reward_box.pack(fill="x", padx=35, pady=5)

        tk.Label(reward_box, text="REWARD HIBURAN", font=("Arial", 11, "bold"), fg="black", bg="white").pack(pady=(12, 5))

        coin_row = tk.Frame(reward_box, bg="white")
        coin_row.pack(anchor="center", pady=(0, 12))

        lbl_icon = tk.Label(coin_row, text="💰", font=("Arial", 21), fg="#FFB300", bg="white")
        lbl_icon.pack(side="left", padx=(0, 5))
        lbl_koin = tk.Label(coin_row, text=f"+{koin_hiburan}", font=("Arial", 20, "bold"), fg="#FFB300", bg="white")
        lbl_koin.pack(side="left")

        stats_frame = tk.Frame(self, bg="white")
        stats_frame.pack(fill="x", padx=45, pady=15)

        m, s = divmod(sisa_waktu, 60)
        items = [
            ("⏱️", "#4CAF50", 14, "Sisa Waktu", f"{m:02d}:{s:02d}"),
            ("❤️", "#E53935", 14, "Sisa HP Kamu", f"{hp_player}/100"),
            ("🎯", "#FFB300", 14, "Tebakan Benar", f"{kata_tertebak}")
        ]

        for icon, icon_col, icon_size, label_teks, label_val in items:
            row = tk.Frame(stats_frame, bg="white")
            row.pack(fill="x", pady=8)
            tk.Label(row, text=icon, font=("Arial", icon_size), fg=icon_col, bg="white").pack(side="left", padx=(0, 8))
            tk.Label(row, text=label_teks, font=("Arial", 11, "bold"), fg="black", bg="white").pack(side="left")
            tk.Label(row, text=label_val, font=("Arial", 11), fg="#333333", bg="white").pack(side="right", padx=20)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=30)

        btn_coba = tk.Button(btn_frame, text="COBA LAGI", font=("Arial", 12, "bold"), bg="#E53935", fg="white", relief="flat", height=2, command=self._action_coba_lagi)
        btn_coba.pack(fill="x", pady=6)

        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu)
        btn_menu.pack(fill="x", pady=6)

    def _action_coba_lagi(self):
        putar_sfx("klik.mp3")
        self.sudah_game_over = False
        level = getattr(self, "level_sekarang", 1)
        try:
            self.controller.show_frame("Screen5PersiapanPerang", data={"level": level})
        except AttributeError:
            print("[PREVIEW] Tombol Coba Lagi Diklik")

    def _action_menu(self):
        putar_sfx("klik.mp3")
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
            cursor = None
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
                    waktu_maksimal = TIME_ATTACK_CONFIG["waktu_detik"] if level <= 0 else LEVEL_CONFIG.get(level, LEVEL_CONFIG[1])["waktu_detik"]
                    waktu_bermain = waktu_maksimal - sisa_waktu
                    if waktu_bermain < 0:
                        waktu_bermain = 0

                    cursor.execute(query_score, (user_id, level, waktu_bermain, 'GAME OVER', kata, sisa_waktu, hp, benar, salah, koin))
                    db_koneksi.commit()
                    print(f"[DATABASE] Sukses mencatat data LOSE & menambah +{koin} koin hiburan untuk user '{username}' (ID: {user_id})!")
                else:
                    print(f"[DATABASE] User '{username}' tidak ditemukan di database.")
            except Exception as e:
                print(f"[DATABASE] Error saat mencatat data kekalahan: {e}")
            finally:
                if cursor is not None:
                    cursor.close()
                db_koneksi.close()
        else:
            print("[DATABASE] Gagal terhubung ke database.")