-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Waktu pembuatan: 15 Jul 2026 pada 03.21
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `credit_risk_db`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `predictions`
--

CREATE TABLE `predictions` (
  `id_prediction` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `id_card` varchar(20) NOT NULL,
  `work` varchar(50) NOT NULL,
  `revolving_utilization` float DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `delinquency_30_59` int(11) DEFAULT NULL,
  `debt_ratio` float DEFAULT NULL,
  `monthly_income` float DEFAULT NULL,
  `number_credit` int(11) DEFAULT NULL,
  `delinquency_90` int(11) DEFAULT NULL,
  `real_estate_loans` int(11) DEFAULT NULL,
  `delinquency_60_89` int(11) DEFAULT NULL,
  `dependents` int(11) DEFAULT NULL,
  `prediction_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `results`
--

CREATE TABLE `results` (
  `id_result` int(11) NOT NULL,
  `id_prediction` int(11) NOT NULL,
  `logistic_probability` float NOT NULL,
  `credit_eligibility` varchar(20) NOT NULL,
  `risk_probability` float DEFAULT NULL,
  `risk_level` varchar(20) DEFAULT NULL,
  `knn_k_value` int(11) DEFAULT NULL,
  `recommendation` text DEFAULT NULL,
  `recommended_plafond` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `username` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `nomor_telepon` varchar(15) DEFAULT NULL,
  `role` varchar(20) NOT NULL,
  `instansi` varchar(40) DEFAULT NULL,
  `status_aktif` tinyint(1) DEFAULT NULL,
  `terakhir_login` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `reset_code` varchar(6) DEFAULT NULL,
  `reset_code_expired_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id_user`, `username`, `password`, `nama_lengkap`, `email`, `nomor_telepon`, `role`, `instansi`, `status_aktif`, `terakhir_login`, `created_at`, `updated_at`, `reset_code`, `reset_code_expired_at`) VALUES
(1, 'ZahadiRizfy12345!', '$2b$12$JA9ZaHLcYgXTl4O5yKhZlutNiTFtpPaei/JIoeldxFp6ITqYKSAxy', 'Zahadi Rizfy', 'admin@gmail.com', '081275850002', 'super_admin', 'System', 1, '2026-07-15 00:25:46', '2026-07-14 03:09:40', '2026-07-15 00:25:46', NULL, NULL),
(2, 'test', '$2b$12$xdlDRBdNLt6.1vq0hJFNj.0vV4/oofhsfe4H5f1zXOgXiQ6HhUE7a', '3a Zahadi Rizfy', 'wahyuputra23456789@gmail.com', '081412121212', 'nasabah', '', 1, '2026-07-14 08:15:08', '2026-07-14 03:11:21', '2026-07-14 08:15:08', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `predictions`
--
ALTER TABLE `predictions`
  ADD PRIMARY KEY (`id_prediction`),
  ADD KEY `id_user` (`id_user`);

--
-- Indeks untuk tabel `results`
--
ALTER TABLE `results`
  ADD PRIMARY KEY (`id_result`),
  ADD UNIQUE KEY `id_prediction` (`id_prediction`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `nomor_telepon` (`nomor_telepon`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `predictions`
--
ALTER TABLE `predictions`
  MODIFY `id_prediction` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `results`
--
ALTER TABLE `results`
  MODIFY `id_result` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `predictions`
--
ALTER TABLE `predictions`
  ADD CONSTRAINT `predictions_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`);

--
-- Ketidakleluasaan untuk tabel `results`
--
ALTER TABLE `results`
  ADD CONSTRAINT `results_ibfk_1` FOREIGN KEY (`id_prediction`) REFERENCES `predictions` (`id_prediction`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
