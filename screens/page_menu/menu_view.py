import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from database.koneksi import ambil_koin_user, ambil_highest_level, MAX_LEVEL
from audio.sound_manager import putar_sfx, normalkan_musik_latar

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        try:
            gambar = Image.open("assets/background.png") 
            gambar = gambar.resize((400, 700), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(gambar)
                    
            bg_label = tk.Label(self, image=self.bg_image)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Gambar background login tidak ditemukan!")

        # Header
        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", ipady=10, pady=(0,20))
        
        self.label_pemain = tk.Label(top_bar, text="👤 Player", font=("Arial", 12, "bold"), bg="white")
        self.label_pemain.pack(side="left", padx=20)

        frame_koin = tk.Frame(top_bar, bg="white")
        frame_koin.pack(side="right", padx=20)

        self.label_koin = tk.Label(frame_koin, text="💰 0", font=("Arial", 12, "bold"), fg="#FF9800", bg="white")
        self.label_koin.pack(side="left", padx=(0, 5))

        tk.Button(frame_koin, text=" ➕ ", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), bd=0,
                  command=lambda: self._pindah(controller, "TokoView")).pack(side="left")
        
        # Kumpulan Tombol Menu yang sudah dipindah dari depan
        tk.Button(self, text="MULAI PERMAINAN", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self._mulai_permainan).pack(pady=8)
                  
        tk.Button(self, text="PILIH LEVEL", bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=lambda: self._pindah(controller, "PilihLevelApp")).pack(pady=8)
                  
        tk.Button(self, text="TOKO", bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=lambda: self._pindah(controller, "TokoView")).pack(pady=8)
                  
        tk.Button(self, text="TANTANGAN", bg="#757575", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=lambda: self._pindah(controller, "MisiHarianApp")).pack(pady=8)
                  
        tk.Button(self, text="PAPAN PERINGKAT", bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=lambda: self._pindah(controller, "LeaderboardView")).pack(pady=8)

        # Tombol Keluar
        tk.Button(self, text="KELUAR (LOGOUT)", bg="#F44336", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, 
                  command=lambda: self.proses_keluar()).pack(side="bottom", pady=30)

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        # Pastikan musik latar selalu normal setiap kali Menu Utama tampil
        normalkan_musik_latar()
        # Ambil ulang koin terbaru dari database setiap halaman ini tampil,
        # supaya tidak menampilkan angka lama dari saat login.
        if self.controller.user_aktif:
            koin_terbaru = ambil_koin_user(self.controller.user_aktif["id"])
            self.controller.user_aktif["coins"] = koin_terbaru
        self.perbarui_tampilan()

    def perbarui_tampilan(self):
        # Fungsi untuk menarik data dari memori lalu mencetaknya ke layar
        if self.controller.user_aktif:
            nama = self.controller.user_aktif["username"]
            koin = self.controller.user_aktif["coins"]
            
            self.label_pemain.config(text=f"👤 {nama}")
            # Format pemisah ribuan agar 1250 tampil sebagai 1.250
            self.label_koin.config(text=f"💰 {koin:,}".replace(',', '.'))

    def _pindah(self, controller, page_name):
        # Bunyikan sfx klik lalu pindah ke halaman tujuan
        putar_sfx("klik.mp3")
        controller.show_frame(page_name)

    def _mulai_permainan(self):
        """Loncat ke Persiapan pada level lanjutan sesuai progres user di database"""
        putar_sfx("klik.mp3")
        if self.controller.user_aktif is None:
            self.cek_akses("Mulai Permainan")
            return
        level = min(ambil_highest_level(self.controller.user_aktif["id"]), MAX_LEVEL)
        self.controller.show_frame("Screen5PersiapanPerang", data={"level": level})

    def cek_akses(self, nama_fitur):
        # Kalau ingatan aplikasi kosong (belum login)
        if self.controller.user_aktif is None:
            messagebox.showwarning("Ditahan", "Kamu harus Login terlebih dahulu agar progres tercatat!")
            self.controller.show_frame("LoginPage") # Lempar paksa ke halaman login
        else:
            # Kalau sudah login, tombol bisa ditekan
            messagebox.showinfo("Info", f"Fitur {nama_fitur} akan dikerjakan oleh teman kelompok yang lain.")

    def proses_keluar(self):
        # Hapus nama dari ingatan saat menekan tombol keluar
        putar_sfx("klik.mp3")
        self.controller.user_aktif = None
        self.controller.show_frame("SplashPage")

    def belum_tersedia(self):
        messagebox.showinfo("Info", "Bagian ini akan dikerjakan oleh teman kelompok yang lain.")