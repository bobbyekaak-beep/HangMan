import tkinter as tk
from tkinter import ttk
import random
import winsound

class Screen6Gameplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A") # Deep Slate Navy Background
        self.parent = parent

        # ── CONFIG LEVEL 1 (MULTI-KATA) ──────────────────────────
        self.daftar_kata = ["KUCING", "AYAM", "SINGA", "RUSA"]
        self.indeks_kata_sekarang = 0
        self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
        
        self.huruf_ditebak = set()
        self.hp_player,   self.hp_player_max   = 100,  100
        self.hp_musuh,    self.hp_musuh_max    = 100,  100
        self.sisa_waktu = 120  

        self.total_tebakan_benar = 0
        self.total_tebakan_salah = 0

        self.hitung_damage_kata()

        self.stok_hint  = 3  
        self.stok_waktu = 2
        self.stok_heal  = 3

        self.game_selesai  = False
        self.pindah_kata_berjalan = False # Guard flag untuk mencegah bug multi-trigger transisi kata

        self.style = ttk.Style()
        self.style.theme_use('default')
        
        self.style.configure("Player.Horizontal.TProgressbar", 
                             troughcolor="#334155", background="#10B981", thickness=14) # Emerald Green
        self.style.configure("Enemy.Horizontal.TProgressbar", 
                             troughcolor="#334155", background="#EF4444", thickness=14) # Rose Red

        self.setup_ui()
        self.update_timer()

    def hitung_damage_kata(self):
        """Menghitung proporsi damage berdasarkan jumlah huruf unik kata saat ini"""
        self.huruf_unik = set(self.kata_rahasia)
        self.damage_per_huruf = self.hp_musuh_max / len(self.huruf_unik)

    def setup_ui(self):
        # ── 1. MODERN COMPACT HUD (SPILLED SIDE-BY-SIDE) ──────────────────
        hud_main = tk.Frame(self, bg="#1E293B", padx=14, pady=10, bd=0)
        hud_main.pack(fill="x", padx=12, pady=(12, 4))

        # Sisi Kiri (Player)
        kiri = tk.Frame(hud_main, bg="#1E293B")
        kiri.pack(side="left", fill="x", expand=True)
        tk.Label(kiri, text="PLAYER HP", bg="#1E293B", font=("Impact", 10), fg="#38BDF8").pack(anchor="w")
        self.bar_p = ttk.Progressbar(kiri, mode='determinate', style="Player.Horizontal.TProgressbar")
        self.bar_p.pack(fill="x", pady=2)
        self.bar_p['value'] = (self.hp_player / self.hp_player_max) * 100
        self.lbl_hp_p = tk.Label(kiri, bg="#1E293B", text=f"{self.hp_player} / {self.hp_player_max}", font=("Arial", 9, "bold"), fg="#94A3B8")
        self.lbl_hp_p.pack(anchor="w")

        # VS Divider Spacer
        tk.Label(hud_main, text="VS", bg="#1E293B", font=("Impact", 14, "italic"), fg="#64748B", width=4).pack(side="left")

        # Sisi Kanan (Enemy)
        kanan = tk.Frame(hud_main, bg="#1E293B")
        kanan.pack(side="right", fill="x", expand=True)
        tk.Label(kanan, text="ENEMY HP", bg="#1E293B", font=("Impact", 10), fg="#F43F5E").pack(anchor="e")
        self.bar_g = ttk.Progressbar(kanan, mode='determinate', style="Enemy.Horizontal.TProgressbar")
        self.bar_g.pack(fill="x", pady=2)
        self.bar_g['value'] = (self.hp_musuh / self.hp_musuh_max) * 100
        self.lbl_hp_g = tk.Label(kanan, bg="#1E293B", text=f"{int(self.hp_musuh)} / {self.hp_musuh_max}", font=("Arial", 9, "bold"), fg="#94A3B8")
        self.lbl_hp_g.pack(anchor="e")

        # ── 2. CENTRAL TIMER BAR ─────────────────────────────────────────
        timer_frame = tk.Frame(self, bg="#0F172A")
        timer_frame.pack(fill="x", padx=12, pady=4)
        self.lbl_timer = tk.Label(timer_frame, text="⏱ 02:00", bg="#0F172A", font=("Consolas", 14, "bold"), fg="#F59E0B")
        self.lbl_timer.pack(expand=True)

        # ── 3. STATUS BANNER (NOTIFIKASI AKSI) ───────────────────────────
        self.status_banner = tk.Frame(self, bg="#3B82F6", height=26)
        self.status_banner.pack(fill="x", padx=12, pady=2)
        self.status_banner.pack_propagate(False)
        self.lbl_status = tk.Label(self.status_banner, bg="#3B82F6", text="SISTEM SIAP! SILAKAN TEBAK HURUF", font=("Arial", 9, "bold"), fg="white")
        self.lbl_status.pack(expand=True)

        # ── 4. INFO LEVEL CARD ────────────────────────────────────────────
        info_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, pady=6)
        info_frame.pack(fill="x", padx=12, pady=6)
        self.lbl_level = tk.Label(info_frame, text=f"LEVEL 1 • KATA {self.indeks_kata_sekarang + 1}/{len(self.daftar_kata)}", bg="#FFFFFF", font=("Arial", 11, "bold"), fg="#1E293B")
        self.lbl_level.pack()
        tk.Label(info_frame, text="Kategori: Hewan Mudah", bg="#FFFFFF", font=("Arial", 9), fg="#64748B").pack()

        # ── 5. SLOT KATA RAHASIA (PREMIUM CARD SLOTS) ────────────────────
        self.word_frame = tk.Frame(self, bg="#0F172A")
        self.word_frame.pack(pady=10)

        # Keterangan Huruf Ditebak
        self.lbl_ditebak = tk.Label(self, bg="#0F172A", text="Riwayat Tebakan: -", font=("Arial", 9), fg="#64748B")
        self.lbl_ditebak.pack(pady=(0, 4))

        # ── 6. KEYBOARD ARCADE A–Z ───────────────────────────────────────
        self.kb_frame = tk.Frame(self, bg="#0F172A")
        self.kb_frame.pack(pady=6)
        self.keys = {}
        self.build_keyboard()

        # ── 7. UTILITY ITEM BAR (BOTTOM ATTACHED) ────────────────────────
        self.item_bar = tk.Frame(self, bg="#1E293B", height=65)
        self.item_bar.pack(side="bottom", fill="x", padx=12, pady=12)
        self.item_bar.pack_propagate(False)
        self.render_bottom_items()

        self.update_slots()

    def update_slots(self):
        for w in self.word_frame.winfo_children():
            w.destroy()

        for char in self.kata_rahasia:
            terbuka = char in self.huruf_ditebak
            box = tk.Frame(self.word_frame, bg="#1E293B" if terbuka else "#334155",
                           highlightbackground="#38BDF8" if terbuka else "#475569", highlightthickness=2, width=36, height=40)
            box.pack(side="left", padx=4)
            box.pack_propagate(False)

            tk.Label(box, text=char if terbuka else "•", bg="#1E293B" if terbuka else "#334155",
                     font=("Consolas", 18, "bold"), fg="#38BDF8" if terbuka else "#94A3B8").pack(expand=True)

        if self.huruf_ditebak:
            huruf_str = " ".join(sorted(self.huruf_ditebak))
            self.lbl_ditebak.configure(text=f"Riwayat Tebakan: [ {huruf_str} ]")
        else:
            self.lbl_ditebak.configure(text="Riwayat Tebakan: -")

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
            f = tk.Frame(self.kb_frame, bg="#0F172A")
            f.pack(pady=1)
            for char in row:
                btn = tk.Button(f, text=char, font=("Arial", 10, "bold"), bg="#1E293B", fg="#F1F5F9",
                    activebackground="#334155", activeforeground="#FFFFFF", relief="flat", bd=0, 
                    width=3, height=1, command=lambda c=char: self.proses_tebakan(c))
                btn.pack(side="left", padx=2)
                btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, "#334155"))
                btn.bind("<Leave>", lambda e, b=btn: self._on_leave(b, "#1E293B"))
                self.keys[char] = btn

    def _on_hover(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def _on_leave(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def render_bottom_items(self):
        for w in self.item_bar.winfo_children(): w.destroy()
        items = [
            ("HINT LIGHT", f"x{self.stok_hint}",  "#475569", self.aksi_hint),
            ("ADD TIME",   f"x{self.stok_waktu}", "#475569", self.aksi_waktu),
            ("REGEN HP",   f"x{self.stok_heal}",  "#475569", self.aksi_heal),
        ]
        for i, (nama, stok, warna_bg, aksi) in enumerate(items):
            col = tk.Frame(self.item_bar, bg="#1E293B")
            col.grid(row=0, column=i, sticky="nsew", padx=6, pady=6)

            kotak = tk.Button(col, text=f"{nama}\n{stok}", font=("Arial", 8, "bold"), bg=warna_bg, fg="#F1F5F9",
                activebackground="#334155", relief="flat", bd=0, command=aksi)
            kotak.pack(fill="both", expand=True)
            kotak.bind("<Enter>", lambda e, b=kotak: self._on_hover(b, "#334155"))
            kotak.bind("<Leave>", lambda e, b=kotak, c=warna_bg: self._on_leave(b, c))

        self.item_bar.columnconfigure((0, 1, 2), weight=1)

    def proses_tebakan(self, h):
        if h in self.huruf_ditebak or self.game_selesai or self.pindah_kata_berjalan: return
        self.huruf_ditebak.add(h)

        if h in self.kata_rahasia:
            self.total_tebakan_benar += 1
            self.keys[h].configure(bg="#059669", fg="white", state="disabled") # Emerald Dark
            
            self.hp_musuh = max(0, self.hp_musuh - self.damage_per_huruf)
            
            kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)
            if kata_terbuka:
                self.hp_musuh = 0

            self._set_banner("#10B981", f"🎯 TEBAKAN BENAR! HP MUSUH BERKURANG")
            winsound.Beep(1000, 120)

            self.bar_g['value'] = (self.hp_musuh / self.hp_musuh_max) * 100
            self.lbl_hp_g.configure(text=f"{int(self.hp_musuh)} / {self.hp_musuh_max}")
        else:
            self.total_tebakan_salah += 1
            self.keys[h].configure(bg="#DC2626", fg="white", state="disabled") # Rose Dark
            self._set_banner("#EF4444", "💥 TEBAKAN SALAH! -15 PLAYER HP")
            
            winsound.Beep(300, 180)

            self.hp_player = max(0, self.hp_player - 15)
            self.bar_p['value'] = (self.hp_player / self.hp_player_max) * 100
            self.lbl_hp_p.configure(text=f"{self.hp_player} / {self.hp_player_max}")
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
        self.lbl_hp_g.configure(text=f"{self.hp_musuh} / {self.hp_musuh_max}")
        
        self.hitung_damage_kata()
        
        self.lbl_level.configure(text=f"LEVEL 1 • KATA {self.indeks_kata_sekarang + 1}/{len(self.daftar_kata)}")
        self._set_banner("#3B82F6", "KATA BARU DIMULAI! LANJUTKAN!")
        
        self.update_slots()
        self.build_keyboard()
        
        self.pindah_kata_berjalan = False # Buka kunci setelah state kata baru selesai dimuat

    def cek_kondisi(self):
        if self.game_selesai: return

        kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)

        if kata_terbuka and self.hp_musuh <= 0:
            if self.indeks_kata_sekarang < len(self.daftar_kata) - 1:
                if not self.pindah_kata_berjalan:
                    self.pindah_kata_berjalan = True # Kunci proses transisi agar tidak terpanggil berulang kali
                    winsound.Beep(1200, 100)
                    self._set_banner("#10B981", "✨ KATA TERTEBAK! MENYAPU MUSUH BERIKUTNYA...")
                    self.after(1000, self.lanjut_kata_berikutnya)
            else:
                self.game_selesai = True
                self._set_banner("#10B981", "🏆 LEVEL 1 BERHASIL DIKLAIM! VICTORY!")

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
            self._set_banner("#EF4444", "💀 ANNIHILATED! GAME OVER!")

            self.after(100, lambda: winsound.Beep(400, 200))
            self.after(320, lambda: winsound.Beep(250, 400))

            if hasattr(self.parent, "set_hasil_game"):
                self.parent.set_hasil_game(
                    kata=self.kata_rahasia, skor=0, sisa_waktu=0, hp_player=0,
                    tebakan_benar=self.total_tebakan_benar, tebakan_salah=self.total_tebakan_salah, huruf_ditebak=set(), mode="defeat"
                )
            self.after(1200, lambda: self.parent.switch_screen("screenresult.py"))

    def hitung_skor(self):
        base        = self.total_tebakan_benar * 20
        bonus_waktu = self.sisa_waktu * 2
        bonus_hp    = self.hp_player
        penalti     = self.total_tebakan_salah * 10  
        return max(0, base + bonus_waktu + bonus_hp - penalti)

    def aksi_hint(self):
        if self.stok_hint <= 0 or self.game_selesai or self.pindah_kata_berjalan:
            self._notif_habis("💡 ITEM HINT HABIS!")
            return
            
        huruf_ditemukan = None
        for c in self.kata_rahasia:
            if c not in self.huruf_ditebak:
                huruf_ditemukan = c
                break
                
        if huruf_ditemukan:
            self.stok_hint -= 1
            self.render_bottom_items()
            self.proses_tebakan(huruf_ditemukan)

    def aksi_waktu(self):
        if self.stok_waktu <= 0 or self.game_selesai:
            self._notif_habis("🕒 ITEM WAKTU HABIS!")
            return
        self.stok_waktu -= 1
        self.sisa_waktu += 30
        self.render_bottom_items()
        winsound.Beep(800, 100)

    def aksi_heal(self):
        if self.stok_heal <= 0 or self.game_selesai:
            self._notif_habis("❤️ ITEM HEAL HABIS!")
            return
        self.stok_heal -= 1
        self.hp_player = min(self.hp_player_max, self.hp_player + 25) 
        self.bar_p['value'] = (self.hp_player / self.hp_player_max) * 100
        self.lbl_hp_p.configure(text=f"{self.hp_player} / {self.hp_player_max}")
        self.render_bottom_items()
        winsound.Beep(900, 150)

    def _notif_habis(self, pesan):
        self._set_banner("#D97706", pesan) # Dark Amber
        winsound.Beep(200, 300)
        self.after(1800, lambda: self._set_banner("#3B82F6", "SILAKAN LANJUTKAN MENEBAK"))

    def guncang_window(self, loop):
        if loop > 0:
            try:
                root  = self.winfo_toplevel()
                x, y  = root.winfo_x(), root.winfo_y()
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

    def update_timer(self):
        if self.game_selesai: return
        
        if self.sisa_waktu > 0 and self.hp_player > 0:
            # Pengurangan waktu hanya berjalan saat game aktif & tidak sedang dalam transisi jeda kata
            if not self.pindah_kata_berjalan and self.hp_musuh > 0:
                self.sisa_waktu -= 1
                
            m, s = divmod(self.sisa_waktu, 60)
            self.lbl_timer.configure(text=f"⏱ {m:02d}:{s:02d}", fg="#EF4444" if self.sisa_waktu <= 15 else "#F59E0B")
            
            if self.sisa_waktu <= 5 and not self.pindah_kata_berjalan and self.hp_musuh > 0:
                winsound.Beep(600, 80)
                
            self.after(1000, self.update_timer)
        else:
            self.cek_kondisi()

# ── BAGIAN WRAPPER RUN ───────────────────────────────────────────
if __name__ == "__main__":
    class MockParent(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Hangman: Shadow Arcade")
            self.geometry("440x600")
            self.configure(bg="#0F172A")
            self.game_results = {}
            
        def switch_screen(self, screen_name):
            print(f"[NAVIGASI] Berhasil pindah ke: {screen_name}")
            
        def set_hasil_game(self, **kwargs):
            print("[DATA] Hasil game tersimpan:")
            self.game_results = kwargs 
            for k, v in kwargs.items(): print(f"  - {k}: {v}")

    app_parent = MockParent()
    game_frame = Screen6Gameplay(parent=app_parent)
    game_frame.pack(fill="both", expand=True)
    app_parent.mainloop()