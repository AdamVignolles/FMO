from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.graphics import Rectangle

from functools import partial


class Search(Screen):
    def __init__(self, sm, user, music_player, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)

        self.sm = sm
        self.user = user
        self.music_player = music_player

        self.content_search = []
        
        if self.music_player.current_music is not None:
            self.music_bar()

        self.nav_bar()

        self.search_bar()


    def search_bar(self):
        search_bar = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, .1), pos_hint={'center_x': .5, 'center_y': .9})

        search_input = TextInput(hint_text='Search', multiline=False, size_hint=(.8, 1))
        search_button = Button(text='Search', size_hint=(.2, 1) , on_press=lambda i: self.search(search_input.text))

        search_bar.add_widget(search_input)
        search_bar.add_widget(search_button)

        self.add_widget(search_bar)

    def search(self, search):
        print(search)
        self.content_search.append(self.user.playlists[0]['musics'][0])

        self.display_search()

    def display_search(self):
        self.clear_widgets()

        if self.music_player.current_music is not None:
            self.music_bar()

        self.nav_bar()
        self.search_bar()

        for i in range(len(self.content_search)):
            print(self.content_search)
            box = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(1, .1), pos_hint={'center_x': .5, 'center_y': .8 - i*.1})

            title = Label(text=self.content_search[i]['title'], size_hint=(.7, 1))
            play_button = Button(text='Play', size_hint=(.2, 1), on_press=partial(self.music_player.play_music, self.content_search[i]))
            img = Button(background_normal=self.content_search[i]['img'], size_hint=(.1, 1))

            box.add_widget(img)
            box.add_widget(title)
            box.add_widget(play_button)

            self.add_widget(box)


    def music_bar(self):
        float_layout = FloatLayout(size=(500, 50), pos_hint={'center_x': .5, 'center_y': .1})

        bar_button = Button(text='', background_normal="img/music_bar.png", size_hint=(.98, .08), pos_hint={'center_x': .5, 'center_y': .51})
        
        play_button = Button(text='', background_normal="img/vide_area.png", size_hint=(.05, .05), pos_hint={'center_x': .14, 'center_y': .51})
        play_button.bind(on_press=lambda i: self.music_player.pause_resume())

        float_layout.add_widget(Label(text=f'{self.music_player.current_music["title"]} - {self.music_player.current_music["artist"]}', size_hint=(.5, .1), pos_hint={'center_x': .5, 'center_y': .5}))

        next_button = Button(text='', background_normal="img/vide_area.png", size_hint=(.05, .05), pos_hint={'center_x': .84, 'center_y': .51})
        next_button.bind(on_press=lambda i: self.music_player.next())

        float_layout.add_widget(bar_button)
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