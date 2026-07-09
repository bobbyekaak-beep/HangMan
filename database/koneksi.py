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
            query = "SELECT coins FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            hasil = cursor.fetchone()

            if hasil:
                return hasil[0]
        except mysql.connector.Error as err:
            print(f"Error mengambil koin: {err}")
        finally:
            db.close()
    return 0

def tambah_koin_user(user_id, jumlah_tambahan):
    """Fungsi untuk menambahkan koin pemain saat misi selesai"""
    db = hubungkan_database()
    if db is not None:
        try:
            cursor = db.cursor()
            query = "UPDATE users SET coins = coins + %s WHERE id = %s"
            cursor.execute(query, (jumlah_tambahan, user_id))
            db.commit()
        except mysql.connector.Error as err:
            print(f"Error menambah koin: {err}")
        finally:
            db.close()

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