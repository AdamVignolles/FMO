from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle


class Home(Screen):
    def __init__(self, sm, user, music_player, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)

        self.sm = sm
        self.user = user
        self.music_player = music_player
        
        self.page = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.7})

        self.add_widget(Label(text="Home"))

        self.nav_bar()

        if self.music_player.current_music is not None:
            self.music_bar()

        self.add_widget(self.page)

    def music_bar(self):
        float_layout = FloatLayout(size=(500, 50), pos_hint={'center_x': .5, 'center_y': .1})

        # create a box with a background image under the music bar
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
        sm.transition.direction = 'left'

    def go_search(self, sm):
        sm.current = 'Search'
        sm.transition.direction = 'left'

        