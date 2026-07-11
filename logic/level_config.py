# Sumber data HP musuh, waktu, kesulitan, dan stok item tiap level
LEVEL_CONFIG = {
    1: {
        "hp_musuh": 100,
        "waktu_detik": 120,
        "kesulitan": "EASY",
        "stok_hint": 3,
        "stok_waktu": 2,
        "stok_heal": 3,
    },
    2: {
        "hp_musuh": 100,
        "waktu_detik": 90,
        "kesulitan": "MEDIUM",
        "stok_hint": 2,
        "stok_waktu": 2,
        "stok_heal": 2,
    },
    3: {
        "hp_musuh": 100,
        "waktu_detik": 60,
        "kesulitan": "HARD",
        "stok_hint": 1,
        "stok_waktu": 1,
        "stok_heal": 1,
    },
}

# Konfigurasi tampilan persiapan khusus mode Time Attack
TIME_ATTACK_CONFIG = {
    "kategori": "Profesi",
    "hp_musuh": 100,
    "waktu_detik": 30,
    "kesulitan": "VERY HARD",
}