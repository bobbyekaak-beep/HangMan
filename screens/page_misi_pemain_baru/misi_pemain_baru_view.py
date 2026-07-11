import tkinter as tk
from tkinter import messagebox
from database.koneksi import (
    ambil_koin_user, ambil_main_time_attack, BATAS_MAIN_TIME_ATTACK,
    ambil_misi_user, klaim_misi, ambil_bonus_misi, klaim_bonus_misi, BONUS_MISI_REWARD, MISI_DEFINISI,
)
from audio.sound_manager import putar_sfx

class MisiHarianApp(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.coins = 0
        self.total_misi = 4
        self.bonus_reward = BONUS_MISI_REWARD
        self.bonus_diambil = False
        self.main_time_attack = 0
        self.misi_list = []

        self.header_frame = tk.Frame(self, bg="white")
        self.header_frame.pack(fill="x", padx=12, pady=(10, 10))
        self._buat_header()

        self.konten_frame = tk.Frame(self, bg="white")
        self.konten_frame.pack(fill="both", expand=True)

        self.daftar_frame = tk.Frame(self.konten_frame, bg="white")
        self.daftar_frame.pack(fill="x")

        self.refresh_ui()

    def _ambil_user_id(self):
        # Ambil id user aktif dari controller jika sudah login
        if self.controller is not None and hasattr(self.controller, "user_aktif") and self.controller.user_aktif is not None:
            return self.controller.user_aktif["id"]
        return None

    def populate_data(self, data=None):
        # Ambil ulang seluruh progress dari database (koin, misi, bonus, sisa kesempatan Time Attack)
        self._muat_data_dari_db()

    def on_show(self):
        # Segarkan data setiap kali halaman ini ditampilkan
        self._muat_data_dari_db()

    def _muat_data_dari_db(self):
        # Satu titik pemanggilan database supaya progress selalu sinkron dengan hasil main Time Attack
        user_id = self._ambil_user_id()
        if user_id is None:
            self.coins, self.main_time_attack = 0, 0
            self.misi_list = [{**m, "current": 0, "diambil": False} for m in MISI_DEFINISI]
            self.bonus_diambil = False
            self.refresh_ui()
            return

        self.coins = ambil_koin_user(user_id)
        self.main_time_attack = ambil_main_time_attack(user_id)
        self.misi_list = ambil_misi_user(user_id)
        self.bonus_diambil = ambil_bonus_misi(user_id)
        self.refresh_ui()

    def _buat_header(self):
        # Bangun baris judul dengan tombol kembali dan info koin
        # Gunakan tinggi tetap agar posisi place() untuk judul konsisten
        self.header_frame.configure(height=28)
        self.header_frame.pack_propagate(False)

        tk.Button(self.header_frame, text="←", font=("Arial", 13), bg="white", fg="black",
                  bd=0, activebackground="#F5F5F5", command=self.kembali).pack(side="left")

        coin_frame = tk.Frame(self.header_frame, bg="white")
        coin_frame.pack(side="right")
        self._buat_ikon_koin(coin_frame, size=16).pack(side="left", anchor="center", padx=(0, 4))
        self.coin_lbl = tk.Label(coin_frame, text=self.format_koin(), font=("Arial", 11, "bold"),
                                  bg="white", fg="#FFC107")
        self.coin_lbl.pack(side="left", anchor="center")

        # Judul selalu dikunci tepat di tengah horizontal header_frame,
        # tidak terpengaruh lebar tombol kembali maupun info koin di sisinya
        tk.Label(self.header_frame, text="TANTANGAN", font=("Arial", 13, "bold"),
                 bg="white", fg="black").place(relx=0.5, rely=0.5, anchor="center")

    def _buat_banner(self):
        # Bangun banner progress harian dan tombol masuk ke persiapan Time Attack
        selesai = self.hitung_misi_selesai()

        banner = tk.Frame(self.daftar_frame, bg="#43A047")
        banner.pack(fill="x", padx=12, pady=(14, 10))

        isi = tk.Frame(banner, bg="#43A047")
        isi.pack(fill="x", padx=12, pady=13)

        baris_atas = tk.Frame(isi, bg="#43A047")
        baris_atas.pack(fill="x", pady=(0, 4))
        tk.Label(baris_atas, text="Misi Selesai", font=("Arial", 8, "bold"),
                 fg="white", bg="#43A047").pack(side="left")
        tk.Label(baris_atas, text=f"{selesai} / {self.total_misi}", font=("Arial", 8, "bold"),
                 fg="white", bg="#43A047").pack(side="right")

        ratio = selesai / self.total_misi if self.total_misi else 0
        self._buat_progress_bar(isi, width=340, height=7, ratio=ratio,
                                 bg_color="#A5D6A7", fill_color="white").pack(fill="x")

        sisa_main = max(0, BATAS_MAIN_TIME_ATTACK - self.main_time_attack)
        habis = sisa_main <= 0
        label_sisa = f"{self.main_time_attack}/{BATAS_MAIN_TIME_ATTACK}"
        tk.Button(isi, text=f"⚔️ MULAI MAIN TIME ATTACK ({label_sisa}) ⚔️",
                  font=("Arial", 10, "bold"),
                  bg="#BDBDBD" if habis else "#FF9800", fg="white",
                  relief="flat", cursor="arrow" if habis else "hand2",
                  state="disabled" if habis else "normal",
                  command=self.mulai_time_attack).pack(fill="x", pady=(11, 0), ipady=3)

    def mulai_time_attack(self):
        # Buka halaman persiapan Time Attack, kesempatan main baru dicatat saat pemain menekan mulai di sana
        putar_sfx("klik.mp3")
        if self.main_time_attack >= BATAS_MAIN_TIME_ATTACK:
            messagebox.showinfo("Kesempatan Habis",
                                 f"Kesempatan main Time Attack sudah habis ({BATAS_MAIN_TIME_ATTACK}x/akun).")
            return
        self.controller.show_frame("Screen5PersiapanPerang", data={"level": 0})

    def _buat_daftar_misi(self):
        # Render semua kartu misi harian sesuai progress dari database
        for misi in self.misi_list:
            self._buat_kartu(
                bg="white",
                icon=misi["icon"], icon_bg=misi["icon_bg"],
                judul=misi["judul"],
                keterangan=f"{misi['current']}/{misi['target']}",
                ratio=misi["current"] / misi["target"] if misi["target"] else 0,
                reward=misi["reward"],
                selesai=misi["current"] >= misi["target"],
                diambil=misi["diambil"],
                on_ambil=lambda m=misi: self.ambil_hadiah_misi(m),
            )

    def _buat_bonus(self):
        # Render kartu hadiah bonus saat semua misi harian selesai
        selesai_semua = self.hitung_misi_selesai() >= self.total_misi
        self._buat_kartu(
            bg="#FFF8E1", border="#FFE082",
            icon="🎁", icon_bg="#F4511E",
            judul="HADIAH BONUS", judul_color="#E65100",
            keterangan="Selesaikan semua misi harian!",
            reward=self.bonus_reward,
            selesai=selesai_semua,
            diambil=self.bonus_diambil,
            on_ambil=self.ambil_bonus,
        )

    def _buat_kartu(self, icon, icon_bg, judul, keterangan, reward, selesai, diambil, on_ambil,
                     bg="white", border="#E0E0E0", judul_color="black", ratio=None):
        # Bangun satu kartu misi atau bonus dengan grid supaya kolom ikon, judul,
        # progress, reward, dan tombol AMBIL selalu presisi dan pasti tampil
        kartu = tk.Frame(self.daftar_frame, bg=bg, highlightbackground=border, highlightthickness=1)
        kartu.pack(fill="x", padx=12, pady=6)
        kartu.grid_columnconfigure(1, weight=1)

        self._buat_kotak_icon(kartu, icon, icon_bg, size=30).grid(
            row=0, column=0, rowspan=2, padx=(11, 9), pady=11, sticky="n")

        tk.Label(kartu, text=judul, font=("Arial", 9, "bold"), bg=bg, fg=judul_color,
                 anchor="w", justify="left", wraplength=195).grid(
            row=0, column=1, sticky="ew", pady=(11, 2))

        if ratio is None:
            tk.Label(kartu, text=keterangan, font=("Arial", 7), bg=bg, fg="#795548",
                     anchor="w", justify="left", wraplength=195).grid(
                row=1, column=1, sticky="ew", pady=(0, 11))
        else:
            baris_bar = tk.Frame(kartu, bg=bg)
            baris_bar.grid(row=1, column=1, sticky="ew", pady=(0, 11))
            self._buat_progress_bar(baris_bar, width=150, height=6, ratio=ratio,
                                     bg_color="#E0E0E0", fill_color="#4CAF50").pack(side="left")
            tk.Label(baris_bar, text=keterangan, font=("Arial", 7, "bold"),
                     bg=bg, fg="black").pack(side="left", padx=(10, 0))

        tk.Frame(kartu, bg="#E0E0E0", width=1).grid(row=0, column=2, rowspan=2, sticky="ns", pady=10)

        hadiah = tk.Frame(kartu, bg=bg)
        hadiah.grid(row=0, column=3, padx=(11, 12), pady=(11, 2))
        self._buat_ikon_koin(hadiah, size=15).grid(row=0, column=0, padx=(0, 3))
        tk.Label(hadiah, text=str(reward), font=("Arial", 9, "bold"), bg=bg, fg="#FFC107").grid(row=0, column=1)

        if diambil:
            warna, aksi = "#81C784", None
        elif selesai:
            warna, aksi = "#2E7D32", on_ambil
        else:
            warna, aksi = "#9E9E9E", None

        self._buat_tombol_rounded(kartu, "AMBIL", warna, "white", 65, 24,
                                   on_click=aksi, radius=5).grid(row=1, column=3, padx=(11, 12), pady=(0, 11))

    def _gambar_kotak_bulat(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        # Gambar poligon sudut membulat untuk kotak, bar, dan tombol
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def _buat_kotak_icon(self, parent, icon, bg_color, size=32):
        # Buat kotak bulat berwarna berisi emoji ikon misi
        canvas = tk.Canvas(parent, width=size, height=size, bg=parent.cget("bg"), highlightthickness=0)
        self._gambar_kotak_bulat(canvas, 1, 1, size - 1, size - 1, radius=8, fill=bg_color, outline=bg_color)
        canvas.create_text(size / 2, size / 2, text=icon, font=("Segoe UI Emoji", int(size * 0.4)), fill="white")
        return canvas

    def _buat_ikon_koin(self, parent, size=16):
        # Gambar ikon kantung uang berbentuk karung (leher sempit, badan melebar ke bawah)
        canvas = tk.Canvas(parent, width=size, height=size, bg=parent.cget("bg"), highlightthickness=0)
        cx = size / 2
        atas, bawah = size * 0.20, size * 0.96
        lebar_badan, lebar_leher = size * 0.40, size * 0.14
        titik = [
            cx - lebar_leher, atas, cx + lebar_leher, atas,
            cx + lebar_badan, size * 0.55, cx + lebar_badan * 0.82, bawah,
            cx - lebar_badan * 0.82, bawah, cx - lebar_badan, size * 0.55,
        ]
        canvas.create_polygon(titik, smooth=True, fill="#FFC107", outline="#F9A825", width=1)
        canvas.create_line(cx - lebar_leher - 1, atas, cx + lebar_leher + 1, atas, fill="#F9A825", width=2)
        canvas.create_text(cx, size * 0.62, text="$", font=("Arial", max(6, int(size * 0.42)), "bold"), fill="#8D6E00")
        return canvas

    def _buat_progress_bar(self, parent, width, height, ratio, bg_color, fill_color):
        # Gambar progress bar berbentuk pil
        ratio = max(0, min(ratio, 1))
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0)
        radius = height / 2
        self._gambar_kotak_bulat(canvas, 0, 0, width, height, radius=radius, fill=bg_color, outline=bg_color)
        if ratio > 0:
            lebar_isi = max(height, width * ratio)
            self._gambar_kotak_bulat(canvas, 0, 0, lebar_isi, height, radius=radius, fill=fill_color, outline=fill_color)
        return canvas

    def _buat_tombol_rounded(self, parent, text, bg_color, fg_color, width, height, on_click=None, radius=6):
        # Gambar tombol sudut membulat berbasis canvas
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0,
                            cursor="hand2" if on_click else "arrow")
        self._gambar_kotak_bulat(canvas, 1, 1, width - 1, height - 1, radius=radius, fill=bg_color, outline=bg_color)
        canvas.create_text(width / 2, height / 2, text=text, font=("Arial", 8, "bold"), fill=fg_color)
        if on_click:
            canvas.bind("<Button-1>", lambda e: on_click())
        return canvas

    def kembali(self):
        # Kembali ke menu utama
        putar_sfx("klik.mp3")
        self.controller.show_frame("MenuPage")

    def format_koin(self):
        # Format angka koin pakai titik ribuan
        return f"{self.coins:,}".replace(",", ".")

    def hitung_misi_selesai(self):
        # Hitung jumlah misi yang progressnya sudah penuh
        return sum(1 for m in self.misi_list if m["current"] >= m["target"])

    def ambil_hadiah_misi(self, misi):
        # Klaim hadiah satu misi ke database, sumber progresnya selalu dari sesi mode Time Attack
        putar_sfx("klik.mp3")
        user_id = self._ambil_user_id()
        if user_id is None:
            return
        if klaim_misi(user_id, misi["key"], misi["reward"]):
            messagebox.showinfo("Berhasil", f"Berhasil memperoleh {misi['reward']} koin!")
            self._muat_data_dari_db()
        else:
            messagebox.showinfo("Belum Bisa", "Misi ini belum selesai atau hadiahnya sudah pernah diambil.")

    def ambil_bonus(self):
        # Klaim hadiah bonus semua misi selesai ke database
        putar_sfx("klik.mp3")
        user_id = self._ambil_user_id()
        if user_id is None:
            return
        if klaim_bonus_misi(user_id, self.bonus_reward):
            messagebox.showinfo("Berhasil", f"Berhasil memperoleh {self.bonus_reward} koin!")
            self._muat_data_dari_db()
        else:
            messagebox.showinfo("Belum Bisa", "Selesaikan semua misi harian dahulu.")

    def refresh_ui(self):
        # Gambar ulang seluruh konten halaman
        self.coin_lbl.configure(text=self.format_koin())
        for widget in self.daftar_frame.winfo_children():
            widget.destroy()
        self._buat_banner()
        self._buat_daftar_misi()
        self._buat_bonus()
        tk.Frame(self.daftar_frame, bg="white", height=16).pack(fill="x")