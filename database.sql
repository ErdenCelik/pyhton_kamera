-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Anamakine: localhost
-- Üretim Zamanı: 04 Ara 2024, 01:33:09
-- Sunucu sürümü: 8.3.0
-- PHP Sürümü: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `manisa`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `detections`
--

CREATE TABLE `detections` (
  `id` int NOT NULL,
  `uuid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `source` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `source_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `object_count` int NOT NULL,
  `detected_objects` json DEFAULT NULL,
  `is_anomaly` tinyint(1) NOT NULL DEFAULT '0',
  `image_path` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `detection_objects`
--

CREATE TABLE `detection_objects` (
  `id` int NOT NULL,
  `uuid` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `detection_id` int NOT NULL,
  `object_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `confidence` double NOT NULL,
  `image_path` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `permissions`
--

CREATE TABLE `permissions` (
  `id` int NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tablo döküm verisi `permissions`
--

INSERT INTO `permissions` (`id`, `name`, `description`, `created_at`) VALUES
(1, 'user:create:update', 'Permission for user:create:update', '2024-12-04 00:17:22.378'),
(2, 'user:read', 'Permission for user:read', '2024-12-04 00:17:22.381'),
(3, 'user:delete', 'Permission for user:delete', '2024-12-04 00:17:22.383'),
(4, 'history:view', 'Permission for history:view', '2024-12-04 00:17:22.384'),
(5, 'history:delete', 'Permission for history:delete', '2024-12-04 00:17:22.385'),
(6, 'camera:view:live', 'Permission for camera:view:live', '2024-12-04 00:17:22.387'),
(7, 'settings:view', 'Permission for settings:view', '2024-12-04 00:17:22.388'),
(8, 'settings:edit', 'Permission for settings:edit', '2024-12-04 00:17:22.389');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `roles`
--

CREATE TABLE `roles` (
  `id` int NOT NULL,
  `name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tablo döküm verisi `roles`
--

INSERT INTO `roles` (`id`, `name`) VALUES
(1, 'Admin'),
(3, 'Operator'),
(2, 'Supervisor'),
(4, 'Viewer');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `role_permissions`
--

CREATE TABLE `role_permissions` (
  `role_id` int NOT NULL,
  `permission_id` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tablo döküm verisi `role_permissions`
--

INSERT INTO `role_permissions` (`role_id`, `permission_id`) VALUES
(1, 1),
(2, 1),
(1, 2),
(2, 2),
(3, 2),
(1, 3),
(2, 3),
(1, 4),
(2, 4),
(3, 4),
(1, 5),
(2, 5),
(1, 6),
(3, 6),
(4, 6),
(1, 7),
(2, 7),
(1, 8),
(2, 8);

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `system_settings`
--

CREATE TABLE `system_settings` (
  `id` int NOT NULL,
  `setting_key` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_value` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `setting_type` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `setting_description` varchar(191) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tablo döküm verisi `system_settings`
--

INSERT INTO `system_settings` (`id`, `setting_key`, `setting_value`, `setting_type`, `setting_description`) VALUES
(1, 'allowedClasses', NULL, 'json', 'İzin verilen nesne sınıfları'),
(2, 'confidenceThreshold', '0.5', 'float', 'Nesne tespiti için güvenilirlik eşiği'),
(3, 'frameHeight', '480', 'int', 'Kameradan alınacak görüntü yüksekliği'),
(4, 'frameWidth', '640', 'int', 'Kameradan alınacak görüntü genişliği'),
(5, 'fpsLimit', '30', 'int', 'Fps limit'),
(6, 'minAreaDifference', '0.2', 'float', 'Alan farkı eşiği'),
(7, 'densityThreshold', '0.8', 'float', 'Yoğunluk eşiği'),
(8, 'minIou', '0.5', 'float', 'Minimum kesişme eşiği'),
(9, 'minSaveInterval', '2.0', 'float', 'Minimum kaydetme aralığı'),
(10, 'skipFrames', '5', 'int', 'Her kaç karede bir tespit yapılacağı'),
(11, 'pyHost', 'localhost', 'string', 'Python host'),
(12, 'wsPort', '3010', 'int', 'Websocket port'),
(13, 'apiPort', '5000', 'int', 'API port');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `first_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password` varchar(191) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role_id` int NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `last_login` datetime(3) DEFAULT NULL,
  `created_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tablo döküm verisi `users`
--

INSERT INTO `users` (`id`, `first_name`, `last_name`, `email`, `password`, `role_id`, `is_active`, `last_login`, `created_at`) VALUES
(1, 'Erden', 'Çelik', 'erdenclk@gmail.com', '$2b$10$QQZZ7O4N/q86m4SH92nBteVqELDHww3pnV6FtTMipARr1gnaEd6NG', 1, 1, NULL, '2024-12-04 00:17:22.469'),
(2, 'Süpervizör', 'Kullanıcı', 'supervisor@example.com', '$2b$10$UtvxUzJU37t5nAySTwsQF.MpHVZmD7mVggeADiG5c.Il4Wuz5.2k6', 2, 1, NULL, '2024-12-04 00:17:22.521'),
(3, 'Operatör', 'Kullanıcı', 'operator@example.com', '$2b$10$V0hDaSx9S1W.zarUtmEcYeLPRElDMHCsT2gGDJau.1WYuokdDjxre', 3, 1, NULL, '2024-12-04 00:17:22.568'),
(4, 'İzleyici', 'Kullanıcı', 'viewer@example.com', '$2b$10$YI/wQC5wcJ.ixYb2xb88c.BYLfDYJtpHPnWNETgeUFGKlQwoIXXay', 4, 1, NULL, '2024-12-04 00:17:22.615');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `_prisma_migrations`
--

CREATE TABLE `_prisma_migrations` (
  `id` varchar(36) COLLATE utf8mb4_unicode_ci NOT NULL,
  `checksum` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL,
  `finished_at` datetime(3) DEFAULT NULL,
  `migration_name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `logs` text COLLATE utf8mb4_unicode_ci,
  `rolled_back_at` datetime(3) DEFAULT NULL,
  `started_at` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `applied_steps_count` int UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Tablo döküm verisi `_prisma_migrations`
--

INSERT INTO `_prisma_migrations` (`id`, `checksum`, `finished_at`, `migration_name`, `logs`, `rolled_back_at`, `started_at`, `applied_steps_count`) VALUES
('05f742db-1cdd-4004-8dd5-9582690b88c6', 'cab9c16d72336507916814a6d090f15f3153feea1b98ca798db2fda39f78f7dd', '2024-12-04 00:16:22.190', '20241204001102_migration_table', NULL, NULL, '2024-12-04 00:16:22.130', 1);

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `detections`
--
ALTER TABLE `detections`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `detections_uuid_key` (`uuid`),
  ADD KEY `detections_source_idx` (`source`),
  ADD KEY `detections_source_name_idx` (`source_name`),
  ADD KEY `detections_created_at_idx` (`created_at`);

--
-- Tablo için indeksler `detection_objects`
--
ALTER TABLE `detection_objects`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `detection_objects_uuid_key` (`uuid`),
  ADD KEY `detection_objects_created_at_idx` (`created_at`),
  ADD KEY `detection_objects_object_type_idx` (`object_type`),
  ADD KEY `detection_objects_detection_id_fkey` (`detection_id`);

--
-- Tablo için indeksler `permissions`
--
ALTER TABLE `permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `permissions_name_key` (`name`);

--
-- Tablo için indeksler `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roles_name_key` (`name`);

--
-- Tablo için indeksler `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD PRIMARY KEY (`role_id`,`permission_id`),
  ADD KEY `role_permissions_permission_id_fkey` (`permission_id`);

--
-- Tablo için indeksler `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_key` (`email`),
  ADD KEY `users_role_id_fkey` (`role_id`);

--
-- Tablo için indeksler `_prisma_migrations`
--
ALTER TABLE `_prisma_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `detections`
--
ALTER TABLE `detections`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `detection_objects`
--
ALTER TABLE `detection_objects`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Tablo için AUTO_INCREMENT değeri `permissions`
--
ALTER TABLE `permissions`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Tablo için AUTO_INCREMENT değeri `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Tablo için AUTO_INCREMENT değeri `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Tablo için AUTO_INCREMENT değeri `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Dökümü yapılmış tablolar için kısıtlamalar
--

--
-- Tablo kısıtlamaları `detection_objects`
--
ALTER TABLE `detection_objects`
  ADD CONSTRAINT `detection_objects_detection_id_fkey` FOREIGN KEY (`detection_id`) REFERENCES `detections` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `role_permissions`
--
ALTER TABLE `role_permissions`
  ADD CONSTRAINT `role_permissions_permission_id_fkey` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  ADD CONSTRAINT `role_permissions_role_id_fkey` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;

--
-- Tablo kısıtlamaları `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_role_id_fkey` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE RESTRICT ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;