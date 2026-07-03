import tkinter as tk
from tkinter import messagebox

class MenuPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Header
        top_bar = tk.Frame(self, bg="white")
        top_bar.pack(fill="x", padx=20, pady=30)
        
        tk.Label(top_bar, text="👤 Player (Aktif)", font=("Arial", 12, "bold"), bg="white").pack(side="left")
        tk.Label(top_bar, text="💰 1.250", font=("Arial", 12, "bold"), fg="#FF9800", bg="white").pack(side="right")

        # Tombol Menu
        tk.Button(self, text="MULAI PERMAINAN", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=10)
                  
        tk.Button(self, text="PILIH LEVEL", bg="#2196F3", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=10)
                  
        tk.Button(self, text="PAPAN PERINGKAT", bg="#FF9800", fg="white", font=("Arial", 12, "bold"),
                  width=25, height=2, bd=0, command=self.belum_tersedia).pack(pady=10)

        # Tombol Keluar
        tk.Button(self, text="Keluar Akun (Logout)", fg="red", bg="white", bd=0, font=("Arial", 10),
                  command=lambda: controller.show_frame("SplashPage")).pack(side="bottom", pady=40)

    def belum_tersedia(self):
        messagebox.showinfo("Info", "Bagian ini akan dikerjakan oleh teman kelompok yang lain.")