-- phpMyAdmin SQL Dump
-- version 5.0.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 14, 2022 at 05:50 AM
-- Server version: 10.4.11-MariaDB
-- PHP Version: 7.4.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `kosnaivebayes`
--

-- --------------------------------------------------------

--
-- Table structure for table `atribut_kos`
--

CREATE TABLE `atribut_kos` (
  `id_atribut` int(11) NOT NULL,
  `atribut` text NOT NULL,
  `kelompok_atribut` int(11) NOT NULL,
  `nilai_atribut` int(11) NOT NULL,
  `min_range` int(11) DEFAULT NULL,
  `max_range` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `atribut_kos`
--

INSERT INTO `atribut_kos` (`id_atribut`, `atribut`, `kelompok_atribut`, `nilai_atribut`, `min_range`, `max_range`) VALUES
(1, 'jarak kurang dari 7 menit (< 7 menit)', 1, 1, 0, 7),
(2, 'jarak lebih dari sama dengan 7 menit (>= 7 menit)', 1, 2, 7, 20),
(3, 'tidak luas', 2, 1, 0, 16),
(4, 'luas', 2, 2, 16, 100),
(5, 'jumlah fasilitas 1', 3, 1, NULL, NULL),
(6, 'jumlah fasilitas 2', 3, 2, NULL, NULL),
(7, 'jumlah fasilitas 3', 3, 3, NULL, NULL),
(8, 'jumlah fasilitas 4', 3, 4, NULL, NULL),
(9, 'jumlah fasilitas 5', 3, 5, NULL, NULL),
(10, 'banyak tempat fasilitas umum kurang dari 4', 4, 1, 1, 4),
(11, 'banyak tempat fasilitas umum lebih dari sama dengan 4', 4, 2, 4, 10),
(12, 'harga kamar kos kurang dari Rp.500.000/bulan', 5, 1, 200000, 500000),
(13, 'harga kamar kos lebih dari sama dengan Rp.500.000/bulan', 5, 2, 500000, 1000000);

-- --------------------------------------------------------

--
-- Table structure for table `data_training`
--

CREATE TABLE `data_training` (
  `id_label` int(11) NOT NULL,
  `id_kos` int(11) NOT NULL,
  `label_jarak` int(11) NOT NULL,
  `label_luas` int(11) NOT NULL,
  `label_fasilitas` int(11) NOT NULL,
  `label_area` int(11) NOT NULL,
  `label_harga` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `data_training`
--

INSERT INTO `data_training` (`id_label`, `id_kos`, `label_jarak`, `label_luas`, `label_fasilitas`, `label_area`, `label_harga`) VALUES
(6, 6, 1, 1, 2, 1, 1),
(7, 7, 1, 2, 2, 2, 2),
(8, 8, 1, 1, 5, 1, 2),
(9, 9, 1, 2, 2, 2, 2),
(10, 10, 1, 1, 1, 1, 1),
(11, 11, 1, 2, 3, 1, 2),
(12, 12, 2, 1, 4, 2, 2),
(13, 13, 2, 1, 4, 2, 2),
(14, 14, 2, 1, 5, 2, 2),
(15, 15, 2, 1, 4, 2, 2),
(16, 16, 1, 1, 4, 2, 2),
(17, 17, 2, 1, 4, 1, 2),
(18, 18, 2, 1, 4, 1, 2),
(19, 19, 2, 2, 4, 1, 2),
(20, 20, 1, 1, 4, 1, 2),
(21, 21, 2, 2, 4, 1, 2),
(22, 22, 1, 1, 2, 1, 1),
(23, 23, 1, 2, 3, 2, 2),
(24, 24, 2, 2, 2, 2, 2),
(25, 25, 2, 1, 3, 1, 1),
(26, 26, 2, 1, 3, 1, 2),
(27, 27, 2, 1, 2, 1, 1),
(28, 28, 2, 1, 2, 1, 1),
(29, 29, 2, 1, 2, 1, 2),
(30, 30, 1, 1, 1, 2, 1),
(31, 31, 1, 2, 5, 1, 2),
(32, 32, 2, 1, 3, 2, 1),
(33, 33, 1, 1, 4, 2, 2),
(34, 34, 2, 2, 3, 1, 2),
(35, 35, 2, 2, 3, 1, 2);

-- --------------------------------------------------------

--
-- Table structure for table `kelompok`
--

CREATE TABLE `kelompok` (
  `kel_atribut` int(11) NOT NULL,
  `nama_kelompok` varchar(256) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `status_interval` enum('ya','tidak') DEFAULT 'tidak'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kelompok`
--

INSERT INTO `kelompok` (`kel_atribut`, `nama_kelompok`, `deskripsi`, `status_interval`) VALUES
(1, 'jarak', 'Jarak perjalanan dari Universitas ke kos dalam satuan menit', 'ya'),
(2, 'ukuran', 'Ukuran kamar kos dalam satuan luas meter persegi', 'ya'),
(3, 'fasilitas', 'Isi fasilitas yang dimiliki oleh kos', 'tidak'),
(4, 'area', 'Area tempat umum di sekitar kos', 'ya'),
(5, 'harga', 'Harga kamar kos perbulan', 'ya');

-- --------------------------------------------------------

--
-- Table structure for table `kos`
--

CREATE TABLE `kos` (
  `id_kos` int(11) NOT NULL,
  `jarak` int(11) NOT NULL,
  `panjang` decimal(3,1) NOT NULL,
  `lebar` decimal(3,1) NOT NULL,
  `fasilitas` text NOT NULL,
  `area` text NOT NULL,
  `harga` int(11) NOT NULL,
  `alamat` text DEFAULT NULL,
  `kontak` varchar(50) DEFAULT NULL,
  `nama` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kos`
--

INSERT INTO `kos` (`id_kos`, `jarak`, `panjang`, `lebar`, `fasilitas`, `area`, `harga`, `alamat`, `kontak`, `nama`) VALUES
(6, 5, '2.5', '2.5', 'Kamar mandi dalam, dapur umum', 'ATM, apotek, warung makan', 450000, 'Jalan Fathur Kost', '8342902435', 'Fathur Kost'),
(7, 5, '4.0', '4.0', 'Kamar mandi dalam, listrik', 'ATM, apotek, warung makan, masjid', 510000, 'Jalan Pondok Satria', '82938274', 'Pondok Satria'),
(8, 2, '4.0', '3.0', 'Kamar mandi dalam, dapur umum, kloset, duduk, kasur, lemari baju', 'puskesmas', 700000, 'Jalan Kosan Kurnia Tipe A', '8350348', 'Kosan Kurnia Tipe A'),
(9, 5, '4.0', '6.0', 'Kamar mandi dalam, wifi', 'Apotek, warung makan, masjid, fotocopy', 600000, 'Jalan Zessica Kost', '93048534', 'Zessica Kost'),
(10, 5, '3.0', '4.0', 'Listrik', 'ATM, apotek, warung makan', 470000, 'Jalan Kosan Bu Leni', '8239247', 'Kosan Bu Leni'),
(11, 5, '4.0', '4.0', 'Kamar mandi dalam, listrik, wifi', 'ATM, warung makan', 650000, 'Jalan Kost Niken', '72375274', 'Kost Niken'),
(12, 7, '3.0', '3.0', 'Kamar mandi dalam, lemari baju, wifi, shower', 'ATM, apotek, warung makan, masjid, minimarket, pusat belanja', 650000, 'Jalan Kost Java Kostmix Tipe B', '2938238', 'Kost Java Kostmix Tipe B'),
(13, 7, '2.5', '3.5', 'Kamar mandi dalam, kasur, lemari baju, wifi', 'ATM, apotek, warung makan, masjid, minimarket, pusat belanja', 600000, 'Jalan Kost Java Kostmix Tipe Standard', '72361989', 'Kost Java Kostmix Tipe Standard'),
(14, 7, '2.5', '6.0', 'Kamar mandi dalam, kasur, lemari baju, wifi, shower', 'ATM, apotek, warung makan, masjid, minimarket, pusat belanja', 750000, 'Jalan Kost Java Kostmix Tipe A', '273288', 'Kost Java Kostmix Tipe A'),
(15, 9, '3.0', '4.0', 'Kamar mandi dalam, wifi, wastafel, balkon', 'ATM, apotek, warung makan, masjid, rumah sakit', 850000, 'Jalan Kost Rentelman I', '72374329', 'Kost Rentelman I'),
(16, 4, '3.0', '3.0', 'Kamar mandi dalam, dapur umum, kasur, lemari baju', 'ATM, apotek, warung makan, pusat belanja', 500000, 'Jalan Kost Pondok Asri', '238237', 'Kost Pondok Asri'),
(17, 12, '3.0', '4.0', 'Kamar mandi dalam, kasur, lemari baju, balkon', 'ATM, warung makan, rumah sakit', 750000, 'Jalan Kost Pondok Aodry Tipe A', '1326742', 'Kost Pondok Aodry Tipe A'),
(18, 12, '3.0', '3.0', 'Kamar mandi dalam, kasur, lemari baju, balkon', 'ATM, warung makan, rumah sakit', 650000, 'Jalan Kost Pondok Aodry Tipe B', '32483748', 'Kost Pondok Aodry Tipe B'),
(19, 10, '5.0', '5.0', 'Kamar mandi dalam, lemari baju, wastafel, balkon', 'ATM, warung makan, masjid', 700000, 'Jalan Kost Kembar', '3248327', 'Kost Kembar'),
(20, 4, '3.0', '4.0', 'Kamar mandi dalam, kasur, lemari baju, balkon', 'Apotek, warung makan, pusat belanja', 600000, 'Jalan Kost Pondok Mutiara', '2328729', 'Kost Pondok Mutiara'),
(21, 10, '9.0', '4.0', 'Kamar mandi dalam, dapur umum, kloset duduk, wastafel', 'Warung makan, masjid, rumah sakit', 500000, 'Jalan Kost KSM Tipe A', '328436438', 'Kost KSM Tipe A'),
(22, 4, '3.0', '4.0', 'Kamar mandi dalam, listrik', 'Apotek, puskesmas, pusat belanja', 410000, 'Jalan Kost Rai Raka', '2382638', 'Kost Rai Raka'),
(23, 5, '5.0', '4.0', 'Kamar mandi dalam, wifi, listrik', 'ATM, apotek, warung makan, masjid, pusat belanja', 500000, 'Jalan Kost Sri', '238236', 'Kost Sri'),
(24, 12, '4.0', '4.0', 'Kamar mandi dalam, wifi', 'ATM, warung makan, pusat belanja, rumah sakit', 600000, 'Jalan Kost Pondok Ilma', '27263726', 'Kost Pondok Ilma'),
(25, 15, '3.0', '4.0', 'Kamar mandi luar, kasur, listrik', 'Apotek, masjid', 350000, 'Jalan Pondok Aswira', '237367', 'Kost Pondok Aswira'),
(26, 15, '3.0', '4.0', 'Kamar mandi dalam, kasur, listrik', 'Apotek, masjid', 500000, 'Jalan Kost Pondok Aswira Tipe A', '237236', 'Kost Pondok Aswira Tipe A'),
(27, 10, '2.5', '3.0', 'Kamar mandi luar, listrik', 'ATM, warung makan, rumah sakit', 350000, 'Jalan Kost WPM Tipe A', '23723', 'Kost WPM Tipe A'),
(28, 10, '2.5', '3.0', 'Kamar mandi dalam, listrik', 'ATM, warung makan, rumah sakit', 400000, 'Jalan Kost WPM Tipe B', '232176', 'Kost WPM Tipe B'),
(29, 10, '2.5', '4.0', 'Kamar mandi dalam, listrik', 'ATM, warung makan, rumah sakit', 500000, 'Jalan Kost WPM Tipe C', '232837', 'Kost WPM Tipe C'),
(30, 5, '3.0', '3.0', 'Kamar mandi dalam', 'ATM, apotek, warung makan, minimarket', 400000, 'Jalan Kost Pondok Qafisha', '2372689', 'Kost Pondok Qafisha'),
(31, 2, '4.0', '5.0', 'Kamar mandi dalam, dapur umum, kloset duduk, kasur, lemari baju', 'Puskesmas', 750000, 'Jalan Kosan Kurnia Tipe B', '2373', 'Kosan Kurnia Tipe B'),
(32, 10, '3.0', '3.0', 'Kamar mandi dalam, kasur, wifi', 'ATM, apotek, warung makan, minimarket', 400000, 'Jalan Kost Fathlani', '237367', 'Kost Fathlani'),
(33, 5, '3.0', '4.0', 'Kamar mandi dalam, listrik, wastafel, balkon', 'ATM, apotek, warung makan, masjid, rumah sakit', 500000, 'Jalan Kost Rentelman II', '237236', 'Kost Rentelman II'),
(34, 10, '10.0', '4.0', 'Kamar mandi dalam, kloset duduk, dapur', 'Warung makan, masjid, minimarket', 600000, 'Jalan Kos KSM Tipe A', '2382372', 'Kost KSM Tipe A'),
(35, 15, '4.0', '4.0', 'Kamar mandi dalam, kasur, wifi', 'Warung makan, masjid', 550000, 'Jalan Kost Dania', '34874837', 'Kost Dania');

-- --------------------------------------------------------

--
-- Table structure for table `pengguna`
--

CREATE TABLE `pengguna` (
  `id_user` int(11) NOT NULL,
  `username` varchar(256) NOT NULL,
  `pass` varchar(256) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pengguna`
--

INSERT INTO `pengguna` (`id_user`, `username`, `pass`) VALUES
(1, 'admin', 'admin'),
(4, 'lorem ipsum', 'lorem');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `atribut_kos`
--
ALTER TABLE `atribut_kos`
  ADD PRIMARY KEY (`id_atribut`),
  ADD KEY `fk_kel_atribut` (`kelompok_atribut`);

--
-- Indexes for table `data_training`
--
ALTER TABLE `data_training`
  ADD PRIMARY KEY (`id_label`),
  ADD KEY `fk_kos` (`id_kos`);

--
-- Indexes for table `kelompok`
--
ALTER TABLE `kelompok`
  ADD PRIMARY KEY (`kel_atribut`);

--
-- Indexes for table `kos`
--
ALTER TABLE `kos`
  ADD PRIMARY KEY (`id_kos`);

--
-- Indexes for table `pengguna`
--
ALTER TABLE `pengguna`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `atribut_kos`
--
ALTER TABLE `atribut_kos`
  MODIFY `id_atribut` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `data_training`
--
ALTER TABLE `data_training`
  MODIFY `id_label` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `kos`
--
ALTER TABLE `kos`
  MODIFY `id_kos` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `pengguna`
--
ALTER TABLE `pengguna`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `atribut_kos`
--
ALTER TABLE `atribut_kos`
  ADD CONSTRAINT `fk_kel_atribut` FOREIGN KEY (`kelompok_atribut`) REFERENCES `kelompok` (`kel_atribut`);

--
-- Constraints for table `data_training`
--
ALTER TABLE `data_training`
  ADD CONSTRAINT `fk_kos` FOREIGN KEY (`id_kos`) REFERENCES `kos` (`id_kos`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
