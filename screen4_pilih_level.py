import customtkinter as ctk

class Screen4PilihLevel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F4F6F7")
        self.parent = parent
        
        # Header
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=15, pady=10)
        ctk.CTkButton(hdr, text="⬅", font=("Arial", 16, "bold"), width=35, fg_color="#E0E0E0", text_color="black", command=lambda: parent.switch_screen("screen3_menu_utama")).pack(side="left")
        ctk.CTkLabel(hdr, text="PILIH LEVEL", font=("Arial", 14, "bold"), text_color="black").pack(side="left", padx=70)
        
        # Progress Card Dunia 1
        dunia_card = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E0E0E0")
        dunia_card.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(dunia_card, text="DUNIA 1 - KOTA HANCUR", font=("Arial", 11, "bold"), text_color="black").pack(anchor="w", padx=15, pady=(5,0))
        
        prog_bar = ctk.CTkProgressBar(dunia_card, progress_color="#4CAF50", fg_color="#E0E0E0", height=10)
        prog_bar.pack(fill="x", padx=15, pady=8)
        prog_bar.set(0.5) # Set setengah jalan
        
        # Grid Level 5x4
        grid_frame = ctk.CTkFrame(self, fg_color="transparent")
        grid_frame.pack(pady=10, padx=15)
        
        for i in range(15):
            lvl = i + 1
            r, c = i // 5, i % 5
            
            if lvl < parent.level_terbuka:
                bg, text_label, state = "#4CAF50", f"{lvl}\n⭐⭐⭐", "normal"
            elif lvl == parent.level_terbuka:
                bg, text_label, state = "#2196F3", f"{lvl}\n☆☆☆", "normal"
            else:
                bg, text_label, state = "#B0BEC5", "🔒", "disabled"
                
            btn = ctk.CTkButton(grid_frame, text=text_label, font=("Arial", 11, "bold"), 
                                fg_color=bg, text_color="white", width=62, height=52, corner_radius=10, state=state,
                                command=lambda: parent.switch_screen("screen5_persiapan"))
            btn.grid(row=r, column=c, padx=3, pady=4)