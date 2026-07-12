import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from audio.sound_manager import putar_sfx
class SplashPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.canvas = tk.Canvas(self, width=400, height=700, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Background
        try:
            gambar = Image.open("assets/background.png")
            gambar = gambar.resize((400, 700), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(gambar)
            
            # Tempel gambar ke kanvas
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
        except FileNotFoundError:
            print("Gambar tidak ditemukan! Pastikan file gambar ada di folder yang sama dengan script python ini.")

        # Judul
        self.gif_frames = []
        self.current_frame = 0
        try:
            gif_image = Image.open("assets/byta_game.gif")

            # Ekstrak semua frame yang ada di dalam GIF
            for i in range(gif_image.n_frames):
                gif_image.seek(i)
                frame = gif_image.copy().convert("RGBA")    
                frame = frame.resize((400, 230), Image.Resampling.LANCZOS)
                self.gif_frames.append(ImageTk.PhotoImage(frame))
        except FileNotFoundError:
            print("File GIF tidak ditemukan! Pastikan file ada di folder 'assets'.")

        # Tampilkan GIF di kanvas
        if self.gif_frames:
            self.gif_canvas_id = self.canvas.create_image(200, 150, image=self.gif_frames[0])
            self._animate_gif() # Panggil fungsi untuk mulai looping animasi
        else:
            # Fallback (cadangan) teks jika GIF gagal dimuat
            self.canvas.create_text(200, 150, text="BYTA GAME", font=("Helvetica", 32, "bold"), fill="black")
        self.canvas.create_text(200, 190, text="WORD QUEST", font=("Helvetica", 18, "bold"), fill="black")
        self.canvas.create_text(200, 270, text="Satu huruf tepat, musuh sekarat.\nSatu tebakan melesat, nyawamu tamat!", 
                                font=("Arial", 10), fill="black", justify="center")

        # Tombol tunggal untuk memaksa masuk ke halaman Login
        btn_login = tk.Button(self, text="LOGIN / DAFTAR", bg="#2196F3", fg="white", font=("Arial", 12, "bold"), 
                          width=25, height=3, bd=0, 
                          command=lambda: self._aksi_login(controller))
        
        # Posisi y=550 agar tombol berada di bagian bawah layar
        self.canvas.create_window(200, 550, window=btn_login)

    def _animate_gif(self):
        # memperbarui frame GIF secara terus-menerus (looping).
        if self.gif_frames:
            # Pindah ke frame berikutnya. Jika sudah di ujung, kembali ke 0
            self.current_frame = (self.current_frame + 1) % len(self.gif_frames)
            self.canvas.itemconfig(self.gif_canvas_id, image=self.gif_frames[self.current_frame])
            self.after(50, self._animate_gif)

    def _aksi_login(self, controller):
        # Bunyikan sfx klik lalu pindah ke halaman Login
        putar_sfx("klik.mp3")
        controller.show_frame("LoginPage")