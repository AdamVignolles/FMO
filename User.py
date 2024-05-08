# Author : Adam Vignolles
import json
from Programe_Python.Class_interaction_sql_sur_BD_Projet_FMO import Interaction_sql

class User:
    '''Classe permettant de gérer les informations de l'utilisateur'''
    def __init__(self, file='user.json', music_player=None) -> None:
        self.file = file
        self.data = self.load_json()
        self.is_connected = self.data['is_connected']
        self.current_queue = []
        self.playlists = []
        self.music_player = music_player
        self.user_sql = Interaction_sql()
        if self.is_connected:
            self.get_info_user(self.data['id'])
            self.current_queue = self.data['curent_queue']
        
    def load_json(self) -> dict:
        '''Fonction permettant de charger les informations de l'utilisateur depuis un fichier json'''
        # on essaye de charger les informations de l'utilisateur depuis le fichier json si il existe sinon on le crée
        try :
            with open(self.file, 'r') as f:
                return json.load(f)
        except:
            with open(self.file, 'w') as f:
                json.dump({'is_connected': False}, f)
            return {'is_connected': False}
        
    def save_json(self) -> None:
        '''Fonction permettant de sauvegarder les informations de l'utilisateur dans un fichier json'''
        try:
            with open(self.file, 'w') as f:
                json.dump(self.data, f)
        except:
            print('Error saving data')

    def get_info_user(self, id_user: int) -> None:
        '''Fonction permettant de récupérer les informations de l'utilisateur depuis la base de données'''

        user = self.user_sql.rechercheBD("id_users", id_user, "users")
        playlists = self.user_sql.rechercheBD("id_users", id_user, "playlists")
        
        for playlist in playlists:
            info_playlist = self.user_sql.rechercheBD("id_playlists", playlist['id_playlists'], "playlist")
            # ajouter une musique
                
            list_music = []
            for music in info_playlist:
                info_music = self.user_sql.rechercheBD("id_music", music['id_music'], "music")
                for m in info_music:
                    list_music.append({
                        "title": m['title'],
                        "artist": m['auteur'],
                        "img": m['picture'],
                        "id": m['id_music'],
                        "date_ajout": music['date_ajout'],
                        #"url": music['url']
                        "url": m['link']
                    })
            self.playlists.append({
                "title": playlist['title'],
                "img": playlist['picture'],
                "id": playlist['id_playlists'],
                "musics": list_music
            })

        # on met à jour les informations de l'utilisateur
        self.data['is_connected'] = True
        self.data['id'] = id_user
        self.data['curent_queue'] = self.music_player.queue
        self.data['pseudo'] = user[0]['pseudo']
        self.data['img'] = user[0]['picture']
        self.data['nom'] = user[0]['nom']
        self.data['prenom'] = user[0]['prenom']
        self.save_json()

        