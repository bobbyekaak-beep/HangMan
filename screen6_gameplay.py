import customtkinter as ctk
import random

class Screen6Gameplay(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#F0F4F6")
        self.parent = parent

        self.kata_rahasia = "HARIMAU"
        self.huruf_ditebak = set()
        self.hp_player,   self.hp_player_max   = 100,  100
        self.hp_musuh,    self.hp_musuh_max     = 100,  100
        self.sisa_waktu = 90  # 01:30

        self.stok_hint  = 2
        self.stok_waktu = 2
        self.stok_heal  = 3

        self.tebakan_benar = 0
        self.tebakan_salah = 0
        self.game_selesai  = False

        self.setup_ui()
        self.update_timer()

    # ══════════════════════════════════════════════════════════════
    #  UI — sama persis dengan mockup
    # ══════════════════════════════════════════════════════════════
    def setup_ui(self):

        # ── 1. TOP HUD: HP KAMU | TIMER | HP MUSUH ───────────────
        hud = ctk.CTkFrame(self, fg_color="transparent")
        hud.pack(fill="x", padx=12, pady=(12, 6))

        # HP Kamu (kiri)
        kiri = ctk.CTkFrame(hud, fg_color="transparent")
        kiri.pack(side="left")

        ctk.CTkLabel(kiri, text="HP KAMU",
                     font=("Arial", 9, "bold"), text_color="#555555").pack(anchor="w")

        self.bar_p = ctk.CTkProgressBar(kiri, width=105, height=18,
                                         progress_color="#4CAF50",
                                         fg_color="#D0D0D0", corner_radius=4)
        self.bar_p.pack()
        self.bar_p.set(self.hp_player / self.hp_player_max)

        self.lbl_hp_p = ctk.CTkLabel(kiri,
                                      text=f"{self.hp_player}/{self.hp_player_max}",
                                      font=("Arial", 9), text_color="#333333")
        self.lbl_hp_p.pack(anchor="w")

        # Timer (tengah)
        self.lbl_timer = ctk.CTkLabel(hud, text="⏱  01:30",
                                       font=("Arial", 15, "bold"),
                                       text_color="#3E2723")
        self.lbl_timer.pack(side="left", expand=True)

        # HP Musuh (kanan)
        kanan = ctk.CTkFrame(hud, fg_color="transparent")
        kanan.pack(side="right")

        ctk.CTkLabel(kanan, text="HP MUSUH",
                     font=("Arial", 9, "bold"), text_color="#555555").pack(anchor="e")

        self.bar_g = ctk.CTkProgressBar(kanan, width=105, height=18,
                                         progress_color="#E53935",
                                         fg_color="#D0D0D0", corner_radius=4)
        self.bar_g.pack()
        self.bar_g.set(self.hp_musuh / self.hp_musuh_max)

        self.lbl_hp_g = ctk.CTkLabel(kanan,
                                      text=f"{self.hp_musuh}/{self.hp_musuh_max}",
                                      font=("Arial", 9), text_color="#333333")
        self.lbl_hp_g.pack(anchor="e")

        # ── 2. STATUS BANNER (BENAR / SALAH / info) ──────────────
        self.status_banner = ctk.CTkFrame(self, fg_color="#1E88E5",
                                           corner_radius=6, height=30)
        self.status_banner.pack(fill="x", padx=12, pady=(4, 2))
        self.status_banner.pack_propagate(False)

        self.lbl_status = ctk.CTkLabel(self.status_banner,
                                        text="MULAI PERMAINAN!",
                                        font=("Arial", 11, "bold"),
                                        text_color="white")
        self.lbl_status.pack(expand=True)

        # ── 3. INFO LEVEL & KATEGORI ──────────────────────────────
        info_frame = ctk.CTkFrame(self, fg_color="white",
                                   corner_radius=10, border_width=1,
                                   border_color="#E0E0E0")
        info_frame.pack(fill="x", padx=12, pady=(4, 2))

        ctk.CTkLabel(info_frame, text="LEVEL 5",
                     font=("Arial", 13, "bold"),
                     text_color="#1E88E5").pack(pady=(8, 0))
        ctk.CTkLabel(info_frame, text="Kategori: Hewan",
                     font=("Arial", 11),
                     text_color="#555555").pack(pady=(0, 8))

        # ── 4. SLOT KATA RAHASIA ──────────────────────────────────
        self.word_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.word_frame.pack(pady=14)
        self.update_slots()

        # ── 5. KETERANGAN HURUF DITEBAK ──────────────────────────
        self.lbl_ditebak = ctk.CTkLabel(self,
                                         text="Huruf sudah ditebak: -",
                                         font=("Arial", 10),
                                         text_color="#777777")
        self.lbl_ditebak.pack()

        # ── 6. KEYBOARD A–Z ──────────────────────────────────────
        self.kb_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.kb_frame.pack(pady=10)
        self.keys = {}
        self.build_keyboard()

        # ── 7. ITEM BAR BAWAH ─────────────────────────────────────
        self.item_bar = ctk.CTkFrame(self, fg_color="white",
                                      corner_radius=12, border_width=1,
                                      border_color="#E0E0E0", height=75)
        self.item_bar.pack(side="bottom", fill="x", padx=12, pady=10)
        self.item_bar.pack_propagate(False)
        self.render_bottom_items()

    # ── Slot huruf ────────────────────────────────────────────────
    def update_slots(self):
        for w in self.word_frame.winfo_children():
            w.destroy()

        for char in self.kata_rahasia:
            terbuka = char in self.huruf_ditebak
            box = ctk.CTkFrame(self.word_frame,
                                fg_color="#FFFFFF" if terbuka else "transparent",
                                border_width=0 if not terbuka else 1,
                                border_color="#B0BEC5",
                                width=38, height=44, corner_radius=6)
            box.pack(side="left", padx=5)
            box.pack_propagate(False)

            ctk.CTkLabel(box,
                         text=char if terbuka else "_",
                         font=("Arial", 22, "bold"),
                         text_color="#1565C0" if terbuka else "#333333"
                         ).pack(expand=True)

        # Update label huruf sudah ditebak
        if self.huruf_ditebak:
            huruf_str = ", ".join(sorted(self.huruf_ditebak))
            self.lbl_ditebak.configure(text=f"Huruf sudah ditebak: {huruf_str}")

    # ── Keyboard ──────────────────────────────────────────────────
    def build_keyboard(self):
        layout = [
            ["A","B","C","D","E","F","G","H","I"],
            ["J","K","L","M","N","O","P","Q","R"],
            ["S","T","U","V","W","X","Y","Z"],
        ]
        for row in layout:
            f = ctk.CTkFrame(self.kb_frame, fg_color="transparent")
            f.pack(pady=2)
            for char in row:
                btn = ctk.CTkButton(
                    f, text=char,
                    font=("Arial", 11, "bold"),
                    fg_color="#FFFFFF", text_color="black",
                    hover_color="#E3F2FD",
                    border_width=1, border_color="#BDBDBD",
                    width=36, height=36, corner_radius=6,
                    command=lambda c=char: self.proses_tebakan(c))
                btn.pack(side="left", padx=1)
                self.keys[char] = btn

    # ── Item bar ──────────────────────────────────────────────────
    def render_bottom_items(self):
        for w in self.item_bar.winfo_children():
            w.destroy()

        items = [
            ("PETUNJUK\nHURUF", f"x{self.stok_hint}",  "#FFF9C4", self.aksi_hint),
            ("TAMBAH\nWAKTU",   f"x{self.stok_waktu}", "#E3F2FD", self.aksi_waktu),
            ("PULIHKAN\nHP",    f"x{self.stok_heal}",  "#FCE4EC", self.aksi_heal),
        ]

        for i, (nama, stok, warna_bg, aksi) in enumerate(items):
            col = ctk.CTkFrame(self.item_bar, fg_color="transparent")
            col.grid(row=0, column=i, sticky="nsew", padx=8, pady=8)

            kotak = ctk.CTkButton(
                col, text=f"{nama}\n{stok}",
                font=("Arial", 9, "bold"),
                fg_color=warna_bg, text_color="#333333",
                hover_color="#E0E0E0",
                border_width=1, border_color="#CFD8DC",
                height=55, corner_radius=8,
                command=aksi)
            kotak.pack(fill="both", expand=True)

        self.item_bar.columnconfigure((0, 1, 2), weight=1)

    # ══════════════════════════════════════════════════════════════
    #  LOGIKA TEBAKAN
    # ══════════════════════════════════════════════════════════════
    def proses_tebakan(self, h):
        if h in self.huruf_ditebak or self.game_selesai:
            return
        self.huruf_ditebak.add(h)

        if h in self.kata_rahasia:
            jumlah = self.kata_rahasia.count(h)
            damage = jumlah * 20

            self.tebakan_benar += 1
            self.keys[h].configure(fg_color="#4CAF50", text_color="white",
                                    hover_color="#4CAF50", state="disabled")
            self._set_banner("#4CAF50", f"✅  TEBAKAN BENAR!  -{damage} HP Musuh")

            self.hp_musuh = max(0, self.hp_musuh - damage)
            self.bar_g.set(self.hp_musuh / self.hp_musuh_max)
            self.lbl_hp_g.configure(text=f"{self.hp_musuh}/{self.hp_musuh_max}")

        else:
            self.tebakan_salah += 1
            self.keys[h].configure(fg_color="#E53935", text_color="white",
                                    hover_color="#E53935", state="disabled")
            self._set_banner("#E53935", "❌  TEBAKAN SALAH!  -20 HP Kamu")

            self.hp_player = max(0, self.hp_player - 20)
            self.bar_p.set(self.hp_player / self.hp_player_max)
            self.lbl_hp_p.configure(text=f"{self.hp_player}/{self.hp_player_max}")

            # Efek salah: getaran window + flash merah progress bar
            self.guncang_window(10)
            self.flash_bar_merah(4)

        self.update_slots()
        self.cek_kondisi()

    # ══════════════════════════════════════════════════════════════
    #  CEK KONDISI MENANG / KALAH
    # ══════════════════════════════════════════════════════════════
    def cek_kondisi(self):
        if self.game_selesai:
            return

        kata_terbuka = all(c in self.huruf_ditebak for c in set(self.kata_rahasia))

        if kata_terbuka or self.hp_musuh <= 0:
            self.game_selesai = True
            self.hp_musuh = 0
            self.bar_g.set(0)
            self.lbl_hp_g.configure(text=f"0/{self.hp_musuh_max}")
            self._set_banner("#4CAF50", "🏆  KAMU MENANG!")

            skor = self.hitung_skor()
            if hasattr(self.parent, "set_hasil_game"):
                self.parent.set_hasil_game(
                    kata          = self.kata_rahasia,
                    skor          = skor,
                    sisa_waktu    = self.sisa_waktu,
                    hp_player     = self.hp_player,
                    tebakan_benar = self.tebakan_benar,
                    tebakan_salah = self.tebakan_salah,
                    huruf_ditebak = set(self.huruf_ditebak),
                    mode          = "victory",
                )
            self.after(900, lambda: self.parent.switch_screen("screen9_result"))

        elif self.hp_player <= 0 or self.sisa_waktu <= 0:
            self.game_selesai = True
            self._set_banner("#E53935", "💀  GAME OVER!")
            if hasattr(self.parent, "set_hasil_game"):
                self.parent.set_hasil_game(
                    kata          = self.kata_rahasia,
                    skor          = 0,
                    sisa_waktu    = 0,
                    hp_player     = 0,
                    tebakan_benar = self.tebakan_benar,
                    tebakan_salah = self.tebakan_salah,
                    huruf_ditebak = set(self.huruf_ditebak),
                    mode          = "defeat",
                )
            self.after(500, lambda: self.parent.switch_screen("screen9_result"))

    # ══════════════════════════════════════════════════════════════
    #  SISTEM SKOR
    # ══════════════════════════════════════════════════════════════
    def hitung_skor(self):
        base        = self.tebakan_benar * 20
        bonus_waktu = self.sisa_waktu * 2
        bonus_hp    = self.hp_player
        penalti     = self.tebakan_salah * 15
        return max(0, base + bonus_waktu + bonus_hp - penalti)

    # ══════════════════════════════════════════════════════════════
    #  ITEM ACTIONS
    # ══════════════════════════════════════════════════════════════
    def aksi_hint(self):
        if self.stok_hint <= 0 or self.game_selesai:
            self._notif_habis("💡 Petunjuk habis! Beli di Toko.")
            return
        for c in self.kata_rahasia:
            if c not in self.huruf_ditebak:
                self.stok_hint -= 1
                self.render_bottom_items()
                self.proses_tebakan(c)
                break

    def aksi_waktu(self):
        if self.stok_waktu <= 0 or self.game_selesai:
            self._notif_habis("🕒 Tambah Waktu habis! Beli di Toko.")
            return
        self.stok_waktu -= 1
        self.sisa_waktu += 30
        self.render_bottom_items()

    def aksi_heal(self):
        if self.stok_heal <= 0 or self.game_selesai:
            self._notif_habis("❤️ Pulihkan HP habis! Beli di Toko.")
            return
        self.stok_heal -= 1
        self.hp_player = min(self.hp_player_max, self.hp_player + 20)
        self.bar_p.set(self.hp_player / self.hp_player_max)
        self.lbl_hp_p.configure(text=f"{self.hp_player}/{self.hp_player_max}")
        self.render_bottom_items()

    def _notif_habis(self, pesan):
        self._set_banner("#FF8F00", pesan)
        self.after(2000, lambda: self._set_banner("#1E88E5", "Pilih huruf!"))

    # ══════════════════════════════════════════════════════════════
    #  EFEK VISUAL
    # ══════════════════════════════════════════════════════════════
    def guncang_window(self, loop):
        if loop > 0:
            try:
                root  = self.winfo_toplevel()
                x, y  = root.winfo_x(), root.winfo_y()
                root.geometry(f"+{x + random.choice([-7, 7])}+{y}")
                self.after(28, lambda: self.guncang_window(loop - 1))
            except Exception:
                pass

    def flash_bar_merah(self, sisa):
        """Kedipkan progress bar HP player merah saat tebakan salah."""
        if sisa > 0:
            warna = "#E53935" if sisa % 2 == 0 else "#4CAF50"
            self.bar_p.configure(progress_color=warna)
            self.after(90, lambda: self.flash_bar_merah(sisa - 1))
        else:
            self.bar_p.configure(progress_color="#4CAF50")

    def _set_banner(self, warna, teks):
        self.status_banner.configure(fg_color=warna)
        self.lbl_status.configure(text=teks)

    # ══════════════════════════════════════════════════════════════
    #  TIMER
    # ══════════════════════════════════════════════════════════════
    def update_timer(self):
        if self.game_selesai:
            return
        if self.sisa_waktu > 0 and self.hp_player > 0 and self.hp_musuh > 0:
            self.sisa_waktu -= 1
            m, s = divmod(self.sisa_waktu, 60)
            self.lbl_timer.configure(
                text=f"⏱  {m:02d}:{s:02d}",
                text_color="#E53935" if self.sisa_waktu <= 10 else "#3E2723")
            self.after(1000, self.update_timer)
        else:
            self.cek_kondisi()