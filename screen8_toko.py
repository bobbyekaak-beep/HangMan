import customtkinter as ctk

class Screen8Toko(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.parent = parent
        
        ctk.CTkLabel(self, text="TOKO & ITEM SAYA", font=("Arial", 14, "bold"), text_color="black").pack(pady=10)
        
        # Koin Display
        k_box = ctk.CTkFrame(self, fg_color="#FFF8E1", height=30, corner_radius=15)
        k_box.pack(pady=5)
        ctk.CTkLabel(k_box, text=f"🪙 {parent.koin:,}", font=("Arial", 12, "bold"), text_color="#E65100", padx=15).pack()
        
        # Grid Katalog Item Toko (2 Kolom sesuai gambar)
        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(expand=True, fill="both", padx=20, pady=10)
        
        pasar = [("💡 Petunjuk", 50), ("🕒 Waktu", 70), ("❤️ Pulihkan", 60), ("🎯 Tebak Kata", 120)]
        
        for idx, (name, harga) in enumerate(pasar):
            r, c = idx // 2, idx % 2
            box = ctk.CTkFrame(grid, fg_color="#FAFAFA", border_width=1, border_color="#E0E0E0", corner_radius=10)
            box.grid(row=r, column=c, padx=6, pady=6, sticky="nsew")
            
            ctk.CTkLabel(box, text=name, font=("Arial", 12, "bold"), text_color="black").pack(pady=(10,2))
            
            btn = ctk.CTkButton(box, text=f"🪙 {harga}", font=("Arial", 11, "bold"), fg_color="#FFF3E0", text_color="#E65100", height=28, width=80, corner_radius=6,
                                    command=lambda n=name, h=harga: self.beli(n, h))
            btn.pack(pady=(0,10))
            
        grid.columnconfigure((0,1), weight=1)
        grid.rowconfigure((0,1), weight=1)
        
        # Paket Hemat Card
        pkt = ctk.CTkFrame(self, fg_color="#FFF9C4", corner_radius=10, border_width=1, border_color="#FFF176")
        pkt.pack(fill="x", padx=25, pady=10)
        ctk.CTkLabel(pkt, text="🔥 PAKET HEMAT COMBAT: 🪙 150", font=("Arial", 11, "bold"), text_color="black").pack(pady=8)
        
        ctk.CTkButton(self, text="⬅ KEMBALI KE MENU", font=("Arial", 12, "bold"), fg_color="#757575", text_color="white", height=38, corner_radius=10, command=lambda: parent.switch_screen("screen3_menu_utama")).pack(pady=15)

    def beli(self, item, cost):
        if self.parent.koin >= cost:
            self.parent.koin -= cost
            self.parent.switch_screen("screen8_toko")