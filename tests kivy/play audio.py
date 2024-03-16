import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import vlc

class MusicPlayer(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        
        # Create a label to display the current song
        self.current_song_label = Label(text='No song playing')
        layout.add_widget(self.current_song_label)
        
        # Create buttons for controlling the music
        play_button = Button(text='Play', on_press=self.play_song)
        self.pause_button = Button(text='Pause', on_press=self.pause_song)
        stop_button = Button(text='Stop', on_press=self.stop_song)
        layout.add_widget(play_button)
        layout.add_widget(self.pause_button)
        layout.add_widget(stop_button)
        
        return layout
    
    def play_song(self, instance):
        # Create a new instance of the VLC MediaPlayer
        self.media_player = vlc.MediaPlayer()
        
        # Load the song using the media player
        media = vlc.Media('music.mp3')
        self.media_player.set_media(media)
        
        # Start playing the song
        self.media_player.play()
        self.current_song_label.text = 'Playing: path_to_your_song.mp3'
    
    def pause_song(self, instance):
        if self.media_player:
            # Pause the currently playing song
            self.media_player.pause() # it s a toggle
            self.current_song_label.text = 'Paused: path_to_your_song.mp3'
            if self.pause_button.text == 'Pause':
                self.pause_button.text = 'Resume'
            else:
                self.pause_button.text = 'Pause'
    
    def stop_song(self, instance):
        if self.media_player:
            # Stop the currently playing song
            self.media_player.stop()
            self.current_song_label.text = 'Stopped: path_to_your_song.mp3'

if __name__ == '__main__':
    MusicPlayer().run()