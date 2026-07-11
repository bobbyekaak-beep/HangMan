import mysql.connector

def hubungkan_database():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",          
            password="",          
            database="db_hangman" 
        )
        return db
    except mysql.connector.Error as err:
        print(f"Gagal terhubung ke database: {err}")
        return None

def ambil_koin_user(user_id):
    """Fungsi untuk mengambil jumlah koin pemain dari database"""
    db = hubungkan_database()
    if db is not None:
        cursor = None
        try:
            cursor = db.cursor()
            query = "SELECT coins FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            hasil = cursor.fetchone()

            if hasil:
                return hasil[0]
        except mysql.connector.Error as err:
            print(f"Error mengambil koin: {err}")
        finally:
            if cursor is not None:
                cursor.close()
            db.close()
    return 0

MAX_LEVEL = 3

def ambil_highest_level(user_id):
    """Ambil level tertinggi yang sudah terbuka untuk user, default 1"""
    db = hubungkan_database()
    if db is not None:
        cursor = None
        try:
            cursor = db.cursor()
            query = "SELECT highest_level FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            hasil = cursor.fetchone()

            if hasil:
                return hasil[0]
        except mysql.connector.Error as err:
            print(f"Error mengambil highest_level: {err}")
        finally:
            if cursor is not None:
                cursor.close()
            db.close()
    return 1

def buka_level_berikutnya(user_id, level_yang_dimenangkan):
    """Naikkan highest_level user kalau level yang baru dimenangkan membuka level baru"""
    db = hubungkan_database()
    if db is not None:
        cursor = None
        try:
            cursor = db.cursor()
            query = "UPDATE users SET highest_level = GREATEST(highest_level, %s) WHERE id = %s"
            cursor.execute(query, (level_yang_dimenangkan + 1, user_id))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error membuka level berikutnya: {err}")
        finally:
            if cursor is not None:
                cursor.close()
            db.close()

def tambah_koin_user(user_id, jumlah_tambahan):
    """Fungsi untuk menambahkan koin pemain saat misi selesai"""
    db = hubungkan_database()
    if db is not None:
        cursor = None
        try:
            cursor = db.cursor()
            query = "UPDATE users SET coins = coins + %s WHERE id = %s"
            cursor.execute(query, (jumlah_tambahan, user_id))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error menambah koin: {err}")
        finally:
            if cursor is not None:
                cursor.close()
            db.close()

ITEM_ID_PETUNJUK = 1
ITEM_ID_TAMBAH_WAKTU = 2
ITEM_ID_PULIHKAN_HP = 3

def ambil_qty_item(user_id):
    """Ambil jumlah item bantuan milik user dari tabel user_inventory"""
    db = hubungkan_database()
    if db is None:
        return 0, 0, 0
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT item_id, jumlah FROM user_inventory WHERE user_id = %s", (user_id,))
        jumlah_per_item = dict(cursor.fetchall())
        return (
            jumlah_per_item.get(ITEM_ID_PETUNJUK, 0),
            jumlah_per_item.get(ITEM_ID_TAMBAH_WAKTU, 0),
            jumlah_per_item.get(ITEM_ID_PULIHKAN_HP, 0),
        )
    except mysql.connector.Error as err:
        print(f"Error mengambil item: {err}")
        return 0, 0, 0
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

def pakai_item(user_id, item_id, jumlah=1):
    """Kurangi jumlah item milik user di tabel user_inventory setelah dipakai di dalam game"""
    db = hubungkan_database()
    if db is None:
        return
    cursor = None
    try:
        cursor = db.cursor()
        query = "UPDATE user_inventory SET jumlah = GREATEST(0, jumlah - %s) WHERE user_id = %s AND item_id = %s"
        cursor.execute(query, (jumlah, user_id, item_id))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error memakai item: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

BATAS_MAIN_TIME_ATTACK = 3

def ambil_main_time_attack(user_id):
    """Ambil berapa kali akun ini sudah main mode Time Attack"""
    db = hubungkan_database()
    if db is None:
        return 0
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("SELECT time_attack_played FROM users WHERE id = %s", (user_id,))
        hasil = cursor.fetchone()
        return hasil[0] if hasil else 0
    except mysql.connector.Error as err:
        print(f"Error mengambil jumlah main Time Attack: {err}")
        return 0
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

def tambah_main_time_attack(user_id):
    """Tambah 1 catatan main Time Attack untuk akun ini"""
    db = hubungkan_database()
    if db is None:
        return
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute("UPDATE users SET time_attack_played = time_attack_played + 1 WHERE id = %s", (user_id,))
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error menambah jumlah main Time Attack: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

MISI_DEFINISI = [
    {"key": "menang_time_attack", "judul": "Menangkan Mode Time Attack", "icon": "⚔️", "icon_bg": "#E65100", "target": 1, "reward": 700},
    {"key": "tebak_kata", "judul": "Tebak 3 Kata dengan Benar", "icon": "🎯", "icon_bg": "#2196F3", "target": 3, "reward": 150},
    {"key": "pulihkan_hp", "judul": "Pulihkan HP 2 Kali", "icon": "♥", "icon_bg": "#F44336", "target": 2, "reward": 100},
    {"key": "tambah_waktu", "judul": "Gunakan Item Waktu 1 Kali", "icon": "⏱", "icon_bg": "#FF9800", "target": 1, "reward": 50},
]
BONUS_MISI_REWARD = 1000
REWARD_PER_KATA_TIME_ATTACK = 50

def ambil_misi_user(user_id):
    """Pastikan baris misi harian ada di database lalu kembalikan progress terbaru tiap misi"""
    db = hubungkan_database()
    if db is None:
        return [{**m, "current": 0, "diambil": False} for m in MISI_DEFINISI]
    cursor = None
    try:
        cursor = db.cursor()
        for m in MISI_DEFINISI:
            cursor.execute(
                "INSERT IGNORE INTO user_misi (user_id, misi_key, current, target, selesai, diambil) VALUES (%s, %s, 0, %s, 0, 0)",
                (user_id, m["key"], m["target"]),
            )
        db.commit()
        cursor.execute("SELECT misi_key, current, target, selesai, diambil FROM user_misi WHERE user_id = %s", (user_id,))
        baris = {r[0]: r for r in cursor.fetchall()}
        hasil = []
        for m in MISI_DEFINISI:
            r = baris.get(m["key"])
            current, diambil = (r[1], bool(r[4])) if r else (0, False)
            hasil.append({**m, "current": current, "diambil": diambil})
        return hasil
    except mysql.connector.Error as err:
        print(f"Error mengambil misi user: {err}")
        return [{**m, "current": 0, "diambil": False} for m in MISI_DEFINISI]
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

def tambah_progress_misi(user_id, misi_key, jumlah=1):
    """Tambah progress satu misi harian, hanya dipanggil dari mode Time Attack"""
    db = hubungkan_database()
    if db is None:
        return
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute(
            """UPDATE user_misi
               SET current = LEAST(target, current + %s),
                   selesai = IF(LEAST(target, current + %s) >= target, 1, selesai)
               WHERE user_id = %s AND misi_key = %s""",
            (jumlah, jumlah, user_id, misi_key),
        )
        db.commit()
    except mysql.connector.Error as err:
        print(f"Error menambah progress misi: {err}")
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

def klaim_misi(user_id, misi_key, reward):
    """Klaim hadiah satu misi jika sudah selesai dan belum pernah diambil"""
    db = hubungkan_database()
    if db is None:
        return False
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE user_misi SET diambil = 1 WHERE user_id = %s AND misi_key = %s AND selesai = 1 AND diambil = 0",
            (user_id, misi_key),
        )
        db.commit()
        berhasil = cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error klaim misi: {err}")
        berhasil = False
    finally:
        if cursor is not None:
            cursor.close()
        db.close()
    if berhasil:
        tambah_koin_user(user_id, reward)
    return berhasil

def ambil_bonus_misi(user_id):
    """Pastikan baris bonus harian ada lalu kembalikan status diambilnya"""
    db = hubungkan_database()
    if db is None:
        return False
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute(
            "INSERT IGNORE INTO user_misi (user_id, misi_key, current, target, selesai, diambil) VALUES (%s, 'bonus_harian', 0, 1, 0, 0)",
            (user_id,),
        )
        db.commit()
        cursor.execute("SELECT diambil FROM user_misi WHERE user_id = %s AND misi_key = 'bonus_harian'", (user_id,))
        hasil = cursor.fetchone()
        return bool(hasil[0]) if hasil else False
    except mysql.connector.Error as err:
        print(f"Error mengambil status bonus misi: {err}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        db.close()

def klaim_bonus_misi(user_id, reward):
    """Klaim hadiah bonus setelah semua misi harian selesai"""
    db = hubungkan_database()
    if db is None:
        return False
    cursor = None
    try:
        cursor = db.cursor()
        cursor.execute(
            "UPDATE user_misi SET diambil = 1 WHERE user_id = %s AND misi_key = 'bonus_harian' AND diambil = 0",
            (user_id,),
        )
        db.commit()
        berhasil = cursor.rowcount > 0
    except mysql.connector.Error as err:
        print(f"Error klaim bonus misi: {err}")
        berhasil = False
    finally:
        if cursor is not None:
            cursor.close()
        db.close()
    if berhasil:
        tambah_koin_user(user_id, reward)
    return berhasil

def test_items():
    """Fungsi testing untuk cek isi tabel items"""
    db = hubungkan_database()
    if db is not None:
        try:
            cursor = db.cursor()
            cursor.execute("SELECT * FROM items")
            hasil = cursor.fetchall()
            for baris in hasil:
                print(baris)
            print(f"Total item ditemukan: {len(hasil)}")
        except mysql.connector.Error as err:
            print(f"Error mengambil items: {err}")
        finally:
            db.close()


if __name__ == "__main__":
    test_items()