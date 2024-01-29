from kivy.app import App
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase

from Algorithm.config import abs_path_to_res

# Set the application to fullscreen
Window.fullscreen = 'auto'

# Custom fonts registration
font_path = abs_path_to_res + 'AristaSans-OV314.ttf'
LabelBase.register(name='AristaSans', fn_regular=font_path)
font_path = abs_path_to_res + 'Antichona-VGlAy.ttf'
LabelBase.register(name='Antichona', fn_regular=font_path)

# Calculate scale factors for responsive design
scale_x = 1920 / 2350
scale_y = 1080 / 1323

class ExitButton(ButtonBehavior, Image):
    """
    A custom button widget combining button behavior with an image, designed to serve as an exit button.

    Attributes:
        normal_source (str): Path to the image for the button's normal state.
        highlighted_source (str): Path to the image for the button's highlighted state (on hover).
        size_hint (tuple): Size hint for the button's size (None, None for no scaling).
        size (tuple): Size of the button in pixels.
        pos_hint (dict): Position hint for button's position on the screen.
        keep_ratio (bool): Maintain the aspect ratio of the button's image.
        allow_stretch (bool): Allow stretching of the button's image.

    Methods:
        on_mouse_pos(*args): Handles the change of the button's appearance based on mouse position.
        exit_app(instance): Closes the application when the button is clicked.
    """

    def __init__(self, **kwargs):
        """
        Initializes the ExitButton instance.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(ExitButton, self).__init__(**kwargs)
        self.normal_source = abs_path_to_res + 'icon_exit.png'
        self.highlighted_source = abs_path_to_res + 'icon_exit_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'right': 0.99, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True
        self.bind(on_release=self.exit_app)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        """
        Handles the mouse position event for hover effect.

        Changes the source of the button image when the mouse hovers over it.

        Args:
            *args: Variable length argument list, where the second argument
                   is expected to be the mouse position.
        """

        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def exit_app(self, instance):
        """
        Closes the application.

        This method is called when the exit button is clicked.

        Args:
            instance: The instance of the button that was clicked.
        """

        App.get_running_app().stop()


class MainMenuScreen(Screen):
    """
    A screen representing the main menu of the application.

    Attributes:
        layout (FloatLayout): The main layout to hold all widgets.
        bg_texture (Texture): Texture of the background image.
        logo (Image): Image widget for the logo.
        spotamix_label (Image): Image widget for the Spotamix label.
        normal_bg (str): Path to the normal button background image.
        hover_bg (str): Path to the hover state button background image.
        continue_button (Button): Button to continue without login.
        login_button (Button): Button to initiate the login process.

    Methods:
        create_styled_button(text): Creates a styled button with specified text.
        update_graphics_pos(instance, *args): Updates the graphics position of a widget.
        adjust_layout(): Adjusts the layout of the screen elements.
        on_mouse_pos(*args): Handles hover effect over buttons.
        go_to_home_screen(instance): Transitions to the home screen.
    """

    def __init__(self, **kwargs):
        """
        Initializes the MainMenuScreen instance.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(MainMenuScreen, self).__init__(**kwargs)

        # Initialize layout and background
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)

        # Setup background image
        bg_path = abs_path_to_res + 'spotamix_background_main.png'
        self.bg_texture = Image(source=bg_path).texture
        with Window.canvas.before:
            Rectangle(texture=self.bg_texture, size=Window.size, pos=(0, 0))

        # Setup logo and label
        logo_path = (abs_path_to_res + 'logo_spotamix.png')
        self.logo = Image(source=logo_path, allow_stretch=True, keep_ratio=True)
        self.logo.size_hint = None, None
        self.logo.size = (dp(300) * scale_x, dp(300) * scale_y)
        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.75}
        self.layout.add_widget(self.logo)

        # Setup the "Spotamix" image below the logo
        self.spotamix_label = Image(source=(abs_path_to_res + 'spotamix_name.png'), allow_stretch=True, keep_ratio=True)
        self.spotamix_label.size_hint = None, None
        self.spotamix_label.width = self.logo.width
        self.spotamix_label.height = self.logo.height
        self.spotamix_label.pos_hint = {'center_x': 0.5, 'y': 0.4}
        self.layout.add_widget(self.spotamix_label)

        # Add Exit Button
        exit_button = ExitButton()
        self.layout.add_widget(exit_button)

        # Define paths for normal and hover background images
        self.normal_bg = abs_path_to_res + 'button_background.png'
        self.hover_bg = abs_path_to_res + 'button_background_highlighted.png'

        # Create buttons with their styles
        self.continue_button = self.create_styled_button("Continue without login")
        self.login_button = self.create_styled_button("Login")

        # Adjust buttons width and height
        button_width = Window.width * 0.4
        button_height = dp(110) * scale_y
        self.continue_button.size = (button_width, button_height)
        self.login_button.size = (button_width, button_height)

        # Position buttons
        self.continue_button.pos_hint = {'center_x': 0.5, 'y': 0.30}
        self.login_button.pos_hint = {'center_x': 0.5, 'y': 0.15}

        # Add buttons to the layout
        self.layout.add_widget(self.continue_button)
        self.layout.add_widget(self.login_button)

    def create_styled_button(self, text):
        """
        Creates a styled button with the given text.

        This method initializes a Button widget with specific styling, including
        font, size, and background images. The button is also bound to an event
        handler for release if it's the 'Continue without login' button.

        Args:
            text (str): The text to display on the button.

        Returns:
            Button: The styled button with the specified text.
        """

        button = Button(text=text, font_name='AristaSans', font_size='25sp', size_hint=(None, None), height=dp(110))
        button.background_normal = self.normal_bg
        button.background_down = self.normal_bg
        button.border = (0, 0, 0, 0)

        if text == "Continue without login":
            button.bind(on_release=self.go_to_home_screen)

        return button

    def update_graphics_pos(self, instance, *args):
        """
        Updates the graphical position of a widget.

        This method clears the previous canvas and redraws the rectangle with updated
        position and size, ensuring the visual elements align with the widget's position.

        Args:
            instance: The widget instance whose graphical position is to be updated.
            *args: Additional arguments, not used in this method.
        """

        instance.canvas.before.clear()
        with instance.canvas.before:
            Color(rgba=get_color_from_hex('#003756'))
            RoundedRectangle(pos=instance.pos, size=instance.size, radius=[dp(15)])

    def adjust_layout(self):
        """
        Adjusts the layout of screen elements.

        This method increases the space between the logo, label, and buttons and
        recalculates their graphics positions.
        """

        self.logo.pos_hint = {'center_x': 0.5, 'center_y': 0.7}
        self.label.pos_hint = {'center_x': 0.5, 'y': 0.6}
        self.continue_button.pos_hint = {'center_x': 0.5, 'y': 0.45}
        self.login_button.pos_hint = {'center_x': 0.5, 'y': 0.35}

        self.update_graphics_pos(self.continue_button, None)
        self.update_graphics_pos(self.login_button, None)

    def on_mouse_pos(self, *args):
        """
        Handles hover effect over buttons.

        Changes the background of buttons based on mouse position.

        Args:
            *args: Additional arguments where the second argument is expected to be the mouse position.
        """

        pos = args[1]
        for child in self.layout.children:
            if isinstance(child, Button):
                if child.collide_point(*pos):
                    child.background_normal = self.hover_bg
                else:
                    child.background_normal = self.normal_bg

    def go_to_home_screen(self, instance):
        """
        Transitions to the home screen.

        Changes the current screen to the home screen when the button is clicked.

        Args:
            instance: The instance of the button that was clicked.
        """

        # Change the current screen to 'home'
        self.manager.current = 'home'