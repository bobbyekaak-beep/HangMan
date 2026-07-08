import tkinter as tk
import mysql.connector

TOTAL_LEVEL = 20
KOLOM = 4

HIJAU = "#43a047"
ABU_BG = "#eeeeee"
ABU_TEKS = "#9e9e9e"
BIRU_GELAP = "#1e2a38"
BORDER = "#dcdcdc"
KUNING = "#f4b400"

USERNAME_AKTIF = "mama"


def buat_koneksi():
    # membuka koneksi baru ke database MySQL/MariaDB
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_hangman"
    )


def ambil_user_id(username):
    # mengambil id user berdasarkan username yang sedang login
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    hasil = cursor.fetchone()
    cursor.close()
    conn.close()
    return hasil[0] if hasil else None


def ambil_data_progres(user_id):
    # mengambil daftar level yang sudah pernah dimenangkan user dari tabel scores
    if user_id is None:
        return set()
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT level_reached FROM scores WHERE user_id = %s AND status_game = 'VICTORY'",
        (user_id,)
    )
    hasil = cursor.fetchall()
    cursor.close()
    conn.close()
    return {baris[0] for baris in hasil}


def ambil_bintang_level(user_id):
    # menghitung bintang terbaik tiap level berdasarkan jumlah tebakan salah pada percobaan VICTORY
    if user_id is None:
        return {}
    conn = buat_koneksi()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT level_reached, tebakan_salah FROM scores WHERE user_id = %s AND status_game = 'VICTORY'",
        (user_id,)
    )
    hasil = cursor.fetchall()
    cursor.close()
    conn.close()

    bintang_per_level = {}
    for level, salah in hasil:
        if salah <= 1:
            bintang = 3
        elif salah <= 3:
            bintang = 2
        else:
            bintang = 1
        bintang_per_level[level] = max(bintang_per_level.get(level, 0), bintang)
    return bintang_per_level


class PilihLevelApp(tk.Tk):
    def __init__(self):
        # setup window dan ambil data user dari database lalu bangun tampilan
        super().__init__()
        self.title("Hangman Word Quest - Pilih Level")
        self.geometry("400x700")
        self.configure(bg="white")

        self.user_id = ambil_user_id(USERNAME_AKTIF)
        self.level_selesai = ambil_data_progres(self.user_id)
        self.level_bintang = ambil_bintang_level(self.user_id)

        self.buat_header()
        self.buat_kartu_dunia()
        self.buat_grid_level()
        self.buat_status_bar()

    def level_terbuka(self, level):
        # cek apakah level boleh dimainkan, level 1-3 selalu terbuka
        if level <= 3:
            return True
        return (level - 1) in self.level_selesai

    def teks_bintang(self, level):
        # ubah jumlah bintang jadi tampilan simbol ★ dan ☆
        rating = self.level_bintang.get(level, 0)
        return "★" * rating + "☆" * (3 - rating)

    def buat_header(self):
        # membuat bagian atas berisi tombol kembali dan judul halaman
        header = tk.Frame(self, bg="white")
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="←", font=("Arial", 16, "bold"), bg="white").pack(side="left")
        tk.Label(header, text="PILIH LEVEL", font=("Arial", 16, "bold"), bg="white").pack(side="left", padx=15)

    def buat_kartu_dunia(self):
        # membuat kartu info dunia beserta progress bar penyelesaian level
        kartu = tk.Frame(self, bg="white", highlightbackground=BORDER, highlightthickness=1)
        kartu.pack(fill="x", padx=20, pady=(0, 10))

        judul_frame = tk.Frame(kartu, bg="white")
        judul_frame.pack(fill="x", padx=15, pady=(8, 4))
        tk.Label(judul_frame, text="★", font=("Arial", 12), fg=KUNING, bg="white").pack(side="left")
        tk.Label(judul_frame, text="DUNIA 1 - BINATANG DARAT", font=("Arial", 11, "bold"),
                 bg="white", fg=BIRU_GELAP).pack(side="left", padx=5)

        canvas = tk.Canvas(kartu, height=18, bg="#e0e0e0", highlightthickness=0)
        canvas.pack(fill="x", padx=15, pady=(0, 10))

        jumlah_selesai = len(self.level_selesai)
        proporsi = jumlah_selesai / TOTAL_LEVEL

        def gambar_progress(event=None):
            canvas.delete("all")
            lebar = canvas.winfo_width()
            canvas.create_rectangle(0, 0, lebar * proporsi, 18, fill=HIJAU, width=0)
            canvas.create_text(lebar - 30, 9, text=f"{jumlah_selesai}/{TOTAL_LEVEL}",
                                fill=BIRU_GELAP, font=("Arial", 8, "bold"))

        canvas.bind("<Configure>", gambar_progress)

    def buat_grid_level(self):
        # membuat grid tombol level lengkap dengan status terbuka/terkunci dan bintangnya
        frame_grid = tk.Frame(self, bg="white")
        frame_grid.pack(padx=20, pady=(0, 5), fill="both", expand=True)

        jumlah_baris = -(-TOTAL_LEVEL // KOLOM)
        for kolom in range(KOLOM):
            frame_grid.grid_columnconfigure(kolom, weight=1, uniform="kolom_level")
        for baris in range(jumlah_baris):
            frame_grid.grid_rowconfigure(baris, weight=1, uniform="baris_level")

        for level in range(1, TOTAL_LEVEL + 1):
            baris = (level - 1) // KOLOM
            kolom = (level - 1) % KOLOM
            terbuka = self.level_terbuka(level)

            if kolom == 0:
                padx_cell = (0, 3)
            elif kolom == KOLOM - 1:
                padx_cell = (3, 0)
            else:
                padx_cell = 3

            cell = tk.Frame(frame_grid, bg="white")
            cell.grid(row=baris, column=kolom, padx=padx_cell, pady=5, sticky="nsew")

            if terbuka:
                bg, fg, state = HIJAU, "white", "normal"
                teks = str(level)
            else:
                bg, fg, state = ABU_BG, ABU_TEKS, "disabled"
                teks = "🔒"

            tombol = tk.Button(
                cell, text=teks, font=("Arial", 12, "bold"),
                bg=bg, fg=fg, disabledforeground=ABU_TEKS, relief="flat",
                state=state, command=lambda lv=level: self.mulai_level(lv)
            )
            tombol.pack(fill="both", expand=True, pady=(0, 2))

            warna_bintang = KUNING if terbuka else ABU_TEKS
            tk.Label(cell, text=self.teks_bintang(level), font=("Arial", 8),
                     bg="white", fg=warna_bintang).pack(pady=(0, 4))

    def buat_status_bar(self):
        # membuat label status di bagian bawah layar
        self.label_status = tk.Label(self, text="Pilih Level Untuk Mulai Bermain",
                                      bg="white", fg=BIRU_GELAP, font=("Arial", 9))
        self.label_status.pack(side="bottom", pady=8)

    def mulai_level(self, level):
        # dipanggil saat tombol level ditekan, sementara baru update status
        self.label_status.config(text=f"Level {level} dipilih, memuat permainan...")


if __name__ == "__main__":
    app = PilihLevelApp()
    app.mainloop()