from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window


class Connection(Screen):
    def __init__(self, sm, user, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)
        self.connection_done = False
        self.sm = sm
        self.user = user
        
        self.page = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.7})
        # Labels
        self.page.add_widget(Label(text='Login', color=self.color, size=(500, 100), size_hint=(None, None), halign='center'))
        self.page.add_widget(Label(text='', color=(1, 0, 0, 1), size=(500, 50), size_hint=(None, None), halign='center'))
        # TextInputs
        self.usename = TextInput(multiline=False, hint_text='Username', pos_hint={'center_x': 0.5}, size_hint=(None, None), size=(300, 50))
        self.password = TextInput(password=True, multiline=False, hint_text='Password', pos_hint={'center_x': 0.5}, size_hint=(None, None), size=(300, 50))
        self.page.add_widget(self.usename)
        self.page.add_widget(self.password)
        # Buttons
        self.page.add_widget(Button(text='Login', on_press=self.check_connection, size=(200, 75), size_hint=(None, None), pos_hint={'center_x': 0.5}, color=self.color))
        self.page.add_widget(Button(text='Sign up', on_press=self.go_to_page2, size=(200, 75), size_hint=(None, None), pos_hint={'center_x': 0.5}, color=self.color))
        
        self.add_widget(self.page)

    def check_connection(self, instance):
        print(self.usename.text)
        print(self.password.text)
        self.connection_done = True
        self.sm.current = 'Home'

    def go_to_page2(self, instance):
        app = App.get_running_app()
        app.root.current = 'Inscription'
        app.root.transition.direction = 'left'


class Inscription(Screen):
    def __init__(self, sm, user, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)
        self.connection_done = False
        self.sm = sm
        self.user = user

        self.page = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.6})
        # Labels
        self.page.add_widget(Label(text='Sign up', color=self.color, size=(500, 100), size_hint=(None, None), halign='center'))
        self.page.add_widget(Label(text='', color=(1, 0, 0, 1), size=(500, 50), size_hint=(None, None), halign='center'))
        # TextInputs
        self.usename = TextInput(multiline=False, hint_text='Username', pos_hint={'center_x': 0.5}, size_hint=(None, None), size=(300, 50))
        self.email = TextInput(multiline=False, hint_text='Email', pos_hint={'center_x': 0.5}, size_hint=(None, None), size=(300, 50))
        self.password = TextInput(password=True, multiline=False, hint_text='Password', pos_hint={'center_x': 0.5}, size_hint=(None, None), size=(300, 50))
        self.confirm_password = TextInput(password=True, multiline=False, hint_text='Confirm Password', pos_hint={'center_x': 0.5}, size_hint=(None, None), size=(300, 50))
        self.page.add_widget(self.usename)
        self.page.add_widget(self.email)
        self.page.add_widget(self.password)
        self.page.add_widget(self.confirm_password)
        # Buttons
        self.page.add_widget(Button(text='Create Account', on_press=self.create_account, size=(200, 75), size_hint=(None, None), pos_hint={'center_x': 0.5}, color=self.color))
        self.page.add_widget(Button(text='Login', on_press=self.go_to_page1, size=(200, 75), size_hint=(None, None), pos_hint={'center_x': 0.5}, color=self.color))

        self.add_widget(self.page)

    def create_account(self, instance):
        print(self.usename.text)
        print(self.email.text)
        print(self.password.text)
        print(self.confirm_password.text)
        self.connection_done = True
        self.sm.current = 'Home'

    def go_to_page1(self, instance):
        app = App.get_running_app()
        app.root.current = 'Connection'
        app.root.transition.direction = 'right'



if __name__ == '__main__':

    class MyApp(App):
        def build(self):
            Window.size = (500, 700)
            Window.clearcolor = (0.2, 0.2, 0.2, 1)
            
            # Create a screen manager
            sm = ScreenManager()

            # Create the pages
            page1 = Connection(name='Connection')
            page2 = Inscription(name='Inscription')

            # Add the pages to the screen manager
            sm.add_widget(page1)
            sm.add_widget(page2)

            return sm

    MyApp().run()