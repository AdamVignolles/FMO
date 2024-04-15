from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle

from functools import partial

class Library(Screen):
    def __init__(self, sm, user, music_player, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)

        self.sm = sm
        self.user = user
        self.music_player = music_player
        
        self.playlits()

        self.nav_bar()

        if self.music_player.current_music is not None:
            self.music_bar()

    def playlits(self):

        self.playlists_area = ScrollView(size_hint=(1, None), size=(500, 450), pos_hint={'center_x': 0.65, 'center_y': 0.5})

        self.playlists_grid = GridLayout(cols=2, spacing=20, padding=10, size_hint=(1, None), size=(500, 450))
        self.playlists_grid.bind(minimum_height=self.playlists_grid.setter('height'))

        self.add_widget(Label(text="PLAYLISTS", size_hint=(1, .1), pos_hint={'center_x': 0.2, 'center_y': 0.9}))

        self.playlists_grid.add_widget(Button(text='+', size_hint=(None, None), size=(150, 150), on_press=self.new_playlist))

        for i in  range(len(self.user.playlists)):
            self.playlists_grid.add_widget(Button(text=self.user.playlists[i]["title"], background_normal=self.user.playlists[i]["img"], size_hint=(None, None), size=(150, 150), on_press=partial(self.afficher_playlist, i)))


        self.playlists_area.add_widget(self.playlists_grid)

        self.add_widget(self.playlists_area)

    def new_playlist(self, instance):
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

    def add_playlist(self, title, layout):


        self.user.playlists.append({
            "title": title,
            "img": self.choose_img_path if self.choose_img_path is not None else "img/playlist.png",
            "id": len(self.user.playlists) + 1,
            "musics": []
        })

        self.remove_widget(layout)

        self.playlists_area.remove_widget(self.playlists_grid)

        self.playlits()

    def page_choose_img(self, instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=(500, 600))

        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=layout.size, pos=(layout.x, layout.y + 50))

        layout.add_widget(Label(text='Choose Image', size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))

        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.1}, on_press=self.back))

        file_chooser = FileChooserListView(size_hint=(1, .8), on_submit=self.choose_img, filters=['*.png', '*.jpg'])
        layout.add_widget(file_chooser)

        self.add_widget(layout)

    def choose_img(self, instance, files, *args): 
        self.choose_img_path = files[0]

        self.remove_widget(instance.parent)


    def afficher_playlist(self, i, instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.6}, size=(500, 600))

        playlist = self.user.playlists[i]
        
        with layout.canvas.before:
            Color(0.2, 0.2, 0.2, 1)
            Rectangle(size=layout.size, pos=(layout.x, layout.y + 50))

        layout.add_widget(Label(text=playlist['title'], size_hint=(1, .1), pos_hint={'center_x': 0.5, 'center_y': 0.9}))

        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.1}, on_press=self.back))

        musics_scroll = ScrollView(size_hint=(1, None), size=(500, 350))
        musics_grid = GridLayout(cols=1, spacing=10, padding=10, size_hint=(1, None))
        musics_grid.bind(minimum_height=musics_grid.setter('height'))

        for i in range(len(playlist['musics'])):
            box = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, None), size=(500, 100))
            #img
            box.add_widget(Button(text='', background_normal=playlist['musics'][i]['img'], size_hint=(.2, 1)))
            #title
            box.add_widget(Label(text=playlist['musics'][i]['title'], size_hint=(.6, 1)))
            #play button
            box.add_widget(Button(text='>', size_hint=(.2, 1), on_press=partial(self.music_player.play_playlist, [playlist['musics'], i])))

            musics_grid.add_widget(box)


        musics_scroll.add_widget(musics_grid)
        layout.add_widget(musics_scroll)

        self.add_widget(layout)

    def back(self, instance):
        self.remove_widget(instance.parent)

    def music_bar(self):
        float_layout = FloatLayout(size=(500, 50), pos_hint={'center_x': .5, 'center_y': .1})

        with float_layout.canvas.before:
            Rectangle(source='img/music_bar.png', size=float_layout.size, pos=(float_layout.x, float_layout.y + 50))

        play_button = Button(text='', background_normal="img/play.png", size_hint=(.02, .02), pos_hint={'center_x': .1, 'center_y': .5})
        play_button.bind(on_press=lambda i: self.music_player.pause_resume())

        float_layout.add_widget(Label(text=f'{self.music_player.current_music["title"]} - {self.music_player.current_music["artist"]}', size_hint=(.5, .1), pos_hint={'center_x': .5, 'center_y': .5}))

        next_button = Button(text='', background_normal="img/forward.png", size_hint=(.02, .02), pos_hint={'center_x': .9, 'center_y': .5})
        next_button.bind(on_press=lambda i: self.music_player.next())

        float_layout.add_widget(play_button)
        float_layout.add_widget(next_button)

        self.add_widget(float_layout)


    def nav_bar(self):
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

    def go_home(self, sm): 
        sm.current = 'Home'
        sm.transition.direction = 'right'

    def go_library(self, sm): 
        sm.current = 'Library'
        sm.transition.direction = 'right'

    def go_search(self, sm): 
        sm.current = 'Search'
        sm.transition.direction = 'left'