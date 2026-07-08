import tkinter as tk
import random
import winsound
from logic import misiharianlogic

class ScreenDailyMission(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#111827")
        self.parent = parent
        
        # Inisialisasi logika permainan dengan menghubungkan ke fungsi UI (Callback)
        self.logic = misiharianlogic(
            on_timer_update=self.ui_update_timer,
            on_banner_update=self._set_banner,
            on_game_over=self.ui_game_over,
            on_slots_update=self.update_slots,
            on_shake=self.guncang_window
        )
        
        self.keys = {}
        self.setup_ui()
        self.update_timer_loop()

    def setup_ui(self):
        # ── 1. TOP HUD (CUMA TIMER BESAR DI TENGAH) ─────────────────
        hud = tk.Frame(self, bg="#111827")
        hud.pack(fill="x", padx=20, pady=(25, 5))

        m, s = divmod(self.logic.sisa_waktu, 60)
        self.lbl_timer = tk.Label(hud, text=f"⏱   {m:02d}:{s:02d}", 
                                  font=("Arial", 20, "bold"), fg="#3B82F6", bg="#111827")
        self.lbl_timer.pack(expand=True)

        # ── 2. STATUS BANNER ─────────────────────────────────────
        self.status_banner = tk.Frame(self, bg="#D97706", height=35) 
        self.status_banner.pack(fill="x", padx=20, pady=10)
        self.status_banner.pack_propagate(False)

        self.lbl_status = tk.Label(self.status_banner, bg="#D97706", 
                                   text="⚡ DAILY MISSION: TIME ATTACK MODE ⚡", 
                                   font=("Arial", 10, "bold"), fg="white")
        self.lbl_status.pack(expand=True)

        # ── 3. SLOT KATA RAHASIA ──────────────────────────────────
        self.word_frame = tk.Frame(self, bg="#111827")
        self.word_frame.pack(pady=30, padx=10)

        # ── 4. KETERANGAN HURUF MASUK ──────────────────────────
        self.lbl_ditebak = tk.Label(self, bg="#111827", text="Huruf masuk: -", 
                                    font=("Arial", 10), fg="#6B7280")
        self.lbl_ditebak.pack(pady=(0, 10))

        # ── 5. KEYBOARD A–Z ──────────────────────────────────────
        self.kb_frame = tk.Frame(self, bg="#111827")
        self.kb_frame.pack(pady=15)
        self.build_keyboard()

        self.update_slots()

    def update_slots(self):
        for w in self.word_frame.winfo_children():
            w.destroy()

        for char in self.logic.kata_rahasia:
            terbuka = char in self.logic.huruf_ditebak
            box = tk.Frame(self.word_frame, bg="#1F2937" if terbuka else "#374151",
                           highlightbackground="#F59E0B" if terbuka else "#4B5563", 
                           highlightthickness=1, width=28, height=40)
            box.pack(side="left", padx=2) 
            box.pack_propagate(False)

            tk.Label(box, text=char if terbuka else "_", bg="#1F2937" if terbuka else "#374151",
                     font=("Arial", 14, "bold"), fg="#F59E0B" if terbuka else "#9CA3AF").pack(expand=True)

        if self.logic.huruf_ditebak:
            huruf_str = ", ".join(sorted(self.logic.huruf_ditebak))
            self.lbl_ditebak.configure(text=f"Huruf masuk: {huruf_str}")
        else:
            self.lbl_ditebak.configure(text="Huruf masuk: -")

    def build_keyboard(self):
        layout = [
            ["A","B","C","D","E","F","G","H","I"],
            ["J","K","L","M","N","O","P","Q","R"],
            ["S","T","U","V","W","X","Y","Z"],
        ]
        for row in layout:
            f = tk.Frame(self.kb_frame, bg="#111827")
            f.pack(pady=3)
            for char in row:
                btn = tk.Button(f, text=char, font=("Arial", 11, "bold"), bg="#1F2937", fg="#F9FAFB",
                    activebackground="#374151", activeforeground="#F59E0B", relief="flat", bd=0, 
                    highlightbackground="#4B5563", highlightthickness=1, width=3, height=1,
                    command=lambda c=char: self.handle_tebakan(c))
                btn.pack(side="left", padx=2)
                btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, "#374151"))
                btn.bind("<Leave>", lambda e, b=btn: self._on_leave(b, "#1F2937"))
                self.keys[char] = btn

    def _on_hover(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def _on_leave(self, button, color):
        if button['state'] != 'disabled': button.configure(bg=color)

    def _set_banner(self, warna, teks):
        self.status_banner.configure(bg=warna)
        self.lbl_status.configure(bg=warna, text=teks)

    def guncang_window(self, loop):
        if loop > 0:
            try:
                root = self.winfo_toplevel()
                x, y = root.winfo_x(), root.winfo_y()
                root.geometry(f"+{x + random.choice([-4, 4])}+{y}")
                self.after(28, lambda: self.guncang_window(loop - 1))
            except Exception: pass

    def handle_tebakan(self, h):
        # Jalankan logika tebakan
        is_correct = self.logic.proses_tebakan(h)
        
        if is_correct is None: 
            return # Huruf sudah diklik sebelumnya / game over

        if is_correct:
            self.keys[h].configure(bg="#059669", fg="white", state="disabled")
            winsound.Beep(1000, 120)
        else:
            self.keys[h].configure(bg="#DC2626", fg="white", state="disabled")
            winsound.Beep(300, 150)

    def ui_update_timer(self, sisa_waktu):
        m, s = divmod(sisa_waktu, 60)
        self.lbl_timer.configure(text=f"⏱   {m:02d}:{s:02d}", fg="#EF4444" if sisa_waktu <= 20 else "#3B82F6")
        
        if sisa_waktu <= 5 and sisa_waktu > 0:
            winsound.Beep(600, 80)

    def update_timer_loop(self):
        lanjut = self.logic.hitung_mundur()
        if lanjut:
            self.after(1000, self.update_timer_loop)

    def ui_game_over(self, mode):
        if mode == "victory":
            winsound.Beep(1200, 200)
            skor_akhir = self.logic.sisa_waktu * 15
            hp = 100
            delay = 1200
        else:
            winsound.Beep(250, 400)
            skor_akhir = 0
            hp = 0
            delay = 1500

        if hasattr(self.parent, "set_hasil_game"):
            self.parent.set_hasil_game(
                kata=self.logic.kata_rahasia, 
                skor=skor_akhir, 
                sisa_waktu=self.logic.sisa_waktu, 
                hp_player=hp, 
                tebakan_benar=self.logic.total_tebakan_benar, 
                tebakan_salah=self.logic.total_tebakan_salah, 
                huruf_ditebak=set(), 
                mode=mode
            )
        self.after(delay, lambda: self.parent.switch_screen("screenresult.py"))


# ── RUN TESTING ──────────────────────────────────────────────────
if __name__ == "__main__":
    class MockParent(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Daily Mission - Time Attack")
            self.geometry("460x420")
            self.configure(bg="#111827")
            
        def switch_screen(self, screen_name):
            print(f"[NAVIGASI] Pindah ke: {screen_name}")
            
        def set_hasil_game(self, **kwargs):
            print("[DATA] Hasil akhir dikirim:")
            for k, v in kwargs.items(): print(f"  - {k}: {v}")

    app_parent = MockParent()
    game_frame = ScreenDailyMission(parent=app_parent)
    game_frame.pack(fill="both", expand=True)
    app_parent.mainloop()