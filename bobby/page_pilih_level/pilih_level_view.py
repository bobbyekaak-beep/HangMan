import tkinter as tk

TOTAL_LEVEL = 20
KOLOM = 4

HIJAU = "#43a047"
ABU_BG = "#eeeeee"
ABU_TEKS = "#9e9e9e"
BIRU_GELAP = "#1e2a38"
BORDER = "#dcdcdc"
KUNING = "#f4b400"


def ambil_data_progres():
    """Simulasi data dari database asli. Isi set berikut nomor level yang sudah selesai."""
    return set()


def ambil_bintang_level():
    """Simulasi rating bintang per level (0-3) dari database. Dikosongkan dulu karena belum ada hasil."""
    return {}


class PilihLevelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hangman Word Quest - Pilih Level")
        self.geometry("400x700")
        self.configure(bg="white")

        self.level_selesai = ambil_data_progres()
        self.level_bintang = ambil_bintang_level()

        self.buat_header()
        self.buat_kartu_dunia()
        self.buat_grid_level()
        self.buat_status_bar()

    def level_terbuka(self, level):
        if level <= 3:
            return True
        return (level - 1) in self.level_selesai

    def teks_bintang(self, level):
        rating = self.level_bintang.get(level, 0)
        return "★" * rating + "☆" * (3 - rating)

    def buat_header(self):
        header = tk.Frame(self, bg="white")
        header.pack(fill="x", padx=20, pady=(10, 5))
        tk.Label(header, text="←", font=("Arial", 16, "bold"), bg="white").pack(side="left")
        tk.Label(header, text="PILIH LEVEL", font=("Arial", 16, "bold"), bg="white").pack(side="left", padx=15)

    def buat_kartu_dunia(self):
        kartu = tk.Frame(self, bg="white", highlightbackground=BORDER, highlightthickness=1)
        kartu.pack(fill="x", padx=20, pady=(0, 10))

        judul_frame = tk.Frame(kartu, bg="white")
        judul_frame.pack(fill="x", padx=15, pady=(8, 4))
        tk.Label(judul_frame, text="★", font=("Arial", 12), fg=KUNING, bg="white").pack(side="left")
        tk.Label(judul_frame, text="DUNIA 1 - RIMBA BELANTARA", font=("Arial", 11, "bold"),
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
        # padx disamakan dengan kartu dunia (20) agar lebar kiri-kanan sejajar
        frame_grid = tk.Frame(self, bg="white")
        frame_grid.pack(padx=20, pady=(0, 5), fill="both", expand=True)

        jumlah_baris = -(-TOTAL_LEVEL // KOLOM)  # pembulatan ke atas
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
        self.label_status = tk.Label(self, text="Pilih Level Untuk Mulai Bermain",
                                      bg="white", fg=BIRU_GELAP, font=("Arial", 9))
        self.label_status.pack(side="bottom", pady=8)

    def mulai_level(self, level):
        self.label_status.config(text=f"Level {level} dipilih, memuat permainan...")


if __name__ == "__main__":
    app = PilihLevelApp()
    app.mainloop()