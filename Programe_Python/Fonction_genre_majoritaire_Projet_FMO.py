#Code by Lenny Cohen ,Project FMO
import Class_interaction_sql_sur_BD_Projet_FMO as inter

def genre_maj(id_users):
    """Permet de recupéré l'id du genre majoritair de ces musique par l'utilisateur via ces playlistes,
    afin de pouvoir lui proposé des musique du meme genre via l'id_users"""
    interac = inter.Interaction_sql()
    list_id_playlist = interac.rechercheBD("id_users", str(id_users), "playlists", "id_playlists")["id_playlists"]
    list_id_musique = []
    for id_playlist in list_idplaylist:
        list_id_music += interac.rechercheBD("id_playlists", str(id_playlist), "playlist", "id_music")["id_music"]
    dict_genre ={}
    temp_genre = 0
    for id_music in list_id_music:
        temp_genre = interac.rechercheBD("id_music", str(id_music), "genres", "id_genre")["id_genre"]
        if temp_genre not in dict_genre:
            dict_genre[str(temp_genre)] = 1
        else:
            value_temp = dict_genre[str(temp_genre)]
            dict_genre[str(temp_genre)] = vlaue_temp + 1
    value_temp = (0,0)
    for cle in dict_genre.items():
        if value_temp[1] < cle[1] :
            value_temp = cle
    return value_temp[0]