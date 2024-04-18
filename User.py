import json

class User:
    def __init__(self, file='user.json', music_player=None):
        self.file = file
        self.data = self.load_json()
        self.is_connected = self.data['is_connected']
        self.playlists = [{
            "title": "Playlist 1",
            "img": "img/playlist.png",
            "id": 1,
            "musics": [
                {
                    "title": "Music 1",
                    "artist": "Artist 1",
                    "img": "img/logo.png",
                    "id": 1,
                    "url": "download_music/music.mp3"
                },
                {
                    "title": "Music 2",
                    "artist": "Artist 2",
                    "img": "img/logo.png",
                    "id": 2,
                    "url": "download_music/music.mp3"
                },
                {
                    "title": "Music 3",

                    "img": "img/logo.png",
                    "id": 3,
                    "url": "download_music/music.mp3"
                }
            ]
        },
        {
            "title": "Playlist 2",
            "img": "img/playlist.png",
            "id": 2,
            "musics": [
                {
                    "title": "Music 4",
                    "artist": "Artist 4",
                    "img": "img/logo.png",
                    "id": 4,
                    "url": "download_music/music.mp3"
                },
                {
                    "title": "Music 5",
                    "artist": "Artist 5",
                    "img": "img/logo.png",
                    "id": 5,
                    "url": "download_music/music.mp3"
                }
            ]
        }
        ]
        self.current_queue = []
        self.music_player = music_player
        

    def load_json(self):
        try :
            with open(self.file, 'r') as f:
                return json.load(f)
        except:
            with open(self.file, 'w') as f:
                json.dump({'is_connected': False}, f)
            return {'is_connected': False}
        
    def save_json(self):
        try:
            with open(self.file, 'w') as f:
                json.dump(self.data, f)
        except:
            print('Error saving data')