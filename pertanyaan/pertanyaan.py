from database.koneksi import hubungkan_database

def ambil_pertanyaan(level):

    conn = hubungkan_database()
    if conn is None:
        print("[DATABASE] Gagal terhubung ke database, soal tidak dapat dimuat.")
        return []

    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT kategori, kata, petunjuk
            FROM pertanyaan
            WHERE id_level = %s
        """, (level,))

        return cursor.fetchall()
    except Exception as e:
        print(f"[DATABASE] Error mengambil pertanyaan: {e}")
        return []
    finally:
        conn.close()