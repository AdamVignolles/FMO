# Author : Adam Vignolles
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock 
from kivy.graphics import Color, Rectangle

from Programe_Python.Class_interaction_sql_sur_BD_Projet_FMO import Interaction_sql as BD

from functools import partial

class Library(Screen):
    '''classe permettant de gérer la page de la bibliothèque de l'application'''
    def __init__(self, sm, user, music_player, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)

        self.sm = sm
        self.user = user
        self.music_player = music_player

        self.bd = BD()
        
        # affichage de la page
        self.playlits()
        self.n_playlist_afficher = 0

        self.nav_bar()
        
        self.music_bar()
        self.update_music_bar()
        self.update_playlist()

    def playlits(self) -> None:
        '''Fonction permettant de gérer l'affichage des playlists'''

        self.playlists_area = ScrollView(size_hint=(1, None), size=(500, 450), pos_hint={'center_x': 0.65, 'center_y': 0.5})

        self.playlists_grid = GridLayout(cols=2, spacing=20, padding=10, size_hint=(1, None), size=(500, 450))
        self.playlists_grid.bind(minimum_height=self.playlists_grid.setter('height'))

        self.add_widget(Label(text="PLAYLISTS", size_hint=(1, .1), pos_hint={'center_x': 0.2, 'center_y': 0.9}))

        self.playlists_grid.add_widget(Button(text='+', size_hint=(None, None), size=(150, 150), on_press=self.new_playlist))

        for i in  range(len(self.user.playlists)):
            self.playlists_grid.add_widget(Button(text=self.user.playlists[i]["title"], background_normal=self.user.playlists[i]["img"], size_hint=(None, None), size=(150, 150), on_press=partial(self.afficher_playlist, i)))
        
        self.n_playlist_afficher = len(self.user.playlists)

        self.playlists_area.add_widget(self.playlists_grid)

        self.add_widget(self.playlists_area)

    def update_playlist(self) -> None:
        '''Fonction permettant de mettre à jour la liste des playlists'''
        Clock.schedule_interval(self.update_playlist_area, 1 / 60)

    def update_playlist_area(self, dt) -> None:
        '''Fonction permettant de mettre à jour la liste des playlists'''
        if self.n_playlist_afficher != len(self.user.playlists):
            self.playlists_area.clear_widgets()

            self.playlists_grid = GridLayout(cols=2, spacing=20, padding=10, size_hint=(1, None), size=(500, 450))
            self.playlists_grid.bind(minimum_height=self.playlists_grid.setter('height'))

            self.playlists_grid.add_widget(Button(text='+', size_hint=(None, None), size=(150, 150), on_press=self.new_playlist))

            for i in  range(len(self.user.playlists)):
                self.playlists_grid.add_widget(Button(text=self.user.playlists[i]["title"], background_normal=self.user.playlists[i]["img"], size_hint=(None, None), size=(150, 150), on_press=partial(self.afficher_playlist, i)))
            
            self.n_playlist_afficher = len(self.user.playlists)

            self.playlists_area.add_widget(self.playlists_grid)



    def new_playlist(self, instance) -> None:
        '''Fonction permettant de créer une nouvelle playlist'''
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=(500, 600))

        self.choose_img_path = None

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=layout.size, pos=(layout.x, layout.y + 50))

        layout.add_widget(Label(text='New Playlist', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))

        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.1}, on_press=self.back))

        layout.add_widget(Button(text='Choose Image', size_hint=(1, .1), on_press=self.page_choose_img))


        title_input = TextInput(hint_text='Title', size_hint=(1, .1))
        layout.add_widget(title_input)

        add_button = Button(text='create', size_hint=(1, .1), on_press=lambda i: self.add_playlist(title_input.text, layout))
        layout.add_widget(add_button)

        self.add_widget(layout)

    def add_playlist(self, title:str, layout) -> None:
        '''Fonction permettant d'ajouter une playlist'''


        self.user.playlists.append({
            "title": title,
            "img": self.choose_img_path if self.choose_img_path is not None else "img/playlist.png",
            "id": len(self.user.playlists) + 1,
            "musics": []
        })

        # update data base
        command = "INSERT INTO playlists (title, id_users, picture) VALUES (%s, %s, %s)"
        value = [title, self.user.data["id"], self.choose_img_path if self.choose_img_path is not None else "img/playlist.png"]
        self.bd.inssertionBD("playlists", value, column=["title", "id_users", "picture"])

        self.remove_widget(layout)

        self.playlists_area.remove_widget(self.playlists_grid)

        self.playlits()

    def page_choose_img(self, instance) -> None:
        '''Fonction permettant de choisir une image pour la playlist'''
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=(500, 600))

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=layout.size, pos=(layout.x, layout.y + 50))

        layout.add_widget(Label(text='Choose Image', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))

        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.1}, on_press=self.back))

        file_chooser = FileChooserListView(size_hint=(1, .8), on_submit=self.choose_img, filters=['*.png', '*.jpg'])
        layout.add_widget(file_chooser)

        self.add_widget(layout)

    def choose_img(self, instance, files, *args) -> None:
        '''Fonction permettant de choisir une image pour la playlist''' 
        self.choose_img_path = files[0]

        self.remove_widget(instance.parent)


    def afficher_playlist(self, i:int, instance) -> None:
        '''Fonction permettant d'afficher une playlist'''
        self.playlist_layout = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=(500, 600))

        playlist = self.user.playlists[i]
        
        with self.playlist_layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=self.playlist_layout.size, pos=(self.playlist_layout.x, self.playlist_layout.y + 50))

        self.playlist_layout.add_widget(Label(text=playlist['title'], size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))

        self.playlist_layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.1}, on_press=self.back))
        self.playlist_layout.add_widget(Button(text='SUPRIMER', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.9, 'center_y': 0.05}, on_press=partial(self.remove_playlist, i)))

        musics_scroll = ScrollView(size_hint=(1, None), size=(500, 350))
        musics_grid = GridLayout(cols=1, spacing=10, padding=10, size_hint=(1, None))
        musics_grid.bind(minimum_height=musics_grid.setter('height'))

        for i in range(len(playlist['musics'])):
            box = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, None), size=(500, 100))
            #img
            box.add_widget(Button(text='', background_normal=playlist['musics'][i]['img'], size_hint=(.2, 1)))
            # suprimer playlist
            box.add_widget(Button(text='-', size_hint=(.1, 1), on_press=partial(self.remove_music, i, playlist)))
            #title
            box.add_widget(Label(text=playlist['musics'][i]['title'], size_hint=(.6, 1)))
            #play button
            box.add_widget(Button(text='>', size_hint=(.2, 1), on_press=partial(self.music_player.play_playlist, [playlist['musics'], i])))

            musics_grid.add_widget(box)


        musics_scroll.add_widget(musics_grid)
        self.playlist_layout.add_widget(musics_scroll)

        self.add_widget(self.playlist_layout)
    
    def remove_playlist(self, i:int, instance) -> None:
        '''Fonction permettant de supprimer une playlist'''
        # update data base
        command = "DELETE FROM playlists WHERE id_playlists = %s"
        self.bd.interBD(command, (self.user.playlists[i]['id']))

        self.user.playlists.pop(i)
        self.remove_widget(instance.parent)

    def remove_music(self, i:int, playlist:dict, instance) -> None:
        '''Fonction permettant de supprimer une musique d'une playlist'''

        # update data base
        command = "DELETE FROM playlist WHERE id_playlists = %s AND id_music = %s"
        self.bd.interBD(command, (playlist['id'], playlist['musics'][i]['id']))

        playlist['musics'].pop(i)
        self.remove_widget(self.playlist_layout)

    def back(self, instance) -> None:
        '''Fonction permettant de revenir en arrière'''
        self.remove_widget(instance.parent)

    def music_bar(self) -> None:
        '''Fonction permettant de gérer la barre de musique'''
        self.music_bar_layout = FloatLayout(size=(500, 50), pos_hint={'center_x': .5, 'center_y': .1})

        # create a button with the bar image
        bar_button = Button(text='', background_normal="img/music_bar.png", size_hint=(.98, .08), pos_hint={'center_x': .5, 'center_y': .51}, on_press=self.show_music)
        
        if self.music_player.current_music is not None:
            title = self.music_player.current_music['title']
            artist = self.music_player.current_music['artist']
        else:
            title = 'No music playing'
            artist = ''

        play_button = Button(text='', background_normal="img/vide_area.png", size_hint=(.05, .05), pos_hint={'center_x': .14, 'center_y': .51})
        play_button.bind(on_press=lambda i: self.music_player.pause_resume())

        self.music_bar_layout.add_widget(Label(text=f'{title} - {artist}', size_hint=(.5, .1), pos_hint={'center_x': .5, 'center_y': .5}))

        next_button = Button(text='', background_normal="img/vide_area.png", size_hint=(.05, .05), pos_hint={'center_x': .84, 'center_y': .51})
        next_button.bind(on_press=lambda i: self.music_player.next())

        self.music_bar_layout.add_widget(bar_button)
        self.music_bar_layout.add_widget(play_button)
        self.music_bar_layout.add_widget(next_button)

        self.add_widget(self.music_bar_layout)

    def update_music_bar(self) -> None:
        '''Fonction permettant de mettre à jour la barre de musique'''
        Clock.schedule_interval(self.update_music, 1 / 60)

    def update_music(self, dt) -> None:
        '''Fonction permettant de mettre à jour la barre de musique'''
        if self.music_player.is_playing() and self.music_player.current_music is not None :
            self.music_bar_layout.children[3].text = f'{self.music_player.current_music["title"]} - {self.music_player.current_music["artist"]}'
        else:
            if not self.music_player.paused:
                self.music_bar_layout.children[3].text = 'No music playing'

    def show_music(self, instance) -> None:
        '''Fonction permettant d'afficher les informations de la musique en cours de lecture'''
        layout = FloatLayout(size=(500, 650), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        # remove all widget from the screen
        self.clear_widgets()

        if self.music_player.current_music is not None:
            title = self.music_player.current_music['title']
            artist = self.music_player.current_music['artist']
            img= self.music_player.current_music['img']
        else:
            title = 'No music playing'
            artist = ''
            img = 'img/final_logo.png'

    
        layout.add_widget(Button(background_normal=img, size=(350, 350), size_hint=(None, None), pos_hint={'center_x': 0.5, 'center_y': 0.7}))

        layout.add_widget(Label(text=title, size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.35}))
        layout.add_widget(Label(text=artist, size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.3}))

        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.9}, on_press=self.back_playlist))

        # avancement bar
        self.progress = ProgressBar(max=100, value=0, size_hint=(.9, .1), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        self.progress.bind(on_press=self.music_player.set_time)
        self.update_progress(self.progress)

        # volume bar
        self.volume = ProgressBar(max=100, value=self.music_player.volume, size_hint=(.6, .1), pos_hint={'center_x': 0.4, 'center_y': 0.1})
        self.volume.bind(on_press=self.music_player.set_volume)
        layout.add_widget(Button(text='+', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.8, 'center_y': 0.1}, on_press=self.music_player.plus_volume))
        layout.add_widget(Button(text='- ', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.9, 'center_y': 0.1}, on_press=self.music_player.minus_volume))

        layout.add_widget(Button(text='Play', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.3}, on_press=self.music_player.pause_resume))
        layout.add_widget(Button(text='Next', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.2, 'center_y': 0.3}, on_press=self.next_music))

        layout.add_widget(self.progress)
        layout.add_widget(self.volume)
        self.add_widget(layout)
    
    def next_music(self, instance) -> None:
        '''Fonction permettant de passer à la musique suivante'''
        self.music_player.next()

        self.clear_widgets()

        self.show_music(instance)


    def back_playlist(self, instance) -> None:
        '''Fonction permettant de revenir à la page de la playlist'''
        self.clear_widgets()
        self.playlits()

        self.music_bar()
        self.nav_bar()


    def show_volume(self, instance) -> None:
        '''Fonction permettant d'afficher le volume'''
        self.popup_volume.open()

    def update_progress(self, instance) -> None:
        '''Fonction permettant de mettre à jour la barre de progression de la musique'''
        Clock.schedule_interval(self.update_progress_bar, 1 / 60)
        Clock.schedule_interval(self.update_volume, 1 / 60)

    def update_volume(self, dt) -> None:
        '''Fonction permettant de mettre à jour la barre de volume'''
        self.volume.value = self.music_player.volume

    def update_progress_bar(self, dt) -> None:
        '''Fonction permettant de mettre à jour la barre de progression de la musique'''
        if self.music_player.is_playing() and self.music_player.current_music is not None:
            if self.music_player.music_length() == 0:
                self.progress.value = 0
            else:
                self.progress.value = self.music_player.music_time() / self.music_player.music_length() * 100


    def nav_bar(self) -> None:
        '''Fonction permettant de gérer la barre de navigation'''
        float_layout = FloatLayout(size=(300, 300), pos_hint={'center_x': .5, 'center_y': .03})

        home_button = Button(text='', background_normal="img/home_nav.png", size_hint=(.3, .07), pos_hint={'center_x': .2, 'center_y': .5})
        home_button.bind(on_press=lambda i: self.go_home(self.sm))

        library_button = Button(text='', background_normal="img/playlist_nav.png", size_hint=(.3, .07), pos_hint={'center_x': .5, 'center_y': .5})
        library_button.bind(on_press=lambda i: self.go_library(self.sm))

        search_button = Button(text='', background_normal="img/search_nav.png", size_hint=(.3, .07), pos_hint={'center_x': .8, 'center_y': .5})
        search_button.bind(on_press=lambda i: self.go_search(self.sm))


        float_layout.add_widget(home_button)
        float_layout.add_widget(library_button)
        float_layout.add_widget(search_button)

        self.add_widget(float_layout)

    def go_home(self, sm) -> None:
        '''Fonction permettant de revenir à la page d'accueil'''
        sm.current = 'Home'
        sm.transition.direction = 'right'

    def go_library(self, sm) -> None:
        '''Fonction permettant de changer de page vers la page de la bibliothèque'''
        sm.current = 'Library'
        sm.transition.direction = 'right'

    def go_search(self, sm) -> None:
        '''Fonction permettant de changer de page vers la page de recherche'''
        sm.current = 'Search'
        sm.transition.direction = 'left'