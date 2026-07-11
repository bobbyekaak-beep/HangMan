import tkinter as tk
from tkinter import messagebox
from database.koneksi import hubungkan_database
from audio.sound_manager import putar_sfx


def ambil_koin_user(user_id):
    koneksi = hubungkan_database()
    if koneksi is None:
        return 0
    cursor = None
    try:
        cursor = koneksi.cursor()
        cursor.execute("SELECT coins FROM users WHERE id = %s", (user_id,))
        baris = cursor.fetchone()
        return baris[0] if baris else 0
    except Exception as e:
        print(f"[DATABASE] Error mengambil koin user: {e}")
        return 0
    finally:
        if cursor is not None:
            cursor.close()
        koneksi.close()


def ambil_semua_item(user_id):
    koneksi = hubungkan_database()
    if koneksi is None:
        return []
    cursor = None
    try:
        cursor = koneksi.cursor(dictionary=True)
        cursor.execute("""
            SELECT items.id, items.nama, items.icon, items.color, items.harga, items.kategori,
                   COALESCE(user_inventory.jumlah, 0) AS owned_qty
            FROM items
            LEFT JOIN user_inventory
              ON user_inventory.item_id = items.id AND user_inventory.user_id = %s
            ORDER BY items.id
        """, (user_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"[DATABASE] Error mengambil item toko: {e}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        koneksi.close()


def beli_item_db(user_id, item_id, harga):
    koneksi = hubungkan_database()
    if koneksi is None:
        return False
    cursor = None
    try:
        cursor = koneksi.cursor()
        cursor.execute(
            "UPDATE users SET coins = coins - %s WHERE id = %s AND coins >= %s",
            (harga, user_id, harga)
        )
        if cursor.rowcount == 0:
            return False
        cursor.execute("""
            INSERT INTO user_inventory (user_id, item_id, jumlah)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
        """, (user_id, item_id))
        koneksi.commit()
        return True
    except Exception as e:
        print(f"[DATABASE] Error membeli item: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        koneksi.close()


def beli_paket_hemat_db(user_id, harga, item_ids):
    koneksi = hubungkan_database()
    if koneksi is None:
        return False
    cursor = None
    try:
        cursor = koneksi.cursor()
        cursor.execute(
            "UPDATE users SET coins = coins - %s WHERE id = %s AND coins >= %s",
            (harga, user_id, harga)
        )
        if cursor.rowcount == 0:
            return False
        for item_id in item_ids:
            cursor.execute("""
                INSERT INTO user_inventory (user_id, item_id, jumlah)
                VALUES (%s, %s, 1)
                ON DUPLICATE KEY UPDATE jumlah = jumlah + 1
            """, (user_id, item_id))
        koneksi.commit()
        return True
    except Exception as e:
        print(f"[DATABASE] Error membeli paket hemat: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        koneksi.close()


class TokoView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.current_page = "TOKO"
        self.selected_category = "SEMUA"
        self.coins = 0
        self.db_items = []

        self.header_frame = tk.Frame(self, bg="white")
        self.header_frame.pack(fill="x", ipady=10, pady=(0, 20))

        tk.Button(self.header_frame, text="←", font=("Arial", 17, "bold"), bg="white", fg="#333333",
                  bd=0, activebackground="white", activeforeground="#333333",
                  command=self.kembali).pack(side="left", padx=10)

        self.coin_frame = tk.Frame(self.header_frame, bg="white")
        self.coin_frame.pack(side="right", padx=20)

        self.coin_lbl = tk.Label(self.coin_frame, text=self.format_koin(), font=("Arial", 12, "bold"),
                                  bg="white", fg="#FF9800")
        self.coin_lbl.pack(side="left")

        self.tab_frame = tk.Frame(self, bg="#F5F5F5", highlightbackground="#F5F5F5", highlightthickness=2)
        self.tab_frame.pack(fill="x", padx=(12, 21), pady=10)

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

        self.btn_bundle_price = self._buat_tag_harga(self.bundle_row, 150, self.beli_paket_hemat)
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
        putar_sfx("klik.mp3")
        self.current_page = page_name
        self.refresh_ui()

    def filter_category(self, category_name):
        putar_sfx("klik.mp3")
        self.selected_category = category_name
        self.refresh_ui()

    def kembali(self):
        putar_sfx("klik.mp3")
        self.controller.go_back()

    def format_koin(self):
        return f"💰 {self.coins:,}".replace(",", ".")

    def _buat_tag_harga(self, parent, harga, on_click):
        tag = tk.Frame(parent, bg="#FFFDE7", cursor="hand2")
        koin = tk.Label(tag, text="💰", font=("Segoe UI Emoji", 9), bg="#FFFDE7", fg="#FFC107", anchor="center")
        koin.pack(side="left", padx=(8, 4), pady=6)
        lbl = tk.Label(tag, text=str(harga), font=("Arial", 8, "bold"), bg="#FFFDE7", fg="black", anchor="center")
        lbl.pack(side="left", padx=(0, 8), pady=6)
        for w in (tag, koin, lbl):
            w.bind("<Button-1>", lambda e: on_click())
        return tag

    def beli_item(self, itm):
        putar_sfx("klik.mp3")
        nama_item = itm["nama"].replace("\n", " ")
        yakin = messagebox.askyesno("Konfirmasi Pembelian",
                                     f"Apakah anda yakin ingin membeli {nama_item} seharga {itm['harga']} koin?")
        if not yakin:
            return
        if self.coins < itm["harga"]:
            messagebox.showwarning("Koin Tidak Cukup", "Koin kamu tidak cukup untuk membeli item ini.")
            return
        user_id = self.controller.user_aktif["id"]
        berhasil = beli_item_db(user_id, itm["id"], itm["harga"])
        if not berhasil:
            messagebox.showwarning("Gagal", "Pembelian tidak berhasil, coba lagi.")
            return
        self.populate_data()
        self.refresh_ui()

    def beli_paket_hemat(self):
        putar_sfx("klik.mp3")
        harga_paket = 150
        yakin = messagebox.askyesno("Konfirmasi Pembelian",
                                     f"Apakah anda yakin ingin membeli Paket Hemat seharga {harga_paket} koin?")
        if not yakin:
            return
        if self.coins < harga_paket:
            messagebox.showwarning("Koin Tidak Cukup", "Koin kamu tidak cukup untuk membeli paket hemat ini.")
            return
        item_ids = [itm["id"] for itm in self.db_items[:3]]
        user_id = self.controller.user_aktif["id"]
        berhasil = beli_paket_hemat_db(user_id, harga_paket, item_ids)
        if not berhasil:
            messagebox.showwarning("Gagal", "Pembelian tidak berhasil, coba lagi.")
            return
        self.populate_data()
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