import tkinter as tk
from tkinter import messagebox
from database.koneksi import hubungkan_database

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        tk.Label(self, text="LOGIN ATAU DAFTAR", font=("Arial", 16, "bold"), bg="white").pack(pady=(40, 20))

        # Form Input
        tk.Label(self, text="Username", bg="white", font=("Arial", 10)).pack(anchor="w", padx=40)
        self.entry_user = tk.Entry(self, font=("Arial", 12), bg="#F9F9F9", relief="solid", bd=1)
        self.entry_user.pack(fill="x", padx=40, pady=(0, 15), ipady=6)
        
        tk.Label(self, text="Kata Sandi", bg="white", font=("Arial", 10)).pack(anchor="w", padx=40)

        frame_pass = tk.Frame(self, bg="white")
        frame_pass.pack(fill="x", padx=40, pady=(0, 25))

        self.entry_pass = tk.Entry(frame_pass, font=("Arial", 12), bg="#F9F9F9", show="*", relief="solid", bd=1)
        self.entry_pass.pack(side="left", fill="x", expand=True, ipady=6)

        # Tombol Mata
        btn_lihat = tk.Button(frame_pass, text="👁", font=("Arial", 12), bg="#E0E0E0", bd=0, cursor="hand2")
        btn_lihat.pack(side="right", padx=(5, 0), ipadx=10, fill="y")
        
        # Mengikat tombol dengan aksi tekan (ButtonPress-1) dan lepas (ButtonRelease-1)
        btn_lihat.bind("<ButtonPress-1>", self.tampilkan_password)
        btn_lihat.bind("<ButtonRelease-1>", self.sembunyikan_password)

        # Tombol Aksi
        tk.Button(self, text="LOGIN", bg="#4CAF50", fg="white", font=("Arial", 12, "bold"), height=2, bd=0,
                  command=self.proses_login).pack(fill="x", padx=40, pady=5, ipady=5)
                  
        tk.Button(self, text="DAFTAR AKUN BARU", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), height=2, bd=0,
                  command=self.proses_daftar).pack(fill="x", padx=40, pady=5, ipady=5)

        # Tombol Kembali
        tk.Button(self, text="← Kembali ke Awal", bg="white", bd=0, fg="#888",
                  command=lambda: controller.show_frame("SplashPage")).pack(pady=30)

    def tampilkan_password(self, event):
        # Menghilangkan bintang (show="")
        self.entry_pass.config(show="")

    def sembunyikan_password(self, event):
        # Mengembalikan bintang (show="*")
        self.entry_pass.config(show="*")
        
    def proses_daftar(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        
        if not user or not password:
            messagebox.showwarning("Peringatan", "Username dan Password tidak boleh kosong!")
            return
            
        db = hubungkan_database()
        if db:
            kursor = db.cursor()
            try:
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                kursor.execute(sql, (user, password))
                db.commit()
                messagebox.showinfo("Sukses", "Akun berhasil dibuat! Silakan klik Login.")
            except:
                messagebox.showerror("Error", "Gagal mendaftar. Mungkin username sudah ada.")
            finally:
                db.close()
        else:
            messagebox.showerror("Error", "Database XAMPP belum menyala!")

    def proses_login(self):
        user = self.entry_user.get()
        password = self.entry_pass.get()
        
        db = hubungkan_database()
        if db:
            kursor = db.cursor()
            sql = "SELECT * FROM users WHERE username=%s AND password=%s"
            kursor.execute(sql, (user, password))
            hasil = kursor.fetchone()
            
            if hasil:
                messagebox.showinfo("Sukses", f"Selamat datang, {user}!")
                self.controller.user_aktif = user
                # Kosongkan kolom isian setelah berhasil masuk
                self.entry_user.delete(0, tk.END)
                self.entry_pass.delete(0, tk.END)
                self.controller.show_frame("MenuPage")
            else:
                messagebox.showerror("Gagal", "Username atau Password salah!")
            db.close()