# home_screen.py
from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
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

# Define the active and inactive colors
active_input_color = get_color_from_hex('#67E26D')
inactive_input_color = get_color_from_hex('#313131')
darker_color = get_color_from_hex('#303030')  # Darker shade for inactive input

dark_grey = get_color_from_hex('#404040')


class BackButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)
        self.normal_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_go_back_button.png'
        self.highlighted_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_go_back_button_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'x': 0.01, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True

        # Bind the on_release event to the go_to_main_menu method
        self.bind(on_release=self.go_to_main_menu)

        # Bind mouse position to change button appearance on hover
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        # Change the source of the button when mouse hovers over it
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def go_to_main_menu(self, instance):
        # Get the current screen (which is a direct child of ScreenManager)
        current_screen = self.parent
        while current_screen and not isinstance(current_screen, Screen):
            current_screen = current_screen.parent

        # Now we can check if we have a Screen and its manager exists
        if current_screen and hasattr(current_screen, 'manager'):
            current_screen.manager.current = 'main_menu'


class ExitButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ExitButton, self).__init__(**kwargs)
        self.normal_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_exit.png'
        self.highlighted_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_exit_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'right': 0.99, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True
        self.bind(on_release=self.exit_app)

        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def exit_app(self, instance):
        App.get_running_app().stop()


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

        # Add Exit Button
        exit_button = ExitButton()
        self.layout.add_widget(exit_button)

        # Add Back Button (if needed)
        back_button = BackButton()
        self.layout.add_widget(back_button)

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
        # Bind the on_input_song method to the text property
        self.song_input.bind(text=self.on_input_song)
        self.layout.add_widget(self.song_input)

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
        # Bind the on_input_playlist method to the text property
        self.playlist_input.bind(text=self.on_input_playlist)
        self.layout.add_widget(self.playlist_input)

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

    def on_input_song(self, instance, value):
        if value.strip():
            # If there is text in the song input, disable the playlist input
            self.playlist_input.disabled = True
        else:
            # If the song input is empty, enable the playlist input
            self.playlist_input.disabled = False

    def on_input_playlist(self, instance, value):
        if value.strip():
            # If there is text in the playlist input, disable the song input
            self.song_input.disabled = True
        else:
            # If the playlist input is empty, enable the song input
            self.song_input.disabled = False

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

    def on_input_song(self, instance, value):
        if value.strip():
            # If there is text in the song input, disable the playlist input
            self.playlist_input.disabled = True
        else:
            # If the song input is empty, enable the playlist input
            self.playlist_input.disabled = False

    def on_input_playlist(self, instance, value):
        if value.strip():
            # If there is text in the playlist input, disable the song input
            self.song_input.disabled = True
        else:
            # If the playlist input is empty, enable the song input
            self.song_input.disabled = False