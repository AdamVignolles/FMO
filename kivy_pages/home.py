from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton, ActionGroup, ActionOverflow
from kivy.core.window import Window


class Home(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.color = (1, 0.5, 0.3, 1)
        
        self.page = BoxLayout(orientation='vertical', spacing=10, padding=10, pos_hint={'center_x': 0.5, 'center_y': 0.7})

        self.add_widget(Label(text="Home"))
        '''
        self.action_bar = ActionBar()
        self.action_view = ActionView()
        self.action_group = ActionGroup()
        self.action_group.add_widget(ActionPrevious(title="a"))
        self.action_group.add_widget(ActionButton(text='Home'))
        self.action_group.add_widget(ActionButton(text='About'))
        self.action_group.add_widget(ActionButton(text='Contact'))
        self.action_view.add_widget(self.action_group)
        self.action_bar.add_widget(self.action_view)


        self.add_widget(self.action_bar)
        '''



        self.add_widget(self.page)