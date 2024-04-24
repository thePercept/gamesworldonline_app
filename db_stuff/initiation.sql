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

-- Create the games table
CREATE TABLE IF NOT EXISTS `games` (
    `id` VARCHAR(10) PRIMARY KEY,
    `game_name` VARCHAR(255),
    `year_launched` INT,
    `game_rating` VARCHAR(10),
    `base_price` INT,
    `platform` VARCHAR(50),
    `created_by` VARCHAR(100) DEFAULT 'admin@gamesworldonline.in'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Insert data into the games table
INSERT INTO `games` (`id`, `game_name`, `year_launched`, `game_rating`, `base_price`, `platform`) VALUES
('GWO_2001', 'Prince Of Persia', 2004, '4.5/10', 4200, 'PC'),
('GWO_0032', 'Prince Of Persia', 2004, '4.5/10', 4200, 'PS2'),
('GWO_1001', 'The Legend of Zelda: Breath of the Wild', 2017, '9.7/10', 4999, 'Nintendo Switch'),
('GWO_4050', 'Red Dead Redemption 2', 2018, '9.5/10', 3499, 'PS4'),
('GWO_7890', 'Grand Theft Auto V', 2013, '9.4/10', 1999, 'Xbox One'),
('GWO_2345', 'Super Mario Odyssey', 2017, '9.6/10', 3999, 'Nintendo Switch'),
('GWO_5001', 'The Witcher 3: Wild Hunt', 2015, '9.9/10', 2999, 'PC'),
('GWO_7320', 'God of War', 2018, '9.8/10', 3499, 'PS4'),
('GWO_8623', 'Call of Duty: Modern Warfare', 2019, '8.7/10', 2999, 'Xbox One'),
('GWO_1520', 'Minecraft', 2011, '9.0/10', 1999, 'PS3'),
('GWO_3567', 'FIFA 22', 2021, '8.9/10', 4499, 'PS5'),
('GWO_9381', 'Among Us', 2018, '8.0/10', 299, 'Android'),
('GWO_1123', 'Cyberpunk 2077', 2020, '7.2/10', 2999, 'PC'),
('GWO_2810', 'Assassin\'s Creed Valhalla', 2020, '8.5/10', 3999, 'Xbox Series X'),
('GWO_7777', 'Animal Crossing: New Horizons', 2020, '9.3/10', 4999, 'Nintendo Switch');
