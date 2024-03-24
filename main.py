from kivy.app import App
from kivy_pages.connection import Connection, Inscription
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

title = 'Free Muisc Online'

page_size = (500, 700)
orange = (1, 0.5, 0.3, 1)
grey = (0.2, 0.2, 0.2, 1)

class MainApp(App):

    def build(self):
        self.title = title
        self.icon = 'img/logo.png'
        Window.size = page_size
        Window.clearcolor = grey

        sm = ScreenManager()
        sm.add_widget(Connection(name='Connection'))
        sm.add_widget(Inscription(name='Inscription'))
        return sm
    
if __name__ == '__main__':
    MainApp().run()