import tkinter as tk
from tkinter import messagebox
import mysql.connector


# Membuka koneksi baru ke database MySQL
def buat_koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_hangman"
    )


# Mengambil jumlah koin milik user berdasarkan user_id
def ambil_koin_user(user_id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute("SELECT coins FROM users WHERE id = %s", (user_id,))
    baris = cursor.fetchone()
    koneksi.close()
    return baris[0] if baris else 0


# Mengambil semua item toko beserta jumlah yang sudah dimiliki user (JOIN dengan inventory)
def ambil_semua_item(user_id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor(dictionary=True)
    cursor.execute("""
        SELECT items.id, items.nama, items.icon, items.color, items.harga, items.kategori,
               COALESCE(user_inventory.jumlah, 0) AS owned_qty
        FROM items
        LEFT JOIN user_inventory
          ON user_inventory.item_id = items.id AND user_inventory.user_id = %s
    """, (user_id,))
    hasil = cursor.fetchall()
    koneksi.close()
    return hasil


# Memproses pembelian satu item: kurangi koin user, tambah item ke inventory
def beli_item_db(user_id, item_id, harga):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    # kurangi koin, syarat koin harus cukup (coins >= harga)
    cursor.execute(
        "UPDATE users SET coins = coins - %s WHERE id = %s AND coins >= %s",
        (harga, user_id, harga)
    )
    if cursor.rowcount == 0:
        # tidak ada baris terupdate berarti koin tidak cukup
        koneksi.close()
        return False
    # tambahkan item ke inventory, kalau sudah ada tinggal tambah jumlahnya
    cursor.execute("""
        INSERT INTO user_inventory (user_id, item_id, jumlah)
        VALUES (%s, %s, 1)
        ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
    """, (user_id, item_id))
    koneksi.commit()
    koneksi.close()
    return True


# Memproses pembelian paket hemat: kurangi koin user, tambah beberapa item sekaligus ke inventory
def beli_paket_hemat_db(user_id, harga, item_ids):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute(
        "UPDATE users SET coins = coins - %s WHERE id = %s AND coins >= %s",
        (harga, user_id, harga)
    )
    if cursor.rowcount == 0:
        koneksi.close()
        return False
    # loop untuk memasukkan setiap item dalam paket ke inventory
    for item_id in item_ids:
        cursor.execute("""
            INSERT INTO user_inventory (user_id, item_id, jumlah)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
        """, (user_id, item_id))
    koneksi.commit()
    koneksi.close()
    return True


# Frame utama halaman Toko (dipakai dalam sistem navigasi frame-stacking)
class MisiPemainBaruView(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg="white")
        self.controller = controller

        # state halaman: TOKO atau ITEM SAYA, serta kategori yang lagi difilter
        self.current_page = "TOKO"
        self.selected_category = "SEMUA"
        self.coins = ambil_koin_user(self.controller.user_id)
        self.db_items = ambil_semua_item(self.controller.user_id)

        # header atas: tombol kembali, tampilan koin, tombol misi harian
        self.header_frame = tk.Frame(self, bg="white")
        self.header_frame.pack(fill="x", pady=(15, 5), padx=15)

        tk.Button(self.header_frame, text="←", font=("Arial", 16), bg="white", fg="#333333",
          bd=0, activebackground="white", activeforeground="#333333",
          command=self.kembali).pack(side="left")
        self.coin_frame = tk.Frame(self.header_frame, bg="#F5F5F5")
        self.coin_gold = tk.Canvas(self.coin_frame, width=16, height=16, bg="#F5F5F5", highlightthickness=0)
        self.coin_gold.create_oval(1, 1, 15, 15, fill="#FFC107", outline="#FFA000")
        self.coin_gold.pack(side="left", padx=(8, 2), pady=4)
        self.coin_lbl = tk.Label(self.coin_frame, text=self.format_koin(), font=("Arial", 10, "bold"),
                                  bg="#F5F5F5", fg="black", padx=8, pady=4)
        self.coin_lbl.pack(side="left")

        self.btn_misi_harian = self._buat_tombol_tambah_misi(self.header_frame, self.buka_misi_harian)
        self.btn_misi_harian.pack(side="right")
        self.coin_frame.pack(side="right", padx=(0, 8))

        # tab untuk pindah antara halaman TOKO dan ITEM SAYA
        self.tab_frame = tk.Frame(self, bg="#F5F5F5", highlightbackground="#F5F5F5", highlightthickness=2)
        self.tab_frame.pack(fill="x", padx=15, pady=10)

        self.btn_tab_toko = tk.Button(self.tab_frame, text="TOKO", font=("Arial", 10, "bold"), bd=0, height=2,
                                       command=lambda: self.switch_page("TOKO"))
        self.btn_tab_toko.pack(side="left", expand=True, fill="x")

        self.btn_tab_item = tk.Button(self.tab_frame, text="ITEM SAYA", font=("Arial", 10, "bold"), bd=0, height=2,
                                       command=lambda: self.switch_page("ITEM SAYA"))
        self.btn_tab_item.pack(side="right", expand=True, fill="x")

        # area utama: sidebar kategori di kiri, grid item di kanan
        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(fill="x", expand=False, padx=15, pady=5)

        self.side_cat_frame = tk.Frame(self.main_area, bg="white")
        self.side_cat_frame.pack(side="left", fill="y", padx=(0, 10), anchor="n")

        # tombol filter kategori (SEMUA, BANTUAN, WAKTU, HEALING)
        self.cat_buttons = {}
        for cat in ["SEMUA", "BANTUAN", "WAKTU", "HEALING"]:
            btn = tk.Button(self.side_cat_frame, text=cat, font=("Arial", 8, "bold"), bd=0, width=10, height=2,
                             command=lambda c=cat: self.filter_category(c))
            btn.pack(pady=2, fill="x")
            self.cat_buttons[cat] = btn

        self.grid_container = tk.Frame(self.main_area, bg="white", bd=1)
        self.grid_container.pack(side="right", fill="both", expand=True)

        # panel paket hemat di bagian bawah
        self.paket_frame = tk.Frame(self, bg="white", highlightbackground="#E0E0E0", highlightthickness=1,
                                     bd=0, height=80)
        self.paket_frame.pack(fill="x", padx=15, pady=(20, 20), side="bottom")
        self.paket_frame.pack_propagate(False)

        self.lbl_paket_title = tk.Label(self.paket_frame, text="PAKET HEMAT", font=("Arial", 8, "bold"),
                                         bg="white", fg="gray")
        self.lbl_paket_title.pack(anchor="w", padx=10, pady=(6, 0))

        self.bundle_row = tk.Frame(self.paket_frame, bg="white")
        self.bundle_row.pack(fill="x", padx=10, pady=2)

        self.lbl_bundle_light = tk.Label(self.bundle_row, text="💡", font=("Segoe UI Emoji", 12), bg="white", fg="#FFC107")
        self.lbl_bundle_light.pack(side="left")

        tk.Label(self.bundle_row, text=" + ", font=("Arial", 11, "bold"), bg="white").pack(side="left")

        self.lbl_bundle_time = tk.Label(self.bundle_row, text="⏱", font=("Segoe UI Emoji", 12), bg="white", fg="#2196F3")
        self.lbl_bundle_time.pack(side="left")

        tk.Label(self.bundle_row, text=" + ", font=("Arial", 11, "bold"), bg="white").pack(side="left")

        self.lbl_love_fix = tk.Label(self.bundle_row, text="♥", font=("Segoe UI Emoji", 12, "bold"), bg="white", fg="#F44336")
        self.lbl_love_fix.pack(side="left")

        self.btn_bundle_price = self._buat_tombol_koin_hijau(self.bundle_row, 150, self.beli_paket_hemat)
        self.btn_bundle_price.pack(side="right")

        # render tampilan awal
        self.refresh_ui()

    # ganti halaman aktif (TOKO / ITEM SAYA) lalu render ulang
    def switch_page(self, page_name):
        self.current_page = page_name
        self.refresh_ui()

    # ganti kategori yang difilter lalu render ulang
    def filter_category(self, category_name):
        self.selected_category = category_name
        self.refresh_ui()

    # kembali ke frame sebelumnya lewat controller
    def kembali(self):
        self.controller.go_back()

    # buka frame misi harian lewat controller
    def buka_misi_harian(self):
        self.controller.buka_misi()

    # format angka koin jadi string dengan pemisah ribuan pakai titik
    def format_koin(self):
        return f"{self.coins:,}".replace(",", ".")

    # bikin widget tag harga (icon koin + angka) yang bisa diklik untuk beli item
    def _buat_tag_harga(self, parent, harga, on_click):
        tag = tk.Frame(parent, bg="#FFFDE7", cursor="hand2")
        koin = tk.Canvas(tag, width=12, height=12, bg="#FFFDE7", highlightthickness=0)
        koin.create_oval(1, 1, 11, 11, fill="#FFC107", outline="#FFA000")
        koin.pack(side="left", padx=(8, 4), pady=4)
        lbl = tk.Label(tag, text=str(harga), font=("Arial", 8, "bold"), bg="#FFFDE7", fg="black")
        lbl.pack(side="left", padx=(0, 8), pady=4)
        for w in (tag, koin, lbl):
            w.bind("<Button-1>", lambda e: on_click())
        return tag

    # bikin tombol hijau berisi harga untuk beli paket hemat
    def _buat_tombol_koin_hijau(self, parent, harga, on_click):
        tombol = tk.Frame(parent, bg="#4CAF50", cursor="hand2")
        koin = tk.Canvas(tombol, width=12, height=12, bg="#4CAF50", highlightthickness=0)
        koin.create_oval(1, 1, 11, 11, fill="#FFC107", outline="#FFA000")
        koin.pack(side="left", padx=(15, 4), pady=4)
        lbl = tk.Label(tombol, text=str(harga), font=("Arial", 9, "bold"), bg="#4CAF50", fg="white")
        lbl.pack(side="left", padx=(0, 15), pady=4)
        for w in (tombol, koin, lbl):
            w.bind("<Button-1>", lambda e: on_click())
        return tombol

    # bikin tombol bulat "+" di pojok header untuk buka misi harian
    def _buat_tombol_tambah_misi(self, parent, on_click):
        size = 28
        canvas = tk.Canvas(parent, width=size, height=size, bg="white", highlightthickness=0, cursor="hand2")
        self._gambar_kotak_bulat(canvas, 1, 1, size - 1, size - 1, radius=8, fill="#4CAF50", outline="#4CAF50")
        canvas.create_text(size / 2, size / 2, text="+", font=("Arial", 13, "bold"), fill="white")
        canvas.bind("<Button-1>", lambda e: on_click())
        return canvas

    # gambar kotak dengan sudut membulat di atas canvas (dipakai tombol misi)
    def _gambar_kotak_bulat(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

    # proses klik beli item: konfirmasi, cek koin cukup, update DB, lalu render ulang
    def beli_item(self, itm):
        nama_item = itm["nama"].replace("\n", " ")
        yakin = messagebox.askyesno("Konfirmasi Pembelian",
                                     f"Apakah anda yakin ingin membeli {nama_item} seharga {itm['harga']} koin?")
        if not yakin:
            return
        if self.coins < itm["harga"]:
            messagebox.showwarning("Koin Tidak Cukup", "Koin kamu tidak cukup untuk membeli item ini.")
            return
        berhasil = beli_item_db(self.controller.user_id, itm["id"], itm["harga"])
        if not berhasil:
            messagebox.showwarning("Gagal", "Pembelian tidak berhasil, coba lagi.")
            return
        # update tampilan koin dan jumlah item secara lokal biar tidak perlu query ulang
        self.coins -= itm["harga"]
        itm["owned_qty"] += 1
        self.coin_lbl.configure(text=self.format_koin())
        self.refresh_ui()

    # proses klik beli paket hemat: sama seperti beli_item tapi untuk 3 item sekaligus
    def beli_paket_hemat(self):
        harga_paket = 150
        yakin = messagebox.askyesno("Konfirmasi Pembelian",
                                     f"Apakah anda yakin ingin membeli Paket Hemat seharga {harga_paket} koin?")
        if not yakin:
            return
        if self.coins < harga_paket:
            messagebox.showwarning("Koin Tidak Cukup", "Koin kamu tidak cukup untuk membeli paket hemat ini.")
            return
        item_ids = [itm["id"] for itm in self.db_items[:3]]
        berhasil = beli_paket_hemat_db(self.controller.user_id, harga_paket, item_ids)
        if not berhasil:
            messagebox.showwarning("Gagal", "Pembelian tidak berhasil, coba lagi.")
            return
        self.coins -= harga_paket
        for itm in self.db_items[:3]:
            itm["owned_qty"] += 1
        self.coin_lbl.configure(text=self.format_koin())
        self.refresh_ui()

    # render ulang seluruh tampilan: tab aktif, tombol kategori, dan grid item sesuai filter
    def refresh_ui(self):
        # atur warna tab TOKO/ITEM SAYA sesuai halaman yang aktif
        if self.current_page == "TOKO":
            self.btn_tab_toko.configure(bg="#2196F3", fg="white", activebackground="#2196F3", activeforeground="white")
            self.btn_tab_item.configure(bg="#F5F5F5", fg="#757575", activebackground="#F5F5F5", activeforeground="#757575")
            self.side_cat_frame.pack(side="left", fill="y", padx=(0, 10), anchor="n")
            self.paket_frame.pack(fill="x", padx=15, pady=(20, 20), side="bottom")
        else:
            self.btn_tab_toko.configure(bg="#F5F5F5", fg="#757575", activebackground="#F5F5F5", activeforeground="#757575")
            self.btn_tab_item.configure(bg="#2196F3", fg="white", activebackground="#2196F3", activeforeground="white")
            self.side_cat_frame.pack_forget()
            self.paket_frame.pack_forget()

        # atur warna tombol kategori sesuai kategori yang lagi dipilih
        for cat, btn in self.cat_buttons.items():
            if cat == self.selected_category:
                btn.configure(bg="#2196F3", fg="white", activebackground="#2196F3", activeforeground="white")
            else:
                btn.configure(bg="#F5F5F5", fg="black", activebackground="#E0E0E0", activeforeground="black")

        # hapus semua kotak item lama sebelum digambar ulang
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        # tentukan item mana saja yang ditampilkan sesuai halaman dan kategori aktif
        filtered_items = []
        for itm in self.db_items:
            if self.current_page == "ITEM SAYA":
                if itm["owned_qty"] > 0:
                    filtered_items.append(itm)
            else:
                if self.selected_category == "SEMUA" or itm["kategori"] == self.selected_category:
                    filtered_items.append(itm)

        # gambar setiap item ke dalam grid 3 kolom
        for idx, itm in enumerate(filtered_items):
            r, c = idx // 3, idx % 3

            box = tk.Frame(self.grid_container, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
            box.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

            lbl_name = tk.Label(box, text=itm["nama"], font=("Arial", 7, "bold"), bg="white", fg="black", justify="center")
            lbl_name.pack(pady=(12, 2))

            lbl_icon = tk.Label(box, text=itm["icon"], font=("Segoe UI Emoji", 20), bg="white", fg=itm["color"])
            lbl_icon.pack(pady=10)

            # di halaman TOKO tampilkan tag harga (bisa diklik beli), di ITEM SAYA tampilkan jumlah dimiliki
            if self.current_page == "TOKO":
                tag_harga = self._buat_tag_harga(box, itm["harga"], lambda itm=itm: self.beli_item(itm))
                tag_harga.pack(fill="x", side="bottom", padx=8, pady=(15, 8))
            else:
                lbl_bottom = tk.Label(box, text=f"x{itm['owned_qty']}", font=("Arial", 8, "bold"), bg="white", fg="black", pady=4)
                lbl_bottom.pack(fill="x", side="bottom", pady=(15, 4))

        # atur ukuran baris dan kolom grid
        for i in range(2):
            self.grid_container.grid_rowconfigure(i, weight=0, minsize=135)
        for i in range(3):
            self.grid_container.grid_columnconfigure(i, weight=1, minsize=80)


# blok testing mandiri: jalankan file ini langsung untuk preview TokoView tanpa lewat App utama
if __name__ == "__main__":
    from bobby.page_misi_pemain_baru import misi_pemain_baru_view

    class DummyController:
        def __init__(self, container):
            self.container = container
            self.user_id = 4
            self.toko_frame = MisiPemainBaruView(container, self)
            self.misi_frame = misi_pemain_baru_view.MisiPemainBaruView(container, self)
            self.toko_frame.place(relwidth=1, relheight=1)
            self.misi_frame.place(relwidth=1, relheight=1)
            self.toko_frame.tkraise()

        def go_back(self):
            self.toko_frame.tkraise()

        def buka_misi(self):
            self.misi_frame.tkraise()

    root = tk.Tk()
    root.geometry("400x700")
    controller = DummyController(root)
    root.mainloop()