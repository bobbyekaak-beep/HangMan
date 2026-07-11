import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
from logic.page_game.level2logic import Level2Logic
from audio.sound_manager import putar_sfx, kecilkan_musik_latar, putar_sfx_hitung_mundur

class Screen7GameplayLevel2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#111827")
        self.parent = parent
        self.controller = controller

        self.logic = Level2Logic(self._ambil_user_id())
        self._run_id = 0

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Player.Horizontal.TProgressbar",
                             troughcolor="#1F2937", background="#10B981", thickness=18)
        self.style.configure("Enemy.Horizontal.TProgressbar",
                             troughcolor="#1F2937", background="#EF4444", thickness=18)

        self.keys = {}
        self.setup_ui()

        self.bind("<Key>", self.tekan_keyboard)
        self.focus_set()

    def _ambil_user_id(self):
        if self.controller is not None and hasattr(self.controller, "user_aktif") and self.controller.user_aktif is not None:
            return self.controller.user_aktif["id"]
        return None

    def on_show(self):
        kecilkan_musik_latar()
        try:
            self.logic = Level2Logic(self._ambil_user_id())
        except ValueError as e:
            messagebox.showerror("Gagal Memuat Soal", str(e))
            self.controller.go_back()
            return
        self._run_id += 1
        self.build_keyboard()
        self.bar_p['value'] = (self.logic.hp_player / self.logic.hp_player_max) * 100
        self.lbl_hp_p.configure(text=f"{self.logic.hp_player}/{self.logic.hp_player_max}")
        self.bar_g['value'] = (self.logic.hp_musuh / self.logic.hp_musuh_max) * 100
        self.lbl_hp_g.configure(text=f"{int(self.logic.hp_musuh)}/{self.logic.hp_musuh_max}")
        m, s = divmod(self.logic.sisa_waktu, 60)
        self.lbl_timer.configure(text=f"⏱  {m:02d}:{s:02d}", fg="#F59E0B")
        self.update_slots()
        self.render_bottom_items()
        self._set_banner("#FF6B00", "LEVEL 2 DIMULAI! SILAKAN TEBAK HURUF")
        self.focus_set()
        self.update_timer(self._run_id)

    def setup_ui(self):
        hud = tk.Frame(self, bg="#111827")
        hud.pack(fill="x", padx=14, pady=(14, 6))

        kiri = tk.Frame(hud, bg="#111827")
        kiri.pack(side="left")
        tk.Label(kiri, text="HP KAMU", bg="#111827", font=("Arial", 9, "bold"), fg="#9CA3AF").pack(anchor="w")

        self.bar_p = ttk.Progressbar(kiri, length=110, mode='determinate', style="Player.Horizontal.TProgressbar")
        self.bar_p.pack(pady=2)
        self.bar_p['value'] = (self.logic.hp_player / self.logic.hp_player_max) * 100

        self.lbl_hp_p = tk.Label(kiri, bg="#111827", text=f"{self.logic.hp_player}/{self.logic.hp_player_max}", font=("Arial", 9, "bold"), fg="#10B981")
        self.lbl_hp_p.pack(anchor="w")

        m, s = divmod(self.logic.sisa_waktu, 60)
        self.lbl_timer = tk.Label(hud, text=f"⏱  {m:02d}:{s:02d}", font=("Arial", 16, "bold"), fg="#F59E0B", bg="#111827")
        self.lbl_timer.pack(side="left", expand=True)

        kanan = tk.Frame(hud, bg="#111827")
        kanan.pack(side="right")
        tk.Label(kanan, text="HP MUSUH", bg="#111827", font=("Arial", 9, "bold"), fg="#9CA3AF").pack(anchor="e")

        self.bar_g = ttk.Progressbar(kanan, length=110, mode='determinate', style="Enemy.Horizontal.TProgressbar")
        self.bar_g.pack(pady=2)
        self.bar_g['value'] = (self.logic.hp_musuh / self.logic.hp_musuh_max) * 100

        self.lbl_hp_g = tk.Label(kanan, bg="#111827", text=f"{int(self.logic.hp_musuh)}/{self.logic.hp_musuh_max}", font=("Arial", 9, "bold"), fg="#EF4444")
        self.lbl_hp_g.pack(anchor="e")

        self.status_banner = tk.Frame(self, bg="#FF6B00", height=32)
        self.status_banner.pack(fill="x", padx=14, pady=(6, 4))
        self.status_banner.pack_propagate(False)

        self.lbl_status = tk.Label(self.status_banner, bg="#FF6B00", text="⚠️ MEMASUKI LEVEL 2: MODE HARD ⚠️", font=("Arial", 10, "bold"), fg="white")
        self.lbl_status.pack(expand=True)

        info_frame = tk.Frame(self, bg="#1F2937", highlightbackground="#374151", highlightthickness=1)
        info_frame.pack(fill="x", padx=14, pady=4)

        self.lbl_level = tk.Label(
            info_frame,
            bg="#1F2937",
            font=("Arial", 12, "bold"),
            fg="#FF8C00"
        )
        self.lbl_level.pack(pady=(6, 0))

        self.lbl_kategori = tk.Label(
            info_frame,
            bg="#1F2937",
            font=("Arial", 10, "bold"),
            fg="#60A5FA"
        )
        self.lbl_kategori.pack()

        self.lbl_petunjuk = tk.Label(
            info_frame,
            bg="#1F2937",
            font=("Arial", 9),
            fg="#9CA3AF",
            wraplength=350,
            justify="center"
        )
        self.lbl_petunjuk.pack(pady=(0,6))
        self.word_frame = tk.Frame(self, bg="#111827")
        self.word_frame.pack(pady=16)

        self.lbl_ditebak = tk.Label(self, bg="#111827", text="Huruf sudah ditebak: -", font=("Arial", 9), fg="#6B7280")
        self.lbl_ditebak.pack()

        self.kb_frame = tk.Frame(self, bg="#111827")
        self.kb_frame.pack(pady=12)
        self.build_keyboard()

        self.item_bar = tk.Frame(self, bg="#1F2937", highlightbackground="#374151", highlightthickness=1, height=75)
        self.item_bar.pack(side="bottom", fill="x", padx=14, pady=14)
        self.item_bar.pack_propagate(False)
        self.render_bottom_items()

        self.update_slots()

    def update_slots(self):
        for w in self.word_frame.winfo_children():
            w.destroy()

        for char in self.logic.kata_rahasia:
            terbuka = char in self.logic.huruf_ditebak
            box = tk.Frame(self.word_frame, bg="#1F2937" if terbuka else "#374151",
                           highlightbackground="#00E5FF" if terbuka else "#4B5563", highlightthickness=1, width=38, height=44)
            box.pack(side="left", padx=3)
            box.pack_propagate(False)

            tk.Label(box, text=char if terbuka else "_", bg="#1F2937" if terbuka else "#374151",
                     font=("Arial", 20, "bold"), fg="#00E5FF" if terbuka else "#9CA3AF").pack(expand=True)

        if self.logic.huruf_ditebak:
            huruf_str = ", ".join(sorted(self.logic.huruf_ditebak))
            self.lbl_ditebak.configure(text=f"Huruf sudah ditebak: {huruf_str}")
        else:
            self.lbl_ditebak.configure(text="Huruf sudah ditebak: -")
        self.lbl_level.configure(
            text=f"LEVEL 2 (Kata {self.logic.indeks_kata_sekarang + 1}/{len(self.logic.daftar_kata)})"
        )

        self.lbl_kategori.configure(
            text=f"Kategori : {self.logic.kategori}"
        )

        self.lbl_petunjuk.configure(
            text=f"Petunjuk : {self.logic.petunjuk}"
        )
        self.focus_set()

    def build_keyboard(self):
        for w in self.kb_frame.winfo_children():
            w.destroy()
        self.keys.clear()

        layout = [
            ["A","B","C","D","E","F","G","H","I"],
            ["J","K","L","M","N","O","P","Q","R"],
            ["S","T","U","V","W","X","Y","Z"],
        ]
        for row in layout:
            f = tk.Frame(self.kb_frame, bg="#111827")
            f.pack(pady=2)
            for char in row:
                btn = tk.Button(f, text=char, font=("Arial", 11, "bold"), bg="#1F2937", fg="#F9FAFB",
                    activebackground="#374151", activeforeground="#00E5FF", relief="flat", bd=0,
                    highlightbackground="#4B5563", highlightthickness=1, width=3, height=1,
                    command=lambda c=char: self.proses_tebakan(c))
                btn.pack(side="left", padx=2)
                btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, "#374151"))
                btn.bind("<Leave>", lambda e, b=btn: self._on_leave(b, "#1F2937"))
                self.keys[char] = btn

    def tekan_keyboard(self, event):
        if self.logic.game_selesai:
            return

        huruf = event.char.upper()

        if huruf.isalpha():
            huruf = huruf.upper()

            if huruf in self.keys:
                if self.keys[huruf]["state"] == "normal":
                    self.proses_tebakan(huruf)

    def _on_hover(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def _on_leave(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def render_bottom_items(self):
        for w in self.item_bar.winfo_children(): w.destroy()
        items = [
            ["PETUNJUK\nHURUF", f"x{self.logic.stok_hint}",  "#78350F", self.aksi_hint],
            ["TAMBAH\nWAKTU",   f"x{self.logic.stok_waktu}", "#1E3A8A", self.aksi_waktu],
            ["PULIHKAN\nHP",    f"x{self.logic.stok_heal}",  "#701A75", self.aksi_heal],
        ]
        for i, (nama, stok, warna_bg, aksi) in enumerate(items):
            col = tk.Frame(self.item_bar, bg="#1F2937")
            col.grid(row=0, column=i, sticky="nsew", padx=6, pady=6)

            kotak = tk.Button(col, text=f"{nama}\n{stok}", font=("Arial", 9, "bold"), bg=warna_bg, fg="white",
                activebackground="#4B5563", relief="flat", bd=0, highlightbackground="#374151", highlightthickness=1, command=aksi)
            kotak.pack(fill="both", expand=True)
            kotak.bind("<Enter>", lambda e, b=kotak: self._on_hover(b, "#4B5563"))
            kotak.bind("<Leave>", lambda e, b=kotak, c=warna_bg: self._on_leave(b, c))

        self.item_bar.columnconfigure((0, 1, 2), weight=1)

    def proses_tebakan(self, h):
        is_benar, status = self.logic.tebak_huruf(h)
        if status == "ignored":
            return

        if is_benar:
            self.keys[h].configure(bg="#059669", fg="white", state="disabled")
            self._set_banner("#10B981", f"✅  TEBAKAN BENAR! HP Musuh Berkurang")

            self.bar_g['value'] = (self.logic.hp_musuh / self.logic.hp_musuh_max) * 100
            self.lbl_hp_g.configure(text=f"{int(self.logic.hp_musuh)}/{self.logic.hp_musuh_max}")
        else:
            self.keys[h].configure(bg="#DC2626", fg="white", state="disabled")
            self._set_banner("#EF4444", "❌  TEBAKAN SALAH!  -20 HP Kamu")

            self.bar_p['value'] = (self.logic.hp_player / self.logic.hp_player_max) * 100
            self.lbl_hp_p.configure(text=f"{self.logic.hp_player}/{self.logic.hp_player_max}")
            self.guncang_window(10)
            self.flash_bar_merah(4)

        self.update_slots()
        self.focus_set()
        self.cek_kondisi()

    def lanjut_kata_berikutnya(self):
        if self.logic.lanjut_kata_berikutnya():
            self.bar_g['value'] = 100
            self.lbl_hp_g.configure(text=f"{self.logic.hp_musuh}/{self.logic.hp_musuh_max}")
            self._set_banner("#FF6B00", "KATA BARU! Lanjutkan Menebak.")
            self.update_slots()
            self.build_keyboard()
            self.focus_set()

    def cek_kondisi(self):
        if self.logic.game_selesai: return

        kata_terbuka = self.logic.cek_kata_terbuka()

        if kata_terbuka and self.logic.hp_musuh <= 0:
            if self.logic.indeks_kata_sekarang < len(self.logic.daftar_kata) - 1:
                if not self.logic.pindah_kata_berjalan:
                    self.logic.pindah_kata_berjalan = True
                    self._set_banner("#10B981", "✨ KATA TERTEBAK! Menuju kata selanjutnya...")
                    self.after(1000, self.lanjut_kata_berikutnya)
            else:
                self.logic.game_selesai = True
                self._set_banner("#10B981", "🏆  LEVEL 2 SELESAI! KAMU MENANG TOTAL!")

                skor = self.logic.hitung_skor()
                if hasattr(self.controller, "set_hasil_game"):
                    self.controller.set_hasil_game(
                        kata=", ".join(self.logic.daftar_kata), skor=skor, sisa_waktu=self.logic.sisa_waktu, hp_player=self.logic.hp_player,
                        tebakan_benar=self.logic.total_tebakan_benar, tebakan_salah=self.logic.total_tebakan_salah, huruf_ditebak=set(), mode="victory", level=2
                    )

        elif self.logic.hp_player <= 0 or self.logic.sisa_waktu <= 0:
            self.logic.game_selesai = True
            self._set_banner("#EF4444", "💀  GAME OVER LEVEL 2!")

            if hasattr(self.controller, "set_hasil_game"):
                self.controller.set_hasil_game(
                    kata=self.logic.kata_rahasia, skor=0, sisa_waktu=0, hp_player=0,
                    tebakan_benar=self.logic.total_tebakan_benar, tebakan_salah=self.logic.total_tebakan_salah, huruf_ditebak=set(), mode="defeat", level=2
                )

    def aksi_hint(self):
        huruf_hint = self.logic.gunakan_hint()
        if huruf_hint:
            self.render_bottom_items()
            self.proses_tebakan(huruf_hint)
            self.focus_set()
        else:
            self._notif_habis("💡 Petunjuk habis! Beli di Toko.")

    def aksi_waktu(self):
        if self.logic.gunakan_waktu():
            self.render_bottom_items()
        else:
            self._notif_habis("🕒 Tambah Waktu habis! Beli di Toko.")

    def aksi_heal(self):
        if self.logic.gunakan_heal():
            self.bar_p['value'] = (self.logic.hp_player / self.logic.hp_player_max) * 100
            self.lbl_hp_p.configure(text=f"{self.logic.hp_player}/{self.logic.hp_player_max}")
            self.render_bottom_items()
        else:
            self._notif_habis("❤️ Pulihkan HP habis! Beli di Toko.")

    def _notif_habis(self, pesan):
        self._set_banner("#D97706", pesan)
        self.after(1800, lambda: self._set_banner("#FF6B00", "SILAKAN LANJUTKAN MENEBAK"))

    def guncang_window(self, loop):
        if loop > 0:
            try:
                root = self.winfo_toplevel()
                x, y = root.winfo_x(), root.winfo_y()
                root.geometry(f"+{x + random.choice([-5, 5])}+{y}")
                self.after(25, lambda: self.guncang_window(loop - 1))
            except Exception: pass

    def flash_bar_merah(self, sisa):
        if sisa > 0:
            warna = "#EF4444" if sisa % 2 == 0 else "#10B981"
            self.style.configure("Player.Horizontal.TProgressbar", background=warna)
            self.after(90, lambda: self.flash_bar_merah(sisa - 1))
        else:
            self.style.configure("Player.Horizontal.TProgressbar", background="#10B981")

    def _set_banner(self, warna, teks):
        self.status_banner.configure(bg=warna)
        self.lbl_status.configure(bg=warna, text=teks)

    def update_timer(self, run_id=None):
        if run_id != self._run_id:
            return

        if self.logic.game_selesai: return

        if self.logic.sisa_waktu > 0 and self.logic.hp_player > 0:
            if not self.logic.pindah_kata_berjalan and self.logic.hp_musuh > 0:
                self.logic.sisa_waktu -= 1

            m, s = divmod(self.logic.sisa_waktu, 60)
            self.lbl_timer.configure(text=f"⏱  {m:02d}:{s:02d}", fg="#EF4444" if self.logic.sisa_waktu <= 10 else "#F59E0B")

            # Bunyikan sfx hitung mundur saat sisa waktu 10 detik atau kurang
            if self.logic.sisa_waktu <= 10:
                putar_sfx_hitung_mundur()

            self.after(1000, lambda: self.update_timer(run_id))
        else:
            self.cek_kondisi()

if __name__ == "__main__":
    class MockParent(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Hangman: Cyber Dark Level 2")
            self.geometry("400x700")
            self.configure(bg="#111827")
            self.game_results = {}

        def switch_screen(self, screen_name):
            print(f"[NAVIGASI] Pindah ke screen: {screen_name}")

        def set_hasil_game(self, **kwargs):
            print("[DATA] Hasil game Level 2 tersimpan:")
            self.game_results = kwargs
            for k, v in kwargs.items(): print(f"  - {k}: {v}")

    app_parent = MockParent()
    game_frame = Screen7GameplayLevel2(parent=app_parent, controller=app_parent)
    game_frame.pack(fill="both", expand=True)
    app_parent.mainloop()