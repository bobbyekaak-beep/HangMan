from pertanyaan import ambil_pertanyaan
from logic.level_config import LEVEL_CONFIG
from database.koneksi import ambil_qty_item, pakai_item, ITEM_ID_PETUNJUK, ITEM_ID_TAMBAH_WAKTU, ITEM_ID_PULIHKAN_HP
from audio.sound_manager import putar_sfx
import random

class Level3Logic:
    def __init__(self, user_id=None):
        cfg = LEVEL_CONFIG[3]
        self.user_id = user_id
       # Ambil soal dari database Level 3
        self.data_soal = ambil_pertanyaan(3)

        self.daftar_kata = []
        self.daftar_petunjuk = []
        self.daftar_kategori = []

        for soal in self.data_soal:
            self.daftar_kata.append(soal["kata"])
            self.daftar_petunjuk.append(soal["petunjuk"])
            self.daftar_kategori.append(soal["kategori"])

        if not self.daftar_kata:
            raise ValueError(f"Tidak ada soal untuk level {3}")

        self.indeks_kata_sekarang = 0

        self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
        self.petunjuk = self.daftar_petunjuk[self.indeks_kata_sekarang]
        self.kategori = self.daftar_kategori[self.indeks_kata_sekarang]
        
        self.huruf_ditebak = set()
        self.hp_player, self.hp_player_max = 100, 100
        self.hp_musuh, self.hp_musuh_max = cfg["hp_musuh"], cfg["hp_musuh"]
        self.sisa_waktu = cfg["waktu_detik"]

        self.total_tebakan_benar = 0
        self.total_tebakan_salah = 0

        if self.user_id is not None:
            self.stok_hint, self.stok_waktu, self.stok_heal = ambil_qty_item(self.user_id)
        else:
            self.stok_hint = cfg["stok_hint"]
            self.stok_waktu = cfg["stok_waktu"]
            self.stok_heal = cfg["stok_heal"]

        self.game_selesai = False
        self.pindah_kata_berjalan = False  
        
        self.hitung_damage_kata()

    def hitung_damage_kata(self):
        self.huruf_unik = set(self.kata_rahasia)
        self.damage_per_huruf = self.hp_musuh_max / len(self.huruf_unik)

    def proses_huruf(self, h):
        """
        Memproses tebakan huruf.
        Mengembalikan tuple: (is_benar, status_berubah)
        status_berubah bisa berupa: 'normal', 'kata_terbuka', 'menang', 'kalah'
        """
        if h in self.huruf_ditebak or self.game_selesai or self.pindah_kata_berjalan: 
            return None, 'normal'
            
        self.huruf_ditebak.add(h)

        if h in self.kata_rahasia:
            self.total_tebakan_benar += 1
            # Bunyikan sfx tebakan benar
            putar_sfx("benar.mp3")
            self.hp_musuh = max(0, self.hp_musuh - self.damage_per_huruf)
            
            kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)
            if kata_terbuka:
                self.hp_musuh = 0
                if self.indeks_kata_sekarang < len(self.daftar_kata) - 1:
                    return True, 'kata_terbuka'
                else:
                    self.game_selesai = True
                    return True, 'menang'
            return True, 'normal'
        else:
            self.total_tebakan_salah += 1
            # Bunyikan sfx tebakan salah
            putar_sfx("salah.mp3")
            self.hp_player = max(0, self.hp_player - 25)
            if self.hp_player <= 0:
                self.game_selesai = True
                return False, 'kalah'
            return False, 'normal'

    def lanjut_kata(self):
        if self.indeks_kata_sekarang < len(self.daftar_kata) - 1:
            self.indeks_kata_sekarang += 1
            self.kata_rahasia = self.daftar_kata[self.indeks_kata_sekarang]
            self.petunjuk = self.daftar_petunjuk[self.indeks_kata_sekarang]
            self.kategori = self.daftar_kategori[self.indeks_kata_sekarang]
            self.huruf_ditebak = set()
            self.hp_musuh = self.hp_musuh_max
            self.hitung_damage_kata()
            self.pindah_kata_berjalan = False
            return True
        return False

    def kurangi_waktu(self):
        if not self.game_selesai and not self.pindah_kata_berjalan and self.hp_musuh > 0:
            self.sisa_waktu -= 1
            if self.sisa_waktu <= 0:
                self.game_selesai = True
                return 'kalah'
        return 'jalan'

    def gunakan_hint(self):
        if self.stok_hint > 0 and not self.game_selesai and not self.pindah_kata_berjalan:
            for c in self.kata_rahasia:
                if c not in self.huruf_ditebak:
                    self.stok_hint -= 1
                    if self.user_id is not None:
                        pakai_item(self.user_id, ITEM_ID_PETUNJUK)
                    return c
        return None

    def gunakan_waktu(self):
        if self.stok_waktu > 0 and not self.game_selesai:
            self.stok_waktu -= 1
            if self.user_id is not None:
                pakai_item(self.user_id, ITEM_ID_TAMBAH_WAKTU)
            self.sisa_waktu += 30
            return True
        return False

    def gunakan_heal(self):
        if self.stok_heal > 0 and not self.game_selesai:
            self.stok_heal -= 1
            if self.user_id is not None:
                pakai_item(self.user_id, ITEM_ID_PULIHKAN_HP)
            self.hp_player = min(self.hp_player_max, self.hp_player + 15)
            return True
        return False

    def hitung_skor(self):
        base = self.total_tebakan_benar * 30 
        bonus_waktu = self.sisa_waktu * 5           
        bonus_hp = self.hp_player * 3
        penalti = self.total_tebakan_salah * 20 
        return max(0, base + bonus_waktu + bonus_hp - penalti)