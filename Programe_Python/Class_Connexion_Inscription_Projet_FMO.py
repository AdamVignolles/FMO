#Code by Lenny Cohen ,Project FMO
import Class_interaction_sql_sur_BD_Projet_FMO as inter 
import Fonction_hashage_Projet_FMO as hasch

class Connection_Inscription:
    def __init__(self) -> None:
        self.user = inter.Interaction_sql()

    def inscription(self, pseudo_inscrip : str, pasword : str, nom : str, premon : str):
        """Fonction d'inscription d'un nouveau utilisateur dans la base de donné, renvoi l'id_users si l'inscription ses bien passé"""
        if pseudo_inscrip == self.user.rechercheBD("pseudo", pseudo_inscrip, "users", "pseudo")["pseudo"]:
            return "Pseudo indisponible"
        id_list = self.user.interBD("SELECT id_users FOM users ;")
        id_inscrip = id_list[-1] + 1
        self.user.inssertionBD("users", (id_inscrip, pseudo_inscrip, hasch.hachage_str(pasword+"SELPOIVRE"), "picture", nom, premon))
        return id_inscrip

    def connexion(self, pseudo_conex : str, pasword : str):
        """Fonction de connexion d'un utilisateur verrifie le pseudo et pasword renvoie l'id_users si la connexion est faite"""
        if pseudo_conex != self.user.rechercheBD("pseudo", pseudo_conex, "users", "pseudo")["pseudo"]:
            return "Pseudo incorrecte"
        hashpasword = hasch.hachage_str(pasword+"SELPOIVRE")
        dict_pseudo = self.user.rechercheBD("pseudo", pseudo_conex, "users")
        if hashpasword == dict_pseudo["pasword"]:
            return dict_pseudo["id_users"]
        return "Wrong pasword"
        