import tkinter as tk
from tkinter import ttk
import random
from logic.page_game.misiharianlogic import DailyMissionLogic
from database.koneksi import hubungkan_database
from audio.sound_manager import putar_sfx, kecilkan_musik_latar, putar_sfx_hitung_mundur

class ScreenDailyMission(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#111827")
        self.parent = parent
        self.controller = controller

        self.username = None
        self.user_id = self._ambil_user_id()
        self.koin_sesi = 0
        self._run_id = 0

        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("PlayerTA.Horizontal.TProgressbar",
                             troughcolor="#1F2937", background="#10B981", thickness=14)
        self.style.configure("EnemyTA.Horizontal.TProgressbar",
                             troughcolor="#1F2937", background="#EF4444", thickness=14)

        self.logic = DailyMissionLogic(
            user_id=self.user_id,
            on_timer_update=self.ui_update_timer,
            on_banner_update=self._set_banner,
            on_game_over=self.ui_game_over,
            on_slots_update=self.update_slots,
            on_shake=self.guncang_window,
            on_next_soal=self.ui_next_soal,
            on_hp_update=self.ui_update_hp,
            on_koin_update=self.ui_tambah_koin,
        )

        self.keys = {}
        self.setup_ui()

        self.bind("<Key>", self.tekan_keyboard)
        self.focus_set()

    def _ambil_user_id(self):
        # Ambil id user aktif dari controller jika sudah login
        if self.controller is not None and hasattr(self.controller, "user_aktif") and self.controller.user_aktif is not None:
            return self.controller.user_aktif["id"]
        return None

    def on_show(self):
        # Reset logic, timer, dan tampilan tiap kali layar ini dibuka
        kecilkan_musik_latar()
        self.user_id = self._ambil_user_id()
        self.koin_sesi = 0
        self._run_id += 1
        self.logic = DailyMissionLogic(
            user_id=self.user_id,
            on_timer_update=self.ui_update_timer,
            on_banner_update=self._set_banner,
            on_game_over=self.ui_game_over,
            on_slots_update=self.update_slots,
            on_shake=self.guncang_window,
            on_next_soal=self.ui_next_soal,
            on_hp_update=self.ui_update_hp,
            on_koin_update=self.ui_tambah_koin,
        )
        self.lbl_koin.configure(text=f"💰 {self.koin_sesi}")
        m, s = divmod(self.logic.sisa_waktu, 60)
        self.lbl_timer.configure(text=f"⏱   {m:02d}:{s:02d}", fg="#3B82F6")
        self._set_banner("#D97706", "⚡ DAILY MISSION: TIME ATTACK MODE ⚡")
        self.lbl_kategori.configure(text=f"Kategori : {self.logic.kategori}")
        self.lbl_petunjuk.configure(text=f"Petunjuk : {self.logic.petunjuk}")
        self.ui_update_hp(self.logic.hp_player, self.logic.hp_musuh)
        self.update_progress()
        self.update_slots()
        self.build_keyboard()
        self.render_bottom_items()
        self.update_timer_loop(self._run_id)
        self.focus_set()

    def setup_ui(self):
        # Bangun seluruh elemen layar
        hpbar = tk.Frame(self, bg="#111827")
        hpbar.pack(fill="x", padx=20, pady=(18, 0))

        kiri = tk.Frame(hpbar, bg="#111827")
        kiri.pack(side="left")
        tk.Label(kiri, text="HP KAMU", bg="#111827", font=("Arial", 8, "bold"), fg="#9CA3AF").pack(anchor="w")
        self.bar_p = ttk.Progressbar(kiri, length=100, mode='determinate', style="PlayerTA.Horizontal.TProgressbar")
        self.bar_p.pack(pady=2)
        self.bar_p['value'] = (self.logic.hp_player / self.logic.hp_player_max) * 100
        self.lbl_hp_p = tk.Label(kiri, bg="#111827", text=f"{self.logic.hp_player}/{self.logic.hp_player_max}",
                                  font=("Arial", 8, "bold"), fg="#10B981")
        self.lbl_hp_p.pack(anchor="w")

        kanan = tk.Frame(hpbar, bg="#111827")
        kanan.pack(side="right")
        tk.Label(kanan, text="HP MUSUH", bg="#111827", font=("Arial", 8, "bold"), fg="#9CA3AF").pack(anchor="e")
        self.bar_g = ttk.Progressbar(kanan, length=100, mode='determinate', style="EnemyTA.Horizontal.TProgressbar")
        self.bar_g.pack(pady=2)
        self.bar_g['value'] = (self.logic.hp_musuh / self.logic.hp_musuh_max) * 100
        self.lbl_hp_g = tk.Label(kanan, bg="#111827", text=f"{int(self.logic.hp_musuh)}/{self.logic.hp_musuh_max}",
                                  font=("Arial", 8, "bold"), fg="#EF4444")
        self.lbl_hp_g.pack(anchor="e")

        hud = tk.Frame(self, bg="#111827")
        hud.pack(fill="x", padx=20, pady=(4, 5))

        m, s = divmod(self.logic.sisa_waktu, 60)
        self.lbl_timer = tk.Label(hud, text=f"⏱   {m:02d}:{s:02d}", 
                                  font=("Arial", 20, "bold"), fg="#3B82F6", bg="#111827")
        self.lbl_timer.pack(side="left", expand=True)

        self.lbl_koin = tk.Label(hud, text=f"💰 {self.koin_sesi}",
                                  font=("Arial", 12, "bold"), fg="#FBBF24", bg="#111827")
        self.lbl_koin.pack(side="right")

        self.status_banner = tk.Frame(self, bg="#D97706", height=35) 
        self.status_banner.pack(fill="x", padx=20, pady=10)
        self.status_banner.pack_propagate(False)

        self.lbl_status = tk.Label(self.status_banner, bg="#D97706", 
                                   text="⚡ DAILY MISSION: TIME ATTACK MODE ⚡", 
                                   font=("Arial", 10, "bold"), fg="white")
        self.lbl_status.pack(expand=True)

        self.lbl_progress = tk.Label(self, bg="#111827",
                                      text=f"Soal {self.logic.indeks_soal + 1}/{self.logic.total_soal}",
                                      font=("Arial", 9, "bold"), fg="#9CA3AF")
        self.lbl_progress.pack(pady=(0, 4))

        info_frame = tk.Frame(self, bg="#1F2937", highlightbackground="#374151", highlightthickness=1)
        info_frame.pack(fill="x", padx=20, pady=(0, 4))

        self.lbl_kategori = tk.Label(info_frame, bg="#1F2937", text=f"Kategori : {self.logic.kategori}",
                                      font=("Arial", 10, "bold"), fg="#60A5FA")
        self.lbl_kategori.pack(pady=(6, 0))

        self.lbl_petunjuk = tk.Label(info_frame, bg="#1F2937", text=f"Petunjuk : {self.logic.petunjuk}",
                                      font=("Arial", 9), fg="#9CA3AF", wraplength=350, justify="center")
        self.lbl_petunjuk.pack(pady=(0, 6))

        self.word_frame = tk.Frame(self, bg="#111827")
        self.word_frame.pack(pady=20, padx=10)

        self.lbl_ditebak = tk.Label(self, bg="#111827", text="Huruf masuk: -", 
                                    font=("Arial", 10), fg="#6B7280")
        self.lbl_ditebak.pack(pady=(0, 10))

        self.kb_frame = tk.Frame(self, bg="#111827")
        self.kb_frame.pack(pady=15)
        self.build_keyboard()

        self.item_bar = tk.Frame(self, bg="#1F2937", highlightbackground="#374151", highlightthickness=1, height=75)
        self.item_bar.pack(side="bottom", fill="x", padx=20, pady=14)
        self.item_bar.pack_propagate(False)
        self.render_bottom_items()

        self.update_slots()

    def ui_tambah_koin(self, jumlah):
        # Tambah tampilan koin sesi saat satu kata berhasil ditebak
        self.koin_sesi += jumlah
        self.lbl_koin.configure(text=f"💰 {self.koin_sesi}")

    def update_progress(self):
        # Tampilkan progres soal ke berapa dari total
        self.lbl_progress.configure(text=f"Soal {self.logic.indeks_soal + 1}/{self.logic.total_soal}")

    def ui_update_hp(self, hp_player, hp_musuh):
        # Update tampilan bar HP player & musuh
        self.bar_p['value'] = (hp_player / self.logic.hp_player_max) * 100
        self.lbl_hp_p.configure(text=f"{int(hp_player)}/{self.logic.hp_player_max}")
        self.bar_g['value'] = (hp_musuh / self.logic.hp_musuh_max) * 100
        self.lbl_hp_g.configure(text=f"{int(hp_musuh)}/{self.logic.hp_musuh_max}")

    def update_slots(self):
        # Gambar ulang kotak huruf sesuai huruf yang sudah terbuka
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
        # Bangun ulang tombol A-Z
        for w in self.kb_frame.winfo_children(): w.destroy()
        self.keys.clear()
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
        # Ubah warna tombol saat kursor masuk
        if button['state'] != 'disabled': button.configure(bg=color)

    def _on_leave(self, button, color):
        # Ubah warna tombol saat kursor keluar
        if button['state'] != 'disabled': button.configure(bg=color)

    def render_bottom_items(self):
        # Bangun ulang tombol bantuan (hint, tambah waktu, pulihkan hp)
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

    def aksi_hint(self):
        # Buka satu huruf pakai stok petunjuk
        huruf_hint = self.logic.gunakan_hint()
        if huruf_hint:
            self.render_bottom_items()
            self.handle_tebakan(huruf_hint)
            self.focus_set()
        else:
            self._notif_habis("💡 Petunjuk habis!")

    def aksi_waktu(self):
        # Tambah sisa waktu pakai stok tambah waktu
        if self.logic.gunakan_waktu():
            self.render_bottom_items()
        else:
            self._notif_habis("🕒 Tambah Waktu habis!")

    def aksi_heal(self):
        # Pulihkan HP player pakai stok pulihkan HP
        if self.logic.gunakan_heal():
            self.render_bottom_items()
        else:
            self._notif_habis("❤️ Pulihkan HP habis!")

    def _notif_habis(self, pesan):
        # Tampilkan notifikasi stok item habis sesaat
        self._set_banner("#D97706", pesan)
        self.after(1500, lambda: self._set_banner("#D97706", "⚡ DAILY MISSION: TIME ATTACK MODE ⚡"))

    def _set_banner(self, warna, teks):
        # Ganti warna dan teks banner status
        self.status_banner.configure(bg=warna)
        self.lbl_status.configure(bg=warna, text=teks)

    def guncang_window(self, loop):
        # Efek goyang window saat tebakan salah
        if loop > 0:
            try:
                root = self.winfo_toplevel()
                x, y = root.winfo_x(), root.winfo_y()
                root.geometry(f"+{x + random.choice([-4, 4])}+{y}")
                self.after(28, lambda: self.guncang_window(loop - 1))
            except Exception: pass

    def tekan_keyboard(self, event):
        # Teruskan huruf dari keyboard fisik ke tombol yang sama
        huruf = event.char.upper()
        if not huruf.isalpha():
            return
        if huruf in self.keys and self.keys[huruf]["state"] == "normal":
            self.keys[huruf].invoke()

    def handle_tebakan(self, h):
        # Proses satu huruf yang ditebak dari klik atau keyboard
        is_correct = self.logic.proses_tebakan(h)

        if is_correct is None: 
            return

        if is_correct:
            self.keys[h].configure(bg="#059669", fg="white", state="disabled")
        else:
            self.keys[h].configure(bg="#DC2626", fg="white", state="disabled")

        self.focus_set()

    def ui_next_soal(self, soal_berikutnya, total_soal):
        # Beri jeda sebelum pindah ke soal berikutnya
        self.after(900, self.eksekusi_soal_berikutnya)

    def eksekusi_soal_berikutnya(self):
        # Muat soal baru ke tampilan, HP & waktu tetap seperti sebelumnya (tidak ditambah)
        if self.logic.lanjut_soal_berikutnya():
            self._set_banner("#3B82F6", "SOAL BARU DIMULAI! LANJUTKAN!")
            self.lbl_petunjuk.configure(text=f"Petunjuk : {self.logic.petunjuk}")
            self.update_progress()
            self.update_slots()
            self.build_keyboard()
            self.render_bottom_items()
            self.focus_set()

    def ui_update_timer(self, sisa_waktu):
        # Update angka timer di layar
        m, s = divmod(sisa_waktu, 60)
        self.lbl_timer.configure(text=f"⏱   {m:02d}:{s:02d}", fg="#EF4444" if sisa_waktu <= 10 else "#3B82F6")

        # Bunyikan sfx hitung mundur saat sisa waktu 10 detik atau kurang
        if sisa_waktu <= 10:
            putar_sfx_hitung_mundur()

    def update_timer_loop(self, run_id=None):
        # Loop hitung mundur 1 detik sekali
        if run_id != self._run_id:
            return
        lanjut = self.logic.hitung_mundur()
        if lanjut:
            self.after(1000, lambda: self.update_timer_loop(run_id))

    def ui_game_over(self, mode):
        # Kirim hasil akhir permainan ke controller
        kata_terjawab = ",".join(self.logic.daftar_kata_terjawab)

        if mode == "victory":
            skor_akhir = self.logic.sisa_waktu * 15
            hp = int(self.logic.hp_player)
            delay = 1200
        else:
            skor_akhir = 0
            hp = int(self.logic.hp_player)
            delay = 1500

        if hasattr(self.controller, "set_hasil_game"):
            self.after(delay, lambda: self.controller.set_hasil_game(
                kata=kata_terjawab, 
                skor=skor_akhir, 
                sisa_waktu=self.logic.sisa_waktu, 
                hp_player=hp, 
                tebakan_benar=self.logic.total_tebakan_benar, 
                tebakan_salah=self.logic.total_tebakan_salah, 
                huruf_ditebak=set(), 
                mode=mode, level=0,
                total_kata_level=self.logic.total_soal
            ))

    def load_user(self, username):
        # Ambil id dan koin user dari database
        self.username = username

        db = hubungkan_database()
        if db:
            cursor = None
            try:
                cursor = db.cursor()

                cursor.execute(
                    "SELECT id, coins FROM users WHERE username=%s",
                    (username,)
                )

                hasil = cursor.fetchone()

                if hasil:
                    self.user_id = hasil[0]
                    self.koin = hasil[1]
            except Exception as e:
                print(f"[DATABASE] Error mengambil data user: {e}")
            finally:
                if cursor is not None:
                    cursor.close()
                db.close()