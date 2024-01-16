from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

Builder.load_string('''
<SongItem>:
    orientation: 'horizontal'
    padding: dp(10)
    spacing: dp(10)

    Image:
        source: root.play_button
        size_hint_x: None
        width: self.height
    Label:
        text: root.title
        size_hint_x: 0.5
    Label:
        text: root.artist
        size_hint_x: 0.3
    Label:
        text: root.duration
        size_hint_x: 0.2

<SimpleRecycleView>:
    viewclass: 'SongItem'
    RecycleBoxLayout:
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
''')

class RecommendationsScreen(Screen):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super(RecommendationsScreen, self).__init__(**kwargs)
        self.layout = FloatLayout(size=(Window.width, Window.height))
        self.add_widget(self.layout)

        # Set the background image
        with self.canvas.before:
            bg_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_background_main.png'
            self.bg = Rectangle(source=bg_path, size=(Window.width, Window.height))

        # Load and place the smaller logo
        logo_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/logo_spotamix.png'
        self.logo = Image(source=logo_path, allow_stretch=True)
        self.logo.size_hint = None, None
        self.logo.size = (dp(100), dp(100))  # Adjust size as needed
        self.logo.pos_hint = {'center_x': 0.5, 'top': 0.95}
        self.layout.add_widget(self.logo)

        # Load and place the smaller Spotamix image
        spotamix_label_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_name.png'
        self.spotamix_label = Image(source=spotamix_label_path, allow_stretch=True)
        self.spotamix_label.size_hint = None, None
        self.spotamix_label.size = (dp(200), dp(50))  # Adjust size as needed
        self.spotamix_label.pos_hint = {'center_x': 0.5, 'top': 0.85}
        self.layout.add_widget(self.spotamix_label)

        # # Initialize the list of song data
        # self.data_items = self.get_songs_data()
        #
        # # Create the RecycleView
        # self.songs_list = RecycleView()
        # self.songs_list.size_hint = (None, None)
        # self.songs_list.size = (Window.width * 0.8, Window.height * 0.5)  # Make it smaller
        # self.songs_list.pos_hint = {'center_x': 0.5, 'center_y': 0.4}  # Adjust position under logo
        #
        # # Define the viewclass used by the RecycleView
        # self.songs_list.viewclass = 'SongItem'
        #
        # # Assign the data to the RecycleView
        # self.songs_list.data = [{'title': song['title'],
        #                          'artist': song['artist'],
        #                          'duration': song['duration'],
        #                          'play_button': song['play_button']}
        #                         for song in self.data_items]
        #
        # # Add the RecycleView to the layout
        # self.layout.add_widget(self.songs_list)

        # Add a 'Back' button to return to the home screen
        self.back_button = Button(
            text='Back',
            size_hint=(None, None),
            size=(dp(100), dp(50)),
            pos_hint={'x': 0, 'top': 1},
            background_normal='',
            background_color=get_color_from_hex('055065'),  # Midnight Green
            color=get_color_from_hex('FFFFFF')  # White text color
        )
        self.back_button.bind(on_release=self.go_back)
        self.layout.add_widget(self.back_button)

        # Bind to mouse position changes for hover effect
        Window.bind(mouse_pos=self.on_mouse_pos)

        # ... [Set up buttons and other UI elements] ...

    def create_styled_button(self, text):
        # Create a button with the desired style
        button = Button(text=text, font_name='AristaSans', font_size='25sp', size_hint=(None, None), height=dp(110))
        # ... [style the button, set background, etc.] ...
        return button

    def on_mouse_pos(self, *args):
        # Change button color on hover
        pos = args[1]
        if self.back_button.collide_point(*self.to_widget(*pos)):
            self.back_button.background_color = get_color_from_hex('13A95F')  # Pigment Green
            self.back_button.color = get_color_from_hex('67E26D')  # Malachite
        else:
            self.back_button.background_color = get_color_from_hex('055065')  # Midnight Green
            self.back_button.color = get_color_from_hex('FFFFFF')  # White

    def go_back(self, instance):
        # Logic to go back to the previous screen
        self.manager.transition.direction = 'right'
        self.manager.current = 'home'  # Or whatever the name of your home screen is

# ... [Rest of your code, including methods to handle button presses and transitions] ...
# Define the SongItem class
class SongItem(BoxLayout):
    title = StringProperty('')
    artist = StringProperty('')
    duration = StringProperty('')
    play_button = StringProperty('play_image.png')  # Update the path to your play image

class SimpleRecycleView(RecycleView):
    def __init__(self, **kwargs):
        super(SimpleRecycleView, self).__init__(**kwargs)
        self.data = [{'title': f'Song {i}', 'artist': f'Artist {i}', 'duration': '3:00', 'play_button': 'play_image.png'} for i in range(20)]
