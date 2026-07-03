import customtkinter as ctk

class Screen9Result(ctk.CTkFrame):
    """
    Satu file untuk Victory (mode="victory") dan Defeat (mode="defeat").
    Dipanggil dari gameplay via:
      parent.switch_screen("screen9_result")          → victory
      parent.switch_screen("screen9_result", "defeat") → defeat
    
    Atau lebih simpel: parent.hasil_terakhir["mode"] = "victory"/"defeat"
    lalu switch_screen("screen9_result") saja.
    """
    def __init__(self, parent):
        super().__init__(parent, fg_color="#FFFFFF")
        self.parent = parent

        h             = parent.hasil_terakhir
        self.mode     = h.get("mode", "victory")   # "victory" atau "defeat"
        kata          = h.get("kata",          "???")
        skor          = h.get("skor",          0)
        sisa_waktu    = h.get("sisa_waktu",    0)
        hp_player     = h.get("hp_player",     0)
        tebakan_benar = h.get("tebakan_benar", 0)
        tebakan_salah = h.get("tebakan_salah", 0)
        huruf_ditebak = h.get("huruf_ditebak", set())

        bonus_waktu = sisa_waktu * 2
        bonus_hp    = hp_player
        bonus_tebak = tebakan_benar * 20
        penalti     = tebakan_salah * 15

        m, s      = divmod(sisa_waktu, 60)
        waktu_str = f"{m:02d}:{s:02d}"

        # Koin hanya diberikan saat menang
        koin_dapat = 150 if self.mode == "victory" else 20
        parent.koin += koin_dapat

        if self.mode == "victory":
            self._update_leaderboard(parent, skor)

        if self.mode == "victory":
            self._build_victory(
                kata, skor, koin_dapat,
                waktu_str, bonus_waktu,
                hp_player, bonus_hp,
                tebakan_benar, bonus_tebak,
                tebakan_salah, penalti,
                huruf_ditebak,
            )
        else:
            self._build_defeat(kata, koin_dapat, tebakan_benar, tebakan_salah)

    # ── Leaderboard ──────────────────────────────────────────────
    def _update_leaderboard(self, parent, skor_baru):
        nama = parent.player_name
        data = parent.leaderboard_data
        for i, (n, s) in enumerate(data):
            if n == nama:
                if skor_baru > s:
                    data[i] = (nama, skor_baru)
                break
        else:
            data.append((nama, skor_baru))
        parent.leaderboard_data = sorted(data, key=lambda x: x[1], reverse=True)

    # ══════════════════════════════════════════════════════════════
    #  VICTORY UI
    # ══════════════════════════════════════════════════════════════
    def _build_victory(self, kata, skor, koin_dapat,
                       waktu_str, bonus_waktu,
                       hp_player, bonus_hp,
                       tebakan_benar, bonus_tebak,
                       tebakan_salah, penalti,
                       huruf_ditebak):

        # Banner hijau
        banner = ctk.CTkFrame(self, fg_color="#4CAF50", corner_radius=0, height=70)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        ctk.CTkLabel(banner, text="🏆  VICTORY!",
                     font=("Arial", 28, "bold"), text_color="white").pack(expand=True)

        ctk.CTkLabel(self, text=f"KATA: {kata}",
                     font=("Arial", 14, "bold"), text_color="#555555").pack(pady=(16, 2))

        # Reward koin
        rw = ctk.CTkFrame(self, fg_color="#FFF8E1", corner_radius=12,
                           border_width=1, border_color="#FFE082")
        rw.pack(fill="x", padx=35, pady=8)
        ctk.CTkLabel(rw, text="REWARD",
                     font=("Arial", 11, "bold"), text_color="#9E9E9E").pack(pady=(10, 0))
        ctk.CTkLabel(rw, text=f"🪙  +{koin_dapat}",
                     font=("Arial", 24, "bold"), text_color="#FF9800").pack(pady=(2, 10))

        # Rincian poin
        detail = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10,
                               border_width=1, border_color="#E0E0E0")
        detail.pack(fill="x", padx=35, pady=4)

        baris = [
            ("🕒", f"Sisa Waktu  {waktu_str}",         f"+{bonus_waktu}", "#1E88E5"),
            ("❤️", f"Sisa HP Kamu  {hp_player}/100",   f"+{bonus_hp}",    "#4CAF50"),
            ("✅", f"Tebakan Benar  {tebakan_benar}x",  f"+{bonus_tebak}", "#4CAF50"),
            ("❌", f"Tebakan Salah  {tebakan_salah}x",  f"-{penalti}",     "#E53935"),
        ]
        for i, (ikon, label, nilai, warna) in enumerate(baris):
            row = ctk.CTkFrame(detail, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=5)
            ctk.CTkLabel(row, text=f"{ikon}  {label}",
                         font=("Arial", 11), text_color="#333333", anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=nilai,
                         font=("Arial", 11, "bold"), text_color=warna, anchor="e").pack(side="right")
            if i < len(baris) - 1:
                ctk.CTkFrame(detail, fg_color="#E0E0E0", height=1).pack(fill="x", padx=14)

        # Huruf ditebak
        if huruf_ditebak:
            ctk.CTkLabel(self, text=f"Huruf ditebak: {'  '.join(sorted(huruf_ditebak))}",
                         font=("Arial", 10), text_color="#888888").pack(pady=(4, 0))

        # Total skor
        sf = ctk.CTkFrame(self, fg_color="#E8F5E9", corner_radius=10,
                           border_width=1, border_color="#A5D6A7")
        sf.pack(fill="x", padx=35, pady=6)
        ctk.CTkLabel(sf, text="TOTAL SKOR",
                     font=("Arial", 11, "bold"), text_color="#757575").pack(pady=(8, 0))
        ctk.CTkLabel(sf, text=f"⭐  {skor}",
                     font=("Arial", 26, "bold"), text_color="#388E3C").pack(pady=(0, 8))

        # Tombol
        ctk.CTkButton(self, text="LANJUT LEVEL",
                      font=("Arial", 13, "bold"), fg_color="#4CAF50", hover_color="#388E3C",
                      height=44, corner_radius=10,
                      command=lambda: self.parent.switch_screen("screen4_pilih_level")
                      ).pack(fill="x", padx=35, pady=(10, 5))
        ctk.CTkButton(self, text="KEMBALI KE MENU",
                      font=("Arial", 13, "bold"), fg_color="#1E88E5", hover_color="#1565C0",
                      height=44, corner_radius=10,
                      command=lambda: self.parent.switch_screen("screen3_menu_utama")
                      ).pack(fill="x", padx=35, pady=5)
        ctk.CTkButton(self, text="📤  BAGIKAN",
                      font=("Arial", 12), fg_color="transparent", hover_color="#F5F5F5",
                      border_width=1, border_color="#BDBDBD", text_color="#555555",
                      height=36, corner_radius=10, command=self._bagikan
                      ).pack(fill="x", padx=35, pady=5)

    # ══════════════════════════════════════════════════════════════
    #  DEFEAT UI
    # ══════════════════════════════════════════════════════════════
    def _build_defeat(self, kata, koin_dapat, tebakan_benar, tebakan_salah):

        # Banner merah
        banner = ctk.CTkFrame(self, fg_color="#E53935", corner_radius=0, height=70)
        banner.pack(fill="x")
        banner.pack_propagate(False)
        ctk.CTkLabel(banner, text="💀  GAME OVER",
                     font=("Arial", 26, "bold"), text_color="white").pack(expand=True)

        ctk.CTkLabel(self, text="KATA YANG BENAR",
                     font=("Arial", 12), text_color="#777777").pack(pady=(20, 2))
        ctk.CTkLabel(self, text=kata,
                     font=("Arial", 22, "bold"), text_color="#E53935").pack()

        # Reward kecil (hiburan)
        rw = ctk.CTkFrame(self, fg_color="#FFF8E1", corner_radius=12,
                           border_width=1, border_color="#FFE082")
        rw.pack(fill="x", padx=35, pady=16)
        ctk.CTkLabel(rw, text="REWARD",
                     font=("Arial", 11, "bold"), text_color="#9E9E9E").pack(pady=(10, 0))
        ctk.CTkLabel(rw, text=f"🪙  +{koin_dapat}",
                     font=("Arial", 22, "bold"), text_color="#FF9800").pack(pady=(2, 4))
        ctk.CTkLabel(rw, text="Teruslah berlatih dan coba lagi!",
                     font=("Arial", 10), text_color="#AAAAAA").pack(pady=(0, 10))

        # Statistik singkat
        stat = ctk.CTkFrame(self, fg_color="#F5F5F5", corner_radius=10,
                             border_width=1, border_color="#E0E0E0")
        stat.pack(fill="x", padx=35, pady=4)

        for ikon, label, nilai, warna in [
            ("✅", "Tebakan Benar", str(tebakan_benar), "#4CAF50"),
            ("❌", "Tebakan Salah", str(tebakan_salah), "#E53935"),
        ]:
            row = ctk.CTkFrame(stat, fg_color="transparent")
            row.pack(fill="x", padx=14, pady=8)
            ctk.CTkLabel(row, text=f"{ikon}  {label}",
                         font=("Arial", 12), text_color="#333333", anchor="w").pack(side="left")
            ctk.CTkLabel(row, text=nilai,
                         font=("Arial", 13, "bold"), text_color=warna, anchor="e").pack(side="right")

        ctk.CTkLabel(self, text="REWARD",
                     font=("Arial", 11, "bold"), text_color="#9E9E9E").pack(pady=(16, 2))
        ctk.CTkLabel(self, text="🪙  20",
                     font=("Arial", 20, "bold"), text_color="#FF9800").pack()

        # Tombol
        ctk.CTkButton(self, text="🔄  COBA LAGI",
                      font=("Arial", 13, "bold"), fg_color="#E53935", hover_color="#C62828",
                      height=44, corner_radius=10,
                      command=lambda: self.parent.switch_screen("screen6_gameplay")
                      ).pack(fill="x", padx=35, pady=(20, 5))
        ctk.CTkButton(self, text="KEMBALI KE MENU",
                      font=("Arial", 13, "bold"), fg_color="#1E88E5", hover_color="#1565C0",
                      height=44, corner_radius=10,
                      command=lambda: self.parent.switch_screen("screen3_menu_utama")
                      ).pack(fill="x", padx=35, pady=5)
        ctk.CTkButton(self, text="💡  TIPS",
                      font=("Arial", 12), fg_color="transparent", hover_color="#F5F5F5",
                      border_width=1, border_color="#BDBDBD", text_color="#555555",
                      height=36, corner_radius=10, command=self._tampil_tips
                      ).pack(fill="x", padx=35, pady=5)

    # ── Helper ───────────────────────────────────────────────────
    def _bagikan(self):
        try:
            h    = self.parent.hasil_terakhir
            teks = (f"Aku berhasil menebak kata '{h['kata']}' "
                    f"di Hangman Word Quest dengan skor {h['skor']}! 🏆")
            self.clipboard_clear()
            self.clipboard_append(teks)
        except Exception:
            pass

    def _tampil_tips(self):
        tips = [
            "Mulai dengan huruf vokal: A, I, U, E, O",
            "Huruf R, N, T, S, L paling sering muncul",
            "Gunakan Petunjuk Huruf saat tersisa 2 huruf",
            "Simpan Heal untuk darurat — HP di bawah 20",
        ]
        import random
        tip = random.choice(tips)
        # Tampilkan di banner sementara (jika ada) atau popup sederhana
        try:
            top = ctk.CTkToplevel(self)
            top.title("Tips")
            top.geometry("300x130")
            top.resizable(False, False)
            ctk.CTkLabel(top, text=f"💡  {tip}",
                         font=("Arial", 12), wraplength=260,
                         text_color="#333333").pack(expand=True, padx=20)
            ctk.CTkButton(top, text="OK", width=80, fg_color="#1E88E5",
                          command=top.destroy).pack(pady=(0, 15))
        except Exception:
            pass