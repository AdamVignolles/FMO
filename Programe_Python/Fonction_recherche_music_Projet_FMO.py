#Code by Lenny Cohen ,Project FMO
try:
    import Class_interaction_sql_sur_BD_Projet_FMO as inter
except:
    import Programe_Python.Class_interaction_sql_sur_BD_Projet_FMO as inter
"""Fonction de recherche de music"""

def recherche_music_genre(id_genre) -> list:
    """Fonction qui renvoi toutes les musics avec l'id_genre correspondant"""
    interac = inter.Interaction_sql()
    list_id_music = interac.rechercheBD("id_genre", str(id_genre), "genres", "id_music")["id_music"]
    list_music = []
    for id_music in list_id_music :
        list_music.append(interac.rechercheBD("id_music", str(id_music), "music"))
    return list_music

def recherche_music_titre(title:str) -> list:
    """Fonction qui renvoi les musics avec un titre qui a comme charactere title et avant et aprés tous se qu'il veut via %"""
    interac = inter.Interaction_sql()
    return interac.rechercheBD("title", str("%"+title+"%"), "music")