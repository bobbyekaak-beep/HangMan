# game_gui.py
import tkinter as tk
from tkinter import ttk
import random
import winsound
from logic import level1logic

class Screen6Gameplay(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#0F172A")
        self.parent = parent
        
        # Inisialisasi object logic game
        self.logic = level1logic()

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("Player.Horizontal.TProgressbar", troughcolor="#334155", background="#10B981", thickness=14)
        self.style.configure("Enemy.Horizontal.TProgressbar", troughcolor="#334155", background="#EF4444", thickness=14)

        self.setup_ui()
        self.update_timer()

    def setup_ui(self):
        # ── 1. MODERN COMPACT HUD ──────────────────
        hud_main = tk.Frame(self, bg="#1E293B", padx=14, pady=10, bd=0)
        hud_main.pack(fill="x", padx=12, pady=(12, 4))

        kiri = tk.Frame(hud_main, bg="#1E293B")
        kiri.pack(side="left", fill="x", expand=True)
        tk.Label(kiri, text="PLAYER HP", bg="#1E293B", font=("Impact", 10), fg="#38BDF8").pack(anchor="w")
        self.bar_p = ttk.Progressbar(kiri, mode='determinate', style="Player.Horizontal.TProgressbar")
        self.bar_p.pack(fill="x", pady=2)
        
        self.lbl_hp_p = tk.Label(kiri, bg="#1E293B", font=("Arial", 9, "bold"), fg="#94A3B8")
        self.lbl_hp_p.pack(anchor="w")

        tk.Label(hud_main, text="VS", bg="#1E293B", font=("Impact", 14, "italic"), fg="#64748B", width=4).pack(side="left")

        kanan = tk.Frame(hud_main, bg="#1E293B")
        kanan.pack(side="right", fill="x", expand=True)
        tk.Label(kanan, text="ENEMY HP", bg="#1E293B", font=("Impact", 10), fg="#F43F5E").pack(anchor="e")
        self.bar_g = ttk.Progressbar(kanan, mode='determinate', style="Enemy.Horizontal.TProgressbar")
        self.bar_g.pack(fill="x", pady=2)
        
        self.lbl_hp_g = tk.Label(kanan, bg="#1E293B", font=("Arial", 9, "bold"), fg="#94A3B8")
        self.lbl_hp_g.pack(anchor="e")

        # ── 2. CENTRAL TIMER BAR ─────────────────────────────────────────
        timer_frame = tk.Frame(self, bg="#0F172A")
        timer_frame.pack(fill="x", padx=12, pady=4)
        self.lbl_timer = tk.Label(timer_frame, bg="#0F172A", font=("Consolas", 14, "bold"), fg="#F59E0B")
        self.lbl_timer.pack(expand=True)

        # ── 3. STATUS BANNER ───────────────────────────────────────────
        self.status_banner = tk.Frame(self, bg="#3B82F6", height=26)
        self.status_banner.pack(fill="x", padx=12, pady=2)
        self.status_banner.pack_propagate(False)
        self.lbl_status = tk.Label(self.status_banner, bg="#3B82F6", text="SISTEM SIAP! SILAKAN TEBAK HURUF", font=("Arial", 9, "bold"), fg="white")
        self.lbl_status.pack(expand=True)

        # ── 4. INFO LEVEL CARD ────────────────────────────────────────────
        info_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#E2E8F0", highlightthickness=1, pady=6)
        info_frame.pack(fill="x", padx=12, pady=6)
        self.lbl_level = tk.Label(info_frame, bg="#FFFFFF", font=("Arial", 11, "bold"), fg="#1E293B")
        self.lbl_level.pack()
        tk.Label(info_frame, text="Kategori: Hewan Mudah", bg="#FFFFFF", font=("Arial", 9), fg="#64748B").pack()

        # ── 5. SLOT KATA RAHASIA ────────────────────
        self.word_frame = tk.Frame(self, bg="#0F172A")
        self.word_frame.pack(pady=10)

        self.lbl_ditebak = tk.Label(self, bg="#0F172A", font=("Arial", 9), fg="#64748B")
        self.lbl_ditebak.pack(pady=(0, 4))

        # ── 6. KEYBOARD ARCADE A–Z ───────────────────────────────────────
        self.kb_frame = tk.Frame(self, bg="#0F172A")
        self.kb_frame.pack(pady=6)
        self.keys = {}
        self.build_keyboard()

        # ── 7. UTILITY ITEM BAR ────────────────────────
        self.item_bar = tk.Frame(self, bg="#1E293B", height=65)
        self.item_bar.pack(side="bottom", fill="x", padx=12, pady=12)
        self.item_bar.pack_propagate(False)

        self.update_visuals()

    def update_visuals(self):
        # Update HP Bar & Label Player
        self.bar_p['value'] = (self.logic.hp_player / self.logic.hp_player_max) * 100
        self.lbl_hp_p.configure(text=f"{self.logic.hp_player} / {self.logic.hp_player_max}")
        
        # Update HP Bar & Label Musuh
        self.bar_g['value'] = (self.logic.hp_musuh / self.logic.hp_musuh_max) * 100
        self.lbl_hp_g.configure(text=f"{int(self.logic.hp_musuh)} / {self.logic.hp_musuh_max}")

        # Update Level Info Text
        self.lbl_level.configure(text=f"LEVEL 1 • KATA {self.logic.indeks_kata_sekarang + 1}/{len(self.logic.daftar_kata)}")

        # Update Slots Kata Rahasia
        for w in self.word_frame.winfo_children(): w.destroy()
        for char in self.logic.kata_rahasia:
            terbuka = char in self.logic.huruf_ditebak
            box = tk.Frame(self.word_frame, bg="#1E293B" if terbuka else "#334155",
                           highlightbackground="#38BDF8" if terbuka else "#475569", highlightthickness=2, width=36, height=40)
            box.pack(side="left", padx=4)
            box.pack_propagate(False)
            tk.Label(box, text=char if terbuka else "•", bg="#1E293B" if terbuka else "#334155",
                     font=("Consolas", 18, "bold"), fg="#38BDF8" if terbuka else "#94A3B8").pack(expand=True)

        # Update Riwayat Tebakan
        if self.logic.huruf_ditebak:
            self.lbl_ditebak.configure(text=f"Riwayat Tebakan: [ {' '.join(sorted(self.logic.huruf_ditebak))} ]")
        else:
            self.lbl_ditebak.configure(text="Riwayat Tebakan: -")

        # Update Item Bar Stok
        for w in self.item_bar.winfo_children(): w.destroy()
        items = [
            ("HINT LIGHT", f"x{self.logic.stok_hint}",  self.aksi_hint),
            ("ADD TIME",   f"x{self.logic.stok_waktu}", self.aksi_waktu),
            ("REGEN HP",   f"x{self.logic.stok_heal}",  self.aksi_heal),
        ]
        for i, (nama, stok, aksi) in enumerate(items):
            col = tk.Frame(self.item_bar, bg="#1E293B")
            col.grid(row=0, column=i, sticky="nsew", padx=6, pady=6)
            kotak = tk.Button(col, text=f"{nama}\n{stok}", font=("Arial", 8, "bold"), bg="#475569", fg="#F1F5F9", relief="flat", bd=0, command=aksi)
            kotak.pack(fill="both", expand=True)
            kotak.bind("<Enter>", lambda e, b=kotak: b.configure(bg="#334155"))
            kotak.bind("<Leave>", lambda e, b=kotak: b.configure(bg="#475569"))
        self.item_bar.columnconfigure((0, 1, 2), weight=1)

    def build_keyboard(self):
        for w in self.kb_frame.winfo_children(): w.destroy()
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
                btn = tk.Button(f, text=char, font=("Arial", 10, "bold"), bg="#1E293B", fg="#F1F5F9", relief="flat", bd=0, width=3, height=1, command=lambda c=char: self.proses_tebakan(c))
                btn.pack(side="left", padx=2)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#334155") if b['state'] != 'disabled' else None)
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#1E293B") if b['state'] != 'disabled' else None)
                self.keys[char] = btn

    def proses_tebakan(self, huruf):
        hasil, pesan = self.logic.tebak_huruf(huruf)
        if hasil is None: return

        if hasil:
            self.keys[huruf].configure(bg="#059669", fg="white", state="disabled")
            self._set_banner("#10B981", pesan)
            winsound.Beep(1000, 120)
        else:
            self.keys[huruf].configure(bg="#DC2626", fg="white", state="disabled")
            self._set_banner("#EF4444", pesan)
            winsound.Beep(300, 180)
            self.guncang_window(10)
            self.flash_bar_merah(4)

        self.update_visuals()
        self.tangani_kondisi()

    def tangani_kondisi(self):
        status = self.logic.cek_status_game()

        if status == "next_word":
            self.logic.pindah_kata_berjalan = True
            winsound.Beep(1200, 100)
            self._set_banner("#10B981", "✨ KATA TERTEBAK! MENYAPU MUSUH BERIKUTNYA...")
            self.after(1000, self.eksekusi_kata_berikutnya)
            
        elif status == "victory":
            self._set_banner("#10B981", "🏆 LEVEL 1 BERHASIL DIKLAIM! VICTORY!")
            winsound.Beep(1200, 150)
            winsound.Beep(1600, 300)
            self.kirim_data_ke_parent("victory")

        elif status == "defeat":
            self._set_banner("#EF4444", "💀 ANNIHILATED! GAME OVER!")
            winsound.Beep(400, 200)
            winsound.Beep(250, 400)
            self.kirim_data_ke_parent("defeat")

    def eksekusi_kata_berikutnya(self):
        if self.logic.lanjut_kata_berikutnya():
            self._set_banner("#3B82F6", "KATA BARU DIMULAI! LANJUTKAN!")
            self.update_visuals()
            self.build_keyboard()

    def kirim_data_ke_parent(self, mode):
        skor = self.logic.hitung_skor() if mode == "victory" else 0
        sisa_waktu = self.logic.sisa_waktu if mode == "victory" else 0
        hp_player = self.logic.hp_player if mode == "victory" else 0
        kata = ", ".join(self.logic.daftar_kata) if mode == "victory" else self.logic.kata_rahasia
        
        if hasattr(self.parent, "set_hasil_game"):
            self.parent.set_hasil_game(
                kata=kata, skor=skor, sisa_waktu=sisa_waktu, hp_player=hp_player,
                tebakan_benar=self.logic.total_tebakan_benar, tebakan_salah=self.logic.total_tebakan_salah,
                huruf_ditebak=set(), mode=mode
            )
        self.after(1200, lambda: self.parent.switch_screen("screenresult.py"))

    def aksi_hint(self):
        huruf_hint = self.logic.gunakan_hint()
        if huruf_hint:
            self.proses_tebakan(huruf_hint)
        else:
            self._notif_habis("💡 ITEM HINT HABIS ATAU KATA SUDAH TERBUKA!")

    def aksi_waktu(self):
        if self.logic.gunakan_waktu():
            self.update_visuals()
            winsound.Beep(800, 100)
        else:
            self._notif_habis("🕒 ITEM WAKTU HABIS!")

    def aksi_heal(self):
        if self.logic.gunakan_heal():
            self.update_visuals()
            winsound.Beep(900, 150)
        else:
            self._notif_habis("❤️ ITEM HEAL HABIS!")

    def _notif_habis(self, pesan):
        self._set_banner("#D97706", pesan)
        winsound.Beep(200, 300)
        self.after(1800, lambda: self._set_banner("#3B82F6", "SILAKAN LANJUTKAN MENEBAK") if not self.logic.game_selesai else None)

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

    def update_timer(self):
        if self.logic.game_selesai: return
        
        if self.logic.sisa_waktu > 0 and self.logic.hp_player > 0:
            if not self.logic.pindah_kata_berjalan and self.logic.hp_musuh > 0:
                self.logic.sisa_waktu -= 1
                
            m, s = divmod(self.logic.sisa_waktu, 60)
            self.lbl_timer.configure(text=f"⏱ {m:02d}:{s:02d}", fg="#EF4444" if self.logic.sisa_waktu <= 15 else "#F59E0B")
            
            if self.logic.sisa_waktu <= 5 and not self.logic.pindah_kata_berjalan and self.logic.hp_musuh > 0:
                winsound.Beep(600, 80)
                
            self.after(1000, self.update_timer)
        else:
            self.tangani_kondisi()

# ── WRAPPER TESTING RUN ───────────────────────────────────────────
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