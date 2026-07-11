-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 09 Jul 2026 pada 05.43
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 7.4.33
-- CATATAN: Ini adalah versi FINAL v2. Perubahan dari versi sebelumnya:
--   1. Tabel users     -> tambah kolom statistik pemain (total_game, total_win, total_lose, highest_level)
--   2. Tabel save_game -> tambah kolom kategori, huruf_salah, tebakan_benar, tebakan_salah; status disederhanakan jadi PLAYING/PAUSE
--   3. Tabel user_misi -> tambah kolom target dan selesai
--   4. Tabel baru      -> transaksi_koin (riwayat perubahan saldo koin)
--   5. Tabel baru      -> aktivitas_user (log aktivitas untuk kebutuhan debugging)
--   6. Tabel scores    -> tambah index pada level_reached dan tanggal_main untuk leaderboard

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_hangman`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `icon` varchar(10) NOT NULL,
  `color` varchar(20) NOT NULL,
  `harga` int(11) NOT NULL,
  `kategori` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `items`
--

INSERT INTO `items` (`id`, `nama`, `icon`, `color`, `harga`, `kategori`) VALUES
(1, 'PETUNJUK\nHURUF', '💡', '#FFC107', 50, 'BANTUAN'),
(2, 'TAMBAH\nWAKTU', '⏱️', '#2196F3', 70, 'WAKTU'),
(3, 'PULIHKAN\nHP', '♥️', '#F44336', 60, 'HEALING'),
(4, 'HAPUS 3\nHURUF SALAH', '❌', '#757575', 80, 'BANTUAN'),
(5, 'LIHAT\nKATEGORI', '🔎', '#9C27B0', 40, 'BANTUAN'),
(6, 'TEBAK\nKATA', '🎯', '#E91E63', 120, 'BANTUAN');

-- --------------------------------------------------------

--
-- Struktur dari tabel `scores`
--
-- CATATAN: tabel ini adalah RIWAYAT permainan, jadi setiap game selesai
-- harus pakai INSERT baru, jangan pernah di-UPDATE.
--

CREATE TABLE `scores` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `level_reached` int(11) DEFAULT 1,
  `waktu_bermain` int(11) DEFAULT 0,
  `status_game` enum('VICTORY','GAME OVER') NOT NULL,
  `kata_rahasia` varchar(255) NOT NULL,
  `sisa_waktu` int(11) DEFAULT 0,
  `hp_player` int(11) DEFAULT 0,
  `tebakan_benar` int(11) DEFAULT 0,
  `tebakan_salah` int(11) DEFAULT 0,
  `koin_didapat` int(11) DEFAULT 0,
  `tanggal_main` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--
-- CATATAN: kolom coins WAJIB diubah lewat UPDATE setiap ada penambahan/
-- pengurangan koin, jangan hanya diubah di variabel Python.
--
-- TAMBAHAN BARU: kolom total_game, total_win, total_lose, highest_level.
-- Kolom-kolom ini dipakai untuk menampilkan statistik pemain di halaman
-- Profile. Nilainya diupdate setiap kali satu sesi permainan selesai
-- (misalnya bersamaan dengan proses INSERT ke tabel scores).
--
-- PERUBAHAN: default coins diubah dari 0 menjadi 300, sebagai bonus gold
-- untuk setiap akun baru yang mendaftar. Nilai ini hanya berlaku kalau
-- kode Python melakukan INSERT tanpa menyertakan kolom coins secara
-- eksplisit. Untuk lebih aman, sebaiknya kode register tetap mengisi
-- nilai 300 secara langsung di query INSERT-nya.
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `coins` int(11) NOT NULL DEFAULT 300,
  `total_game` int(11) NOT NULL DEFAULT 0,
  `total_win` int(11) NOT NULL DEFAULT 0,
  `total_lose` int(11) NOT NULL DEFAULT 0,
  `highest_level` int(11) NOT NULL DEFAULT 1,
  `tanggal_daftar` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `coins`, `total_game`, `total_win`, `total_lose`, `highest_level`, `tanggal_daftar`) VALUES
(5, 'andre', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 0, 0, 0, 0, 1, '2026-07-08 21:30:50');

-- --------------------------------------------------------

--
-- Struktur dari tabel `user_inventory`
--
-- CATATAN: karena sudah ada UNIQUE(user_id, item_id), pembelian item
-- sebaiknya pakai INSERT ... ON DUPLICATE KEY UPDATE jumlah=jumlah+1,
-- supaya tidak perlu cek manual apakah baris sudah ada atau belum.
--

CREATE TABLE `user_inventory` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `jumlah` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user_misi`
--
-- CATATAN: sudah ada UNIQUE(user_id, misi_key), jadi update progress misi
-- sebaiknya pakai INSERT ... ON DUPLICATE KEY UPDATE current=current+1.
--
-- TAMBAHAN BARU: kolom target dan selesai.
-- target  -> menyimpan target misi (misalnya "menang 5 kali"), jadi kalau
--            target misi berubah di kemudian hari, tinggal update kolom ini
--            tanpa perlu ubah kode program.
-- selesai -> menandai apakah progress current sudah mencapai target,
--            terpisah dari kolom diambil (diambil = hadiah sudah diklaim).
--

CREATE TABLE `user_misi` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `misi_key` varchar(50) NOT NULL,
  `current` int(11) NOT NULL DEFAULT 0,
  `target` int(11) NOT NULL DEFAULT 0,
  `selesai` tinyint(1) NOT NULL DEFAULT 0,
  `diambil` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `save_game`
--
-- Menyimpan progress permainan yang SEDANG berjalan (belum menang/kalah),
-- supaya pemain bisa lanjut dari checkpoint terakhir. user_id dibuat UNIQUE
-- karena satu user hanya boleh punya 1 baris save aktif.
--
-- Alur yang disarankan: begitu pemain MENANG atau KALAH, data di tabel ini
-- dipindahkan ke tabel scores (INSERT), lalu baris di save_game ini DIHAPUS
-- (DELETE), bukan diubah statusnya jadi FINISHED. Jadi status cukup PLAYING
-- (sedang berlangsung) dan PAUSE (ditinggal keluar aplikasi).
--
-- TAMBAHAN BARU: kategori, huruf_salah, tebakan_benar, tebakan_salah.
-- Kolom-kolom ini perlu disimpan juga supaya ketika game dilanjutkan,
-- kondisinya benar-benar identik dengan sebelum ditutup (bukan cuma kata
-- dan huruf yang benar, tapi huruf yang salah tebak dan hitungannya juga
-- harus balik seperti semula).
--
-- PERUBAHAN: kolom coins diganti nama menjadi coins_session, supaya tidak
-- rancu dengan users.coins. users.coins adalah saldo koin PERMANEN milik
-- pemain, sedangkan save_game.coins_session hanya mencatat koin yang
-- didapat SELAMA sesi permainan yang sedang berjalan ini.
--

CREATE TABLE `save_game` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `level` int(11) NOT NULL DEFAULT 1,
  `hp` int(11) NOT NULL DEFAULT 5,
  `waktu` int(11) NOT NULL DEFAULT 60,
  `coins_session` int(11) NOT NULL DEFAULT 0,
  `kategori` varchar(100) DEFAULT NULL,
  `kata` varchar(255) DEFAULT NULL,
  `huruf_ditebak` text DEFAULT NULL,
  `huruf_salah` text DEFAULT NULL,
  `tebakan_benar` int(11) NOT NULL DEFAULT 0,
  `tebakan_salah` int(11) NOT NULL DEFAULT 0,
  `status` enum('PLAYING','PAUSE') NOT NULL DEFAULT 'PLAYING',
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_koin` (TABEL BARU)
--
-- Mencatat setiap perubahan saldo koin (dapat dari menang, dikurangi
-- karena beli item, dari daily reward, dsb). Berguna kalau suatu saat
-- saldo koin pemain terlihat tidak sesuai, tinggal cek tabel ini untuk
-- lacak penyebabnya.
--
-- jumlah -> nilai perubahan, bisa positif (menambah) atau negatif (mengurangi)
-- saldo  -> saldo AKHIR setelah transaksi ini, jadi tidak perlu dihitung ulang
--

CREATE TABLE `transaksi_koin` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `aktivitas` varchar(100) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `saldo` int(11) NOT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `aktivitas_user` (TABEL BARU, opsional)
--
-- Log aktivitas pemain (login, logout, main, menang, kalah, beli item,
-- pakai item). Sifatnya opsional, tapi sangat membantu saat debugging,
-- misalnya untuk melacak urutan kejadian sebelum error terjadi.
--

CREATE TABLE `aktivitas_user` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `aktivitas` varchar(100) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `scores`
--
-- TAMBAHAN BARU: index level_reached dan tanggal_main supaya query
-- leaderboard (ORDER BY level_reached DESC / tanggal_main) lebih cepat
-- saat datanya sudah banyak.
--
ALTER TABLE `scores`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `level_reached` (`level_reached`),
  ADD KEY `tanggal_main` (`tanggal_main`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indeks untuk tabel `user_inventory`
--
ALTER TABLE `user_inventory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`,`item_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indeks untuk tabel `user_misi`
--
ALTER TABLE `user_misi`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_user_misi` (`user_id`,`misi_key`);

--
-- Indeks untuk tabel `save_game`
-- user_id dibuat UNIQUE supaya 1 user cuma punya 1 baris save aktif.
--
ALTER TABLE `save_game`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `transaksi_koin` (BARU)
--
ALTER TABLE `transaksi_koin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `tanggal` (`tanggal`);

--
-- Indeks untuk tabel `aktivitas_user` (BARU)
--
ALTER TABLE `aktivitas_user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `tanggal` (`tanggal`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `scores`
--
ALTER TABLE `scores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT untuk tabel `user_inventory`
--
ALTER TABLE `user_inventory`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `user_misi`
--
ALTER TABLE `user_misi`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `save_game`
--
ALTER TABLE `save_game`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `transaksi_koin` (BARU)
--
ALTER TABLE `transaksi_koin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `aktivitas_user` (BARU)
--
ALTER TABLE `aktivitas_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `scores`
--
ALTER TABLE `scores`
  ADD CONSTRAINT `scores_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `user_inventory`
--
ALTER TABLE `user_inventory`
  ADD CONSTRAINT `user_inventory_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `user_inventory_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `user_misi`
--
ALTER TABLE `user_misi`
  ADD CONSTRAINT `user_misi_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `save_game`
-- ON DELETE CASCADE supaya kalau user dihapus, data save-nya ikut terhapus.
--
ALTER TABLE `save_game`
  ADD CONSTRAINT `save_game_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `transaksi_koin` (BARU)
--
ALTER TABLE `transaksi_koin`
  ADD CONSTRAINT `transaksi_koin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `aktivitas_user` (BARU)
--
ALTER TABLE `aktivitas_user`
  ADD CONSTRAINT `aktivitas_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;