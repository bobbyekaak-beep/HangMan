-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 09 Jul 2026 pada 05.43
-- Versi server: 10.4.27-MariaDB
-- Versi PHP: 7.4.33

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
-- Daftar item yang bisa dibeli pemain di Toko.
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
(3, 'PULIHKAN\nHP', '♥️', '#F44336', 60, 'HEALING');

-- --------------------------------------------------------

--
-- Struktur dari tabel `pertanyaan`
-- Bank soal tebak kata per level (kategori, kata, dan petunjuk).
--

CREATE TABLE `pertanyaan` (
  `id_pertanyaan` int(11) NOT NULL,
  `id_level` int(11) NOT NULL,
  `kategori` varchar(50) NOT NULL,
  `kata` varchar(50) NOT NULL,
  `petunjuk` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `pertanyaan`
--

INSERT INTO `pertanyaan` (`id_pertanyaan`, `id_level`, `kategori`, `kata`, `petunjuk`) VALUES
(1, 1, 'Hewan', 'KUCING', 'Hewan peliharaan yang suka mengeong'),
(2, 1, 'Hewan', 'AYAM', 'Hewan yang berkokok setiap pagi'),
(3, 1, 'Hewan', 'SINGA', 'Dijuluki raja hutan'),
(4, 1, 'Hewan', 'RUSA', 'Memiliki tanduk bercabang'),
(5, 1, 'Hewan', 'GAJAH', 'Mamalia darat terbesar'),
(6, 2, 'Buah', 'APEL', 'Buah berwarna merah'),
(7, 2, 'Buah', 'JERUK', 'Buah yang kaya vitamin C'),
(8, 2, 'Buah', 'MANGGA', 'Buah berwarna hijau saat muda'),
(9, 2, 'Buah', 'NANAS', 'Kulitnya berduri'),
(10, 2, 'Buah', 'SEMANGKA', 'Buah berwarna hijau di luar dan merah di dalam'),
(11, 3, 'Negara', 'INDONESIA', 'Negara kepulauan terbesar di Asia Tenggara'),
(12, 3, 'Negara', 'JEPANG', 'Negeri Sakura'),
(13, 3, 'Negara', 'MALAYSIA', 'Negara tetangga Indonesia'),
(14, 3, 'Negara', 'THAILAND', 'Dijuluki Negeri Gajah Putih'),
(15, 3, 'Negara', 'SINGAPURA', 'Negara kota di Asia Tenggara');

-- --------------------------------------------------------

--
-- Struktur dari tabel `scores`
-- Riwayat permainan yang sudah selesai (menang/kalah), selalu diisi lewat INSERT baru.
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
-- Akun pemain beserta saldo koin dan statistik permainan.
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
-- Item yang sudah dibeli tiap user beserta jumlahnya.
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
-- Progress misi harian tiap user.
--

CREATE TABLE `user_misi` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `misi_key` varchar(50) NOT NULL,
  `current` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `save_game`
-- Progress permainan yang sedang berjalan, supaya bisa dilanjutkan.
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
-- Struktur dari tabel `transaksi_koin`
-- Riwayat setiap perubahan saldo koin pemain.
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
-- Struktur dari tabel `aktivitas_user`
-- Log aktivitas pemain untuk kebutuhan debugging.
--

CREATE TABLE `aktivitas_user` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `aktivitas` varchar(100) NOT NULL,
  `keterangan` varchar(255) DEFAULT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Kolom tambahan untuk mencatat bintang yang diperoleh pemain
--

ALTER TABLE `users`
  ADD COLUMN `total_bintang` int(11) NOT NULL DEFAULT 0;

ALTER TABLE `scores`
  ADD COLUMN `bintang` int(11) NOT NULL DEFAULT 0;

--
-- Kolom tambahan untuk membatasi main mode Time Attack (maks 3 kali per akun)
--

ALTER TABLE `users`
  ADD COLUMN `time_attack_played` int(11) NOT NULL DEFAULT 0;

--
-- Kolom tambahan untuk progress misi harian (target misi, status selesai,
-- dan status sudah/belum diambil hadiahnya)
--

ALTER TABLE `user_misi`
  ADD COLUMN `target` int(11) NOT NULL DEFAULT 0;

ALTER TABLE `user_misi`
  ADD COLUMN `selesai` tinyint(1) NOT NULL DEFAULT 0;

ALTER TABLE `user_misi`
  ADD COLUMN `diambil` tinyint(1) NOT NULL DEFAULT 0;

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `pertanyaan`
--
ALTER TABLE `pertanyaan`
  ADD PRIMARY KEY (`id_pertanyaan`);

--
-- Indeks untuk tabel `scores`
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
--
ALTER TABLE `save_game`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `transaksi_koin`
--
ALTER TABLE `transaksi_koin`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `tanggal` (`tanggal`);

--
-- Indeks untuk tabel `aktivitas_user`
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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `pertanyaan`
--
ALTER TABLE `pertanyaan`
  MODIFY `id_pertanyaan` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

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
-- AUTO_INCREMENT untuk tabel `transaksi_koin`
--
ALTER TABLE `transaksi_koin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `aktivitas_user`
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
--
ALTER TABLE `save_game`
  ADD CONSTRAINT `save_game_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `transaksi_koin`
--
ALTER TABLE `transaksi_koin`
  ADD CONSTRAINT `transaksi_koin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `aktivitas_user`
--
ALTER TABLE `aktivitas_user`
  ADD CONSTRAINT `aktivitas_user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;