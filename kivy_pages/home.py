from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock 
from kivy.graphics import Rectangle, Color


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
        self.add_widget(Button(text='User', on_press=self.go_user, size_hint=(.1, .1), pos_hint={'center_x': .9, 'center_y': .9}))
        self.nav_bar()

        self.music_bar()
        self.update_music_bar()

        self.add_widget(self.page)

    def music_bar(self):
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

    def update_music_bar(self):
        Clock.schedule_interval(self.update_music, 1 / 60)

    def update_music(self, dt):
        if self.music_player.is_playing() and self.music_player.current_music is not None :
            self.music_bar_layout.children[3].text = f'{self.music_player.current_music["title"]} - {self.music_player.current_music["artist"]}'
        else:
            if not self.music_player.paused:
                self.music_bar_layout.children[3].text = 'No music playing'


    def show_music(self, instance):
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

        layout.add_widget(Button(text='Back', size_hint=(None, None), size=(50, 50), pos_hint={'center_x': 0.1, 'center_y': 0.9}, on_press=self.back))

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

    def next_music(self, instance):
        self.music_player.next()

        self.clear_widgets()

        self.show_music(instance)

    def show_volume(self, instance):
        self.popup_volume.open()

    def update_progress(self, instance):
        Clock.schedule_interval(self.update_progress_bar, 1 / 60)
        Clock.schedule_interval(self.update_volume, 1 / 60)

    def update_volume(self, dt):
        self.volume.value = self.music_player.volume


    def update_progress_bar(self, dt):
        if self.music_player.is_playing() and self.music_player.current_music is not None:
            if self.music_player.music_length() == 0:
                self.progress.value = 0
            else:
                self.progress.value = self.music_player.music_time() / self.music_player.music_length() * 100

    

    def back(self, instance):
        self.clear_widgets()

        self.nav_bar()

        
        self.music_bar()

        self.add_widget(self.page)
        

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

    def go_user(self, instance):
        self.sm.current = 'User'
        self.sm.transition.direction = 'left'

        