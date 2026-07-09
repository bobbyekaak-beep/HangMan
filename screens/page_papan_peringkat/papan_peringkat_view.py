import tkinter as tk
import math


def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def gambar_koin(canvas, x, y, radius=7):
    """Gambar ikon koin bulat kuning di posisi (x, y), return id-nya untuk dipindah nanti."""
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                               fill="#F2C94C", outline="#D4A62A", width=1)


def gambar_bintang(canvas, x, y, radius=8, fill="#F2C94C", outline="#D4A62A"):
    """Gambar ikon bintang di posisi (x, y), return id-nya untuk dipindah nanti."""
    points = []
    for i in range(10):
        sudut = math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.45
        px = x + r * math.cos(sudut)
        py = y - r * math.sin(sudut)
        points.extend([px, py])
    return canvas.create_polygon(points, fill=fill, outline=outline, width=1)


def gambar_hexagon(canvas, cx, cy, radius, fill):
    points = []
    for i in range(6):
        sudut = math.pi / 6 + i * math.pi / 3
        px = cx + radius * math.cos(sudut)
        py = cy + radius * math.sin(sudut)
        points.extend([px, py])
    return canvas.create_polygon(points, fill=fill, outline="")


WARNA_AVATAR = ["#AED6F1", "#F5CBA7", "#A9DFBF", "#F5B7B1",
                "#D7BDE2", "#F9E79F", "#A3E4D7", "#F7C9A9"]


def ambil_warna_avatar(nama):
    return WARNA_AVATAR[ord(nama[0].upper()) % len(WARNA_AVATAR)]


class LeaderboardView(tk.Frame):
    def __init__(self, parent, controller): 
        super().__init__(parent, bg="white")
        self.controller = controller
        self.build_top_bar()
        self.build_title()
        self.build_podium()
        self.build_list()

    def build_top_bar(self):
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=15, pady=(15, 0))

        tk.Button(top, text="←", font=("Arial", 16, "bold"), bg="white",
                  relief="flat", command=self.controller.go_back).pack(side="left")

        right = tk.Frame(top, bg="white")
        right.pack(side="right")

        coin_badge = tk.Canvas(right, width=90, height=25, bg="white", highlightthickness=0)
        coin_badge.pack(side="left", padx=(0, 8))
        rounded_rect(coin_badge, 1, 1, 89, 24, 12, fill="#FFF3D6", outline="")
        gambar_koin(coin_badge, 20, 12, radius=8)
        self.coin_text_id = coin_badge.create_text(55, 12, text="0", font=("Arial", 12, "bold"))
        self.coin_badge = coin_badge

        # tombol + pakai widget Button asli supaya benar-benar bisa dipencet dengan efek klik
        btn_frame = tk.Frame(right, width=20, height=20, bg="#27AE60")
        btn_frame.pack(side="left")
        btn_frame.pack_propagate(False)

        btn_plus = tk.Button(btn_frame, text="+", font=("Arial", 11, "bold"),
                      bg="#27AE60", fg="white", activebackground="#219150",
                      activeforeground="white", relief="flat", bd=0,
                      cursor="hand2", command=self.buka_toko)
        btn_plus.pack(fill="both", expand=True)

    def buka_toko(self):
        self.controller.show_frame("MisiPemainBaruView")

    def build_title(self):
        tk.Label(self, text="LEADERBOARD", bg="white", fg="#1a1a2e",
                 font=("Arial", 20, "bold")).pack(pady=(10, 2))

        deco = tk.Canvas(self, width=200, height=16, bg="white", highlightthickness=0)
        deco.pack()
        deco.create_line(10, 8, 90, 8, fill="#E0B33A", dash=(3, 2))
        deco.create_text(100, 8, text="★", fill="#E0B33A", font=("Arial", 10))
        deco.create_line(110, 8, 190, 8, fill="#E0B33A", dash=(3, 2))

    def build_podium(self):
        podium = tk.Frame(self, bg="white")
        podium.pack(fill="x", padx=15, pady=15)

        self.podium_2 = self.buat_kartu(podium, rank=2, bg="#EAF3FC",
                                         medali="#AAB2BC", avatar_bg="#BFDCF7", tinggi=170)
        self.podium_1 = self.buat_kartu(podium, rank=1, bg="#FFF6DE",
                                         medali="#F2B90C", avatar_bg="#F6A93B", tinggi=200)
        self.podium_3 = self.buat_kartu(podium, rank=3, bg="#FDEEE6",
                                         medali="#CD7F32", avatar_bg="#F7C9A9", tinggi=155)

        self.podium_2["canvas"].pack(side="left", expand=True, fill="both", padx=4)
        self.podium_1["canvas"].pack(side="left", expand=True, fill="both", padx=4)
        self.podium_3["canvas"].pack(side="left", expand=True, fill="both", padx=4)

    def buat_kartu(self, parent, rank, bg, medali, avatar_bg, tinggi):
        lebar = 110
        canvas = tk.Canvas(parent, width=lebar, height=tinggi + 20, bg="white", highlightthickness=0)

        rounded_rect(canvas, 5, 20, lebar - 5, tinggi + 20, 15, fill=bg, outline=medali, width=2)
        canvas.create_oval(lebar / 2 - 15, 0, lebar / 2 + 15, 30, fill=medali, outline="white", width=2)
        canvas.create_text(lebar / 2, 15, text=str(rank), fill="white", font=("Arial", 12, "bold"))

        gambar_hexagon(canvas, lebar / 2, 73, radius=28, fill=avatar_bg)
        avatar_text_id = canvas.create_text(lebar / 2, 73, text="-", font=("Arial", 18, "bold"))

        nama_id = canvas.create_text(lebar / 2, 125, text="-", font=("Arial", 12, "bold"))

        # bintang dan skor diposisikan tengah ulang setelah teks diisi (lihat pusatkan_koin_skor)
        koin_id = gambar_bintang(canvas, lebar / 2, 150, radius=9)
        skor_id = canvas.create_text(lebar / 2, 150, text="0", font=("Arial", 11))

        return {"canvas": canvas, "avatar": avatar_text_id, "nama": nama_id,
                "skor": skor_id, "koin": koin_id, "center_x": lebar / 2, "y_skor": 150}

    def pusatkan_koin_skor(self, canvas, koin_id, skor_id, center_x, y):
        canvas.update_idletasks()
        bbox_koin = canvas.bbox(koin_id)
        bbox_skor = canvas.bbox(skor_id)
        lebar_koin = bbox_koin[2] - bbox_koin[0]
        lebar_skor = bbox_skor[2] - bbox_skor[0]
        spasi = 5
        total = lebar_koin + spasi + lebar_skor
        mulai_x = center_x - total / 2

        target_koin_cx = mulai_x + lebar_koin / 2
        target_skor_cx = mulai_x + lebar_koin + spasi + lebar_skor / 2
        cur_koin_cx = (bbox_koin[0] + bbox_koin[2]) / 2
        cur_skor_cx = (bbox_skor[0] + bbox_skor[2]) / 2

        canvas.move(koin_id, target_koin_cx - cur_koin_cx, 0)
        canvas.move(skor_id, target_skor_cx - cur_skor_cx, 0)

    def build_list(self):
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.list_canvas = tk.Canvas(container, bg="white", highlightthickness=0)
        self.list_frame = tk.Frame(self.list_canvas, bg="white")

        self.list_frame.bind("<Configure>", lambda e: self.list_canvas.configure(
            scrollregion=self.list_canvas.bbox("all")))

        window_id = self.list_canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_canvas.bind("<Configure>", lambda e: self.list_canvas.itemconfig(window_id, width=e.width))

        self.list_canvas.pack(side="left", fill="both", expand=True)

        self.list_canvas.bind_all("<MouseWheel>", lambda e: self.list_canvas.yview_scroll(int(-e.delta / 120), "units"))

    def tampilkan_data(self, data_leaderboard, koin_saya, username_saya):
        """
        data_leaderboard: list of dict dari database, contoh:
        [{"rank": 1, "nama": "PlayerOne", "skor": 2450}, ...]
        Panggil fungsi ini setelah data diambil dari database.
        """
        self.coin_badge.itemconfig(self.coin_text_id, text=f"{koin_saya:,}".replace(",", "."))

        podium_map = {1: self.podium_1, 2: self.podium_2, 3: self.podium_3}
        for item in data_leaderboard:
            if item["rank"] in podium_map:
                p = podium_map[item["rank"]]
                canvas = p["canvas"]
                canvas.itemconfig(p["avatar"], text=item["nama"][0].upper())
                canvas.itemconfig(p["nama"], text=item["nama"])
                canvas.itemconfig(p["skor"], text=f"{item['skor']:,}".replace(",", "."))
                self.pusatkan_koin_skor(canvas, p["koin"], p["skor"], p["center_x"], p["y_skor"])

        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.list_frame.columnconfigure(2, weight=1)

        baris_ke = 0
        for item in data_leaderboard:
            if item["rank"] > 3:
                self.buat_baris_list(item, baris_ke, is_saya=(item["nama"] == username_saya))
                baris_ke += 1

    def buat_baris_list(self, item, baris_ke, is_saya=False):
        warna_bg = "#E8F8ED" if is_saya else "white"
        warna_text = "#219653" if is_saya else "#1a1a2e"
        warna_avatar = ambil_warna_avatar(item["nama"])

        baris = tk.Frame(self.list_frame, bg=warna_bg)
        baris.grid(row=baris_ke, column=0, columnspan=4, sticky="ew", pady=2)
        baris.columnconfigure(2, weight=1)

        tk.Label(baris, text=str(item["rank"]), bg=warna_bg, fg=warna_text,
                 font=("Arial", 12, "bold"), width=3).grid(row=0, column=0, padx=(10, 5), pady=10)

        avatar = tk.Canvas(baris, width=32, height=32, bg=warna_bg, highlightthickness=0)
        avatar.grid(row=0, column=1, padx=8)
        gambar_hexagon(avatar, 16, 16, radius=15, fill=warna_avatar)
        avatar.create_text(16, 16, text=item["nama"][0].upper(), font=("Arial", 11, "bold"))

        nama_text = f"{item['nama']} (Anda)" if is_saya else item["nama"]
        tk.Label(baris, text=nama_text, bg=warna_bg, fg=warna_text,
                 font=("Arial", 12, "bold"), anchor="w").grid(row=0, column=2, sticky="w", padx=8)

        kanan = tk.Frame(baris, bg=warna_bg)
        kanan.grid(row=0, column=3, sticky="e", padx=15)
        tk.Label(kanan, text=f"{item['skor']:,}".replace(",", "."), bg=warna_bg, fg=warna_text,
                 font=("Arial", 12, "bold")).pack(side="right", padx=(4, 0))

        bintang_canvas = tk.Canvas(kanan, width=16, height=16, bg=warna_bg, highlightthickness=0)
        bintang_canvas.pack(side="right")
        gambar_bintang(bintang_canvas, 8, 8, radius=6)

        garis = tk.Frame(self.list_frame, bg="#F0F0F0", height=1)
        garis.grid(row=baris_ke, column=0, columnspan=4, sticky="sew")


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("420x750")
        self.frame = LeaderboardView(self, self)
        self.frame.pack(fill="both", expand=True)

    def go_back(self):
        print("Kembali ke halaman sebelumnya")


if __name__ == "__main__":
    app = App()

    data_dummy = [
        {"rank": 1, "nama": "PlayerOne", "skor": 2450},
        {"rank": 2, "nama": "LexiQuiz", "skor": 2120},
        {"rank": 3, "nama": "ThinkFast", "skor": 1980},
        {"rank": 4, "nama": "AlphaBrain", "skor": 1750},
        {"rank": 5, "nama": "Bobby", "skor": 1250},
        {"rank": 6, "nama": "WordMaster", "skor": 1120},
        {"rank": 7, "nama": "BrainyBoy", "skor": 980},
        {"rank": 8, "nama": "PuzzleQueen", "skor": 820},
        {"rank": 9, "nama": "WordHunter", "skor": 750},
        {"rank": 10, "nama": "HangPro", "skor": 620},
    ]
    app.frame.tampilkan_data(data_dummy, koin_saya=1250, username_saya="Bobby")

    app.mainloop()