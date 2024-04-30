#Code by Lenny Cohen ,Project FMO
try:
    import Class_interaction_sql_sur_BD_Projet_FMO as inter
    import Fonction_hashage_Projet_FMO as hasch 
except:
    import Programe_Python.Class_interaction_sql_sur_BD_Projet_FMO as inter
    import Programe_Python.Fonction_hashage_Projet_FMO as hasch


class Connection_Inscription:
    def __init__(self) -> None:
        self.user = inter.Interaction_sql()

    def inscription(self, pseudo_inscrip : str, pasword : str, nom : str, premon : str):
        """Fonction d'inscription d'un nouveau utilisateur dans la base de donné, renvoi l'id_users si l'inscription ses bien passé"""
        if len(self.user.rechercheBD("pseudo", pseudo_inscrip, "users", "pseudo")) != 0:
            return "Pseudo indisponible"
        id_list = self.user.interBD("SELECT id_users FROM users ;")
        if len(id_list) == 0:
            id_inscrip = 1
        else:
            id_inscrip = len(id_list) + 1
        self.user.inssertionBD("users", (id_inscrip, pseudo_inscrip, hasch.hachage_str(pasword+"SELPOIVRE"), "picture", nom, premon))
        return id_inscrip

    def connexion(self, pseudo_conex : str, pasword : str):
        """Fonction de connexion d'un utilisateur verrifie le pseudo et pasword renvoie l'id_users si la connexion est faite"""
        if len(self.user.rechercheBD("pseudo", pseudo_conex, "users", "pseudo")) == 0:
            return "Pseudo incorrecte"
        hashpasword = hasch.hachage_str(pasword+"SELPOIVRE")
        dict_pseudo = self.user.rechercheBD("pseudo", pseudo_conex, "users")[0]
        if hashpasword == dict_pseudo["pasword"]:
            return dict_pseudo["id_users"]
        return "Wrong pasword"
        