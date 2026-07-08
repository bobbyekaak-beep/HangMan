import random

class Level2Logic:
    def __init__(self):
        # Configuration Level 2
        self.daftar_kata = ["HARIMAU", "JERAPAH", "MERPATI", "KOMODO", "SERGALA", "BANTENG"]
        self.indeks_kata_sekarang = 0
        self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
        
        self.huruf_ditebak = set()
        self.hp_player, self.hp_player_max = 100, 100
        self.hp_musuh, self.hp_musuh_max = 100, 100
        self.sisa_waktu = 90  # 01:30

        self.total_tebakan_benar = 0
        self.total_tebakan_salah = 0

        self.stok_hint = 2  
        self.stok_waktu = 2
        self.stok_heal = 2

        self.game_selesai = False
        self.pindah_kata_berjalan = False  # Guard flag anti-bug transisi kata

        self.hitung_damage_kata()

    def hitung_damage_kata(self):
        self.huruf_unik = set(self.kata_rahasia)
        self.damage_per_huruf = self.hp_musuh_max / len(self.huruf_unik)

    def tebak_huruf(self, h):
        """Mengembalikan tuple (apakah_benar, detail_status)"""
        if h in self.huruf_ditebak or self.game_selesai or self.pindah_kata_berjalan:
            return None, "ignored"
            
        self.huruf_ditebak.add(h)

        if h in self.kata_rahasia:
            self.total_tebakan_benar += 1
            self.hp_musuh = max(0, self.hp_musuh - self.damage_per_huruf)
            
            kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)
            if kata_terbuka:
                self.hp_musuh = 0
            return True, "correct"
        else:
            self.total_tebakan_salah += 1
            self.hp_player = max(0, self.hp_player - 20)
            return False, "wrong"

    def lanjut_kata_berikutnya(self):
        if self.indeks_kata_sekarang < len(self.daftar_kata) - 1:
            self.indeks_kata_sekarang += 1
            self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
            self.huruf_ditebak = set()
            self.hp_musuh = self.hp_musuh_max
            self.hitung_damage_kata()
            self.pindah_kata_berjalan = False
            return True
        return False

    def gunakan_hint(self):
        if self.stok_hint <= 0 or self.game_selesai or self.pindah_kata_berjalan:
            return None
        for c in self.kata_rahasia:
            if c not in self.huruf_ditebak:
                self.stok_hint -= 1
                return c
        return None

    def gunakan_waktu(self):
        if self.stok_waktu <= 0 or self.game_selesai:
            return False
        self.stok_waktu -= 1
        self.sisa_waktu += 30
        return True

    def gunakan_heal(self):
        if self.stok_heal <= 0 or self.game_selesai:
            return False
        self.stok_heal -= 1
        self.hp_player = min(self.hp_player_max, self.hp_player + 20)
        return True

    def hitung_skor(self):
        base = self.total_tebakan_benar * 25 
        bonus_waktu = self.sisa_waktu * 3
        bonus_hp = self.hp_player * 2
        penalti = self.total_tebakan_salah * 15 
        return max(0, base + bonus_waktu + bonus_hp - penalti)

    def cek_kata_terbuka(self):
        return all(c in self.huruf_ditebak for c in self.huruf_unik)