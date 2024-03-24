from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

class HomePage(Screen):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.add_widget(Label(text='Home Page'))

class AboutPage(Screen):
    def __init__(self, **kwargs):
        super(AboutPage, self).__init__(**kwargs)
        self.add_widget(Label(text='About Page'))

class ContactPage(Screen):
    def __init__(self, **kwargs):
        super(ContactPage, self).__init__(**kwargs)
        self.add_widget(Label(text='Contact Page'))

class MainApp(App):
    def build(self):
        # Create a screen manager
        sm = ScreenManager()

        # Create the screens
        home_screen = HomePage(name='home')
        about_screen = AboutPage(name='about')
        contact_screen = ContactPage(name='contact')

        # Add the screens to the screen manager
        sm.add_widget(home_screen)
        sm.add_widget(about_screen)
        sm.add_widget(contact_screen)

        # Create the bottom navigation bar
        nav_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.15))
        home_button = Button(text='Home', on_release=lambda x: sm.switch_to(home_screen), background_color=(0.5, 0.5, 0.5, 1), border=(16, 16, 16, 16), background_down='')
        about_button = Button(text='About', on_release=lambda x: sm.switch_to(about_screen))
        contact_button = Button(text='Contact', on_release=lambda x: sm.switch_to(contact_screen))

        # Add the buttons to the navigation bar
        nav_bar.add_widget(home_button)
        nav_bar.add_widget(about_button)
        nav_bar.add_widget(contact_button)

        # Create the main layout
        main_layout = BoxLayout(orientation='vertical')
        main_layout.add_widget(sm)
        main_layout.add_widget(nav_bar)

        return main_layout

if __name__ == '__main__':
    MainApp().run()