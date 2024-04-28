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

from google_drive.Google_drive_api import google_drive_api

from functools import partial

class User_Page(Screen):
    def __init__(self, sm, user, music_player, **kw):
        super().__init__(**kw)
        self.sm = sm
        self.user = user
        self.music_player = music_player

        self.google_api = google_drive_api()

        self.bd = BD()

        self.afficger_user_page()
    

    def afficger_user_page(self):
        """Affiche la page de l'utilisateur"""
        self.clear_widgets()
        self.add_widget(self.user_page())

    def user_page(self):
        """Renvoi la page de l'utilisateur"""
        layout = FloatLayout()
        layout.add_widget(Label(text='User Page', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        layout.add_widget(Button(text='Back', on_press=self.go_home, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.9}))
        img = self.user.data['img'] if 'img' in self.user.data.keys() else 'img/final_logo.png'
        username = self.user.data['pseudo'] if 'pseudo' in self.user.data.keys() else 'Username'
        nom = self.user.data['nom'] if 'nom' in self.user.data.keys() else 'Nom'
        prenom = self.user.data['prenom'] if 'prenom' in self.user.data.keys() else 'Prenom'

        layout.add_widget(Button(text='img', background_normal=img, on_press=self.change_img, size_hint=(0.3, 0.3), pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        layout.add_widget(Label(text=f'Username: {username}', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.5}))
        layout.add_widget(Label(text=f'Nom: {nom}', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.4}))
        layout.add_widget(Label(text=f'Prenom: {prenom}', size_hint=(0.1, 0.1), pos_hint={'center_x': 0.3, 'center_y': 0.3}))

        layout.add_widget(Button(text='my music', on_press=self.my_music, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.7, 'center_y': 0.5}))

        return layout
    
    def change_img(self, *args):
        pass

    def my_music(self, *args):
        self.add_widget(self.my_music_page())

    def my_music_page(self):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=(500, 650), pos=(0, 0))

        layout.add_widget(Label(text='My Music', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        layout.add_widget(Button(text='Back', on_press=self.back, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.9}))
        layout.add_widget(Button(text='Add Music', on_press=self.add_music, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.9, 'center_y': 0.9}))

        music = self.bd.rechercheBD("auteur", self.user.data['pseudo'], "music")
        layout.add_widget(self.music_list(music))

        return layout
    
    def go_back(self, instance):
        self.sm.remove_widget(instance.parent)
    
    def music_list(self, music):
        layout = GridLayout(cols=1, size_hint=(0.9, 0.7), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        for m in music:
            layout.add_widget(self.music_widget(m))
        return layout
    
    def music_widget(self, music):
        box = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        box.add_widget(Label(text=music['picture'], size_hint=(0.1, 1)))
        box.add_widget(Label(text=music['title'], size_hint=(0.5, 1)))
        box.add_widget(Button(text='Delete', on_press=partial(self.delete_music, music), size_hint=(0.5, 1)))

        return box
    
    def delete_music(self, music, *args):
        self.bd.interBD("DELETE FROM music WHERE id_music = %s", [music['id_music']])
        self.afficger_user_page()

    def add_music(self, *args):
        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=(500, 650), pos=(0, 0))

        layout.add_widget(Label(text='Add Music', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        layout.add_widget(Button(text='Back', on_press=self.back, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.9}))
        self.input_title_music = TextInput(hint_text='Title', size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.8})
        layout.add_widget(self.input_title_music)

        layout.add_widget(Button(text='IMG', on_press=self.choose_img, size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.7}))
        layout.add_widget(Button(text='Choose File', on_press=self.choose_file, size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.6}))
        layout.add_widget(Button(text='Add', on_press=self.add, size_hint=(0.5, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.5}))

        self.add_widget(layout)

    def back(self, *args):
        self.remove_widget(args[0].parent)

    def choose_img(self, *args):
        self.chose_music_img = None

        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=(500, 650), pos=(0, 0))

        layout.add_widget(Label(text='Choose Image', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        layout.add_widget(Button(text='Back', on_press=self.add_music, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.9}))
        layout.add_widget(FileChooserListView(size_hint=(0.9, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.4}, filters=['*.png', '*.jpg', '*.jpeg'], on_submit=self.add_img))
        self.clear_widgets()
        self.add_widget(layout)

    def choose_file(self, *args):
        self.chose_music_file = None

        layout = FloatLayout()

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=(500, 650), pos=(0, 0))

        layout.add_widget(Label(text='Choose File', size_hint=(1, 0.1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))
        layout.add_widget(Button(text='Back', on_press=self.add_music, size_hint=(0.1, 0.1), pos_hint={'center_x': 0.1, 'center_y': 0.9}))
        layout.add_widget(FileChooserListView(size_hint=(0.9, 0.8), pos_hint={'center_x': 0.5, 'center_y': 0.4}, filters=['*.mp3'], on_submit=self.add_file))
        self.remove_widget(self.parent)
        self.add_widget(layout)

    def add_img(self, instance, file, *args):
        self.chose_music_img = file[0]
        self.add_music()

    def add_file(self, instance, file, *args):
        self.chose_music_file = file[0]
        self.add_music()

    def add(self, *args):
        if self.chose_music_img is None :
            return
        if self.chose_music_file is None:
            return
        
        file = self.chose_music_file.split('\\')[-1]
        img = self.chose_music_img.split('\\')[-1]

        title = self.input_title_music.text
        autor = self.user.data['pseudo']

        duree = 0
        played = 0

        self.google_api.upload_file(self.chose_music_file)
        self.google_api.upload_file(self.chose_music_img)

        self.bd.interBD("INSERT INTO music (title, auteur, picture, temp, played, link) VALUES (%s, %s, %s, %s, %s, %s)", [title, autor, img, duree, played, file])

        self.afficger_user_page()

        
    def go_home(self, *args):
        self.sm.current = 'Home'


    