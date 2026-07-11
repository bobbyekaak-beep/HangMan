import os
import time
import pygame

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER_SFX = os.path.join(BASE_DIR, "assets", "sfx")

_sudah_init = False
_channel_musik = None
_channel_sfx = None
_channel_hitung_mundur = None
_waktu_terakhir_sfx = {}
_cooldown_default = 0.15
VOLUME_MUSIK_NORMAL = 0.5
VOLUME_MUSIK_IN_GAME = 0.15

def _pastikan_init():
    global _sudah_init, _channel_musik, _channel_sfx, _channel_hitung_mundur
    if _sudah_init:
        return
    pygame.mixer.init()
    pygame.mixer.set_num_channels(16)
    _channel_musik = pygame.mixer.Channel(0)
    _channel_sfx = pygame.mixer.Channel(1)
    _channel_hitung_mundur = pygame.mixer.Channel(2)
    _sudah_init = True

def putar_musik_latar(nama_file="sound_latar.mp3", volume=0.5, loop=True):
    _pastikan_init()
    path = os.path.join(FOLDER_SFX, nama_file)
    if not os.path.isfile(path):
        print(f"[AUDIO] File musik latar tidak ditemukan: {path}")
        return
    try:
        suara = pygame.mixer.Sound(path)
        _channel_musik.play(suara, loops=-1 if loop else 0)
        _channel_musik.set_volume(volume)
    except Exception as e:
        print(f"[AUDIO] Gagal memutar musik latar: {e}")

def hentikan_musik_latar():
    _pastikan_init()
    _channel_musik.stop()

def set_volume_musik_latar(volume):
    _pastikan_init()
    _channel_musik.set_volume(volume)

def kecilkan_musik_latar(volume=VOLUME_MUSIK_IN_GAME):
    # Kecilkan musik latar saat masuk ke layar gameplay agar tidak menabrak sfx
    set_volume_musik_latar(volume)

def normalkan_musik_latar(volume=VOLUME_MUSIK_NORMAL):
    # Kembalikan musik latar ke volume normal saat keluar dari gameplay
    set_volume_musik_latar(volume)

def hentikan_semua_sfx():
    _pastikan_init()
    for nomor_channel in range(pygame.mixer.get_num_channels()):
        if nomor_channel == 0:
            continue
        pygame.mixer.Channel(nomor_channel).stop()

def putar_sfx_hitung_mundur(nama_file="hitung_mundur.mp3", volume=0.8):
    # Pakai channel khusus agar tiap detik otomatis memotong bunyi detik sebelumnya,
    # bukan numpuk main bareng seperti sfx lain yang pakai find_channel()
    _pastikan_init()
    path = os.path.join(FOLDER_SFX, nama_file)
    if not os.path.isfile(path):
        print(f"[AUDIO] File sfx tidak ditemukan: {path}")
        return
    try:
        suara = pygame.mixer.Sound(path)
        suara.set_volume(volume)
        _channel_hitung_mundur.play(suara)
    except Exception as e:
        print(f"[AUDIO] Gagal memutar sfx {nama_file}: {e}")

def putar_sfx(nama_file, volume=0.8, cooldown=_cooldown_default):
    _pastikan_init()
    sekarang = time.time()
    terakhir = _waktu_terakhir_sfx.get(nama_file, 0)
    if sekarang - terakhir < cooldown:
        return
    _waktu_terakhir_sfx[nama_file] = sekarang

    path = os.path.join(FOLDER_SFX, nama_file)
    if not os.path.isfile(path):
        print(f"[AUDIO] File sfx tidak ditemukan: {path}")
        return
    try:
        suara = pygame.mixer.Sound(path)
        suara.set_volume(volume)
        channel = pygame.mixer.find_channel()
        if channel is None:
            channel = _channel_sfx
        channel.play(suara)
    except Exception as e:
        print(f"[AUDIO] Gagal memutar sfx {nama_file}: {e}")