from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.app import runTouchApp

layout = GridLayout(cols=2, spacing=10, size_hint_y=None, size=(50 ,50))
# Make sure the height is such that there is something to scroll.
layout.bind(minimum_height=layout.setter('height'))

for i in range(100):
    btn = Button(text=str(i), size_hint=(None, None), size=(50, 50))
    layout.add_widget(btn)

root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height), pos_hint={'center_x': 0.9, 'center_y': 0.5})
root.add_widget(layout)

runTouchApp(root)