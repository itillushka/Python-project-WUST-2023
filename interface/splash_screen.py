from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

from Algorithm.config import abs_path_to_res


class SplashScreen(Screen):
    """
    A screen class that displays a splash screen with a video animation.

    Inherits from the Screen class of Kivy and is used as the initial screen
    to display a branding or introductory video.

    Attributes:
        animation (Video): A Video widget to play the animation.
        rect (RoundedRectangle): A RoundedRectangle for the background with rounded corners.
    """
    def __init__(self, **kwargs):
        """
        Initializes the SplashScreen instance.

        Sets up the rounded corner background, video widget, and schedules the transition
        to the next screen after the video duration.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(SplashScreen, self).__init__(**kwargs)

        # Setup rounded corners for the screen
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#151515'))
            self.rect = RoundedRectangle(size=(Window.size), pos=(0, 0), radius=[20])

        # Bind size changes to update rounded corners
        Window.bind(size=self.update_rounded_corners)

        # Initialize and add the video widget
        self.animation = Video(
            source=(abs_path_to_res + 'animation_spotamix_cropped.mp4'),
            state='play',  # Start playing the video automatically
            options={'eos': 'loop'},  # Loop the video when it reaches the end
            allow_stretch=True  # Allow the video to stretch to fill the space
        )
        self.add_widget(self.animation)

        # Schedule transition to the main menu
        Clock.schedule_once(self.change_screen, 6.014)  # Duration of the video

    def change_screen(self, *args):
        """
        Handles the transition to the next screen.

        Args:
            *args: Additional arguments, not used in this method.
        """

        # Change to the next screen
        if self.manager.has_screen('main_menu'):
            self.manager.current = 'main_menu'

    def update_rounded_corners(self, instance, value):
        """
        Updates the size of the rounded corners background when the window size changes.

        Args:
            instance: The instance of the window whose size has changed.
            value: The new size value.
        """

        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#151515'))
            self.rect.size = Window.size
