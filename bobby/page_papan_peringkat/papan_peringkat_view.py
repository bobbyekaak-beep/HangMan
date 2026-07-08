import tkinter as tk
import math
import mysql.connector
import toko_view
import misi_pemain_baru_view

# koneksi ke database mysql/mariadb
def buat_koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_hangman"
    )

# ambil data leaderboard, total koin tiap user dijumlahkan lalu diurutkan dari terbesar
def ambil_data_leaderboard():
    koneksi = buat_koneksi()
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute("""
        SELECT users.id AS user_id, users.username AS nama,
               COALESCE(SUM(scores.koin_didapat), 0) AS skor
        FROM users
        LEFT JOIN scores ON scores.user_id = users.id
        GROUP BY users.id, users.username
        ORDER BY skor DESC
    """)
    hasil = cursor.fetchall()
    koneksi.close()
    # kasih nomor ranking 1, 2, 3, dst
    for i, baris in enumerate(hasil, start=1):
        baris["rank"] = i
    return hasil

# ambil jumlah koin milik user yang sedang login
def ambil_koin_user(user_id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute("SELECT coins FROM users WHERE id = %s", (user_id,))
    baris = cursor.fetchone()
    koneksi.close()
    return baris[0] if baris else 0

# fungsi bantu gambar kotak dengan sudut melengkung di canvas
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    points = [
        x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r,
        x2, y2 - r, x2, y2, x2 - r, y2, x1 + r, y2,
        x1, y2, x1, y2 - r, x1, y1 + r, x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# fungsi bantu gambar lingkaran koin
def gambar_koin(canvas, x, y, radius=7):
    return canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                               fill="#F2C94C", outline="#D4A62A", width=1)

# fungsi bantu gambar bintang (dipakai buat icon skor)
def gambar_bintang(canvas, x, y, radius=8, fill="#F2C94C", outline="#D4A62A"):
    points = []
    for i in range(10):
        sudut = math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.45
        px = x + r * math.cos(sudut)
        py = y - r * math.sin(sudut)
        points.extend([px, py])
    return canvas.create_polygon(points, fill=fill, outline=outline, width=1)

# fungsi bantu gambar hexagon (dipakai buat bentuk avatar)
def gambar_hexagon(canvas, cx, cy, radius, fill):
    points = []
    for i in range(6):
        sudut = math.pi / 6 + i * math.pi / 3
        px = cx + radius * math.cos(sudut)
        py = cy + radius * math.sin(sudut)
        points.extend([px, py])
    return canvas.create_polygon(points, fill=fill, outline="")

# daftar warna buat avatar user
WARNA_AVATAR = ["#AED6F1", "#F5CBA7", "#A9DFBF", "#F5B7B1",
                "#D7BDE2", "#F9E79F", "#A3E4D7", "#F7C9A9"]

# pilih warna avatar berdasarkan huruf pertama nama
def ambil_warna_avatar(nama):
    return WARNA_AVATAR[ord(nama[0].upper()) % len(WARNA_AVATAR)]

# halaman/tampilan leaderboard
class LeaderboardView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="white")
        self.controller = controller
        self.build_top_bar()   # bagian atas: tombol back & info koin
        self.build_title()     # judul leaderboard
        self.build_podium()    # podium juara 1, 2, 3
        self.build_list()      # daftar ranking 4-10
        self.muat_data()       # ambil data dari database dan tampilkan
        self.mulai_auto_refresh()   # mulai auto-refresh data tiap beberapa menit

    # ambil data terbaru lalu jadwalkan diri sendiri buat jalan lagi tiap 2 menit
    def mulai_auto_refresh(self):
        self.muat_data()
        self.after(120000, self.mulai_auto_refresh)  # 120000 ms = 2 menit, ganti sesuai kebutuhan

    # ambil data leaderboard & koin user, lalu tampilkan ke UI
    def muat_data(self):
        data = ambil_data_leaderboard()
        koin_saya = ambil_koin_user(self.controller.user_id)
        username_saya = ""
        for baris in data:
            if baris["user_id"] == self.controller.user_id:
                username_saya = baris["nama"]
        self.tampilkan_data(data, koin_saya, username_saya)

    # bikin bagian atas halaman: tombol kembali, badge koin, tombol tambah koin (ke toko)
    def build_top_bar(self):
        top = tk.Frame(self, bg="white")
        top.pack(fill="x", padx=15, pady=(15, 0))

        tk.Button(top, text="←", font=("Arial", 16), bg="white", fg="#333333",
                  bd=0, activebackground="white", activeforeground="#333333",
                  command=self.controller.go_back).pack(side="left")

        right = tk.Frame(top, bg="white")
        right.pack(side="right")

        coin_badge = tk.Canvas(right, width=90, height=25, bg="white", highlightthickness=0)
        coin_badge.pack(side="left", padx=(0, 8))
        rounded_rect(coin_badge, 1, 1, 89, 24, 12, fill="#FFF3D6", outline="")
        gambar_koin(coin_badge, 20, 12, radius=8)
        self.coin_text_id = coin_badge.create_text(55, 12, text="0", font=("Arial", 12, "bold"))
        self.coin_badge = coin_badge

        btn_frame = tk.Frame(right, width=20, height=20, bg="#27AE60")
        btn_frame.pack(side="left")
        btn_frame.pack_propagate(False)

        btn_plus = tk.Button(btn_frame, text="+", font=("Arial", 11, "bold"),
                      bg="#27AE60", fg="white", activebackground="#219150",
                      activeforeground="white", relief="flat", bd=0,
                      cursor="hand2", command=self.buka_toko)
        btn_plus.pack(fill="both", expand=True)

    # pindah ke halaman toko
    def buka_toko(self):
        self.controller.buka_toko()

    # bikin judul "LEADERBOARD" beserta garis hiasan
    def build_title(self):
        tk.Label(self, text="LEADERBOARD", bg="white", fg="#1a1a2e",
                 font=("Arial", 20, "bold")).pack(pady=(10, 2))

        deco = tk.Canvas(self, width=200, height=16, bg="white", highlightthickness=0)
        deco.pack()
        deco.create_line(10, 8, 90, 8, fill="#E0B33A", dash=(3, 2))
        deco.create_text(100, 8, text="★", fill="#E0B33A", font=("Arial", 10))
        deco.create_line(110, 8, 190, 8, fill="#E0B33A", dash=(3, 2))

    # bikin 3 kartu podium buat rank 1, 2, 3
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

    # bikin satu kartu podium (canvas + avatar + nama + skor)
    def buat_kartu(self, parent, rank, bg, medali, avatar_bg, tinggi):
        lebar = 110
        canvas = tk.Canvas(parent, width=lebar, height=tinggi + 20, bg="white", highlightthickness=0)

        rounded_rect(canvas, 5, 20, lebar - 5, tinggi + 20, 15, fill=bg, outline=medali, width=2)
        canvas.create_oval(lebar / 2 - 15, 0, lebar / 2 + 15, 30, fill=medali, outline="white", width=2)
        canvas.create_text(lebar / 2, 15, text=str(rank), fill="white", font=("Arial", 12, "bold"))

        gambar_hexagon(canvas, lebar / 2, 73, radius=28, fill=avatar_bg)
        avatar_text_id = canvas.create_text(lebar / 2, 73, text="-", font=("Arial", 18, "bold"))

        nama_id = canvas.create_text(lebar / 2, 125, text="-", font=("Arial", 12, "bold"))

        koin_id = gambar_bintang(canvas, lebar / 2, 150, radius=9)
        skor_id = canvas.create_text(lebar / 2, 150, text="0", font=("Arial", 11))

        return {"canvas": canvas, "avatar": avatar_text_id, "nama": nama_id,
                "skor": skor_id, "koin": koin_id, "center_x": lebar / 2, "y_skor": 150}

    # geser posisi icon bintang & teks skor biar rapi di tengah
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

    # siapkan container kosong buat daftar ranking 4 ke bawah
    def build_list(self):
        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.list_frame = tk.Frame(container, bg="white")
        self.list_frame.pack(fill="both", expand=True)

    # isi data ke tampilan: update podium 1-3 dan render list ranking 4-10
    def tampilkan_data(self, data_leaderboard, koin_saya, username_saya):
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

        # bersihkan list lama sebelum render ulang
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        self.list_frame.columnconfigure(2, weight=1)

        # cuma tampilkan rank 4 sampai 10 di list bawah podium
        baris_ke = 0
        for item in data_leaderboard:
            if 3 < item["rank"] <= 10:
                self.buat_baris_list(item, baris_ke, is_saya=(item["nama"] == username_saya))
                baris_ke += 1

    # bikin satu baris di daftar ranking (nomor, avatar, nama, skor)
    def buat_baris_list(self, item, baris_ke, is_saya=False):
        warna_bg = "#E8F8ED" if is_saya else "white"
        warna_text = "#219653" if is_saya else "#1a1a2e"
        warna_avatar = ambil_warna_avatar(item["nama"])

        baris = tk.Frame(self.list_frame, bg=warna_bg)
        baris.grid(row=baris_ke, column=0, columnspan=4, sticky="ew", pady=1)
        baris.columnconfigure(2, weight=1)

        tk.Label(baris, text=str(item["rank"]), bg=warna_bg, fg=warna_text,
                 font=("Arial", 12, "bold"), width=3).grid(row=0, column=0, padx=(10, 5), pady=3)

        avatar = tk.Canvas(baris, width=28, height=28, bg=warna_bg, highlightthickness=0)
        avatar.grid(row=0, column=1, padx=8, pady=3)
        gambar_hexagon(avatar, 14, 14, radius=13, fill=warna_avatar)
        avatar.create_text(14, 14, text=item["nama"][0].upper(), font=("Arial", 10, "bold"))

        # kasih label "(Anda)" kalau ini baris user yang sedang login
        nama_text = f"{item['nama']} (Anda)" if is_saya else item["nama"]
        tk.Label(baris, text=nama_text, bg=warna_bg, fg=warna_text,
                 font=("Arial", 12, "bold"), anchor="w").grid(row=0, column=2, sticky="w", padx=8, pady=3)

        kanan = tk.Frame(baris, bg=warna_bg)
        kanan.grid(row=0, column=3, sticky="e", padx=12, pady=3)
        tk.Label(kanan, text=f"{item['skor']:,}".replace(",", "."), bg=warna_bg, fg=warna_text,
                 font=("Arial", 12, "bold")).pack(side="right", padx=(4, 0))

        bintang_canvas = tk.Canvas(kanan, width=16, height=16, bg=warna_bg, highlightthickness=0)
        bintang_canvas.pack(side="right")
        gambar_bintang(bintang_canvas, 8, 8, radius=6)

        # garis pemisah antar baris
        garis = tk.Frame(self.list_frame, bg="#F0F0F0", height=1)
        garis.grid(row=baris_ke, column=0, columnspan=4, sticky="sew")


# class utama aplikasi, mengatur perpindahan antar halaman (leaderboard, toko, misi)
class App(tk.Tk):
    def __init__(self, user_id):
        super().__init__()
        self.geometry("400x700")
        self.user_id = user_id

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        # semua halaman ditumpuk pakai place(), lalu ditampilkan pakai tkraise()
        self.leaderboard_frame = LeaderboardView(self.container, self)
        self.toko_frame = toko_view.MisiPemainBaruView(self.container, self)
        self.misi_frame = misi_pemain_baru_view.MisiPemainBaruView(self.container, self)

        self.leaderboard_frame.place(relwidth=1, relheight=1)
        self.toko_frame.place(relwidth=1, relheight=1)
        self.misi_frame.place(relwidth=1, relheight=1)

        self.frame = self.leaderboard_frame
        self.riwayat_halaman = []  # buat nyimpen histori halaman biar bisa "go back"
        self.halaman_sekarang = self.leaderboard_frame
        self.leaderboard_frame.tkraise()

    # pindah ke halaman toko, simpan halaman sebelumnya ke riwayat
    def buka_toko(self):
        self.riwayat_halaman.append(self.halaman_sekarang)
        self.halaman_sekarang = self.toko_frame
        self.toko_frame.tkraise()

    # pindah ke halaman misi harian, simpan halaman sebelumnya ke riwayat
    def buka_misi(self):
        self.riwayat_halaman.append(self.halaman_sekarang)
        self.halaman_sekarang = self.misi_frame
        self.misi_frame.tkraise()

    # kembali ke halaman sebelumnya berdasarkan riwayat
    def go_back(self):
        if self.riwayat_halaman:
            self.halaman_sekarang = self.riwayat_halaman.pop()
        else:
            self.halaman_sekarang = self.leaderboard_frame
        self.halaman_sekarang.tkraise()


# jalankan aplikasi, mulai dari halaman leaderboard
if __name__ == "__main__":
    app = App(user_id=4)
    app.mainloop()