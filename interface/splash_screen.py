from kivy.uix.screenmanager import Screen
from kivy.uix.video import Video
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.core.window import Window
from kivy.utils import get_color_from_hex

class SplashScreen(Screen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        # Add rounded corners to this screen
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#151515'))  # Set to your window background color
            self.rect = RoundedRectangle(size=(Window.size), pos=(0, 0), radius=[20])
        # Bind to size to update rounded corners when the window size changes
        Window.bind(size=self.update_rounded_corners)

        # Create a Video widget instance
        self.animation = Video(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/animation_spotamix_cropped.mp4',
            state='play',  # Start playing the video automatically
            options={'eos': 'loop'},  # Loop the video when it reaches the end
            allow_stretch=True  # Allow the video to stretch to fill the space
        )
        self.add_widget(self.animation)

        # Schedule the transition to the main menu after the video duration
        Clock.schedule_once(self.change_screen, 6.014)  # Duration of the video

    def change_screen(self, *args):
        # Change to the next screen, presumably the main menu
        if self.manager.has_screen('main_menu'):
            self.manager.current = 'main_menu'

    def update_rounded_corners(self, instance, value):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex('#151515'))  # Background color
            self.rect.size = Window.size
