import vlc


class Music:
    def __init__(self):
        self.current_music = None
        self.queue = []
        self.playing = False
        self.paused = False
        self.volume = 1
        self.loop = False
        self.media_player = vlc.MediaPlayer()

    def play(self):
        music = self.queue.pop(0)

        media = vlc.Media(music['url'])
        self.media_player.set_media(media)

        self.media_player.play()
        self.current_music = music
        self.playing = True
        self.paused = False

    def pause(self):
        if ( self.playing or self.current_music is not None ) and not self.paused:
            self.media_player.pause()
            self.playing = False
            self.paused = True


    def resume(self):
        if ( not self.playing or self.current_music is not None ) and self.paused:
            self.media_player.play()
            self.playing = True
            self.paused = False

    def pause_resume(self):
        if self.playing and not self.paused:
            self.pause()
        elif not self.playing and self.paused:
            self.resume()

        elif not self.playing and not self.paused and self.queue:
            self.play()

    def stop(self):
        self.media_player.stop()
        self.playing = False
        self.paused = False
        self.current_music = None

    def next(self):
        if self.queue:
            self.queue.pop(0)
            if self.queue:
                self.play()
        else:
            self.stop()

    def add_to_queue(self, music):
        self.queue.append(music)

    def add_to_queue_and_play(self, music):
        self.add_to_queue(music)
        if not self.playing:
            self.play()

    def play_music(self, music, *args2):
        self.queue = [music]
        self.play()

    def play_playlist(self, args, *args2):
        self.queue = args[0][args[1]:]
        self.play()

    def set_volume(self, volume):
        self.media_player.audio_set_volume(volume)
        self.volume = volume

    def set_loop(self, loop):
        self.media_player.audio_set_loop(loop)
        self.loop = loop

    def get_time(self):
        return self.media_player.get_time()
    
    def get_length(self):
        return self.media_player.get_length()
    
    def is_playing(self):
        return self.playing
    
    def is_paused(self):
        return self.paused
    