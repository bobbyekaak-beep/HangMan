import random

class DailyMissionLogic:
    def __init__(self, on_timer_update=None, on_banner_update=None, on_game_over=None, on_slots_update=None, on_shake=None):
        # Callback untuk komunikasi ke UI
        self.on_timer_update = on_timer_update
        self.on_banner_update = on_banner_update
        self.on_game_over = on_game_over
        self.on_slots_update = on_slots_update
        self.on_shake = on_shake

        # Config kata gaul
        kumpulan_kata_genz = [
            "TERGHOSTING",    # 11 Huruf
            "MENYALAKOK",     # 10 Huruf
            "OVTTERUSAN",     # 10 Huruf
            "REDPFLAGNIH",    # 11 Huruf
            "GAKSIMPATIK",    # 11 Huruf
            "KREATIFABANG",   # 12 Huruf
            "JAKSELBANGET"    # 12 Huruf
        ]
        
        self.kata_rahasia = random.choice(kumpulan_kata_genz)
        self.huruf_unik = set(self.kata_rahasia)
        self.huruf_ditebak = set()
        
        self.total_tebakan_benar = 0
        self.total_tebakan_salah = 0
        self.sisa_waktu = 120  # 2 Menit
        self.game_selesai = False

    def proses_tebakan(self, h):
        if h in self.huruf_ditebak or self.game_selesai: 
            return None
            
        self.huruf_ditebak.add(h)
        is_correct = h in self.kata_rahasia

        if is_correct:
            self.total_tebakan_benar += 1
            if self.on_banner_update:
                self.on_banner_update("#10B981", f"✅   BENAR! Huruf '{h}' ada di dalam kata")
        else:
            self.total_tebakan_salah += 1
            if self.on_banner_update:
                self.on_banner_update("#EF4444", f"❌   SALAH! Huruf '{h}' tidak ada")
            if self.on_shake:
                self.on_shake(6)

        if self.on_slots_update:
            self.on_slots_update()
            
        self.cek_kondisi()
        return is_correct

    def cek_kondisi(self):
        if self.game_selesai: 
            return

        kata_terbuka = all(c in self.huruf_ditebak for c in self.huruf_unik)

        if kata_terbuka:
            self.game_selesai = True
            if self.on_banner_update:
                self.on_banner_update("#10B981", "🏆   MISI HARIAN SELESAI!")
            if self.on_game_over:
                self.on_game_over(mode="victory")

    def hitung_mundur(self):
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