from kivy.app import App
from kivy.uix.button import Button
from kivy.core.text import LabelBase

# Register the custom font
font_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/Antichona-VGlAy.ttf'
LabelBase.register(name='Antichona', fn_regular=font_path)

font_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'
LabelBase.register(name='AristaSans', fn_regular=font_path)

class TestApp(App):
    def build(self):

        return Button(text='Hello, World!', font_name='Antichona', font_size=50)

if __name__ == '__main__':
    TestApp().run()
