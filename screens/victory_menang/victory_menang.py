import tkinter as tk
from database.koneksi import hubungkan_database
from logic.level_config import LEVEL_CONFIG, TIME_ATTACK_CONFIG
from audio.sound_manager import putar_sfx, normalkan_musik_latar, hentikan_semua_sfx

class Screen9Victory(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.parent = parent
        self.controller = controller
        self.sudah_sukses_menang = False

    def populate_data(self, data):
        sisa_waktu = max(0, int(data.get("sisa_waktu", 0)))
        hp_player = max(0, int(data.get("hp_player", 0)))

        if self.sudah_sukses_menang:
            self.tkraise()
            return

        self.sudah_sukses_menang = True

        # Kembalikan musik latar ke volume normal saat keluar dari gameplay
        normalkan_musik_latar()

        # Hentikan sfx yang masih berbunyi (mis. hitung mundur) agar tidak bertabrakan dengan sfx victory
        hentikan_semua_sfx()

        # Bunyikan sfx victory saat layar kemenangan pertama kali tampil
        putar_sfx("victory.mp3")

        for widget in self.winfo_children():
            widget.destroy()

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

        poin_tebakan = kata_tertebak * 25
        poin_waktu = sisa_waktu * 1
        poin_hp = hp_player * 1
        koin_didapat = poin_tebakan + poin_waktu + poin_hp

        poin_koin_tampil = koin_didapat // 2
        poin_bintang_tampil = koin_didapat - poin_koin_tampil

        waktu_maksimal_level = TIME_ATTACK_CONFIG["waktu_detik"] if level_sekarang <= 0 else LEVEL_CONFIG.get(level_sekarang, LEVEL_CONFIG[1])["waktu_detik"]
        koin_maksimal = (total_kata_level * 25) + waktu_maksimal_level + 100
        rasio_koin = koin_didapat / koin_maksimal if koin_maksimal > 0 else 0

        if rasio_koin >= 0.80:
            teks_bintang = "⭐ ⭐ ⭐"
            jumlah_bintang = 3
        elif rasio_koin >= 0.45:
            teks_bintang = "⭐ ⭐"
            jumlah_bintang = 2
        else:
            teks_bintang = "⭐"
            jumlah_bintang = 1

        self._simpan_victory_reward_ke_db(
            self.controller, level_sekarang, koin_didapat, kata_diterima, sisa_waktu, hp_player, kata_tertebak, tebakan_salah
        )

        warna_banner = "#4CAF50"
        banner = tk.Frame(self, bg=warna_banner, height=65)
        banner.pack(fill="x", pady=(30, 15), padx=20)
        banner.pack_propagate(False)

        lbl_victory = tk.Label(banner, text="VICTORY!", font=("Arial", 24, "bold"), fg="white", bg=warna_banner)
        lbl_victory.pack(expand=True)

        lbl_judul_kata = tk.Label(self, text="KATA PADA LEVEL INI :", font=("Arial", 11, "bold"), fg="black", bg="white")
        lbl_judul_kata.pack(pady=(35, 0))
        lbl_isi_kata = tk.Label(self, text=kata_diterima, font=("Arial", 10), fg="#555555", bg="white", wraplength=340)
        lbl_isi_kata.pack(pady=(2, 15))

        reward_box = tk.Frame(self, bg="white")
        reward_box.pack(fill="x", padx=35, pady=5)

        tk.Label(reward_box, text="REWARD LUAR BIASA", font=("Arial", 11, "bold"), fg="black", bg="white").pack(pady=(12, 5))

        double_reward_row = tk.Frame(reward_box, bg="white")
        double_reward_row.pack(anchor="center", pady=(0, 12))

        lbl_icon_coin = tk.Label(double_reward_row, text="💰", font=("Arial", 21), fg="#FFB300", bg="white")
        lbl_icon_coin.pack(side="left", padx=(0, 5))
        lbl_koin = tk.Label(double_reward_row, text=f"+{poin_koin_tampil}", font=("Arial", 20, "bold"), fg="#FFB300", bg="white")
        lbl_koin.pack(side="left", padx=(0, 20))

        lbl_icon_star = tk.Label(double_reward_row, text="⭐", font=("Arial", 20), fg="#FFB300", bg="white")
        lbl_icon_star.pack(side="left", padx=(0, 5))
        lbl_bintang_angka = tk.Label(double_reward_row, text=f"+{poin_bintang_tampil}", font=("Arial", 20, "bold"), fg="#FFB300", bg="white")
        lbl_bintang_angka.pack(side="left")

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

        if level_sekarang >= 3:
            teks_tombol_lanjut = "LIHAT LEADERBOARD"
        elif level_sekarang <= 0:
            teks_tombol_lanjut = "KEMBALI KE MISI HARIAN"
        else:
            teks_tombol_lanjut = "LANJUT LEVEL"

        btn_lanjut = tk.Button(btn_frame, text=teks_tombol_lanjut, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief="flat", height=2, command=self._action_lanjut)
        btn_lanjut.pack(fill="x", pady=6)

        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu)
        btn_menu.pack(fill="x", pady=6)

    def _action_lanjut(self):
        putar_sfx("klik.mp3")
        self.sudah_sukses_menang = False

        daftar_level = [
            "Screen6Gameplay",
            "Screen7GameplayLevel2",
            "Screen8GameplayLevel3",
        ]

        try:
            if self.level_sekarang <= 0:
                self.controller.buka_misi()
            elif self.level_sekarang < len(daftar_level):
                self.controller.show_frame("Screen5PersiapanPerang", data={"level": self.level_sekarang + 1})
            else:
                self.controller.show_frame("LeaderboardView")
        except Exception as e:
            print(f"[NAVIGASI] Error pindah level: {e}")
            self.controller.show_frame("MenuPage")

    def _action_menu(self):
        putar_sfx("klik.mp3")
        self.sudah_sukses_menang = False
        try:
            self.controller.show_frame("MenuPage")
        except AttributeError:
            print("[PREVIEW] Tombol Kembali ke Menu Diklik")

    def _simpan_victory_reward_ke_db(self, controller, level, koin, kata, sisa_waktu, hp, benar, salah):
        if controller is None or not hasattr(controller, 'user_aktif') or controller.user_aktif is None:
            print("[DATABASE] Menjalankan Mode Preview: Database dilewati karena tidak ada session user aktif.")
            return

        user_id = controller.user_aktif["id"]
        db_koneksi = hubungkan_database()
        if db_koneksi is not None:
            cursor = None
            try:
                cursor = db_koneksi.cursor()
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
                cursor.execute(query_score, (user_id, level, waktu_bermain, 'VICTORY', kata, sisa_waktu, hp, benar, salah, koin))
                db_koneksi.commit()
                print(f"[DATABASE] Sukses mencatat skor VICTORY & menambah +{koin} koin untuk User ID: {user_id}!")

                from database.koneksi import buka_level_berikutnya
                buka_level_berikutnya(user_id, level)
            except Exception as e:
                print(f"[DATABASE] Error saat mencatat data kemenangan: {e}")
            finally:
                if cursor is not None:
                    cursor.close()
                db_koneksi.close()
        else:
            print("[DATABASE] Gagal terhubung ke database.")