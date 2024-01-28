from kivy.app import App
from kivy.uix.button import Button
from kivy.core.text import LabelBase

from Algorithm.config import abs_path_to_res

# Register the custom font
font_path = abs_path_to_res + 'Antichona-VGlAy.ttf'
LabelBase.register(name='Antichona', fn_regular=font_path)

font_path = abs_path_to_res + 'AristaSans-OV314.ttf'
LabelBase.register(name='AristaSans', fn_regular=font_path)

class TestApp(App):
    def build(self):

        return Button(text='Hello, World!', font_name='Antichona', font_size=50)

if __name__ == '__main__':
    TestApp().run()
