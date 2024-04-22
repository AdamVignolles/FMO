#Code by Lenny Cohen ,Project FMO
import Class_interaction_sql_sur_BD_Projet_FMO as inter

def create_BD():
    """Crée les tables de la Base de donné"""
    interac = inter.Interaction_sql()
    interac.interBD("CREATE TABLE IF NOT EXISTS users (id_users INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,pseudo VARCHAR(50),pasword VARCHAR(50), picture VARCHAR(150),nom VARCHAR(50),prenom VARCHAR(50)); CREATE TABLE IF NOT EXISTS music (id_music INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,title VARCHAR(80),auteur VARCHAR(50),picture VARCHAR(150),temp INT UNSIGNED ,played VARCHAR(50),link VARCHAR(50));CREATE TABLE IF NOT EXISTS playlists (id_playlists INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,title VARCHAR(80),id_users INT UNSIGNED,picture VARCHAR(150));CREATE TABLE IF NOT EXISTS playlist (id_playlists INT UNSIGNED,id_music INT UNSIGNED,date_ajout DATE );CREATE TABLE IF NOT EXISTS genres (id_genre INT UNSIGNED,id_music INT UNSIGNED);CREATE TABLE IF NOT EXISTS genre (id_genre INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,nom VARCHAR(50));")
    