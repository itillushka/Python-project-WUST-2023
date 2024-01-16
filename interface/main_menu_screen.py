from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.behaviors import ButtonBehavior

# Custom fonts
font_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'
LabelBase.register(name='AristaSans', fn_regular=font_path)
font_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/Antichona-VGlAy.ttf'
LabelBase.register(name='Antichona', fn_regular=font_path)


class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)

        # Bind to mouse position changes
        Window.bind(mouse_pos=self.on_mouse_pos)

        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)

        # Load the background image
        bg_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_background_main.png'
        self.bg_texture = Image(source=bg_path).texture

        # Draw the background
        with Window.canvas.before:
            Rectangle(texture=self.bg_texture, size=Window.size, pos=(0, 0))

        # Load the logo and set its size
        logo_path = (
            'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/logo_spotamix.png')
        self.logo = Image(source=logo_path, allow_stretch=True)
        self.logo.size_hint = None, None
        self.logo.size = dp(500), dp(500)
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.75}
        self.layout.add_widget(self.logo)

        # Add the "Spotamix" image below the logo
        self.spotamix_label = Image(source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_name.png', allow_stretch=True)
        self.spotamix_label.size_hint = None, None
        self.spotamix_label.width = self.logo.width
        self.spotamix_label.height = self.logo.height
        self.spotamix_label.pos_hint = {'center_x': 0.5, 'y': 0.3}
        self.layout.add_widget(self.spotamix_label)

        # Define paths for normal and hover background images
        self.normal_bg = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background.png'
        self.hover_bg = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background_highlighted.png'

        # Create buttons with their styles
        self.continue_button = self.create_styled_button("Continue without login")
        self.login_button = self.create_styled_button("Login")

        # Adjust buttons width and height
        button_width = Window.width * 0.4  # Adjust the width as needed
        button_height = dp(110)
        self.continue_button.size = (button_width, button_height)
        self.login_button.size = (button_width, button_height)

        # Position buttons
        self.continue_button.pos_hint = {'center_x': 0.5, 'y': 0.30}
        self.login_button.pos_hint = {'center_x': 0.5, 'y': 0.15}

        # Add buttons to the layout
        self.layout.add_widget(self.continue_button)
        self.layout.add_widget(self.login_button)

    def create_styled_button(self, text):
        button = Button(text=text, font_name='AristaSans', font_size='25sp', size_hint=(None, None), height=dp(110))
        button.background_normal = self.normal_bg
        button.background_down = self.normal_bg  # or use a different image for the pressed state
        button.border = (0, 0, 0, 0)  # Adjust as necessary based on your image

        if text == "Continue without login":
            button.bind(on_release=self.go_to_home_screen)

        return button

    def update_graphics_pos(self, instance, *args):
        # Update the button graphics
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(rgba=get_color_from_hex('#003756'))
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(15)])

    def adjust_layout(self):
        # Increase the space between elements
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.label.pos_hint = {'center_x': 0.5, 'y': 0.6}
        self.continue_button.pos_hint = {'center_x': 0.5, 'y': 0.45}
        self.login_button.pos_hint = {'center_x': 0.5, 'y': 0.35}

        # Recalculate the graphics positions
        self.update_graphics_pos(self.continue_button, None)
        self.update_graphics_pos(self.login_button, None)

    def on_mouse_pos(self, *args):
        pos = args[1]
        for child in self.layout.children:
            if isinstance(child, Button):
                if child.collide_point(*pos):
                    child.background_normal = self.hover_bg
                else:
                    child.background_normal = self.normal_bg

    def go_to_home_screen(self, instance):
        # Change the current screen to 'home'
        self.manager.current = 'home'