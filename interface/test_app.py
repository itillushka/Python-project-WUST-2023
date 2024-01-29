from kivy.app import App
from kivy.lang import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen

from Algorithm.config import abs_path_to_res

# Define the .kv design
kv_song_list = '''
<SongItem>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(50)
    padding: dp(10)
    spacing: dp(10)

    Image:
        source: root.play_button
        size_hint_x: None
        width: self.height
    Label:
        text: root.title
        font_name: 'C:/Users/illia/OneDrive/Рабочий стол/Study/Python Programming/sem zim 23-24/Python-project/Python-project-WUST-2023/interface/resources/AristaSans-OV314.ttf'
        color: (0.4,0.89, 0.55, 1) if root.title else (1, 1, 1, 1)
        size_hint_x: 0.5
    Label:
        text: root.artist
        font_name: 'C:/Users/illia/OneDrive/Рабочий стол/Study/Python Programming/sem zim 23-24/Python-project/Python-project-WUST-2023/interface/resources/AristaSans-OV314.ttf'
        size_hint_x: 0.3
    Label:
        text: root.duration
        font_name: 'C:/Users/illia/OneDrive/Рабочий стол/Study/Python Programming/sem zim 23-24/Python-project/Python-project-WUST-2023/interface/resources/AristaSans-OV314.ttf'
        size_hint_x: 0.2

<SongsRecycleView>:
    viewclass: 'SongItem'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        canvas.before:
            Color:
                rgba: (0.24, 0.24, 0.24, 0.5) # Semi-transparent dark grey
            RoundedRectangle:
                size: self.size
                pos: self.pos
                radius: [40]  # Rounded corners with radius of 10 pixels
    '''

Builder.load_string(kv_song_list)


class SongItem(BoxLayout):
    """
    A custom BoxLayout widget representing an individual song item.

    This widget displays details of a song, including its title, artist, duration,
    and a play button.

    Attributes:
        title (StringProperty): The title of the song.
        artist (StringProperty): The artist of the song.
        duration (StringProperty): The duration of the song.
        play_button (StringProperty): Path to the play button image.
    """

    title = StringProperty('')
    artist = StringProperty('')
    duration = StringProperty('')
    play_button = StringProperty('')


class SongsRecycleView(RecycleView):
    """
    A RecycleView widget customized for displaying a list of songs.

    Inherits from RecycleView and is used to display multiple SongItem widgets in a
    scrollable list.

    Attributes:
        data (list): A list of dictionaries containing song information.
    """

    def __init__(self, **kwargs):
        """
        Initializes the SongsRecycleView instance.

        Sets up the view with a predefined list of songs and configures the background.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(SongsRecycleView, self).__init__(**kwargs)
        self.data = [{'title': f'Song {i}', 'artist': f'Artist {i}', 'duration': '3:00',
                      'play_button': (abs_path_to_res + 'icon_play_button.png')}
                     for i in range(50)]

        # Set the background for the entire window
        with Window.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            self.bg = Rectangle(
                source=(abs_path_to_res + 'spotamix_background_main.png'),
                size=(Window.width, Window.height))

        # Adjust the size and position of the RecycleView
        self.size_hint = (0.8, 0.6)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        pass


class PlaylistButton(ButtonBehavior, FloatLayout):
    """
    A custom button class with an image background and text, used to navigate to a playlist.

    Inherits from ButtonBehavior and FloatLayout, allowing for button functionality with
    custom layout and styling.

    Attributes:
        background_image (Image): The background image of the button.
        label (Label): The text label displayed on the button.
    """

    def __init__(self, **kwargs):
        """
        Initializes the PlaylistButton instance.

        Sets up the button with a background image, label, and size and position configurations.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(PlaylistButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (Window.width * 0.8, 60)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Image as the background
        self.background_image = Image(
            source=(abs_path_to_res + 'button_background.png'),
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1.3, 1.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )

        # Full path to the font file
        font_path = abs_path_to_res + 'AristaSans-OV314.ttf'

        # Label for the text
        self.label = Label(
            text='Go to your playlist',
            font_name=font_path,
            size_hint=(None, None),
            size=self.size,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )

        # Adding the background image and label to the FloatLayout
        self.add_widget(self.background_image)
        self.add_widget(self.label)

    def on_press(self):
        """
        Defines the action to be taken when the button is pressed.

        Currently, it prints a message indicating navigation to the playlist screen.
        """
        print("Navigate to the playlist screen.")


class RecommendationsScreen(BoxLayout):
    """
    A BoxLayout class for displaying recommendations, used for testing purposes.

    This class represents a screen layout for testing the recommendations feature.
    It includes images, a custom recycle view for song listings, and a playlist button.
    This version of the screen is specifically designed for testing, separate from
    the main application's recommendations screen.

    Attributes:
        None specific to testing.
    """

    def __init__(self, **kwargs):
        """
        Initializes the RecommendationsScreen instance for testing.

        Sets up the layout with images, a custom songs recycle view, and a playlist button.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(RecommendationsScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 10, 0, 10]

        # Images
        logo_image = Image(
            source=(abs_path_to_res + 'logo_spotamix.png'))
        name_image = Image(
            source=(abs_path_to_res + 'spotamix_name.png'))

        # Adjust the size_hint_y to allocate space appropriately
        logo_image.size_hint_y = None
        name_image.size_hint_y = None
        logo_image.height = Window.height * 0.1
        name_image.height = Window.height * 0.03

        # Add images to the main layout
        self.add_widget(logo_image)

        # Spacer between logo and name images
        spacer1 = Widget(size_hint_y=None, height=10)
        self.add_widget(spacer1)

        self.add_widget(name_image)

        # Spacer between name image and recycle view
        spacer2 = Widget(size_hint_y=None, height=20)
        self.add_widget(spacer2)

        # SongsRecycleView
        songs_view = SongsRecycleView()
        songs_view.size_hint = (0.8, 0.6)
        songs_view.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.add_widget(songs_view)

        # Spacer between recycle view and the button
        button_spacer = Widget(size_hint_y=None, height=50)
        self.add_widget(button_spacer)

        # Playlist button
        playlist_button = PlaylistButton()
        self.add_widget(playlist_button)

        # Spacer between the button and the bottom of the screen
        bottom_spacer_final = Widget(size_hint_y=None)
        self.add_widget(bottom_spacer_final)


class MyApp(App):
    """
    The main App class for testing the RecommendationsScreen.

    This class builds the app using the RecommendationsScreen, designed for testing
    the layout and functionality of the recommendations feature.

    Methods:
        build(): Builds the app with the RecommendationsScreen for testing.
    """

    def build(self):
        """
        Builds the app with the RecommendationsScreen.

        Returns:
            RecommendationsScreen: The main widget of the app, used for testing.
        """

        return RecommendationsScreen()


if __name__ == '__main__':
    MyApp().run()
