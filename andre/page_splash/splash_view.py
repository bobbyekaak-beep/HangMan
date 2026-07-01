import tkinter as tk
from tkinter import messagebox

class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Judul
        tk.Label(self, text="HANGMAN", font=("Helvetica", 32, "bold"), bg="white").pack(pady=(80, 0))
        tk.Label(self, text="WORD QUEST", font=("Helvetica", 18, "bold"), bg="white").pack()
        
        tk.Label(self, text="Satu huruf tepat, musuh sekarat.\nSatu tebakan melesat, nyawamu tamat!", 
                 font=("Arial", 10), bg="white", fg="#555").pack(pady=20)

        # Tombol-tombol utama
        tk.Button(self, text="MULAI PERMAINAN", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), width=25, height=2, bd=0, 
                  command=lambda: controller.show_frame("MenuPage")).pack(pady=10)
                  
        tk.Button(self, text="LOGIN / DAFTAR", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), width=25, height=2, bd=0, 
                  command=lambda: controller.show_frame("LoginPage")).pack(pady=10)
                  
        tk.Button(self, text="TOKO", bg="#FF9800", fg="white", font=("Arial", 11, "bold"), width=25, height=2, bd=0, 
                  command=self.belum_tersedia).pack(pady=10)
                  
        tk.Button(self, text="ITEM SAYA", bg="#757575", fg="white", font=("Arial", 11, "bold"), width=25, height=2, bd=0, 
                  command=self.belum_tersedia).pack(pady=10)

    def belum_tersedia(self):
        messagebox.showinfo("Info", "Bagian ini akan dikerjakan oleh teman kelompok yang lain.")

