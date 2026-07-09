<div align="center">

# 🎮 BYTA GAME : WORD GUEST 

### "Satu huruf tepat, musuh sekarat. Satu tebakan melesat, nyawamu tamat!"

![Python](https://img.shields.io/badge/Python-3.14-blue?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-2ea44f?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Development-orange?style=for-the-badge)

</div>

## 🗡️ Tentang Game

Hangman: Word Quest adalah game tebak kata dengan sistem pertarungan. Pemain dan musuh sama-sama punya HP ❤️ (nyawa), dan setiap tebakan huruf akan memengaruhi HP tersebut: tebakan benar mengurangi HP musuh, tebakan salah mengurangi HP pemain. Ada batas waktu ⏳ di setiap pertarungan, jadi selain harus benar menebak kata, pemain juga harus cukup cepat.

## ✨ Fitur Utama

**Sistem Akun** 🔐

Pemain bisa daftar dan login. Progres level, jumlah Gold, dan item yang sudah dibeli tersimpan otomatis sehingga bisa dilanjutkan di sesi berikutnya.

**Pertarungan Berbasis HP** ⚔️

Pemain dan musuh punya bar HP ❤️ masing-masing. Tebakan huruf yang benar membuka huruf pada kata sekaligus mengurangi HP musuh, sedangkan tebakan salah mengurangi HP pemain. Pertarungan berakhir saat salah satu HP habis.

**Timer dan Skor** ⏰

Setiap pertarungan punya batas waktu. Jika waktu habis sebelum kata berhasil ditebak, pemain otomatis kalah. Jika menang, sisa waktu dan sisa HP dihitung menjadi bonus Gold 💰.

**Toko Item** 🛒

Gold 💰 hasil kemenangan bisa dibelanjakan di toko untuk membeli item bantuan seperti petunjuk huruf 💡, tambahan waktu ⏰, atau pemulihan HP ❤️. Item ini berguna terutama di level yang lebih tinggi karena musuh punya HP lebih besar dan timer lebih ketat.

**Multi Level** 🗺️

Semakin tinggi level, musuh yang dihadapi semakin sulit — kata yang digunakan lebih kompleks, HP musuh lebih besar, dan waktu yang diberikan lebih singkat.

**Game Over dan Victory** 💀🏆

Jika HP pemain habis atau waktu habis, akan muncul layar Game Over. Jika berhasil menghabiskan HP musuh, akan muncul layar Victory yang menampilkan rincian Gold yang didapat.

## 🎯 Cara Bermain

1. Login dan pilih level di menu utama
2. Tebak huruf dari kata yang disembunyikan
3. Tebakan benar mengurangi HP musuh, tebakan salah mengurangi HP pemain
4. Gunakan item bantuan saat HP menipis atau waktu hampir habis
5. Habiskan HP musuh sebelum waktu habis untuk mendapatkan Gold
6. Belanjakan Gold di toko sebelum melanjutkan ke level berikutnya

## 🖥️ Alur Layar

Aplikasi ini terdiri dari delapan layar: Splash Screen (pembuka), Login, Menu Utama, Pilih Level, Persiapan (cek item sebelum bertarung), Gameplay (arena tebak kata), Toko, dan Result Screen (Victory atau Game Over).

## 🛠️ Tech Stack

Game ini dibangun menggunakan Python, Tkinter (library GUI bawaan Python) untuk antarmuka, dan MySQL untuk menyimpan data akun beserta progres permainan.

## ⚙️ Instalasi dan Cara Menjalankan

**Persyaratan**

- Python 3.14
- MySQL Server sudah terinstall dan berjalan

**Dependencies (requirements.txt)**

mysql-connector-python==9.7.0
pillow==12.2.0

**Langkah instalasi**

1. Clone repository ini dengan perintah git clone https://github.com/bobbyekaak-beep/HangMan.git lalu masuk ke foldernya dengan cd HangMan
2. Install dependencies yang dibutuhkan dengan perintah pip install -r requirements.txt
3. Import database MySQL menggunakan file db_hangman.sql, lalu sesuaikan konfigurasi koneksi database di database/koneksi.py (host, username, password, nama database) sesuai environment lokal masing-masing
4. Jalankan program dengan perintah python main.py
