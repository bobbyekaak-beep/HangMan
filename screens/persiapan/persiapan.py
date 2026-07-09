import tkinter as tk 
from database.koneksi import hubungkan_database 

class Screen5PersiapanPerang(tk.Frame): 
    def __init__(self, parent, controller): 
        super().__init__(parent, bg="white") 
        self.parent = parent
        self.controller = controller
        self._cek_kesiapan_database() 
        # UI disiapkan terlebih dahulu, konten diisi secara dinamis via populate_data
        self.setup_ui() 

    def buat_kotak_melengkung(self, canvas, x1, y1, x2, y2, radius=15, **kwargs): 
        """Fungsi pembantu untuk menggambar kotak dengan sudut melengkung pada Canvas"""
        points = [x1+radius, y1, x1+radius, y1, x2-radius, y1, x2-radius, y1, x2, y1, x2, y1+radius, x2, y1+radius, x2, y2-radius, x2, y2-radius, x2, y2, x2-radius, y2, x2-radius, y2, x1+radius, y2, x1+radius, y2, x1, y2, x1, y2-radius, x1, y2-radius, x1, y1+radius, x1, y1+radius, x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def setup_ui(self): 
       
        # TOP HEADER BANNER & NAVIGATION
        header_frame = tk.Frame(self, bg="white") 
        header_frame.pack(fill="x", pady=(35, 10), padx=15) 
        
        btn_back = tk.Button(header_frame, text="←", font=("Arial", 16, "bold"), bg="white", fg="black", bd=0, activebackground="white", command=self._action_back) 
        btn_back.pack(side="left") 
        
        lbl_judul = tk.Label(header_frame, text="BERSIAP UNTUK BERTARUNG !", font=("Arial", 12, "bold"), fg="black", bg="white") 
        lbl_judul.pack(side="left", padx=15) 

       
        # BOX KATEGORI WORD (ROUNDED CORNERS)
        self.kategori_canvas = tk.Canvas(self, bg="white", highlightthickness=0, height=110)
        self.kategori_canvas.pack(fill="x", padx=20, pady=10)
        
        self.buat_kotak_melengkung(self.kategori_canvas, 2, 2, 358, 108, radius=15, fill="#E0E0E0")
        self.buat_kotak_melengkung(self.kategori_canvas, 3, 3, 357, 107, radius=14, fill="white") 
        
        self.kategori_canvas.create_text(180, 30, text="KATEGORI", font=("Arial", 11, "bold"), fill="#777777")
        self.txt_kategori = self.kategori_canvas.create_text(180, 68, text="-", font=("Arial", 20, "bold"), fill="#4CAF50")

       
        # TIGA KOTAK STATUS (HP MUSUH, WAKTU, KESULITAN) (ROUNDED CORNERS)
        status_frame = tk.Frame(self, bg="white") 
        status_frame.pack(fill="x", padx=15, pady=10) 
        status_frame.columnconfigure((0, 1, 2), weight=1) 
        
        # Tempat menyimpan id teks untuk diupdate secara dinamis
        self.txt_status_items = {}
        
        status_config = [ 
            ("HP MUSUH", "#E53935"), 
            ("WAKTU", "black"), 
            ("KESULITAN", "black") 
        ] 
        
        for i, (title, color) in enumerate(status_config): 
            box_canvas = tk.Canvas(status_frame, bg="white", highlightthickness=0, height=85, width=110)
            box_canvas.grid(row=0, column=i, padx=5, sticky="nsew")
            
            self.buat_kotak_melengkung(box_canvas, 2, 2, 112, 83, radius=12, fill="#E0E0E0")
            self.buat_kotak_melengkung(box_canvas, 3, 3, 111, 82, radius=11, fill="white") 
            
            box_canvas.create_text(57, 28, text=title, font=("Arial", 9, "bold"), fill="#777777")
            # Simpan reference text id berdasarkan judulnya
            self.txt_status_items[title] = box_canvas.create_text(57, 56, text="-", font=("Arial", 13, "bold"), fill=color)
            self.txt_status_items[f"{title}_canvas"] = box_canvas

       
        # ITEM YANG TERSEDIA PANEL (ROUNDED CORNERS)
        tk.Label(self, text="ITEM YANG TERSEDIA", font=("Arial", 11, "bold"), fg="#333333", bg="white").pack(pady=(20, 8)) 
        
        item_frame = tk.Frame(self, bg="white") 
        item_frame.pack(fill="x", padx=15) 
        item_frame.columnconfigure((0, 1, 2), weight=1) 
        
        self.txt_item_qtys = {}
        
        items_config = [ 
            ("🕒", "PETUNJUK\nHURUF", "petunjuk", "#FFA000"), 
            ("⏱️", "TAMBAH\nWAKTU", "tambah_waktu", "#4CAF50"), 
            ("❤️", "PULIHKAN HP", "pulihkan_hp", "#E53935") 
        ] 
        
        for i, (icon, name, key_data, icon_color) in enumerate(items_config): 
            item_canvas = tk.Canvas(item_frame, bg="white", highlightthickness=0, height=130, width=110)
            item_canvas.grid(row=0, column=i, padx=5, sticky="nsew")
            
            self.buat_kotak_melengkung(item_canvas, 2, 2, 112, 128, radius=12, fill="#E0E0E0")
            self.buat_kotak_melengkung(item_canvas, 3, 3, 111, 127, radius=11, fill="white") 
            
            item_canvas.create_text(57, 35, text=icon, font=("Arial", 28), fill=icon_color)
            item_canvas.create_text(57, 78, text=name, font=("Arial", 8, "bold"), fill="#555555", justify="center")
            self.txt_item_qtys[key_data] = item_canvas.create_text(95, 114, text="x0", font=("Arial", 8, "bold"), fill="black")
            self.txt_item_qtys[f"{key_data}_canvas"] = item_canvas

       
        # TOMBOL UTAMA & FOOTER CONTROL
        bottom_frame = tk.Frame(self, bg="white") 
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 40)) 
        
        btn_mulai = tk.Button(bottom_frame, text="MULAI PERTARUNGAN", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", activebackground="#43A047", activeforeground="white", relief="flat", height=2, command=self._action_mulai) 
        btn_mulai.pack(fill="x", pady=(0, 10)) 
        
        lbl_footer = tk.Label(bottom_frame, text="Persiapkan dirimu dan taklukkan kata misterius!", font=("Arial", 9), fg="#555555", bg="white") 
        lbl_footer.pack() 

   
    # FUNCTION UNTUK MENERIMA DAN UPDATE DATA SECARA DINAMIS
    def populate_data(self, data):
        """Fungsi untuk mengisi teks pada komponen canvas secara dinamis dari data luar"""
        kategori = data.get("kategori", "HEWAN")
        self.kategori_canvas.itemconfig(self.txt_kategori, text=kategori)
        
        hp_musuh = data.get("hp_musuh", "65")
        waktu = data.get("waktu", "01:30")
        kesulitan = data.get("kesulitan", "SEDANG")
        
        hp_canvas = self.txt_status_items["HP MUSUH_canvas"]
        hp_canvas.itemconfig(self.txt_status_items["HP MUSUH"], text=str(hp_musuh))
        
        waktu_canvas = self.txt_status_items["WAKTU_canvas"]
        waktu_canvas.itemconfig(self.txt_status_items["WAKTU"], text=waktu)
        
        kesulitan_canvas = self.txt_status_items["KESULITAN_canvas"]
        kesulitan_canvas.itemconfig(self.txt_status_items["KESULITAN"], text=kesulitan)
        
        qty_petunjuk = data.get("qty_petunjuk", 2)
        qty_waktu = data.get("qty_waktu", 2)
        qty_hp = data.get("qty_hp", 3)
        
        canvas_p = self.txt_item_qtys["petunjuk_canvas"]
        canvas_p.itemconfig(self.txt_item_qtys["petunjuk"], text=f"x{qty_petunjuk}")
        
        canvas_w = self.txt_item_qtys["tambah_waktu_canvas"]
        canvas_w.itemconfig(self.txt_item_qtys["tambah_waktu"], text=f"x{qty_waktu}")
        
        canvas_h = self.txt_item_qtys["pulihkan_hp_canvas"]
        canvas_h.itemconfig(self.txt_item_qtys["pulihkan_hp"], text=f"x{qty_hp}")

    def _action_mulai(self):
        try:
            level = getattr(self, 'level_terpilih', 1) # Angka 1 adalah default pencegahan error
            
            # 2. Logika percabangan untuk memanggil file UI yang tepat
            if level == 1:
                halaman_tujuan = "Screen6Gameplay"
            elif level == 2:
                halaman_tujuan = "Screen7GameplayLevel2"
            elif level == 3:
                halaman_tujuan = "Screen8GameplayLevel3"
            else:
                # Jika level lebih dari 3 atau tidak dikenali, lemparkan ke level 1
                halaman_tujuan = "Screen6Gameplay" 
            
            print(f"Membuka arena untuk Level {level} -> {halaman_tujuan}")
            
            # 3. Eksekusi perpindahan layar (sekaligus mengirim ulang data level jika dibutuhkan)
            self.controller.show_frame(halaman_tujuan, data={"level": level})
            
        except Exception as e:
            print(f"[ERROR] Gagal memuat arena game: {e}") 

    def _action_back(self): 
        try: 
            self.controller.show_frame("PilihLevelApp") 
        except AttributeError: 
            print("[PREVIEW] Tombol Back '←' Diklik -> Kembali ke Pilih Level") 

    def _cek_kesiapan_database(self): 
        db_koneksi = hubungkan_database() 
        if db_koneksi is not None: 
            try: 
                cursor = db_koneksi.cursor() 
                query = "SELECT coins FROM users WHERE username = 'mama'" 
                cursor.execute(query) 
                hasil = cursor.fetchone() 
                if hasil: 
                    print(f"[DATABASE] Koneksi Persiapan Sukses! Koin user 'mama' saat ini: {hasil[0]}") 
            except Exception as e: 
                print(f"[DATABASE] Error: {e}") 
            finally: 
                cursor.close() 
                db_koneksi.close() 
        else: 
            print("[DATABASE] Gagal terhubung pada halaman persiapan.") 

# PENGETESAN TAMPILAN 
if __name__ == "__main__": 
    root = tk.Tk() 
    root.title("Persiapan Pertarungan") 
    root.geometry("400x700") 
    root.resizable(False, False) 
    root.configure(bg="white") 
    
    # Simulasi data dinamis yang dikirim ke halaman persiapan
    data_dummy_level = {
        "kategori": "HEWAN",
        "hp_musuh": "100",
        "waktu": "02:00",
        "kesulitan": "SULIT",
        "qty_petunjuk": 5,
        "qty_waktu": 1,
        "qty_hp": 4
    }
    
    app = Screen5PersiapanPerang(root) 
    app.pack(fill="both", expand=True) 
    
    # Tembakkan data ke fungsi populate_data
    app.populate_data(data_dummy_level)
    
    root.mainloop()