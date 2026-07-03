import customtkinter as ctk

class Screen5Persiapan(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.parent = parent
        
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.pack(fill="x", padx=15, pady=15)
        ctk.CTkButton(hdr, text="⬅", font=("Arial", 14, "bold"), width=35, fg_color="#F5F5F5", text_color="black", command=lambda: parent.switch_screen("screen4_pilih_level")).pack(side="left")
        ctk.CTkLabel(hdr, text="ROOM PREPARATION", font=("Arial", 13, "bold"), text_color="#37474F").pack(side="left", padx=45)
        
        # PERBAIKAN: Menghapus padding=15
        cat_box = ctk.CTkFrame(self, fg_color="#E8F5E9", corner_radius=14, border_width=1, border_color="#C8E6C9")
        cat_box.pack(fill="x", padx=25, pady=10)
        
        ctk.CTkLabel(cat_box, text="TARGET KATEGORI KATA", font=("Arial", 10, "bold"), text_color="#4CAF50").pack(pady=(10, 2))
        ctk.CTkLabel(cat_box, text="HEWAN BUAS", font=("Arial", 20, "bold"), text_color="#1B5E20").pack(pady=(0, 10))
        
        # Info Spek Musuh
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        stats = [("HP GODZILLA", "120 HP", "#D32F2F"), ("TIMER LIMIT", "01:30s", "black"), ("KESULITAN", "STAGE 5", "#E65100")]
        for i, (title, val, color) in enumerate(stats):
            # PERBAIKAN: Menghapus padding=10
            box = ctk.CTkFrame(stats_frame, fg_color="#F5F5F5", corner_radius=10)
            box.grid(row=0, column=i, sticky="nsew", padx=3)
            ctk.CTkLabel(box, text=title, font=("Arial", 8, "bold"), text_color="gray").pack(pady=(5, 2))
            ctk.CTkLabel(box, text=val, font=("Arial", 12, "bold"), text_color=color).pack(pady=(0, 5))
        stats_frame.columnconfigure((0,1,2), weight=1)
        
        # Sinkronisasi Manfaat Item Real-time
        ctk.CTkLabel(self, text="STOK ITEM PERTEMPURAN ANDA", font=("Arial", 11, "bold"), text_color="#546E7A").pack(pady=(15,5))
        items_frame = ctk.CTkFrame(self, fg_color="transparent")
        items_frame.pack(fill="x", padx=20)
        
        for i, (item_name, qty) in enumerate(parent.inventory.items()):
            # PERBAIKAN: Menghapus padding=10
            box = ctk.CTkFrame(items_frame, fg_color="white", border_width=1, border_color="#CFD8DC", corner_radius=10)
            box.grid(row=0, column=i, sticky="nsew", padx=4)
            ctk.CTkLabel(box, text=item_name.replace(" ", "\n"), font=("Arial", 9, "bold"), justify="center", text_color="black").pack(pady=(8, 2))
            ctk.CTkLabel(box, text=f"Milik: {qty}x", font=("Arial", 10, "bold"), text_color="#D32F2F").pack(pady=(0, 8))
        items_frame.columnconfigure((0,1,2), weight=1)
        
        ctk.CTkButton(self, text="⚔️ MASUK KE ARENA JUANG", font=("Arial", 14, "bold"), fg_color="#4CAF50", hover_color="#388E3C", text_color="white", height=48, corner_radius=24,
                      command=lambda: parent.switch_screen("screen6_gameplay")).pack(fill="x", padx=25, side="bottom", pady=20)