import threading

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.utils import get_color_from_hex
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from Algorithm.server import run
from splash_screen import SplashScreen
from main_menu_screen import MainMenuScreen
from home_screen import HomeScreen
from recommendations_screen import RecommendationsScreen

# Setting the application window size
Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
# Uncomment below to enable fullscreen mode
# Config.set('graphics', 'fullscreen', 'auto')
Config.write()

# Configure the window appearance
Window.borderless = True
Window.clearcolor = get_color_from_hex('#151515')


class MyApp(App):
    """
    Main application class for managing different screens and transitions.

    Attributes:
        track_info (ObjectProperty): Stores information about the current track.
    """
    track_info = ObjectProperty(None)

    def build(self):
        """
        Builds the application, setting up screens and transitions.

        Returns:
            ScreenManager: The manager that handles screen transitions and display.
        """
        self.screen_manager = ScreenManager(transition=NoTransition())

        # Initialize and add the splash screen
        splash_screen = SplashScreen(name='splash')
        self.screen_manager.add_widget(splash_screen)

        # Initialize and add the main menu screen
        main_menu_screen = MainMenuScreen(name='main_menu')
        self.screen_manager.add_widget(main_menu_screen)

        # Initialize and add the home screen
        home_screen = HomeScreen(name='home')
        self.screen_manager.add_widget(home_screen)

        # Initialize and add the recommendations screen
        recommendations_screen = RecommendationsScreen(name='recommendations')
        self.screen_manager.add_widget(recommendations_screen)

        # Setting the initial screen
        self.screen_manager.current = 'splash'

        return self.screen_manager


if __name__ == '__main__':
    # Initialize and start the server in a separate thread
    server_thread = threading.Thread(target=run)
    server_thread.start()

    # Create and run the Kivy application
    app = MyApp()
    app.run()
