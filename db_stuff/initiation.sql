CREATE DATABASE IF NOT EXISTS `gameworlds_db` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `gameworlds_db`;

CREATE TABLE IF NOT EXISTS `accounts` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(50) NOT NULL,
    `password` varchar(255) NOT NULL,
    `email` varchar(100) NOT NULL,
    `usercategory` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


