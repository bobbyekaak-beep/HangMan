import tkinter as tk
from tkinter import ttk
import random
import winsound

class Screen8GameplayLevel3(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#F0F4F6")
        self.parent = parent

        # ── CONFIG LEVEL 3 (HARD MODE: 8 KATA & WAKTU 60 DETIK) ──────
        self.daftar_kata = ["BELALANG", "CENDRAWASIH", "TRENGGILING", "ANGGANG", "KANGGURU", "GIRAFFA", "ORANGUTAN", "ALBATROS"]
        self.indeks_kata_sekarang = 0
        self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
        
        self.huruf_ditebak = set()
        self.hp_player,   self.hp_player_max   = 100,  100
        self.hp_musuh,    self.hp_musuh_max    = 100,  100
        self.sisa_waktu = 60  

        self.total_tebakan_benar = 0
        self.total_tebakan_salah = 0

        self.hitung_damage_kata()

        self.stok_hint  = 1  
        self.stok_waktu = 1
        self.stok_heal  = 1

        self.game_selesai  = False

        self.style = ttk.Style()
        self.style.theme_use('default')
        
        self.style.configure("Player.Horizontal.TProgressbar", 
                             troughcolor="#D0D0D0", background="#4CAF50", thickness=18)
        self.style.configure("Enemy.Horizontal.TProgressbar", 
                             troughcolor="#D0D0D0", background="#E53935", thickness=18)

        self.setup_ui()
        self.update_timer()

    def hitung_damage_kata(self):
        self.huruf_unik = set(self.kata_rahasia)
        self.damage_per_huruf = self.hp_musuh_max / len(self.huruf_unik)

    def setup_ui(self):
        # ── 1. TOP HUD ───────────────────────────────────────────
        hud = tk.Frame(self, bg="#F0F4F6")
        hud.pack(fill="x", padx=12, pady=(12, 6))

        kiri = tk.Frame(hud, bg="#F0F4F6")
        kiri.pack(side="left")

        tk.Label(kiri, text="HP KAMU", bg="#F0F4F6", font=("Arial", 9, "bold"), fg="#555555").pack(anchor="w")

        self.bar_p = ttk.Progressbar(kiri, length=105, mode='determinate', style="Player.Horizontal.TProgressbar")
        self.bar_p.pack()
        self.bar_p['value'] = (self.hp_player / self.hp_player_max) * 100

        self.lbl_hp_p = tk.Label(kiri, bg="#F0F4F6", text=f"{self.hp_player}/{self.hp_player_max}", font=("Arial", 9), fg="#333333")
        self.lbl_hp_p.pack(anchor="w")

        m, s = divmod(self.sisa_waktu, 60)
        self.lbl_timer = tk.Label(hud, text=f"⏱  {m:02d}:{s:02d}", font=("Arial", 15, "bold"), fg="#E53935", bg="#F0F4F6")
        self.lbl_timer.pack(side="left", expand=True)

        kanan = tk.Frame(hud, bg="#F0F4F6")
        kanan.pack(side="right")

        tk.Label(kanan, text="HP MUSUH", bg="#F0F4F6", font=("Arial", 9, "bold"), fg="#555555").pack(anchor="e")

        self.bar_g = ttk.Progressbar(kanan, length=105, mode='determinate', style="Enemy.Horizontal.TProgressbar")
        self.bar_g.pack()
        self.bar_g['value'] = (self.hp_musuh / self.hp_musuh_max) * 100

        self.lbl_hp_g = tk.Label(kanan, bg="#F0F4F6", text=f"{int(self.hp_musuh)}/{self.hp_musuh_max}", font=("Arial", 9), fg="#333333")
        self.lbl_hp_g.pack(anchor="e")

        # ── 2. STATUS BANNER ─────────────────────────────────────
        self.status_banner = tk.Frame(self, bg="#D32F2F", height=30) 
        self.status_banner.pack(fill="x", padx=12, pady=(4, 2))
        self.status_banner.pack_propagate(False)

        # Kata "BABAK FINAL" sudah dihapus total dari sini
        self.lbl_status = tk.Label(self.status_banner, bg="#D32F2F", text="LEVEL 3!", font=("Arial", 11, "bold"), fg="white")
        self.lbl_status.pack(expand=True)

        # ── 3. INFO LEVEL & KATEGORI ──────────────────────────────
        info_frame = tk.Frame(self, bg="white", highlightbackground="#E0E0E0", highlightthickness=1)
        info_frame.pack(fill="x", padx=12, pady=(4, 2))

        self.lbl_level = tk.Label(info_frame, text=f"LEVEL 3 (Kata {self.indeks_kata_sekarang + 1}/{len(self.daftar_kata)})", bg="white", font=("Arial", 13, "bold"), fg="#D32F2F")
        self.lbl_level.pack(pady=(8, 0))
        tk.Label(info_frame, text="Kategori: Hewan Langka & Panjang", bg="white", font=("Arial", 11), fg="#555555").pack(pady=(0, 8))

        # ── 4. SLOT KATA RAHASIA ──────────────────────────────────
        self.word_frame = tk.Frame(self, bg="#F0F4F6")
        self.word_frame.pack(pady=14)

        # ── 5. KETERANGAN HURUF DITEBAK ──────────────────────────
        self.lbl_ditebak = tk.Label(self, bg="#F0F4F6", text="Huruf sudah ditebak: -", font=("Arial", 10), fg="#777777")
        self.lbl_ditebak.pack()

        # ── 6. KEYBOARD A–Z ──────────────────────────────────────
        self.kb_frame = tk.Frame(self, bg="#F0F4F6")
        self.kb_frame.pack(pady=10)
        self.keys = {}
        self.build_keyboard()

        # ── 7. ITEM BAR BAWAH ─────────────────────────────────────
        self.item_bar = tk.Frame(self, bg="white", highlightbackground="#E0E0E0", highlightthickness=1, height=75)
        self.item_bar.pack(side="bottom", fill="x", padx=12, pady=10)
        self.item_bar.pack_propagate(False)
        self.render_bottom_items()

        self.update_slots()

    def update_slots(self):
        for w in self.word_frame.winfo_children():
            w.destroy()

        for char in self.kata_rahasia:
            terbuka = char in self.huruf_ditebak
            box = tk.Frame(self.word_frame, bg="#FFFFFF" if terbuka else "#F0F4F6",
                           highlightbackground="#B0BEC5" if terbuka else "#F0F4F6", highlightthickness=1, width=32, height=42)
            box.pack(side="left", padx=2) 
            box.pack_propagate(False)

            tk.Label(box, text=char if terbuka else "_", bg="#FFFFFF" if terbuka else "#F0F4F6",
                     font=("Arial", 18, "bold"), fg="#1565C0" if terbuka else "#333333").pack(expand=True)

        if self.huruf_ditebak:
            huruf_str = ", ".join(sorted(self.huruf_ditebak))
            self.lbl_ditebak.configure(text=f"Huruf sudah ditebak: {huruf_str}")
        else:
            self.lbl_ditebak.configure(text="Huruf sudah ditebak: -")

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
            f = tk.Frame(self.kb_frame, bg="#F0F4F6")
            f.pack(pady=2)
            for char in row:
                btn = tk.Button(f, text=char, font=("Arial", 11, "bold"), bg="#FFFFFF", fg="black",
                    activebackground="#E3F2FD", activeforeground="black", relief="flat", bd=1, 
                    highlightbackground="#BDBDBD", highlightthickness=1, width=3, height=1,
                    command=lambda c=char: self.proses_tebakan(c))
                btn.pack(side="left", padx=2)
                btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, "#E3F2FD"))
                btn.bind("<Leave>", lambda e, b=btn: self._on_leave(b, "#FFFFFF"))
                self.keys[char] = btn

    def _on_hover(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def _on_leave(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def render_bottom_items(self):
        for w in self.item_bar.winfo_children(): w.destroy()
        items = [
            ("PETUNJUK\nHURUF", f"x{self.stok_hint}",  "#FFF9C4", self.aksi_hint),
            ("TAMBAH\nWAKTU",   f"x{self.stok_waktu}", "#E3F2FD", self.aksi_waktu),
            ("PULIHKAN\nHP",    f"x{self.stok_heal}",  "#FCE4EC", self.aksi_heal),
        ]
        for i, (nama, stok, warna_bg, aksi) in enumerate(items):
            col = tk.Frame(self.item_bar, bg="white")
            col.grid(row=0, column=i, sticky="nsew", padx=8, pady=8)

            kotak = tk.Button(col, text=f"{nama}\n{stok}", font=("Arial", 9, "bold"), bg=warna_bg, fg="#333333",
                activebackground="#E0E0E0", relief="flat", bd=1, highlightbackground="#CFD8DC", highlightthickness=1, command=aksi)
            kotak.pack(fill="both", expand=True)
            kotak.bind("<Enter>", lambda e, b=kotak: self._on_hover(b, "#E0E0E0"))
            kotak.bind("<Leave>", lambda e, b=kotak, c=warna_bg: self._on_leave(b, c))

        self.item_bar.columnconfigure((0, 1, 2), weight=1)

    def proses_tebakan(self, h):
        if h in self.huruf_ditebak or self.game_selesai: return
        self.huruf_ditebak.add(h)

        if h in self.kata_rahasia:
            self.total_tebakan_benar += 1
            self.keys[h].configure(bg="#4CAF50", fg="white", state="disabled")
            
            self.hp_musuh = max(0, self.hp_musuh - self.damage_per_huruf)
            
            kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)
            if kata_terbuka:
                self.hp_musuh = 0

            self._set_banner("#4CAF50", f"✅  TEBAKAN BENAR! HP Musuh Berkurang")
            winsound.Beep(1000, 120)

            self.bar_g['value'] = (self.hp_musuh / self.hp_musuh_max) * 100
            self.lbl_hp_g.configure(text=f"{int(self.hp_musuh)}/{self.hp_musuh_max}")
        else:
            self.total_tebakan_salah += 1
            self.keys[h].configure(bg="#E53935", fg="white", state="disabled")
            
            self._set_banner("#E53935", "❌  TEBAKAN SALAH!  -25 HP Kamu")
            winsound.Beep(300, 180)

            self.hp_player = max(0, self.hp_player - 25)
            self.bar_p['value'] = (self.hp_player / self.hp_player_max) * 100
            self.lbl_hp_p.configure(text=f"{self.hp_player}/{self.hp_player_max}")
            self.guncang_window(10)
            self.flash_bar_merah(4)

        self.update_slots()
        self.cek_kondisi()

    def lanjut_kata_berikutnya(self):
        self.indeks_kata_sekarang += 1
        self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
        self.huruf_ditebak = set()
        
        self.hp_musuh = self.hp_musuh_max
        self.bar_g['value'] = 100
        self.lbl_hp_g.configure(text=f"{self.hp_musuh}/{self.hp_musuh_max}")
        
        self.hitung_damage_kata()
        
        self.lbl_level.configure(text=f"LEVEL 3 (Kata {self.indeks_kata_sekarang + 1}/{len(self.daftar_kata)})")
        self._set_banner("#D32F2F", "KATA BARU! Tetap Fokus.")
        
        self.update_slots()
        self.build_keyboard()

    def cek_kondisi(self):
        if self.game_selesai: return

        kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)

        if kata_terbuka and self.hp_musuh <= 0:
            if self.indeks_kata_sekarang < len(self.daftar_kata) - 1:
                winsound.Beep(1200, 100)
                self._set_banner("#4CAF50", "✨ KATA TERTEBAK! Menuju kata selanjutnya...")
                self.after(1000, self.lanjut_kata_berikutnya)
            else:
                self.game_selesai = True
                self._set_banner("#4CAF50", "🏆  GAME SELESAI! KAMU JUARA HANGMAN!")

                self.after(100, lambda: winsound.Beep(1200, 150))
                self.after(250, lambda: winsound.Beep(1600, 300))

                skor = self.hitung_skor()
                if hasattr(self.parent, "set_hasil_game"):
                    self.parent.set_hasil_game(
                        kata=", ".join(self.daftar_kata), skor=skor, sisa_waktu=self.sisa_waktu, hp_player=self.hp_player,
                        tebakan_benar=self.total_tebakan_benar, tebakan_salah=self.total_tebakan_salah, huruf_ditebak=set(), mode="victory"
                    )
                self.after(1200, lambda: self.parent.switch_screen("screenresult.py"))

        elif self.hp_player <= 0 or self.sisa_waktu <= 0:
            self.game_selesai = True
            self._set_banner("#E53935", "💀  GAME OVER DI LEVEL 3!")

            self.after(100, lambda: winsound.Beep(400, 200))
            self.after(320, lambda: winsound.Beep(250, 400))

            if hasattr(self.parent, "set_hasil_game"):
                self.parent.set_hasil_game(
                    kata=self.kata_rahasia, skor=0, sisa_waktu=0, hp_player=0,
                    tebakan_benar=self.total_tebakan_benar, tebakan_salah=self.total_tebakan_salah, huruf_ditebak=set(), mode="defeat"
                )
            self.after(1200, lambda: self.parent.switch_screen("screenresult.py"))

    def hitung_skor(self):
        base        = self.total_tebakan_benar * 30 
        bonus_waktu = self.sisa_waktu * 5           
        bonus_hp    = self.hp_player * 3
        penalti     = self.total_tebakan_salah * 20 
        return max(0, base + bonus_waktu + bonus_hp - penalti)

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
        winsound.Beep(800, 100)

    def aksi_heal(self):
        if self.stok_heal <= 0 or self.game_selesai:
            self._notif_habis("❤️ Pulihkan HP habis! Beli di Toko.")
            return
        self.stok_heal -= 1
        self.hp_player = min(self.hp_player_max, self.hp_player + 15) 
        self.bar_p['value'] = (self.hp_player / self.hp_player_max) * 100
        self.lbl_hp_p.configure(text=f"{self.hp_player}/{self.hp_player_max}")
        self.render_bottom_items()
        winsound.Beep(900, 150)

    def _notif_habis(self, pesan):
        self._set_banner("#FF8F00", pesan)
        winsound.Beep(200, 300)
        self.after(2000, lambda: self._set_banner("#D32F2F", "Pilih huruf!"))

    def guncang_window(self, loop):
        if loop > 0:
            try:
                root  = self.winfo_toplevel()
                x, y  = root.winfo_x(), root.winfo_y()
                root.geometry(f"+{x + random.choice([-7, 7])}+{y}")
                self.after(28, lambda: self.guncang_window(loop - 1))
            except Exception: pass

    def flash_bar_merah(self, sisa):
        if sisa > 0:
            warna = "#E53935" if sisa % 2 == 0 else "#4CAF50"
            self.style.configure("Player.Horizontal.TProgressbar", background=warna)
            self.after(90, lambda: self.flash_bar_merah(sisa - 1))
        else:
            self.style.configure("Player.Horizontal.TProgressbar", background="#4CAF50")

    def _set_banner(self, warna, teks):
        self.status_banner.configure(bg=warna)
        self.lbl_status.configure(bg=warna, text=teks)

    def update_timer(self):
        if self.game_selesai: return
        if self.sisa_waktu > 0 and self.hp_player > 0 and self.hp_musuh > 0:
            self.sisa_waktu -= 1
            m, s = divmod(self.sisa_waktu, 60)
            self.lbl_timer.configure(text=f"⏱  {m:02d}:{s:02d}", fg="#E53935" if self.sisa_waktu <= 20 else "#3E2723")
            if self.sisa_waktu <= 5:
                winsound.Beep(600, 80)
            self.after(1000, self.update_timer)
        else:
            self.cek_kondisi()

# ── BAGIAN WRAPPER RUN (MOCK PARENT UNTUK TESTING) ───────────────
if __name__ == "__main__":
    class MockParent(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Game Hangman Level 3")
            self.geometry("420x580")
            self.configure(bg="#F0F4F6")
            self.game_results = {}
            
        def switch_screen(self, screen_name):
            print(f"[NAVIGASI] Berhasil pindah ke: {screen_name}")
            
        def set_hasil_game(self, **kwargs):
            print("[DATA] Hasil game tersimpan:")
            self.game_results = kwargs 
            for k, v in kwargs.items(): print(f"  - {k}: {v}")

    app_parent = MockParent()
    game_frame = Screen8GameplayLevel3(parent=app_parent)
    game_frame.pack(fill="both", expand=True)
    app_parent.mainloop()