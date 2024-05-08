# Author : Adam Vignolles
import os

# Add the path of the vlc dlls to the system path
os.environ['PATH'] += os.pathsep + os.getcwd() + "\\vlc"

import vlc

from google_drive.Google_drive_api import google_drive_api

class Music:
    '''Classe permettant de gérer la musique de l'application'''
    def __init__(self):
        self.current_music = None
        self.queue = []
        self.playing = False
        self.paused = False
        self.volume = 50
        self.loop = False
        self.media_player = vlc.MediaPlayer()

        self.google_api = google_drive_api()

    def play(self) -> None:
        '''Fonction permettant de jouer la musique suivante de la queue'''
        # si la queue est vide, on ne fait rien 
        if not self.queue:
            return
        # recupere la musique suivante en queue 
        music = self.queue.pop(0)
       
       # si la musique est deja telecharger dans le dossier download_music on la joue directement
        if music['url'] in os.listdir('download_music'):
            media =  vlc.Media('download_music/' + music['url'])
        else:
        # sinon on la telecharge et on la joue
            id_music_file = self.google_api.search_file_by_name(music['url'])[0]['id']
            self.google_api.download_file(id_music_file, 'download_music/' + music['url'])
            
            media =  vlc.Media('download_music/' + music['url'])

            # telecharge l'image de la musique
            id_img_file = self.google_api.search_file_by_name(music['img'])[0]['id']
            self.google_api.download_file(id_img_file, 'download_img/' + music['img'])
            music['img'] = 'download_img/' + music['img']

        self.media_player.set_media(media)

        # jouer la musique et regler le volume
        self.media_player.play()
        self.media_player.audio_set_volume(self.volume)
        self.current_music = music
        self.playing = True
        self.paused = False

    def pause(self) -> None:
        '''Fonction permettant de mettre en pause la musique'''
        # si la musique est en train de jouer et n'est pas en pause, on la met en pause
        if ( self.playing or self.current_music is not None ) and not self.paused:
            self.media_player.pause()
            self.playing = False
            self.paused = True


    def resume(self) -> None:
        '''Fonction permettant de reprendre la musique en pause'''
        # si la musique est en pause, on la reprend
        if ( not self.playing or self.current_music is not None ) and self.paused:
            self.media_player.play()
            self.playing = True
            self.paused = False

    def pause_resume(self, *args) -> None:
        '''Fonction permettant de mettre en pause ou de reprendre la musique'''
        # si la musique est en train de jouer et n'est pas en pause, on la met en pause
        if self.playing and not self.paused:
            self.pause()
        # si la musique est en pause, on la reprend
        elif not self.playing and self.paused:
            self.resume()
        # si la musique n'est ni en pause ni en train de jouer, on la joue
        elif not self.playing and not self.paused and self.queue:
            self.play()

    def stop(self) -> None:
        '''Fonction permettant d'arrêter la musique'''
        self.media_player.stop()
        self.playing = False
        self.paused = False
        self.current_music = None

    def next(self, *args) -> None:
        '''Fonction permettant de jouer la musique suivante'''
        # si la queue n'est pas vide, on joue la musique suivante
        if self.queue:
            self.stop()
            self.play()

    def add_to_queue(self, music: dict) -> None:
        '''Fonction permettant d'ajouter une musique à la queue'''
        self.queue.append(music)

    def add_to_queue_and_play(self, music: dict) -> None:
        '''Fonction permettant d'ajouter une musique à la queue et de la jouer'''
        self.add_to_queue(music)
        if not self.playing:
            self.play()

    def play_music(self, music: dict, *args) -> None:
        '''Fonction permettant de jouer une musique'''
        self.queue = [music]
        self.play()

    def play_playlist(self, args:tuple, *args2) -> None:
        '''Fonction permettant de jouer une playlist a partir de la musique args[1]'''
        self.queue = args[0][args[1]:]
        self.play()

    def set_volume(self, volume: int) -> None:
        '''Fonction permettant de régler le volume de la musique'''
        self.media_player.audio_set_volume(volume)
        self.volume = volume

    def set_loop(self, loop: bool) -> None:
        '''Fonction permettant de régler la boucle de la musique'''
        self.media_player.audio_set_loop(loop)
        self.loop = loop

    def get_time(self) -> int:
        '''Fonction permettant de récupérer le temps de la musique'''
        return self.media_player.get_time()
    
    def get_length(self) -> int:
        '''Fonction permettant de récupérer la longueur de la musique'''
        return self.media_player.get_length()
    
    def is_playing(self) -> bool:
        '''Fonction permettant de savoir si la musique est en train de jouer'''
        return self.playing
    
    def is_paused(self) -> bool:
        '''Fonction permettant de savoir si la musique est en pause'''
        return self.paused
    
    def music_time(self) -> int:
        '''Fonction permettant de récupérer le temps de la musique en secondes'''
        return self.get_time() / 1000
    
    def music_length(self) -> int:
        '''Fonction permettant de récupérer la longueur de la musique en secondes'''
        return self.get_length() / 1000
    
    def set_time(self, instance, value: int) -> None:
        '''Fonction permettant de régler le temps de la musique'''
        self.media_player.set_time(int(value * self.get_length() / 100))
    
    def set_volume(self, instance, value: int) -> None:
        '''Fonction permettant de régler le volume de la musique'''
        self.media_player.audio_set_volume(int(value))

    def minus_volume(self, instance) -> None:
        '''Fonction permettant de baisser le volume de la musique'''
        self.media_player.audio_set_volume(self.media_player.audio_get_volume() - 10)
        self.volume = self.media_player.audio_get_volume()

    def plus_volume(self, instance) -> None:
        '''Fonction permettant d'augmenter le volume de la musique'''
        self.media_player.audio_set_volume(self.media_player.audio_get_volume() + 10)
        self.volume = self.media_player.audio_get_volume()
    