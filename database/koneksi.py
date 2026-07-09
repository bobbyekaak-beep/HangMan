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
        try:
            cursor = db.cursor()
            # Asumsi: nama tabel kamu adalah 'users' dan kolomnya 'koin'
            query = "SELECT koin FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            hasil = cursor.fetchone()
            
            if hasil:
                return hasil[0] # Mengembalikan angka koinnya
        except mysql.connector.Error as err:
            print(f"Error mengambil koin: {err}")
        finally:
            db.close()
    return 0 # Jika gagal atau user tidak ditemukan, koin dianggap 0

def tambah_koin_user(user_id, jumlah_tambahan):
    """Fungsi untuk menambahkan koin pemain saat misi selesai"""
    db = hubungkan_database()
    if db is not None:
        try:
            cursor = db.cursor()
            # Asumsi: nama tabel kamu adalah 'users' dan kolomnya 'koin'
            query = "UPDATE users SET koin = koin + %s WHERE id = %s"
            cursor.execute(query, (jumlah_tambahan, user_id))
            db.commit() # Simpan perubahan ke database
        except mysql.connector.Error as err:
            print(f"Error menambah koin: {err}")
        finally:
            db.close()