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

    def interBD(self, commande : str):
        """Permet de fair un requète directe via "comande" sur la BD mettre dans commande la requete ex : "SELECT ..... FROM ....."""
        with self.conex.cursor() as cursor:
            cursor.execute(commande)
            resultats = cursor.fetchall()
            return resultats
            
        
    