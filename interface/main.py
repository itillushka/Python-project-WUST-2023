# main.py
import threading

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.utils import get_color_from_hex
from kivy.config import Config
from kivy.core.window import Window
from kivy.properties import ObjectProperty

from Algorithm.spotify_connect import connect_sp
from Algorithm.server import run
# Import your screens here
from splash_screen import SplashScreen
from main_menu_screen import MainMenuScreen
from home_screen import HomeScreen
from recommendations_screen import RecommendationsScreen

Config.set('graphics', 'width', '1920')
Config.set('graphics', 'height', '1080')
# Config.set('graphics', 'fullscreen', 'auto')
Config.write()

# Set the window to be borderless for the rounded corners effect
Window.borderless = True
# Set the window background color to match the main menu background
Window.clearcolor = get_color_from_hex('#151515')


class MyApp(App):
    track_info = ObjectProperty(None)
    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())

        # Add the splash screen
        splash_screen = SplashScreen(name='splash')
        self.screen_manager.add_widget(splash_screen)

        # Then add the main menu screen
        main_menu_screen = MainMenuScreen(name='main_menu')
        self.screen_manager.add_widget(main_menu_screen)

        # Then add the home screen
        home_screen = HomeScreen(name='home')
        self.screen_manager.add_widget(home_screen)

        # Add the recommendations screen
        recommendations_screen = RecommendationsScreen()
        recommendations_screen.name = 'recommendations'  # Set the name property here
        self.screen_manager.add_widget(recommendations_screen)

        # Optionally, set the 'splash' screen as the current screen to show first
        self.screen_manager.current = 'splash'

        return self.screen_manager




if __name__ == '__main__':
    # Start the server in a separate thread
    server_thread = threading.Thread(target=run)
    server_thread.start()

    app = MyApp()
    app.run()
