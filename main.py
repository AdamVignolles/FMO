from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from kivy_pages.connection import Connection, Inscription
from kivy_pages.home import Home

title = 'Free Muisc Only'

page_size = (500, 700)
orange = (1, 0.5, 0.3, 1)
grey = (0.2, 0.2, 0.2, 1)

class MainApp(App):

    def build(self):
        self.title = title
        self.icon = 'img/logo_FMO.png'
        Window.size = page_size
        Window.clearcolor = grey

        sm = ScreenManager()

        conn = Connection(name='Connection', sm=sm)
        insc = Inscription(name='Inscription', sm=sm)

        
        sm.add_widget(conn)
        sm.add_widget(insc)

        sm.add_widget(Home(name='Home'))

        return sm
    
if __name__ == '__main__':
    MainApp().run()