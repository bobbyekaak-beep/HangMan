import tkinter as tk
from tkinter import messagebox
import mysql.connector

# konfigurasi koneksi ke database MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "db_hangman",
}


# bikin koneksi baru ke database
def get_conn():
    return mysql.connector.connect(**DB_CONFIG)


# frame halaman Misi Pemain Baru, dipakai di sistem navigasi frame-stacking
class MisiPemainBaruView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="white")
        self.controller = controller
        self.user_id = controller.user_id

        self.coins = 0
        self.total_misi = 7
        self.bonus_reward = 150
        self.bonus_diambil = False

        # daftar misi default, current & diambil akan ditimpa data dari database
        self.misi_list = [
            {"misi_key": "main_3_pertarungan", "judul": "Mainkan 3 Pertarungan", "icon": "▶", "icon_bg": "#4CAF50",
             "target": 3, "current": 0, "reward": 50, "diambil": False, "hitung_progress": True},
            {"misi_key": "tebak_10_kata", "judul": "Tebak 10 Kata dengan Benar", "icon": "🎯", "icon_bg": "#2196F3",
             "target": 10, "current": 0, "reward": 80, "diambil": False, "hitung_progress": True},
            {"misi_key": "pulihkan_hp_2x", "judul": "Pulihkan HP 2 Kali", "icon": "♥", "icon_bg": "#F44336",
             "target": 2, "current": 0, "reward": 40, "diambil": False, "hitung_progress": True},
            {"misi_key": "item_waktu_1x", "judul": "Gunakan Item Waktu 1 Kali", "icon": "⏱", "icon_bg": "#FF9800",
             "target": 1, "current": 0, "reward": 30, "diambil": False, "hitung_progress": True},
            {"misi_key": "lihat_kategori_3x", "judul": "Lihat Kategori 3 Kali", "icon": "🔍", "icon_bg": "#9C27B0",
             "target": 3, "current": 0, "reward": 60, "diambil": False, "hitung_progress": True},
            {"misi_key": "hapus_3_huruf_salah", "judul": "Hapus 3 Huruf Salah", "icon": "❌", "icon_bg": "#9E9E9E",
             "target": 1, "current": 0, "reward": 50, "diambil": False, "hitung_progress": True},
            {"misi_key": "tebak_kata_1x", "judul": "Tebak Kata 1 Kali", "icon": "🎯", "icon_bg": "#E91E63",
             "target": 1, "current": 0, "reward": 120, "diambil": False, "hitung_progress": True},
        ]

        # ambil progress misi & koin user dari database
        self.muat_progress()

        self.header_frame = tk.Frame(self, bg="white")
        self.header_frame.pack(fill="x", padx=12, pady=(10, 6))
        self._buat_header()

        self.konten_frame = tk.Frame(self, bg="white")
        self.konten_frame.pack(fill="both", expand=True)

        self.refresh_ui()

    # ambil koin user dan progress semua misi dari tabel users & user_misi
    def muat_progress(self):
        conn = get_conn()
        cur = conn.cursor(dictionary=True)

        cur.execute("SELECT coins FROM users WHERE id = %s", (self.user_id,))
        row = cur.fetchone()
        self.coins = row["coins"] if row else 0

        cur.execute(
            "SELECT misi_key, current, diambil FROM user_misi WHERE user_id = %s",
            (self.user_id,),
        )
        data_tersimpan = {r["misi_key"]: r for r in cur.fetchall()}

        # timpa data default misi_list dengan data yang sudah tersimpan di database
        for misi in self.misi_list:
            saved = data_tersimpan.get(misi["misi_key"])
            if saved:
                misi["current"] = saved["current"]
                misi["diambil"] = bool(saved["diambil"])

        # status bonus disimpan sebagai baris misi tersendiri dengan misi_key "bonus_pemain_baru"
        bonus_row = data_tersimpan.get("bonus_pemain_baru")
        self.bonus_diambil = bool(bonus_row["diambil"]) if bonus_row else False

        cur.close()
        conn.close()

    # simpan/update progress satu misi ke tabel user_misi
    def simpan_misi(self, misi_key, current, diambil):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO user_misi (user_id, misi_key, current, diambil)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE current = VALUES(current), diambil = VALUES(diambil)
            """,
            (self.user_id, misi_key, current, int(diambil)),
        )
        conn.commit()
        cur.close()
        conn.close()

    # tambah koin user di database sebagai hadiah misi
    def tambah_koin_db(self, jumlah):
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("UPDATE users SET coins = coins + %s WHERE id = %s", (jumlah, self.user_id))
        conn.commit()
        cur.close()
        conn.close()

    # bikin bagian header: tombol kembali, judul halaman, dan tampilan koin
    def _buat_header(self):
        self.header_frame.grid_columnconfigure(0, weight=1)
        self.header_frame.grid_columnconfigure(1, weight=1)
        self.header_frame.grid_columnconfigure(2, weight=1)

        tk.Button(self.header_frame, text="←", font=("Arial", 16), bg="white", fg="#333333",
                  bd=0, activebackground="white", activeforeground="#333333",
                  command=self.kembali).grid(row=0, column=0, sticky="w")

        tk.Label(self.header_frame, text="MISI PEMAIN BARU", font=("Arial", 13, "bold"),
                 bg="white", fg="black").grid(row=0, column=1)

        coin_frame = tk.Frame(self.header_frame, bg="white")
        coin_frame.grid(row=0, column=2, sticky="e")
        self._buat_ikon_koin(coin_frame, size=16).pack(side="left", padx=(0, 4))
        self.coin_lbl = tk.Label(coin_frame, text=self.format_koin(), font=("Arial", 11, "bold"),
                                  bg="white", fg="black")
        self.coin_lbl.pack(side="left")

    # bikin banner hijau yang nunjukkin jumlah misi yang sudah selesai dari total misi
    def _buat_banner(self):
        selesai = self.hitung_misi_selesai()

        banner = tk.Frame(self.konten_frame, bg="#43A047")
        banner.pack(fill="x", padx=12, pady=(8, 6))

        isi = tk.Frame(banner, bg="#43A047")
        isi.pack(fill="x", padx=12, pady=8)

        baris_atas = tk.Frame(isi, bg="#43A047")
        baris_atas.pack(fill="x", pady=(0, 3))
        tk.Label(baris_atas, text="Misi Selesai", font=("Arial", 8, "bold"),
                 fg="white", bg="#43A047").pack(side="left")
        tk.Label(baris_atas, text=f"{selesai} / {self.total_misi}", font=("Arial", 8, "bold"),
                 fg="white", bg="#43A047").pack(side="right")

        ratio = selesai / self.total_misi if self.total_misi else 0
        self._buat_progress_bar(isi, width=340, height=7, ratio=ratio,
                                 bg_color="#A5D6A7", fill_color="white").pack(fill="x")

    # render kartu untuk tiap misi di misi_list
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

    # render kartu hadiah bonus, hanya bisa diambil kalau semua misi sudah selesai
    def _buat_bonus(self):
        selesai_semua = self.hitung_misi_selesai() >= self.total_misi
        self._buat_kartu(
            bg="#FFF8E1", border="#FFE082",
            icon="🎁", icon_bg="#F4511E",
            judul="HADIAH BONUS", judul_color="#E65100",
            keterangan="Selesaikan semua misi pemain baru!",
            reward=self.bonus_reward,
            selesai=selesai_semua,
            diambil=self.bonus_diambil,
            on_ambil=self.ambil_bonus,
        )

    # bikin satu kartu (dipakai untuk kartu misi maupun kartu bonus)
    def _buat_kartu(self, icon, icon_bg, judul, keterangan, reward, selesai, diambil, on_ambil,
                     bg="white", border="#E0E0E0", judul_color="black", ratio=None):
        kartu = tk.Frame(self.konten_frame, bg=bg, highlightbackground=border, highlightthickness=1)
        kartu.pack(fill="x", padx=12, pady=4)

        isi = tk.Frame(kartu, bg=bg)
        isi.pack(fill="both", expand=True, padx=8, pady=6)

        self._buat_kotak_icon(isi, icon, icon_bg, size=28).pack(side="left")

        tengah = tk.Frame(isi, bg=bg)
        tengah.pack(side="left", fill="both", expand=True, padx=8)
        tk.Label(tengah, text=judul, font=("Arial", 8, "bold"),
                 bg=bg, fg=judul_color, anchor="w").pack(fill="x")

        # kalau ratio kosong tampilkan teks keterangan biasa, kalau ada tampilkan progress bar
        if ratio is None:
            tk.Label(tengah, text=keterangan, font=("Arial", 7), bg=bg, fg="#795548",
                     anchor="w", justify="left", wraplength=190).pack(fill="x", pady=(2, 0))
        else:
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

        # tombol AMBIL: abu-abu kalau belum selesai, hijau kalau bisa diambil, hijau tua kalau sudah diambil
        if diambil:
            warna, aksi = "#2E7D32", None
        elif selesai:
            warna, aksi = "#4CAF50", on_ambil
        else:
            warna, aksi = "#9E9E9E", None

        self._buat_tombol_rounded(kanan, "AMBIL", warna, "white", 55, 20,
                                   on_click=aksi, radius=5).pack(pady=(3, 0))

    # teks kecil di bagian bawah halaman
    def _buat_footer(self):
        tk.Label(self.konten_frame, text="Misi ini hanya berlaku sekali untuk pemain baru.",
                 font=("Arial", 7), bg="white", fg="#9E9E9E").pack(side="bottom", pady=(2, 6))

    # spasi kosong pengisi di bawah daftar
    def _buat_filler(self):
        tk.Frame(self.konten_frame, bg="white", height=10).pack(fill="x")

    # gambar bentuk kotak dengan sudut membulat di atas canvas
    def _gambar_kotak_bulat(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    # bikin kotak ikon bulat berwarna dengan emoji/simbol di tengahnya
    def _buat_kotak_icon(self, parent, icon, bg_color, size=32):
        canvas = tk.Canvas(parent, width=size, height=size, bg=parent.cget("bg"), highlightthickness=0)
        self._gambar_kotak_bulat(canvas, 1, 1, size - 1, size - 1, radius=8, fill=bg_color, outline=bg_color)
        canvas.create_text(size / 2, size / 2, text=icon, font=("Segoe UI Emoji", int(size * 0.4)), fill="white")
        return canvas

    # bikin ikon koin bulat kuning kecil
    def _buat_ikon_koin(self, parent, size=16):
        canvas = tk.Canvas(parent, width=size, height=size, bg=parent.cget("bg"), highlightthickness=0)
        canvas.create_oval(1, 1, size - 1, size - 1, fill="#FFC107", outline="#FFA000")
        canvas.create_text(size / 2, size / 2, text="$", font=("Arial", max(6, int(size * 0.4)), "bold"), fill="white")
        return canvas

    # bikin progress bar dengan sudut membulat, ratio menentukan seberapa penuh
    def _buat_progress_bar(self, parent, width, height, ratio, bg_color, fill_color):
        ratio = max(0, min(ratio, 1))
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0)
        radius = height / 2
        self._gambar_kotak_bulat(canvas, 0, 0, width, height, radius=radius, fill=bg_color, outline=bg_color)
        if ratio > 0:
            lebar_isi = max(height, width * ratio)
            self._gambar_kotak_bulat(canvas, 0, 0, lebar_isi, height, radius=radius, fill=fill_color, outline=fill_color)
        return canvas

    # bikin tombol dengan sudut membulat, bisa diklik kalau on_click diisi
    def _buat_tombol_rounded(self, parent, text, bg_color, fg_color, width, height, on_click=None, radius=6):
        canvas = tk.Canvas(parent, width=width, height=height, bg=parent.cget("bg"), highlightthickness=0,
                            cursor="hand2" if on_click else "arrow")
        self._gambar_kotak_bulat(canvas, 1, 1, width - 1, height - 1, radius=radius, fill=bg_color, outline=bg_color)
        canvas.create_text(width / 2, height / 2, text=text, font=("Arial", 7, "bold"), fill=fg_color)
        if on_click:
            canvas.bind("<Button-1>", lambda e: on_click())
        return canvas

    # kembali ke frame sebelumnya lewat controller
    def kembali(self):
        self.controller.go_back()

    # format angka koin jadi string dengan pemisah ribuan pakai titik
    def format_koin(self):
        return f"{self.coins:,}".replace(",", ".")

    # hitung berapa misi yang sudah mencapai target
    def hitung_misi_selesai(self):
        return sum(1 for m in self.misi_list if m["hitung_progress"] and m["current"] >= m["target"])

    # proses ambil hadiah satu misi: tandai diambil, simpan ke DB, tambah koin, render ulang
    def ambil_hadiah_misi(self, misi):
        if misi["diambil"] or misi["current"] < misi["target"]:
            return
        misi["diambil"] = True
        self.simpan_misi(misi["misi_key"], misi["current"], True)
        self.tambah_koin_db(misi["reward"])
        self.coins += misi["reward"]
        self.refresh_ui()
        messagebox.showinfo("Berhasil", f"Berhasil memperoleh {misi['reward']} koin!")

    # proses ambil hadiah bonus, hanya bisa kalau semua misi sudah selesai
    def ambil_bonus(self):
        if self.bonus_diambil or self.hitung_misi_selesai() < self.total_misi:
            return
        self.bonus_diambil = True
        self.simpan_misi("bonus_pemain_baru", 0, True)
        self.tambah_koin_db(self.bonus_reward)
        self.coins += self.bonus_reward
        self.refresh_ui()
        messagebox.showinfo("Berhasil", f"Berhasil memperoleh {self.bonus_reward} koin!")

    # render ulang seluruh isi halaman: koin, banner, daftar misi, kartu bonus, footer
    def refresh_ui(self):
        self.coin_lbl.configure(text=self.format_koin())
        for widget in self.konten_frame.winfo_children():
            widget.destroy()
        self._buat_banner()
        self._buat_daftar_misi()
        self._buat_bonus()
        self._buat_filler()
        self._buat_footer()