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
    """
    TestApp is a simple Kivy application for demonstration purposes.

    This app showcases the usage of custom fonts in a Kivy Button widget. It inherits
    from the App class, which is the base of creating Kivy applications.

    Methods:
        build(): Builds the application's interface.
    """

    def build(self):
        """
        Builds the application's interface.

        This method is called when the application starts and is responsible for
        initializing and returning the application's root widget.

        Returns:
            Button: A Kivy Button widget with customized text, font, and size.
        """

        return Button(text='Hello, World!', font_name='Antichona', font_size=50)


if __name__ == '__main__':
    TestApp().run()
