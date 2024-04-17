SET NAMES utf8;
DROP DATABASE IF EXISTS FMO;
CREATE DATABASE FMO CHARACTER SET = utf8 COLLATE = utf8_general_ci;
USE FMO;
CREATE TABLE IF NOT EXISTS users (id_users INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                  pseudo VARCHAR(50),
				                  pasword VARCHAR(50), 
					              picture VARCHAR(150),
					              nom VARCHAR(50),
				                  prenom VARCHAR(50));


CREATE TABLE IF NOT EXISTS music (id_music INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                  title VARCHAR(80),
				                  auteur VARCHAR(50),
					              picture VARCHAR(150),
					              temp INT UNSIGNED ,
				                  played VARCHAR(50));

CREATE TABLE IF NOT EXISTS playlists (id_playlists INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                  title VARCHAR(80),
				                  id_users INT UNSIGNED,
					              picture VARCHAR(150));

CREATE TABLE IF NOT EXISTS playlist (id_playlists INT UNSIGNED,
                                	id_music INT UNSIGNED,
				                  	date_ajout DATE );

CREATE TABLE IF NOT EXISTS genres (id_genre INT UNSIGNED,
                                	id_music INT UNSIGNED);

CREATE TABLE IF NOT EXISTS genre (id_genre INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
                                	nom VARCHAR(50));
