#Code by Lenny Cohen ,Project FMO
import pymysql as BD

class Interaction_sql():
    def __init__(self):
        self.conex = BD.connect(host='nsijoliotcurie.fr',
                        user='admin_user_FMO',
                        password='Ldjb39&Xn46B',
                        charset='utf8mb4',
                        database="admin_FMO",
                        autocommit=True,
                        port=3306,
                        cursorclass=BD.cursors.DictCursor)
        self.PORT = 3306
    
        
    def closeBD(self) -> None:
        """Ferme la base de donnée ."""
        self.conex.close()
    
    def rechercheBD(self, element_compare : str, caracteristique : str , table : str, element_recherche = "*", comparatif = "="):
        """Effectue une recherche dans la base de donné avec 4 argument str pour les recherche
        "element_compare" est l'element comparé avec WHERE , "carracteristique" la carracteristique recherché
        , "table" est la table de la base de donné et "element_recherche" est l'element de la table que lon veut recupéré vaut * si rien insséré
        "comparatif" est = < > ,etc"""
        
        with self.conex.cursor() as cursor:
            
            request = "SELECT "+element_recherche+" FROM `"+table+"` WHERE `"+element_compare+"`"+comparatif+"%s"
            cursor.execute(request, caracteristique)
            resultats = cursor.fetchall()
            return resultats
        
    def inssertionBD(self, table : str, new_insert : list, column=None):
        """Realise une inssertion dans la table "table" de la BD avec la liste des argument de la nouvelle inssertion dans l'ordre, renvoie rien"""
        with self.conex.cursor() as cursor:
            values = "("
            for i in range(len(new_insert)):
                values += "%s, "
            values = values[:-2] + ")"
            if column == None:
                col= ""
            else:
                col = "("
                for i in range(len(column)):
                    col += f'{column[i]}, '
                col= col[:-2] + ")"
            cursor.execute(str("INSERT INTO `"+table+"` "+str(col)+" VALUES "+values+";"), new_insert)
            
        
    def modifBD(self, table : str, modif_commande : str, element_compare : str, caracteristique : str, comparatif = "="):
        """Permet la modification de la "table" avec la "modif_commande" qui est la modification apporté pour ceux qui
        respecte "element_compare" "comparatif" = "=" "carracteristique" ( Where ), renvoie rien"""
        with self.conex.cursor() as cursor:
            cursor.execute(str("UPDATE "+table+" SET "+modif_commande+" WHERE "+element_compare+" "+comparatif+" "+caracteristique+" ;"))

    def interBD(self, commande : str, param = []):
        """Permet de fair un requète directe via "comande" sur la BD mettre dans commande la requete ex : "SELECT ..... FROM ....."""
        with self.conex.cursor() as cursor:
            if param != []:
                cursor.execute(commande, param)
            else:
                cursor.execute(commande)
            resultats = cursor.fetchall()
            return resultats
    

if __name__ == "__main__":
    sql = Interaction_sql()
    command = [
        "CREATE TABLE IF NOT EXISTS users (id_users INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,pseudo VARCHAR(50),pasword VARCHAR(50), picture VARCHAR(150),nom VARCHAR(50),prenom VARCHAR(50));",
        "CREATE TABLE IF NOT EXISTS music (id_music INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,title VARCHAR(80),auteur VARCHAR(50),picture VARCHAR(150),temp INT UNSIGNED ,played VARCHAR(50),link VARCHAR(50));",
        "CREATE TABLE IF NOT EXISTS playlists (id_playlists INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,title VARCHAR(80),id_users INT UNSIGNED,picture VARCHAR(150));",
        "CREATE TABLE IF NOT EXISTS playlist (id_playlists INT UNSIGNED,id_music INT UNSIGNED,date_ajout DATE );",
        "CREATE TABLE IF NOT EXISTS genres (id_genre INT UNSIGNED,id_music INT UNSIGNED);",
        "CREATE TABLE IF NOT EXISTS genre (id_genre INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,nom VARCHAR(50));"
               ]
    #for i in command:
        #sql.interBD(i)
    
    #add music
    #sql.inssertionBD("music", ["Music 1", "Auteur 1", "img/music.png", 100, "0", "download_music/music.mp3"], ["title", "auteur", "picture", "temp", "played", "link"])
    
    print(sql.interBD("show tables;"))
    print(sql.interBD("SELECT * FROM music;"))
    print(sql.interBD("SELECT * FROM music WHERE title LIKE '%Music%' ;"))
    sql.interBD("DELETE FROM music WHERE title LIKE '%test%' ;")
    sql.closeBD()
        
    