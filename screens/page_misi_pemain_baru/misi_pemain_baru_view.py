import tkinter as tk
from tkinter import messagebox
from database.koneksi import ambil_koin_user, tambah_koin_user

class MisiHarianApp(tk.Frame):
    def __init__(self, parent, controller): 
        super().__init__(parent, bg="white") 
        self.controller = controller

        self.coins = 0
        self.total_misi = 7        # jumlah misi utama yang dihitung untuk progress harian & bonus
        self.bonus_reward = 150
        self.bonus_diambil = False

        # Semua misi mulai dari progress 0 (direset setiap hari)
        # hitung_progress=True -> ikut dihitung ke total 6 misi utama di banner & bonus
        self.misi_list = [
            {"judul": "Mainkan 3 Pertarungan", "icon": "▶", "icon_bg": "#4CAF50",
             "target": 3, "current": 0, "reward": 50, "diambil": False, "hitung_progress": True},
            {"judul": "Tebak 10 Kata dengan Benar", "icon": "🎯", "icon_bg": "#2196F3",
             "target": 10, "current": 0, "reward": 80, "diambil": False, "hitung_progress": True},
            {"judul": "Pulihkan HP 2 Kali", "icon": "♥", "icon_bg": "#F44336",
             "target": 2, "current": 0, "reward": 40, "diambil": False, "hitung_progress": True},
            {"judul": "Gunakan Item Waktu 1 Kali", "icon": "⏱", "icon_bg": "#FF9800",
             "target": 1, "current": 0, "reward": 30, "diambil": False, "hitung_progress": True},
            {"judul": "Lihat Kategori 3 Kali", "icon": "🔍", "icon_bg": "#9C27B0",
             "target": 3, "current": 0, "reward": 60, "diambil": False, "hitung_progress": True},
            {"judul": "Hapus 3 Huruf Salah", "icon": "❌", "icon_bg": "#9E9E9E",
             "target": 1, "current": 0, "reward": 50, "diambil": False, "hitung_progress": True},
            {"judul": "Tebak Kata 1 Kali", "icon": "🎯", "icon_bg": "#E91E63",
             "target": 1, "current": 0, "reward": 120, "diambil": False, "hitung_progress": True},
        ]

        self.header_frame = tk.Frame(self, bg="white")
        self.header_frame.pack(fill="x", padx=12, pady=(10, 6))
        self._buat_header()

        self.konten_frame = tk.Frame(self, bg="white")
        self.konten_frame.pack(fill="both", expand=True)

        self.refresh_ui()

    def populate_data(self, data=None):
        user_id = self.controller.user_aktif["id"]
        self.coins = ambil_koin_user(user_id) 
        self.coin_lbl.configure(text=self.format_koin())
        self.refresh_ui()

    # HEADER 
    def _buat_header(self):
        # Pakai grid 3 kolom (kiri - tengah - kanan) supaya judul presisi di tengah
        # walaupun lebar tombol kembali dan frame koin berbeda
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

        tk.Button(self.header_frame, text="⬅", font=("Arial", 12, "bold"), bg="white", fg="black",
                  bd=0, activebackground="#F5F5F5", command=self.kembali).grid(row=0, column=0, sticky="w")

        tk.Label(self.header_frame, text="MISI HARIAN", font=("Arial", 13, "bold"),
                 bg="white", fg="black").grid(row=0, column=1)

        coin_frame = tk.Frame(self.header_frame, bg="white")
        coin_frame.grid(row=0, column=2, sticky="e")
        self._buat_ikon_koin(coin_frame, size=16).pack(side="left", padx=(0, 4))
        self.coin_lbl = tk.Label(coin_frame, text=self.format_koin(), font=("Arial", 11, "bold"),
                                  bg="white", fg="black")
        self.coin_lbl.pack(side="left")

    # BANNER PROGRESS HARIAN

    def _buat_banner(self):
        selesai = self.hitung_misi_selesai()

        banner = tk.Frame(self.konten_frame, bg="#43A047")
        banner.pack(fill="x", padx=12, pady=(8, 6))

        isi = tk.Frame(banner, bg="#43A047")
        isi.pack(fill="x", padx=12, pady=8)

        baris_atas = tk.Frame(isi, bg="#43A047")
        baris_atas.pack(fill="x", pady=(0, 3))
        tk.Label(baris_atas, text="Misi Selesai Hari Ini", font=("Arial", 8, "bold"),
                 fg="white", bg="#43A047").pack(side="left")
        tk.Label(baris_atas, text=f"{selesai} / {self.total_misi}", font=("Arial", 8, "bold"),
                 fg="white", bg="#43A047").pack(side="right")

        ratio = selesai / self.total_misi if self.total_misi else 0
        self._buat_progress_bar(isi, width=340, height=7, ratio=ratio,
                                 bg_color="#A5D6A7", fill_color="white").pack(fill="x")

        # Tombol Mulai Main Time Attack
        tk.Button(isi, text="⚔️ MULAI MAIN TIME ATTACK ⚔️", font=("Arial", 10, "bold"),
                  bg="#FF9800", fg="white", relief="flat", cursor="hand2",
                  command=lambda: self.controller.show_frame("ScreenDailyMission")).pack(fill="x", pady=(10, 0))

    # KARTU MISI & KARTU BONUS 

    def _buat_daftar_misi(self):
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
        """Satu kartu (dipakai untuk misi biasa maupun kartu bonus) supaya ukuran & gaya selalu sama."""
        kartu = tk.Frame(self.konten_frame, bg=bg, highlightbackground=border, highlightthickness=1)
        kartu.pack(fill="x", padx=12, pady=4)

        isi = tk.Frame(kartu, bg=bg)
        isi.pack(fill="both", expand=True, padx=8, pady=6)

        self._buat_kotak_icon(isi, icon, icon_bg, size=28).pack(side="left")

        tengah = tk.Frame(isi, bg=bg)
        tengah.pack(side="left", fill="both", expand=True, padx=8)
        tk.Label(tengah, text=judul, font=("Arial", 8, "bold"),
                 bg=bg, fg=judul_color, anchor="w").pack(fill="x")

        if ratio is None:
            # Kartu bonus: tampilkan teks keterangan biasa, dibungkus supaya tidak terpotong
            tk.Label(tengah, text=keterangan, font=("Arial", 7), bg=bg, fg="#795548",
                     anchor="w", justify="left", wraplength=190).pack(fill="x", pady=(2, 0))
        else:
            # Kartu misi: tampilkan progress bar + angka current/target
            baris_bar = tk.Frame(tengah, bg=bg)
            baris_bar.pack(fill="x", pady=(2, 0))
            self._buat_progress_bar(baris_bar, width=130, height=5, ratio=ratio,
                                     bg_color="#E0E0E0", fill_color="#4CAF50").pack(side="left")
            tk.Label(baris_bar, text=keterangan, font=("Arial", 7, "bold"),
                     bg=bg, fg="black").pack(side="right")

        tk.Frame(isi, bg="#E0E0E0", width=1).pack(side="left", fill="y", padx=6)

        kanan = tk.Frame(isi, bg=bg)
        kanan.pack(side="left")

        hadiah = tk.Frame(kanan, bg=bg)
        hadiah.pack()
        self._buat_ikon_koin(hadiah, size=12).pack(side="left", padx=(0, 3))
        tk.Label(hadiah, text=str(reward), font=("Arial", 9, "bold"), bg=bg, fg="black").pack(side="left")

        # Tombol AMBIL: abu-abu jika belum selesai / sudah diambil, hijau jika selesai dan belum diambil
        if diambil:
            warna, aksi = "#BDBDBD", None
        elif selesai:
            warna, aksi = "#4CAF50", on_ambil
        else:
            warna, aksi = "#9E9E9E", None

        self._buat_tombol_rounded(kanan, "AMBIL", warna, "white", 55, 20,
                                   on_click=aksi, radius=5).pack(pady=(3, 0))

    def _buat_footer(self):
        tk.Label(self.konten_frame, text="Misi diperbarui setiap hari pukul 00:00.",
                 font=("Arial", 7), bg="white", fg="#9E9E9E").pack(side="bottom", pady=(2, 6))

    def _buat_filler(self):
        # Pengisi ruang kecil di bawah kartu bonus, secukupnya saja agar tidak berlebihan
        tk.Frame(self.konten_frame, bg="white", height=10).pack(fill="x")


    def _gambar_kotak_bulat(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    def _buat_kotak_icon(self, parent, icon, bg_color, size=32):
        canvas = tk.Canvas(parent, width=size, height=size, bg=parent.cget("bg"), highlightthickness=0)
        self._gambar_kotak_bulat(canvas, 1, 1, size - 1, size - 1, radius=8, fill=bg_color, outline=bg_color)
        canvas.create_text(size / 2, size / 2, text=icon, font=("Segoe UI Emoji", int(size * 0.4)), fill="white")
        return canvas

    def _buat_ikon_koin(self, parent, size=16):
        canvas = tk.Canvas(parent, width=size, height=size, bg=parent.cget("bg"), highlightthickness=0)
        canvas.create_oval(1, 1, size - 1, size - 1, fill="#FFC107", outline="#FFA000")
        canvas.create_text(size / 2, size / 2, text="$", font=("Arial", max(6, int(size * 0.4)), "bold"), fill="white")
        return canvas

    def _buat_progress_bar(self, parent, width, height, ratio, bg_color, fill_color):
        ratio = max(0, min(ratio, 1))
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0)
        radius = height / 2
        self._gambar_kotak_bulat(canvas, 0, 0, width, height, radius=radius, fill=bg_color, outline=bg_color)
        if ratio > 0:
            lebar_isi = max(height, width * ratio)
            self._gambar_kotak_bulat(canvas, 0, 0, lebar_isi, height, radius=radius, fill=fill_color, outline=fill_color)
        return canvas

    def _buat_tombol_rounded(self, parent, text, bg_color, fg_color, width, height, on_click=None, radius=6):
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0,
                            cursor="hand2" if on_click else "arrow")
        self._gambar_kotak_bulat(canvas, 1, 1, width - 1, height - 1, radius=radius, fill=bg_color, outline=bg_color)
        canvas.create_text(width / 2, height / 2, text=text, font=("Arial", 7, "bold"), fill=fg_color)
        if on_click:
            canvas.bind("<Button-1>", lambda e: on_click())
        return canvas


    def kembali(self):
        self.controller.show_frame("MenuPage")

    def format_koin(self):
        return f"{self.coins:,}".replace(",", ".")

    def hitung_misi_selesai(self):
        return sum(1 for m in self.misi_list if m["hitung_progress"] and m["current"] >= m["target"])

    def ambil_hadiah_misi(self, misi):
        misi["diambil"] = True
        self.coins += misi["reward"]
        self.refresh_ui()
        messagebox.showinfo("Berhasil", f"Berhasil memperoleh {misi['reward']} koin!")

    def ambil_bonus(self):
        self.bonus_diambil = True
        self.coins += self.bonus_reward
        self.refresh_ui()
        messagebox.showinfo("Berhasil", f"Berhasil memperoleh {self.bonus_reward} koin!")

    def refresh_ui(self):
        self.coin_lbl.configure(text=self.format_koin())
        for widget in self.konten_frame.winfo_children():
            widget.destroy()
        self._buat_banner()
        self._buat_daftar_misi()
        self._buat_bonus()
        self._buat_filler()
        self._buat_footer()

