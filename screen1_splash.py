import customtkinter as ctk
from PIL import Image
import os

class Screen1Splash(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#D7E4EB")
        self.parent = parent
        
        # Kontainer Utama Mengikuti Ukuran Window (Sangat Presisi)
        self.bg_container = ctk.CTkLabel(self, text="")
        self.bg_container.pack(fill="both", expand=True)
        
        # Latar Belakang Ilustrasi Penuh Sesuai Mockup 1
        if os.path.exists("bg_main.png"):
            img_bg = ctk.CTkImage(light_image=Image.open("bg_main.png"), size=(390, 720))
            self.bg_container.configure(image=img_bg)
            
        # --- TOMBOL-TOMBOL MENUMPUK DI ATAS BACKGROUND ---
        # Tombol Mulai Permainan (Hijau Bulat Tebal)
        self.btn_mulai = ctk.CTkButton(self, text="MULAI PERMAINAN", font=("Impact", 18), 
                                       fg_color="#4CAF50", hover_color="#43A047", text_color="white",
                                       height=50, corner_radius=25, border_width=2, border_color="#2E7D32",
                                       command=lambda: parent.switch_screen("screen3_menu_utama"))
        self.btn_mulai.place(relx=0.5, rely=0.72, anchor="center", relwidth=0.75)
        
        # Tombol Login (Biru)
        self.btn_login = ctk.CTkButton(self, text="LOGIN", font=("Impact", 16), 
                                       fg_color="#1E88E5", hover_color="#1565C0", text_color="white",
                                       height=44, corner_radius=22, border_width=2, border_color="#0D47A1",
                                       command=lambda: parent.switch_screen("screen2_login"))
        self.btn_login.place(relx=0.5, rely=0.81, anchor="center", relwidth=0.75)
        
        # Tombol Pengaturan Kecil di Pojok Kanan Atas (Ikon Roda Gigi)
        self.btn_set = ctk.CTkButton(self, text="⚙️", font=("Arial", 16, "bold"), fg_color="#616161", 
                                     text_color="white", width=36, height=36, corner_radius=18,
                                     command=lambda: print("Pengaturan"))
        self.btn_set.place(x=340, y=15)