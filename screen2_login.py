import customtkinter as ctk

class Screen2Login(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.parent = parent
        
        ctk.CTkLabel(self, text="AUTHENTICATION GATEWAY", font=("Arial", 10, "bold"), text_color="gray").pack(pady=(15,5))
        
        # Tab Sistem (Variasi visual agar tidak kaku)
        tab_frame = ctk.CTkFrame(self, fg_color="#F5F5F5", height=40, corner_radius=10)
        tab_frame.pack(pady=15, fill="x", padx=35)
        tab_frame.pack_propagate(False)
        ctk.CTkButton(tab_frame, text="LOGIN ACC", font=("Arial", 11, "bold"), fg_color="#4CAF50", text_color="white", corner_radius=8).pack(side="left", expand=True, fill="both", padx=2, pady=2)
        ctk.CTkButton(tab_frame, text="REGISTRASI", font=("Arial", 11, "bold"), fg_color="transparent", text_color="black", hover_color="#E0E0E0", corner_radius=8).pack(side="right", expand=True, fill="both", padx=2, pady=2)
        
        # Form Isian Input
        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(pady=10, fill="x", padx=35)
        
        ctk.CTkLabel(form_frame, text="👤 ID USER / EMAIL", font=("Arial", 11, "bold"), text_color="#37474F", anchor="w").pack(fill="x", pady=(5,2))
        self.ent_user = ctk.CTkEntry(form_frame, placeholder_text="Masukkan username...", font=("Arial", 12), fg_color="#F5F5F5", border_width=1, border_color="#CFD8DC", height=38, corner_radius=8)
        self.ent_user.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(form_frame, text="🔒 KATA SANDI SECURE", font=("Arial", 11, "bold"), text_color="#37474F", anchor="w").pack(fill="x", pady=(5,2))
        self.ent_pass = ctk.CTkEntry(form_frame, placeholder_text="••••••••", font=("Arial", 12), fg_color="#F5F5F5", border_width=1, border_color="#CFD8DC", show="*", height=38, corner_radius=8)
        self.ent_pass.pack(fill="x")
        
        self.lbl_error = ctk.CTkLabel(self, text="", font=("Arial", 11), text_color="red")
        self.lbl_error.pack(pady=5)
        
        ctk.CTkButton(self, text="MASUK SEKARANG 🔓", font=("Arial", 13, "bold"), fg_color="#4CAF50", hover_color="#43A047", text_color="white", height=45, corner_radius=22,
                      command=self.proses_login).pack(pady=10, fill="x", padx=35)
                      
        ctk.CTkButton(self, text="⬅ KEMBALI", font=("Arial", 11, "bold"), fg_color="#78909C", hover_color="#607D8B", text_color="white", height=35, corner_radius=8,
                      command=lambda: parent.switch_screen("screen1_splash")).pack(pady=5)

    def proses_login(self):
        user = self.ent_user.get()
        pas = self.ent_pass.get()
        if user.strip() != "" and pas.strip() != "":
            self.parent.player_name = user  # Simpan nama user global
            self.parent.switch_screen("screen3_menu_utama")
        else:
            self.lbl_error.configure(text="⚠️ Form login tidak boleh kosong!")