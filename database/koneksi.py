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