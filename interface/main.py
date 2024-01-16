# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.utils import get_color_from_hex
from kivy.config import Config
from kivy.core.window import Window

# Import your screens here
from splash_screen import SplashScreen
from main_menu_screen import MainMenuScreen
from home_screen import HomeScreen
from recommendations_screen import RecommendationsScreen


# Set the configuration before any other Kivy components are imported
Config.set('graphics', 'width', '2350')
Config.set('graphics', 'height', '1323')
Config.write()

# Set the window to be borderless for the rounded corners effect
Window.borderless = True
# Set the window background color to match the main menu background
Window.clearcolor = get_color_from_hex('#151515')

class MyApp(App):
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

        # Then add the recommendations screen
        recommendations_screen = RecommendationsScreen(name='recommendations')
        self.screen_manager.add_widget(recommendations_screen)

        # Optionally, set the 'splash' screen as the current screen to show first
        self.screen_manager.current = 'splash'

        return self.screen_manager

if __name__ == '__main__':
    app = MyApp()
    app.run()