# home_screen.py
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

# # Load the .kv file for the RoundedTextInput.kv
# Builder.load_file('C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/customs/RoundedTextInput'
#                   '.kv')


# Define the active and inactive colors
active_input_color = get_color_from_hex('#67E26D')
inactive_input_color = get_color_from_hex('#313131')
darker_color = get_color_from_hex('#303030')  # Darker shade for inactive input

dark_grey = get_color_from_hex('#404040')


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)

        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)

        # Bind to mouse position changes
        Window.bind(mouse_pos=self.on_mouse_pos)

        # Set the background image
        with self.canvas.before:
            bg_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_background_main.png'
            self.bg = Rectangle(source=bg_path, size=(Window.width, Window.height))

        # Load and place the smaller logo
        logo_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/logo_spotamix.png'
        self.logo = Image(source=logo_path, allow_stretch=True)
        self.logo.size_hint = None, None
        self.logo.size = (dp(250), dp(250))
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.85}
        self.layout.add_widget(self.logo)

        # Load and place the smaller Spotamix image
        spotamix_label_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_name.png'
        self.spotamix_label = Image(source=spotamix_label_path, allow_stretch=True)
        self.spotamix_label.size_hint = None, None
        self.spotamix_label.size = (dp(250), dp(60))  # Half the size of the original
        self.spotamix_label.pos_hint = {'center_x': 0.5, 'center_y': 0.70}
        self.layout.add_widget(self.spotamix_label)

        # Add a short description
        self.description = Label(
            text="Give us your favorite track and we'll give you a Spotify playlist with similar songs that you'll love.",
            font_name='Antichona', font_size='40sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(None, None),
            size=(Window.width * 0.8, dp(100)),
            pos_hint={'center_x': 0.5, 'center_y': 0.60}
        )
        self.layout.add_widget(self.description)

        # Add an editable text input for "Enter track"
        self.song_input = TextInput(
            hint_text="Enter track",
            font_name='Antichona', font_size='40sp',
            size_hint=(0.8, None),
            height=dp(70),
            width=dp(300),
            padding_x=(10, 10),
            pos_hint={'center_x': 0.5, 'center_y': 0.50},
            foreground_color=active_input_color,
            background_color=inactive_input_color,
        )
        self.song_input.bind(focus=self.on_input_focus)
        self.layout.add_widget(self.song_input)
        self.song_input.bind(text=self.on_input_text)

        # Add text "Or enter your playlist link"
        self.playlist_label = Label(
            text="Or enter your playlist link:",
            font_name='Antichona', font_size='40sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(None, None),
            size=(Window.width * 0.8, dp(40)),
            pos_hint={'center_x': 0.5, 'center_y': 0.40}
        )
        self.layout.add_widget(self.playlist_label)

        # Add text input for "Enter playlist link"
        self.playlist_input = TextInput(
            hint_text="Enter playlist link",
            font_name='Antichona', font_size='40sp',
            size_hint=(0.8, None),
            height=dp(70),
            width=dp(300),
            padding_x=(10, 10),
            pos_hint={'center_x': 0.5, 'center_y': 0.30},
            foreground_color=active_input_color,
            background_color=inactive_input_color,
        )
        self.song_input.bind(focus=self.on_input_focus)
        self.layout.add_widget(self.playlist_input)
        self.song_input.bind(text=self.on_input_text)

        # Define paths for normal and hover background images (same as MainMenuScreen)
        self.normal_bg = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background.png'
        self.hover_bg = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background_highlighted.png'

        # Continue button (use the same style as in MainMenuScreen)
        self.continue_button = self.create_styled_button("Continue")
        self.continue_button.size_hint = (None, None)
        self.continue_button.size = (Window.width * 0.4, dp(110))
        self.continue_button.pos_hint = {'center_x': 0.5, 'y': 0.15}
        self.layout.add_widget(self.continue_button)

    def create_styled_button(self, text):
        button = Button(text=text, font_name='AristaSans', font_size='25sp', size_hint=(None, None), height=dp(110))
        button.background_normal = self.normal_bg
        button.background_down = self.normal_bg
        button.border = (0, 0, 0, 0)
        button.bind(size=self.update_graphics_pos, pos=self.update_graphics_pos)
        button.bind(on_release=self.go_to_recommendations_screen)  # Bind to the same or different function as needed
        return button

    def update_graphics_pos(self, instance, *args):
        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(rgba=get_color_from_hex('#003756'))
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(15)])

    def on_input_text(self, instance, value):
        # Check if the other input should be disabled
        if instance == self.song_input and value.strip():
            self.playlist_input.disabled = True
        elif instance == self.playlist_input and value.strip():
            self.song_input.disabled = True
        else:
            # If both inputs are empty, ensure both are enabled
            self.song_input.disabled = False
            self.playlist_input.disabled = False

    def on_mouse_pos(self, *args):
        # Change button background on hover
        pos = args[1]
        for child in self.layout.children:
            if isinstance(child, Button):
                if child.collide_point(*pos):
                    child.background_normal = self.hover_bg
                else:
                    child.background_normal = self.normal_bg

    def go_to_recommendations_screen(self, instance):
        # Check if either of the text inputs is filled
        if self.song_input.text.strip() or self.playlist_input.text.strip():
            print("Proceeding to the next screen...")
            # Change the current screen to the recommendations screen
            self.manager.current = 'recommendations'
        else:
            print("Please fill in at least one of the inputs.")

    def on_input_focus(self, instance, is_focused):
        if is_focused:
            # The focused input has text, darken the other one
            if instance == self.song_input and self.song_input.text.strip():
                self.playlist_input.background_color = darker_color
            elif instance == self.playlist_input and self.playlist_input.text.strip():
                self.song_input.background_color = darker_color
        else:
            # If neither input is focused, return to the inactive color
            self.song_input.background_color = inactive_input_color
            self.playlist_input.background_color = inactive_input_color
