import tkinter as tk
from tkinter import messagebox

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Header
        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", padx=20, pady=20)
        
        tk.Label(top_bar, text="👤 Player (Aktif)", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        tk.Label(top_bar, text="💰 1.250", font=("Arial", 12, "bold"), fg="#FF9800", bg="white").pack(side="right")

        # Kumpulan Tombol Menu yang sudah dipindah dari depan
        tk.Button(self, text="MULAI PERMAINAN", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=8)
                  
        tk.Button(self, text="PILIH LEVEL", bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=8)
                  
        tk.Button(self, text="TOKO", bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=8)
                  
        tk.Button(self, text="ITEM SAYA", bg="#757575", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=8)
                  
        tk.Button(self, text="PAPAN PERINGKAT", bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=8)

        # Tombol Keluar
        tk.Button(self, text="Keluar Akun (Logout)", fg="red", bg="white", bd=0, font=("Arial", 10),
                  command=self.proses_keluar).pack(side="bottom", pady=30)
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
        self.controller.user_aktif = None
        self.controller.show_frame("SplashPage")

    def belum_tersedia(self):
        messagebox.showinfo("Info", "Bagian ini akan dikerjakan oleh teman kelompok yang lain.")