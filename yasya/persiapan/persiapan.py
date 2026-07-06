# persiapan_perang.py
import tkinter as tk

class Screen5PersiapanPerang(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F6")
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        # Judul Atas
        header_frame = tk.Frame(self, bg="#F0F4F6")
        header_frame.pack(fill="x", pady=(35, 10), padx=15)
        
        # Tombol Back (Panah Kiri)
        btn_back = tk.Button(header_frame, text="←", font=("Arial", 16, "bold"), 
                             bg="#F0F4F6", fg="black", bd=0, activebackground="#F0F4F6",
                             command=self._action_back)
        btn_back.pack(side="left")
        
        # Teks Judul Utama
        lbl_judul = tk.Label(header_frame, text="BERSIAP UNTUK BERTARUNG !", 
                             font=("Arial", 12, "bold"), fg="black", bg="#F0F4F6")
        lbl_judul.pack(side="left", padx=15)

        # BOX KATEGORI WORD
        kategori_box = tk.Frame(self, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        kategori_box.pack(fill="x", padx=20, pady=10)
        
        tk.Label(kategori_box, text="KATEGORI", font=("Arial", 11, "bold"), fg="#777777", bg="white").pack(pady=(15, 2))
       
        tk.Label(kategori_box, text="HEWAN", font=("Arial", 20, "bold"), fg="#4CAF50", bg="white").pack(pady=(0, 15))

        # TIGA KOTAK STATUS (HP MUSUH, WAKTU, KESULITAN)
        status_frame = tk.Frame(self, bg="#F0F4F6")
        status_frame.pack(fill="x", padx=16, pady=10)
        status_frame.columnconfigure((0, 1, 2), weight=1) 
        
        status_data = [
            ("HP MUSUH", "65", "#E53935"),    
            ("WAKTU", "01:30", "black"),     
            ("KESULITAN", "SEDANG", "black")  
        ]
        
        for i, (title, val, color) in enumerate(status_data):
            box = tk.Frame(status_frame, bg="white", highlightbackground="#E0E0E0", highlightthickness=1, height=80)
            box.grid(row=0, column=i, padx=5, sticky="nsew")
            box.pack_propagate(False)
            
            # Label judul status (HP MUSUH, WAKTU, KESULITAN)
            tk.Label(box, text=title, font=("Arial", 9, "bold"), fg="#777777", bg="white").pack(pady=(14, 4))
            tk.Label(box, text=val, font=("Arial", 13, "bold"), fg=color, bg="white").pack()

        # ITEM YANG TERSEDIA
        tk.Label(self, text="ITEM YANG TERSEDIA", font=("Arial", 11, "bold"), fg="#333333", bg="#F0F4F6").pack(pady=(20, 8))
        
        item_frame = tk.Frame(self, bg="#F0F4F6")
        item_frame.pack(fill="x", padx=16)
        item_frame.columnconfigure((0, 1, 2), weight=1)
        
        items_data = [
            ("🕒", "PETUNJUK\nHURUF", "x2", "#FFA000"),  # Kuning/Oranye hangat
            ("⏱️", "TAMBAH\nWAKTU", "x2", "#4CAF50"),    # Hijau
            ("❤️", "PULIHKAN HP", "x3", "#E53935")     # Merah
        ]
        
        for i, (icon, name, qty, icon_color) in enumerate(items_data):
            box = tk.Frame(item_frame, bg="white", highlightbackground="#E0E0E0", highlightthickness=1, height=120)
            box.grid(row=0, column=i, padx=5, sticky="nsew")
            box.pack_propagate(False)
            
            tk.Label(box, text=icon, font=("Arial", 28), fg=icon_color, bg="white").pack(pady=(10, 2))
            
            tk.Label(box, text=name, font=("Arial", 8, "bold"), fg="#555555", bg="white", justify="center").pack()
            
            lbl_qty = tk.Label(box, text=qty, font=("Arial", 8, "bold"), fg="black", bg="white")
            lbl_qty.pack(side="bottom", anchor="e", padx=10, pady=6)

        # TOMBOL UTAMA & FOOTER 
        bottom_frame = tk.Frame(self, bg="#F0F4F6")
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=(0, 40))
        
        btn_mulai = tk.Button(bottom_frame, text="MULAI PERTARUNGAN", font=("Arial", 12, "bold"), 
                              bg="#4CAF50", fg="white", activebackground="#43A047", activeforeground="white", 
                              relief="flat", height=2, command=self._action_mulai)
        btn_mulai.pack(fill="x", pady=(0, 10))
        
        lbl_footer = tk.Label(bottom_frame, text="Persiapkan dirimu dan taklukkan kata misterius!", 
                              font=("Arial", 9), fg="#555555", bg="#F0F4F6")
        lbl_footer.pack()


    # LOGIKA NAVIGASI (Proteksi Berdiri Mandiri) 
    def _action_mulai(self):
        try:
            self.parent.switch_screen("game")
        except AttributeError:
            print("[PREVIEW] Tombol 'MULAI PERTARUNGAN' Diklik -> Masuk ke Arena Play")

    def _action_back(self):
        try:
            self.parent.switch_screen("pilih_level")
        except AttributeError:
            print("[PREVIEW] Tombol Back '←' Diklik -> Kembali ke Pilih Level")


# PENGETESAN TAMPILAN
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tugas Ke-3: Persiapan Pertarungan")
    root.geometry("400x700")
    root.resizable(False, False)
    root.configure(bg="#F0F4F6")

    app = Screen5PersiapanPerang(root)
    app.pack(fill="both", expand=True)
    
    root.mainloop()