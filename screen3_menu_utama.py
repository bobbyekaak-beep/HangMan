import customtkinter as ctk

class Screen3MenuUtama(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#E4EDF1") 
        self.parent = parent
        
        # --- TOP USER BAR ---
        u_bar = ctk.CTkFrame(self, fg_color="#FFFFFF", height=54, corner_radius=0, border_width=1, border_color="#CFD8DC")
        u_bar.pack(fill="x", side="top")
        u_bar.pack_propagate(False)
        
        # PERBAIKAN: Jarak padding horizontal dipindah ke .pack() menggunakan padx=15
        ctk.CTkLabel(u_bar, text=f"👤 {parent.player_name}", font=("Arial", 13, "bold"), text_color="#37474F").pack(side="left", padx=15)
        
        # Tempat Koin Emas
        coin_box = ctk.CTkFrame(u_bar, fg_color="#FFF8E1", height=30, corner_radius=15, border_width=1, border_color="#FFE082")
        coin_box.pack(side="left", padx=5)
        
        # PERBAIKAN: Di CTkLabel, gunakan padx di dalam .pack() atau hilangkan jika di dalam Frame kecil
        ctk.CTkLabel(coin_box, text=f"🪙 {parent.koin:,} +", font=("Arial", 12, "bold"), text_color="#E65100").pack(padx=12, pady=3)
        
        # Tombol Pengaturan Atas
        ctk.CTkButton(u_bar, text="⚙️", font=("Arial", 12), fg_color="#F5F5F5", text_color="black", width=32, height=32, corner_radius=16).pack(side="right", padx=15)

        # --- CONTAINER TOMBOL MENU ---
        # Teks sengaja diberi spasi tambahan di awal agar menjorok ke dalam (menggantikan fungsi padx internal button)
        menu_items = [
            ("   ⚔️  MULAI PERMAINAN", "#4CAF50", "#2E7D32", "screen5_persiapan"),
            ("   🗺️  PILIH LEVEL", "#1E88E5", "#0D47A1", "screen4_pilih_level"),
            ("   🛒  TOKO", "#7E57C2", "#4527A0", "screen8_toko"),
            ("   🎒  ITEM SAYA", "#FFA726", "#E65100", "screen5_persiapan"),
            ("   🏆  PAPAN PERINGKAT", "#FB8C00", "#F57C00", "screen10_leaderboard"),
            ("   📋  MISI HARIAN", "#26A69A", "#00695C", "screen3_menu_utama")
        ]
        
        content_frame = ctk.CTkFrame(self, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        for text, bg, border, target in menu_items:
            # PERBAIKAN: Menghapus argumen `padx=25` dari dalam CTkButton
            btn = ctk.CTkButton(content_frame, text=text, font=("Impact", 15), 
                                fg_color=bg, hover_color=bg, text_color="white",
                                height=48, corner_radius=12, border_width=2, border_color=border,
                                anchor="w",
                                command=lambda t=target: parent.switch_screen(t))
            btn.pack(fill="x", pady=5)
            
        # --- BOTTOM NAV BAR ---
        bot_nav = ctk.CTkFrame(self, fg_color="#FFFFFF", height=65, corner_radius=0, border_width=1, border_color="#CFD8DC")
        bot_nav.pack(side="bottom", fill="x")
        bot_nav.pack_propagate(False)
        
        navs = [("🎁 Hadiah", "screen3_menu_utama"), ("📋 Misi", "screen3_menu_utama"), ("📊 Ranking", "screen10_leaderboard"), ("⚙️ Set", "screen1_splash")]
        for i, (txt, scr) in enumerate(navs):
            b = ctk.CTkButton(bot_nav, text=txt, font=("Arial", 11, "bold"), fg_color="transparent", text_color="#546E7A", hover_color="#ECEFF1", command=lambda s=scr: parent.switch_screen(s))
            b.grid(row=0, column=i, sticky="nsew")
        bot_nav.columnconfigure((0,1,2,3), weight=1)