-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Waktu pembuatan: 30 Sep 2024 pada 20.22
-- Versi server: 8.0.17
-- Versi PHP: 7.3.29-to-be-removed-in-future-macOS

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `integrasi`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `orders`
--

CREATE TABLE `orders` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `id_log` varchar(255) NOT NULL,
  `kota_asal` varchar(255) NOT NULL,
  `kota_tujuan` varchar(255) NOT NULL,
  `berat` float NOT NULL,
  `harga_pengiriman` float NOT NULL,
  `lama_pengiriman` varchar(255) NOT NULL,
  `no_resi` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `orders`
--

INSERT INTO `orders` (`id`, `id_log`, `kota_asal`, `kota_tujuan`, `berat`, `harga_pengiriman`, `lama_pengiriman`, `no_resi`) VALUES
(1, '615681b2-7f67-11ef-a95b-60f81db0ccc2', 'Semarang', 'ngawi', 2.5, 2000, '2 hari', NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `produk`
--

CREATE TABLE `produk` (
  `idproduk` int(11) NOT NULL,
  `namaproduk` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `kategori` enum('frame','fork','stang') COLLATE utf8mb4_general_ci NOT NULL,
  `linkgambar` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `stok` int(11) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `deskripsi` text COLLATE utf8mb4_general_ci,
  `berat` decimal(5,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `retail`
--

CREATE TABLE `retail` (
  `idretail` int(11) NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `contact` varchar(255) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier`
--

CREATE TABLE `supplier` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `supplier`
--

INSERT INTO `supplier` (`id`, `name`, `location`) VALUES
(1, 'SUP002', 'Jakarta');

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier_rangka_pengirimanbarang`
--

CREATE TABLE `supplier_rangka_pengirimanbarang` (
  `idpengiriman` int(11) NOT NULL,
  `idorder` int(11) DEFAULT NULL,
  `ongkir` decimal(10,2) DEFAULT NULL,
  `resi` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier_rangka_produk`
--

CREATE TABLE `supplier_rangka_produk` (
  `idproduk` varchar(255) NOT NULL,
  `namaproduk` varchar(255) NOT NULL,
  `kategori` enum('frame','fork','stang') NOT NULL,
  `linkgambar` varchar(255) DEFAULT NULL,
  `stok` int(11) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `deskripsi` text,
  `berat` decimal(5,2) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `supplier_rangka_produk`
--

INSERT INTO `supplier_rangka_produk` (`idproduk`, `namaproduk`, `kategori`, `linkgambar`, `stok`, `harga`, `deskripsi`, `berat`, `created_at`, `updated_at`) VALUES
('10-PRO', 'Test Product', 'fork', 'None', 100, '1000000.00', 'Deskripsi produk tes', '2.50', '2024-09-30 18:04:05', '2024-09-30 18:16:14'),
('3-PRO', 'Speed', 'frame', 'https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188', 49, '300000.00', 'n publishing and graphic design, Lorem ipsum is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before the final copy is available', '0.50', '2024-09-29 11:59:01', '2024-09-29 14:07:20'),
('4-PRO', 'polygon', 'frame', 'https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188', 18, '400000.00', 'Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum Lorem Ipsum', '1.00', '2024-09-29 12:00:24', '2024-09-29 14:07:20'),
('5-PRO', 'polygon', 'stang', 'https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188', 39, '4500000.00', 'lorem ipsum dot lorem ipsum', '1.50', '2024-09-29 12:00:56', '2024-09-29 14:07:20'),
('6-PRO', 'opo ae', 'fork', 'https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188', 91, '50000.00', 'jehnwkjdnkweljnrw', '1.00', '2024-09-30 17:26:04', '2024-09-30 17:26:04'),
('7-PRO', 'opo aewk', 'fork', 'https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188', 20, '70000.00', 'ukuku', '2.00', '2024-09-30 17:39:04', '2024-09-30 17:39:04'),
('8-PRO', 'TEST', 'stang', 'https://standert.de/cdn/shop/files/Kreissage-RS-Road-Bike-Frameset-Navy_500x500@2x.webp?v=1697787188', 333, '50000.00', 'Q EDQDEQ', '2.00', '2024-09-30 18:14:30', '2024-09-30 18:14:30');

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier_rangka_retail`
--

CREATE TABLE `supplier_rangka_retail` (
  `idretail` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `supplier_rangka_retail`
--

INSERT INTO `supplier_rangka_retail` (`idretail`, `name`, `contact`, `created_at`, `updated_at`) VALUES
(1, 'okka', '89898989', NULL, NULL);

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier_rangka_transaksi`
--

CREATE TABLE `supplier_rangka_transaksi` (
  `idtransaksi` int(11) NOT NULL,
  `idretail` int(11) DEFAULT NULL,
  `totalharga` decimal(10,2) DEFAULT NULL,
  `totalberat` decimal(5,2) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `resi` varchar(255) DEFAULT NULL,
  `namapembeli` varchar(255) DEFAULT NULL,
  `kota_asal` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `supplier_rangka_transaksi`
--

INSERT INTO `supplier_rangka_transaksi` (`idtransaksi`, `idretail`, `totalharga`, `totalberat`, `created_at`, `updated_at`, `resi`, `namapembeli`, `kota_asal`) VALUES
(2, 1, '0.00', '0.00', '2024-09-29 13:59:32', '2024-09-29 13:59:32', 'PKO-5277', 'John Doe', 'Jakarta'),
(3, 1, '0.00', '0.00', '2024-09-29 14:03:35', '2024-09-29 14:03:35', 'PKO-9742', 'okkaa', 'Jakarta'),
(4, 1, '0.00', '0.00', '2024-09-29 14:03:44', '2024-09-29 14:03:44', 'PKO-5593', 'okkaa', 'Jakarta'),
(5, 1, '0.00', '0.00', '2024-09-29 14:03:53', '2024-09-29 14:03:53', 'PKO-6274', 'okkaa', 'Jakarta'),
(6, 1, '5600000.00', '4.00', '2024-09-29 14:07:20', '2024-09-29 14:07:20', 'PKO-3668', 'verdyan', 'Jakarta');

-- --------------------------------------------------------

--
-- Struktur dari tabel `supplier_rangka_transaksi_barang`
--

CREATE TABLE `supplier_rangka_transaksi_barang` (
  `idtransaksibarang` int(11) NOT NULL,
  `idtransaksi` int(11) DEFAULT NULL,
  `idproduk` varchar(255) DEFAULT NULL,
  `jumlah` int(11) NOT NULL,
  `harga` decimal(10,2) DEFAULT NULL,
  `berat` decimal(5,2) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `supplier_rangka_transaksi_barang`
--

INSERT INTO `supplier_rangka_transaksi_barang` (`idtransaksibarang`, `idtransaksi`, `idproduk`, `jumlah`, `harga`, `berat`, `created_at`, `updated_at`) VALUES
(1, NULL, '4', 2, '800000.00', '2.00', '2024-09-29 14:07:20', '2024-09-29 14:07:20'),
(2, NULL, '5', 1, '4500000.00', '1.50', '2024-09-29 14:07:20', '2024-09-29 14:07:20'),
(3, 6, '3', 1, '300000.00', '0.50', '2024-09-29 14:07:20', '2024-09-29 14:07:20');

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi`
--

CREATE TABLE `transaksi` (
  `idtransaksi` int(11) NOT NULL,
  `idretail` int(11) NOT NULL,
  `totalharga` decimal(10,2) NOT NULL,
  `totalberat` decimal(5,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `transaksi_barang`
--

CREATE TABLE `transaksi_barang` (
  `idtransaksibarang` int(11) NOT NULL,
  `idtransaksi` int(11) NOT NULL,
  `idproduk` int(11) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `harga` decimal(10,2) NOT NULL,
  `berat` decimal(5,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data untuk tabel `user`
--

INSERT INTO `user` (`id`, `username`, `password`) VALUES
(2, 'SUP002', 'scrypt:32768:8:1$zBH6Owwkg6JlOE0z$7eb1097e8abc3f5339db80348a415f19e412d1eef1a382202d91a53b693f857544cb3804cbd8b4009e0b486a5e2b43f94dd15a5552c11e82d58d0feb3f07fb31');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indeks untuk tabel `produk`
--
ALTER TABLE `produk`
  ADD PRIMARY KEY (`idproduk`);

--
-- Indeks untuk tabel `retail`
--
ALTER TABLE `retail`
  ADD PRIMARY KEY (`idretail`);

--
-- Indeks untuk tabel `supplier`
--
ALTER TABLE `supplier`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `supplier_rangka_pengirimanbarang`
--
ALTER TABLE `supplier_rangka_pengirimanbarang`
  ADD PRIMARY KEY (`idpengiriman`);

--
-- Indeks untuk tabel `supplier_rangka_produk`
--
ALTER TABLE `supplier_rangka_produk`
  ADD PRIMARY KEY (`idproduk`);

--
-- Indeks untuk tabel `supplier_rangka_retail`
--
ALTER TABLE `supplier_rangka_retail`
  ADD PRIMARY KEY (`idretail`);

--
-- Indeks untuk tabel `supplier_rangka_transaksi`
--
ALTER TABLE `supplier_rangka_transaksi`
  ADD PRIMARY KEY (`idtransaksi`),
  ADD KEY `idretail` (`idretail`);

--
-- Indeks untuk tabel `supplier_rangka_transaksi_barang`
--
ALTER TABLE `supplier_rangka_transaksi_barang`
  ADD PRIMARY KEY (`idtransaksibarang`),
  ADD KEY `idtransaksi` (`idtransaksi`),
  ADD KEY `supplier_rangka_transaksi_barang_ibfk_2` (`idproduk`);

--
-- Indeks untuk tabel `transaksi`
--
ALTER TABLE `transaksi`
  ADD PRIMARY KEY (`idtransaksi`),
  ADD KEY `idretail` (`idretail`);

--
-- Indeks untuk tabel `transaksi_barang`
--
ALTER TABLE `transaksi_barang`
  ADD PRIMARY KEY (`idtransaksibarang`),
  ADD KEY `idtransaksi` (`idtransaksi`),
  ADD KEY `idproduk` (`idproduk`);

--
-- Indeks untuk tabel `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `orders`
--
ALTER TABLE `orders`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `produk`
--
ALTER TABLE `produk`
  MODIFY `idproduk` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `retail`
--
ALTER TABLE `retail`
  MODIFY `idretail` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `supplier`
--
ALTER TABLE `supplier`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `supplier_rangka_pengirimanbarang`
--
ALTER TABLE `supplier_rangka_pengirimanbarang`
  MODIFY `idpengiriman` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `supplier_rangka_retail`
--
ALTER TABLE `supplier_rangka_retail`
  MODIFY `idretail` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT untuk tabel `supplier_rangka_transaksi`
--
ALTER TABLE `supplier_rangka_transaksi`
  MODIFY `idtransaksi` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT untuk tabel `supplier_rangka_transaksi_barang`
--
ALTER TABLE `supplier_rangka_transaksi_barang`
  MODIFY `idtransaksibarang` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `transaksi`
--
ALTER TABLE `transaksi`
  MODIFY `idtransaksi` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `transaksi_barang`
--
ALTER TABLE `transaksi_barang`
  MODIFY `idtransaksibarang` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `supplier_rangka_transaksi`
--
ALTER TABLE `supplier_rangka_transaksi`
  ADD CONSTRAINT `supplier_rangka_transaksi_ibfk_1` FOREIGN KEY (`idretail`) REFERENCES `supplier_rangka_retail` (`idretail`);

--
-- Ketidakleluasaan untuk tabel `supplier_rangka_transaksi_barang`
--
ALTER TABLE `supplier_rangka_transaksi_barang`
  ADD CONSTRAINT `supplier_rangka_transaksi_barang_ibfk_1` FOREIGN KEY (`idtransaksi`) REFERENCES `supplier_rangka_transaksi` (`idtransaksi`);

--
-- Ketidakleluasaan untuk tabel `transaksi`
--
ALTER TABLE `transaksi`
  ADD CONSTRAINT `transaksi_ibfk_1` FOREIGN KEY (`idretail`) REFERENCES `retail` (`idretail`) ON DELETE CASCADE;

--
-- Ketidakleluasaan untuk tabel `transaksi_barang`
--
ALTER TABLE `transaksi_barang`
  ADD CONSTRAINT `transaksi_barang_ibfk_1` FOREIGN KEY (`idtransaksi`) REFERENCES `transaksi` (`idtransaksi`) ON DELETE CASCADE,
  ADD CONSTRAINT `transaksi_barang_ibfk_2` FOREIGN KEY (`idproduk`) REFERENCES `produk` (`idproduk`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
