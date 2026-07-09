from os import name
import tkinter as tk
from tkinter import messagebox
import mysql.connector


def buat_koneksi():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_hangman"
    )


def ambil_koin_user(user_id):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute("SELECT coins FROM users WHERE id = %s", (user_id,))
    baris = cursor.fetchone()
    koneksi.close()
    return baris[0] if baris else 0


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


def beli_item_db(user_id, item_id, harga):
    koneksi = buat_koneksi()
    cursor = koneksi.cursor()
    cursor.execute(
        "UPDATE users SET coins = coins - %s WHERE id = %s AND coins >= %s",
        (harga, user_id, harga)
    )
    if cursor.rowcount == 0:
        koneksi.close()
        return False
    cursor.execute("""
        INSERT INTO user_inventory (user_id, item_id, jumlah)
        VALUES (%s, %s, 1)
        ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
    """, (user_id, item_id))
    koneksi.commit()
    koneksi.close()
    return True


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
    for item_id in item_ids:
        cursor.execute("""
            INSERT INTO user_inventory (user_id, item_id, jumlah)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
        """, (user_id, item_id))
    koneksi.commit()
    koneksi.close()
    return True


class TokoView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.current_page = "TOKO"
        self.selected_category = "SEMUA"
        self.coins = 0
        self.db_items = []

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

        self.tab_frame = tk.Frame(self, bg="#F5F5F5", highlightbackground="#F5F5F5", highlightthickness=2)
        self.tab_frame.pack(fill="x", padx=15, pady=10)

        self.btn_tab_toko = tk.Button(self.tab_frame, text="TOKO", font=("Arial", 10, "bold"), bd=0, height=2,
                                       command=lambda: self.switch_page("TOKO"))
        self.btn_tab_toko.pack(side="left", expand=True, fill="x")

        self.btn_tab_item = tk.Button(self.tab_frame, text="ITEM SAYA", font=("Arial", 10, "bold"), bd=0, height=2,
                                       command=lambda: self.switch_page("ITEM SAYA"))
        self.btn_tab_item.pack(side="right", expand=True, fill="x")

        self.main_area = tk.Frame(self, bg="white")
        self.main_area.pack(fill="x", expand=False, padx=15, pady=5)

        self.side_cat_frame = tk.Frame(self.main_area, bg="white")
        self.side_cat_frame.pack(side="left", fill="y", padx=(0, 10), anchor="n")

        self.cat_buttons = {}
        for cat in ["SEMUA", "BANTUAN", "WAKTU", "HEALING"]:
            btn = tk.Button(self.side_cat_frame, text=cat, font=("Arial", 8, "bold"), bd=0, width=10, height=2,
                             command=lambda c=cat: self.filter_category(c))
            btn.pack(pady=2, fill="x")
            self.cat_buttons[cat] = btn

        self.grid_container = tk.Frame(self.main_area, bg="white", bd=1)
        self.grid_container.pack(side="right", fill="both", expand=True)

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

        self.refresh_ui()

    def tkraise(self, aboveThis=None):
        super().tkraise(aboveThis)
        self.populate_data()
        self.refresh_ui()

    def populate_data(self, data=None):
        if self.controller.user_aktif:
            user_id = self.controller.user_aktif["id"]
            self.coins = ambil_koin_user(user_id)
            self.db_items = ambil_semua_item(user_id)
            self.coin_lbl.configure(text=self.format_koin())

    def switch_page(self, page_name):
        self.current_page = page_name
        self.refresh_ui()

    def filter_category(self, category_name):
        self.selected_category = category_name
        self.refresh_ui()

    def kembali(self):
        self.controller.go_back()

    def buka_misi_harian(self):
        self.controller.buka_misi()

    def format_koin(self):
        return f"{self.coins:,}".replace(",", ".")

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

    def _buat_tombol_tambah_misi(self, parent, on_click):
        size = 28
        canvas = tk.Canvas(parent, width=size, height=size, bg="white", highlightthickness=0, cursor="hand2")
        self._gambar_kotak_bulat(canvas, 1, 1, size - 1, size - 1, radius=8, fill="#4CAF50", outline="#4CAF50")
        canvas.create_text(size / 2, size / 2, text="+", font=("Arial", 13, "bold"), fill="white")
        canvas.bind("<Button-1>", lambda e: on_click())
        return canvas

    def _gambar_kotak_bulat(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1,
        ]
        return canvas.create_polygon(points, smooth=True, **kwargs)

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
        self.coins -= itm["harga"]
        itm["owned_qty"] += 1
        self.coin_lbl.configure(text=self.format_koin())
        self.refresh_ui()

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

    def refresh_ui(self):
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

        for cat, btn in self.cat_buttons.items():
            if cat == self.selected_category:
                btn.configure(bg="#2196F3", fg="white", activebackground="#2196F3", activeforeground="white")
            else:
                btn.configure(bg="#F5F5F5", fg="black", activebackground="#E0E0E0", activeforeground="black")

        for widget in self.grid_container.winfo_children():
            widget.destroy()

        filtered_items = []
        for itm in self.db_items:
            if self.current_page == "ITEM SAYA":
                if itm["owned_qty"] > 0:
                    filtered_items.append(itm)
            else:
                if self.selected_category == "SEMUA" or itm["kategori"] == self.selected_category:
                    filtered_items.append(itm)

        for idx, itm in enumerate(filtered_items):
            r, c = idx // 3, idx % 3

            box = tk.Frame(self.grid_container, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
            box.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)

            lbl_name = tk.Label(box, text=itm["nama"], font=("Arial", 7, "bold"), bg="white", fg="black", justify="center")
            lbl_name.pack(pady=(12, 2))

            lbl_icon = tk.Label(box, text=itm["icon"], font=("Segoe UI Emoji", 20), bg="white", fg=itm["color"])
            lbl_icon.pack(pady=10)

            if self.current_page == "TOKO":
                tag_harga = self._buat_tag_harga(box, itm["harga"], lambda itm=itm: self.beli_item(itm))
                tag_harga.pack(fill="x", side="bottom", padx=8, pady=(15, 8))
            else:
                lbl_bottom = tk.Label(box, text=f"x{itm['owned_qty']}", font=("Arial", 8, "bold"), bg="white", fg="black", pady=4)
                lbl_bottom.pack(fill="x", side="bottom", pady=(15, 4))

        for i in range(2):
            self.grid_container.grid_rowconfigure(i, weight=0, minsize=135)
        for i in range(3):
            self.grid_container.grid_columnconfigure(i, weight=1, minsize=80)


if __name__ == "__main__":

    class DummyController:
        def __init__(self, container):
            self.container = container
            self.user_aktif = {"id": 4, "username": "test", "coins": 0}
            self.toko_frame = TokoView(container, self)
            self.toko_frame.place(relwidth=1, relheight=1)
            self.toko_frame.populate_data()
            self.toko_frame.refresh_ui()
            self.toko_frame.tkraise()

        def go_back(self):
            self.toko_frame.tkraise()

        def buka_misi(self):
            messagebox.showinfo("Info", "Testing mandiri, halaman misi belum terhubung.")

    root = tk.Tk()
    root.geometry("400x700")
    controller = DummyController(root)
    root.mainloop()