CREATE DATABASE IF NOT EXISTS `electri`;
USE `electri`;
DROP TABLE IF EXISTS `car_matches`;
CREATE TABLE `car_matches` (
	`id` INT NOT NULL AUTO_INCREMENT,
	`x_coord` FLOAT NOT NULL,
	`y_coord` FLOAT NOT NULL,
	`image_name` VARCHAR(128) NOT NULL,
	`timestamp` DATETIME DEFAULT CURRENT_TIMESTAMP ,
	PRIMARY KEY (`id`)
);

INSERT INTO car_matches (x_coord,y_coord,image_name) VALUES (38.8988, -77.044,'img1.jpg');
SELECT * FROM car_matches;