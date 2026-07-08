import sys 
import os 

# SECTION 1: SYSTEM PATH & IMPORT MODULES
# Menambahkan folder utama HangMan ke dalam jalur pencarian Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))) 

import tkinter as tk 
from andre.database.koneksi import hubungkan_database 

class Screen10GameOver(tk.Frame): 
    def __init__(self, parent): 
        super().__init__(parent, bg="white") 
        self.parent = parent 

    def populate_data(self, data): 
        # Bersihkan widget lama jika fungsi dipanggil ulang agar tidak menumpuk
        for widget in self.winfo_children(): 
            widget.destroy() 
            
        
        # SECTION 2: DATA ACQUISITION (MULTI-USER & PROGRESS)
        username_aktif = data.get("username", "mama")  
        level_sekarang = data.get("level", 1)
        kata_diterima = data.get("kata", "HARIMAU, KANCIL, GAJAH") 
        sisa_waktu = data.get("sisa_waktu", 0)         
        hp_player = data.get("hp_player", 0)           
        kata_tertebak = data.get("kata_tertebak", 2) 
        tebakan_salah = data.get("tebakan_salah", 6)   
        koin_hiburan = data.get("koin_hiburan", 20)

        
        # SECTION 3: DATABASE SYNCHRONIZATION (MULTI-USER EVENT)
        self._simpan_game_over_ke_db(
            username_aktif, level_sekarang, koin_hiburan, kata_diterima, 
            sisa_waktu, hp_player, kata_tertebak, tebakan_salah
        )

        
        # SECTION 4: UI LAYOUT & GRAPHICAL WIDGETS (Tkinter)
        # TOP HEADER BANNER 
        banner = tk.Frame(self, bg="#E53935", height=65) 
        banner.pack(fill="x", pady=(40, 15), padx=20) 
        banner.pack_propagate(False) 
        
        lbl_gameover = tk.Label(banner, text="GAME OVER", font=("Arial", 20, "bold"), fg="white", bg="#E53935") 
        lbl_gameover.pack(expand=True) 

        # REVEAL CORRECT ANSWER 
        lbl_info = tk.Label(self, text="KATA PADA LEVEL INI :", font=("Arial", 11, "bold"), fg="black", bg="white") 
        lbl_info.pack(pady=(25, 2)) 
        
        lbl_kata_asli = tk.Label(self, text=kata_diterima, font=("Arial", 10), fg="black", bg="white", wraplength=340) 
        lbl_kata_asli.pack(pady=(0, 25)) 

        # CENTRAL REWARD VISUALIZER (CONSOLATION PRIZE) 
        reward_box = tk.Frame(self, bg="white") 
        reward_box.pack(fill="x", padx=35, pady=10) 
        
        tk.Label(reward_box, text="REWARD HIBURAN", font=("Arial", 11, "bold"), fg="black", bg="white").pack(pady=(12, 2)) 
        
        # PERBAIKAN SEJAJAR: Menggunakan sub-frame agar emoji dan teks sejajar rata tengah 
        coin_row = tk.Frame(reward_box, bg="white")
        coin_row.pack(anchor="center", pady=(0, 12))
        
        lbl_icon = tk.Label(coin_row, text="💰", font=("Arial", 36), fg="#FFB300", bg="white")
        lbl_icon.pack(side="left", padx=(0, 8))
        
        lbl_text = tk.Label(coin_row, text=f"+{koin_hiburan}", font=("Arial", 36, "bold"), fg="#FFB300", bg="white")
        lbl_text.pack(side="left")

        # MOTIVATIONAL TEXT 
        lbl_motivasi = tk.Label(self, text="Jangan menyerah!\nAsah strategimu dan coba sekali lagi.", font=("Arial", 11, "italic"), fg="#555555", bg="white", justify="center") 
        lbl_motivasi.pack(pady=35) 

        # NAVIGATION CONTROL BUTTONS 
        btn_frame = tk.Frame(self, bg="white") 
        btn_frame.pack(side="bottom", fill="x", padx=35, pady=45) 
        
        btn_coba = tk.Button(btn_frame, text="COBA LAGI", font=("Arial", 12, "bold"), bg="#E53935", fg="white", relief="flat", height=2, command=self._action_coba_lagi) 
        btn_coba.pack(fill="x", pady=6) 
        
        btn_menu = tk.Button(btn_frame, text="KEMBALI KE MENU", font=("Arial", 12, "bold"), bg="#2196F3", fg="white", relief="flat", height=2, command=self._action_menu) 
        btn_menu.pack(fill="x", pady=6) 

    
    # SECTION 5: NAVIGATION HANDLERS (CONTROLLERS)
    
    def _action_coba_lagi(self): 
        try: 
            self.parent.switch_screen("game") 
        except AttributeError: 
            print("[PREVIEW] Tombol Coba Lagi Diklik") 

    def _action_menu(self): 
        try: 
            self.parent.switch_screen("menu") 
        except AttributeError: 
            print("[PREVIEW] Tombol Kembali ke Menu Diklik") 

    
    # SECTION 6: BACKEND DATABASE TRANSACTIONS (MySQL Multi-User)
    
    def _simpan_game_over_ke_db(self, username, level, koin, kata, sisa_waktu, hp, benar, salah): 
        db_koneksi = hubungkan_database() 
        if db_koneksi is not None: 
            try: 
                cursor = db_koneksi.cursor() 
                
                query_user = "SELECT id FROM users WHERE username = %s"
                cursor.execute(query_user, (username,))
                user_data = cursor.fetchone() 
                
                if user_data is not None:
                    user_id = user_data[0]
                    
                    if koin > 0:
                        query_koin = "UPDATE users SET coins = coins + %s WHERE id = %s" 
                        cursor.execute(query_koin, (koin, user_id)) 
                    
                    query_score = """
                        INSERT INTO scores 
                        (user_id, level_reached, waktu_bermain, status_game, kata_rahasia, sisa_waktu, hp_player, tebakan_benar, tebakan_salah, koin_didapat) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    waktu_bermain = 90 - sisa_waktu 
                    if waktu_bermain < 0 or waktu_bermain > 90: 
                        waktu_bermain = 90
                        
                    cursor.execute(query_score, (user_id, level, waktu_bermain, 'LOSE', kata, sisa_waktu, hp, benar, salah, koin))
                    db_koneksi.commit() 
                    print(f"[DATABASE] Sukses mencatat data LOSE & menambah +{koin} koin hiburan untuk user '{username}' (ID: {user_id})!") 
                else:
                    print(f"[DATABASE] User '{username}' tidak ditemukan di database.")
                    
            except Exception as e: 
                print(f"[DATABASE] Error saat mencatat data kekalahan: {e}") 
            finally: 
                cursor.close() 
                db_koneksi.close() 
        else: 
            print("[DATABASE] Gagal terhubung ke database.") 


# SECTION 7: LOCAL APP ISOLATED TESTING (SANDBOX ENVIRONMENT)

if __name__ == "__main__": 
    root = tk.Tk() 
    root.title("Game Over") 
    root.geometry("400x700") 
    root.resizable(False, False) 
    root.configure(bg="white") 
    
    data_dummy_kalah = { 
        "username": "mama",  
        "level": 1,
        "kata": "HARIMAU, KANCIL, GAJAH", 
        "sisa_waktu": 45,    
        "hp_player": 0,
        "kata_tertebak": 2,
        "tebakan_salah": 6,
        "koin_hiburan": 20   
    } 
    
    app = Screen10GameOver(root) 
    app.pack(fill="both", expand=True) 
    app.populate_data(data_dummy_kalah) 
    root.mainloop()