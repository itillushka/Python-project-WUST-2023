from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.graphics import Color, RoundedRectangle

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


class MyApp(App):
    def build(self):
        return SongsRecycleView()


if __name__ == '__main__':
    MyApp().run()


