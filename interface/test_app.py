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
        font_name: 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'
        color: (0.4,0.89, 0.55, 1) if root.title else (1, 1, 1, 1)
        size_hint_x: 0.5
    Label:
        text: root.artist
        font_name: 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'
        size_hint_x: 0.3
    Label:
        text: root.duration
        font_name: 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'
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


# Define the SongItem class
class SongItem(BoxLayout):
    title = StringProperty('')
    artist = StringProperty('')
    duration = StringProperty('')
    play_button = StringProperty('')


class SongsRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(SongsRecycleView, self).__init__(**kwargs)
        self.data = [{'title': f'Song {i}', 'artist': f'Artist {i}', 'duration': '3:00',
                      'play_button': 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_play_button.png'}
                     for i in range(50)]
        # Set the background for the entire window
        with Window.canvas.before:
            Color(rgba=(1, 1, 1, 1))  # White color
            self.bg = Rectangle(
                source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_background_main.png',
                size=(Window.width, Window.height))

        # Adjust the size and position of the RecycleView
        self.size_hint = (0.8, 0.6)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.4}
        pass


# Define the custom button class
class PlaylistButton(ButtonBehavior, FloatLayout):
    def __init__(self, **kwargs):
        super(PlaylistButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (Window.width * 0.8, 60)  # Adjust the size as needed
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Image as the background
        self.background_image = Image(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1.3, 1.3),
            pos_hint={'center_x': 0.5, 'center_y': 0.35}
        )

        # Full path to the font file
        font_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'

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
        # Add action for when the button is pressed
        print("Navigate to the playlist screen.")


class RecommendationsScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(RecommendationsScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 10, 0, 10]

        # Images
        logo_image = Image(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/logo_spotamix.png')
        name_image = Image(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_name.png')

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
    def build(self):
        return RecommendationsScreen()


if __name__ == '__main__':
    MyApp().run()
