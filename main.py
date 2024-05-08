# Author : Adam Vignolles

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.core.window import Window

from kivy_pages.connection import Connection, Inscription
from kivy_pages.home import Home
from kivy_pages.library import Library
from kivy_pages.search import Search
from kivy_pages.user import User_Page

from User import User

import Music

import vlc



title = 'Free Muisc Only'

page_size = (500, 650)
orange = (1, 0.5, 0.3, 1)
grey = (0.2, 0.2, 0.2, 1)

class MainApp(App):
    '''Classe main de l'application, elle permet de lancer l'application et de gérer les différentes pages de l'application'''

    def build(self) -> ScreenManager:
        '''Fonction permettant de construire l'application'''

        # Configuration de la fenêtre
        self.title = title
        self.icon = 'img/final_logo.png'
        Window.size = page_size
        Window.clearcolor = grey

        # Création des différentes pages
        music_player = Music.Music()

        user = User(music_player=music_player)

        sm = ScreenManager(transition=NoTransition())
        conn = Connection(name='Connection', sm=sm, user=user)
        insc = Inscription(name='Inscription', sm=sm, user=user)

        
        sm.add_widget(conn)
        sm.add_widget(insc)

        sm.add_widget(Home(name='Home', sm=sm, user=user, music_player=music_player))
        sm.add_widget(Library(name='Library', sm=sm, user=user, music_player=music_player))
        sm.add_widget(Search(name='Search', sm=sm, user=user, music_player=music_player))
        sm.add_widget(User_Page(name='User', sm=sm, user=user, music_player=music_player))

        # Affichage de la page de connexion si l'utilisateur n'est pas connecté
        if user.is_connected:
            sm.current = 'Home'
        else:
            sm.current = 'Connection'

        

        return sm
    
if __name__ == '__main__':
    MainApp().run()