import random
from database.koneksi import (
    ambil_qty_item, pakai_item, tambah_koin_user, tambah_progress_misi,
    ITEM_ID_PETUNJUK, ITEM_ID_TAMBAH_WAKTU, ITEM_ID_PULIHKAN_HP,
    REWARD_PER_KATA_TIME_ATTACK,
)
from audio.sound_manager import putar_sfx

class DailyMissionLogic:
    def __init__(self, user_id=None, on_timer_update=None, on_banner_update=None, on_game_over=None,
                 on_slots_update=None, on_shake=None, on_next_soal=None, on_hp_update=None,
                 on_koin_update=None):
        # Simpan semua callback ke UI
        self.user_id = user_id
        self.on_timer_update = on_timer_update
        self.on_banner_update = on_banner_update
        self.on_game_over = on_game_over
        self.on_slots_update = on_slots_update
        self.on_shake = on_shake
        self.on_next_soal = on_next_soal
        self.on_hp_update = on_hp_update
        self.on_koin_update = on_koin_update

        self.kategori = "Profesi"
        self.bank_soal_profesi = [
            {"jawaban": "DOKTER", "petunjuk": "Memakai jas putih dan stetoskop"},
            {"jawaban": "GURU", "petunjuk": "Mengajar di depan kelas"},
            {"jawaban": "POLISI", "petunjuk": "Memakai seragam cokelat dan peluit"},
            {"jawaban": "PETANI", "petunjuk": "Bekerja di sawah dengan cangkul"},
            {"jawaban": "NELAYAN", "petunjuk": "Menangkap ikan naik perahu"},
            {"jawaban": "PILOT", "petunjuk": "Mengemudikan pesawat terbang"},
            {"jawaban": "KOKI", "petunjuk": "Memasak memakai topi putih tinggi"},
            {"jawaban": "MASINIS", "petunjuk": "Mengemudikan kereta api"},
            {"jawaban": "PERAWAT", "petunjuk": "Merawat pasien dan membantu dokter"},
            {"jawaban": "SOPIR", "petunjuk": "Mengemudikan mobil"},
        ]

        self.total_soal = 10
        self.daftar_soal = random.sample(self.bank_soal_profesi, len(self.bank_soal_profesi))
        while len(self.daftar_soal) < self.total_soal:
            self.daftar_soal.append(random.choice(self.bank_soal_profesi))

        self.indeks_soal = 0
        self.daftar_kata_terjawab = []
        self._muat_soal_sekarang()

        self.total_tebakan_benar = 0
        self.total_tebakan_salah = 0
        self.sisa_waktu = 30
        self.game_selesai = False
        self.pindah_soal_berjalan = False

        # Stok item Time Attack diambil dari inventory database, sama seperti mode level
        if self.user_id is not None:
            self.stok_hint, self.stok_waktu, self.stok_heal = ambil_qty_item(self.user_id)
        else:
            self.stok_hint, self.stok_waktu, self.stok_heal = 3, 3, 3

        # HP musuh & player dihitung sekali untuk seluruh 10 soal (tidak direset per soal/kata)
        self.hp_player, self.hp_player_max = 100, 100
        self.hp_musuh, self.hp_musuh_max = 100, 100
        total_huruf_unik_semua_soal = sum(len(set(soal["jawaban"])) for soal in self.daftar_soal)
        self.damage_per_huruf_benar = self.hp_musuh_max / max(1, total_huruf_unik_semua_soal)
        self.damage_tebakan_salah = 10

    def _muat_soal_sekarang(self):
        # Ambil soal aktif sesuai indeks_soal
        soal = self.daftar_soal[self.indeks_soal]
        self.kata_rahasia = soal["jawaban"]
        self.petunjuk = soal["petunjuk"]
        self.huruf_unik = set(self.kata_rahasia)
        self.huruf_ditebak = set()

    def proses_tebakan(self, h):
        # Proses satu huruf tebakan dari player, HP musuh/player tidak direset antar soal
        if h in self.huruf_ditebak or self.game_selesai or self.pindah_soal_berjalan:
            return None

        self.huruf_ditebak.add(h)
        is_correct = h in self.kata_rahasia

        if is_correct:
            self.total_tebakan_benar += 1
            # Bunyikan sfx tebakan benar
            putar_sfx("benar.mp3")
            self.hp_musuh = max(0, self.hp_musuh - self.damage_per_huruf_benar)
            if self.on_banner_update:
                self.on_banner_update("#10B981", f"✅   BENAR! Huruf '{h}' ada di dalam kata")
        else:
            self.total_tebakan_salah += 1
            # Bunyikan sfx tebakan salah
            putar_sfx("salah.mp3")
            self.hp_player = max(0, self.hp_player - self.damage_tebakan_salah)
            if self.on_banner_update:
                self.on_banner_update("#EF4444", f"❌   SALAH! Huruf '{h}' tidak ada")
            if self.on_shake:
                self.on_shake(6)

        if self.on_hp_update:
            self.on_hp_update(self.hp_player, self.hp_musuh)

        if self.on_slots_update:
            self.on_slots_update()

        if self.hp_player <= 0:
            self.game_selesai = True
            if self.on_banner_update:
                self.on_banner_update("#EF4444", "💀   HP HABIS! MISI GAGAL!")
            if self.on_game_over:
                self.on_game_over(mode="defeat")
            return is_correct

        self.cek_kondisi()
        return is_correct

    def cek_kondisi(self):
        # Cek apakah kata sekarang sudah tertebak semua, lalu beri reward dan tentukan next soal/victory
        if self.game_selesai or self.pindah_soal_berjalan:
            return

        kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)
        if not kata_terbuka:
            return

        self.daftar_kata_terjawab.append(self.kata_rahasia)
        self._beri_reward_kata_benar()

        if self.indeks_soal >= self.total_soal - 1:
            self.game_selesai = True
            if self.user_id is not None:
                tambah_progress_misi(self.user_id, "menang_time_attack", 1)
            if self.on_banner_update:
                self.on_banner_update("#10B981", "🏆   MISI HARIAN SELESAI!")
            if self.on_game_over:
                self.on_game_over(mode="victory")
        else:
            self.pindah_soal_berjalan = True
            if self.on_banner_update:
                self.on_banner_update(
                    "#10B981",
                    f"✅   SOAL {self.indeks_soal + 1}/{self.total_soal} SELESAI! +{REWARD_PER_KATA_TIME_ATTACK} KOIN"
                )
            if self.on_next_soal:
                self.on_next_soal(self.indeks_soal + 1, self.total_soal)

    def _beri_reward_kata_benar(self):
        # Beri koin dan progress misi 'tebak_kata' setiap satu kata berhasil ditebak penuh
        if self.user_id is None:
            return
        tambah_koin_user(self.user_id, REWARD_PER_KATA_TIME_ATTACK)
        tambah_progress_misi(self.user_id, "tebak_kata", 1)
        if self.on_koin_update:
            self.on_koin_update(REWARD_PER_KATA_TIME_ATTACK)

    def lanjut_soal_berikutnya(self):
        # Pindah ke soal berikutnya, HP dan sisa waktu TIDAK ditambah otomatis
        if self.indeks_soal < self.total_soal - 1:
            self.indeks_soal += 1
            self._muat_soal_sekarang()
            self.pindah_soal_berjalan = False
            return True
        return False

    def gunakan_hint(self):
        # Buka satu huruf yang belum ditebak sebagai bantuan
        if self.stok_hint <= 0 or self.game_selesai or self.pindah_soal_berjalan:
            return None
        for c in self.kata_rahasia:
            if c not in self.huruf_ditebak:
                self.stok_hint -= 1
                if self.user_id is not None:
                    pakai_item(self.user_id, ITEM_ID_PETUNJUK)
                return c
        return None

    def gunakan_waktu(self):
        # Tambah 15 detik sisa waktu, hanya lewat item ini (bukan otomatis)
        if self.stok_waktu <= 0 or self.game_selesai:
            return False
        self.stok_waktu -= 1
        self.sisa_waktu += 15
        if self.user_id is not None:
            pakai_item(self.user_id, ITEM_ID_TAMBAH_WAKTU)
            tambah_progress_misi(self.user_id, "tambah_waktu", 1)
        if self.on_timer_update:
            self.on_timer_update(self.sisa_waktu)
        return True

    def gunakan_heal(self):
        # Pulihkan 20 HP player, hanya lewat item ini (bukan otomatis)
        if self.stok_heal <= 0 or self.game_selesai:
            return False
        self.stok_heal -= 1
        self.hp_player = min(self.hp_player_max, self.hp_player + 20)
        if self.user_id is not None:
            pakai_item(self.user_id, ITEM_ID_PULIHKAN_HP)
            tambah_progress_misi(self.user_id, "pulihkan_hp", 1)
        if self.on_hp_update:
            self.on_hp_update(self.hp_player, self.hp_musuh)
        return True

    def hitung_mundur(self):
        # Kurangi sisa waktu tiap detik
        if self.game_selesai:
            return False

        if self.sisa_waktu > 0:
            self.sisa_waktu -= 1
            if self.on_timer_update:
                self.on_timer_update(self.sisa_waktu)
            return True
        else:
            self.game_selesai = True
            if self.on_banner_update:
                self.on_banner_update("#EF4444", f"⏳ WAKTU HABIS! JAWABAN: {self.kata_rahasia}")
            if self.on_game_over:
                self.on_game_over(mode="defeat")
            return False