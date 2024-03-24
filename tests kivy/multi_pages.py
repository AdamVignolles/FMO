from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen


class Page1(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Page 1'))
        self.add_widget(Button(text='Go to Page 2', on_press=self.go_to_page2))

    def go_to_page2(self, instance):
        app = App.get_running_app()
        app.root.current = 'page2'
        app.root.transition.direction = 'left'


class Page2(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.add_widget(Label(text='Page 2'))
        self.add_widget(Button(text='Go to Page 1', on_press=self.go_to_page1))

    def go_to_page1(self, instance):
        app = App.get_running_app()
        app.root.current = 'page1'
        app.root.transition.direction = 'right'


class MyApp(App):
    def build(self):
        # Create a screen manager
        sm = ScreenManager()

        # Create the pages
        page1 = Page1(name='page1')
        page2 = Page2(name='page2')


        # Add the pages to the screen manager
        sm.add_widget(page1)
        sm.add_widget(page2)


        return sm


if __name__ == '__main__':
    MyApp().run()