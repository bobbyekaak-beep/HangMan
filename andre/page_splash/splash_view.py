import tkinter as tk
from tkinter import messagebox

class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Judul
        tk.Label(self, text="HANGMAN", font=("Helvetica", 32, "bold"), bg="white").pack(pady=(120, 0))
        tk.Label(self, text="WORD QUEST", font=("Helvetica", 18, "bold"), bg="white").pack()
        
        tk.Label(self, text="Satu huruf tepat, musuh sekarat.\nSatu tebakan melesat, nyawamu tamat!", 
                 font=("Arial", 10), bg="white", fg="#555").pack(pady=40)

        # Tombol tunggal untuk memaksa masuk ke halaman Login
        tk.Button(self, text="LOGIN / DAFTAR", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), 
                  width=25, height=3, bd=0, 
                  command=lambda: controller.show_frame("LoginPage")).pack(pady=20)
    def belum_tersedia(self):
        messagebox.showinfo("Info", "Bagian ini akan dikerjakan oleh teman kelompok yang lain.")

