try :
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, NoTransition
    from kivy.core.window import Window

    from kivy_pages.connection import Connection, Inscription
    from kivy_pages.home import Home
    from kivy_pages.library import Library
    from kivy_pages.search import Search
    from kivy_pages.user import User_Page

    from User import User

    from Music import Music

    import vlc

except Exception as e:
    import utils.setup

title = 'Free Muisc Only'

page_size = (500, 650)
orange = (1, 0.5, 0.3, 1)
grey = (0.2, 0.2, 0.2, 1)

class MainApp(App):

    def build(self):
        self.title = title
        self.icon = 'img/final_logo.png'
        Window.size = page_size
        Window.clearcolor = grey

        music_player = Music()

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


        if user.is_connected:
            sm.current = 'Home'
        else:
            sm.current = 'Connection'

        

        return sm
    
if __name__ == '__main__':
    MainApp().run()