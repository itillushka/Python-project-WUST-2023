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

    PlayButton:
        id: play_button_image
        source: root.play_button
        size_hint_x: None
        width: self.height
        on_press: root.on_play_button_press()
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
class SongItem(ButtonBehavior, BoxLayout):
    title = StringProperty('')
    artist = StringProperty('')
    duration = StringProperty('')
    play_button = StringProperty('C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_play_button.png')

    def on_play_button_press(self):
        print("The song is being played")


class PlayButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(PlayButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_play_button_highlighted.png'
        else:
            self.source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_play_button.png'



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
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.35}
        pass


# Define the custom button class
class PlaylistButton(ButtonBehavior, FloatLayout):
    def __init__(self, **kwargs):
        super(PlaylistButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (Window.width * 0.8, 60)  # Adjust the size as needed
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.40}

        # Image as the background
        self.background_image = Image(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background.png',
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.40}
        )

        self.default_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background.png'
        self.highlight_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/button_background_highlighted.png'

        # Add the background image as a widget to the button
        self.add_widget(self.background_image)

        # Full path to the font file
        font_path = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/AristaSans-OV314.ttf'

        # Label for the text
        self.label = Label(
            text='Go to your playlist',
            font_name=font_path,
            size_hint=(None, None),
            size=self.size,
            color=(1, 1, 1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.40}
            )

        # Adding the label to the FloatLayout
        self.add_widget(self.label)

        # Bind on_enter and on_leave events
        self.bind(on_enter=self.on_enter, on_leave=self.on_leave)

        # Register for mouse enter/leave events
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        # Check if mouse is over the button
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            if not hasattr(self, 'hovered'):
                self.hovered = True
                self.on_enter()
        else:
            if hasattr(self, 'hovered'):
                del self.hovered
                self.on_leave()

    def on_enter(self):
        # Change the background image to the highlighted version
        self.background_image.source = self.highlight_source

    def on_leave(self):
        # Change the background image back to the default
        self.background_image.source = self.default_source

    def on_press(self):
        # Add action for when the button is pressed
        print("Navigate to the spotify playlist.")


class BackButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(BackButton, self).__init__(**kwargs)
        self.normal_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_go_back_button.png'
        self.highlighted_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_go_back_button_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'x': 0.01, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True

        # Bind the on_release event to the go_to_main_menu method
        self.bind(on_release=self.go_to_main_menu)

        # Bind mouse position to change button appearance on hover
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        # Change the source of the button when mouse hovers over it
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def go_to_main_menu(self, instance):
        # Get the current screen (which is a direct child of ScreenManager)
        current_screen = self.parent
        while current_screen and not isinstance(current_screen, Screen):
            current_screen = current_screen.parent

        # Now we can check if we have a Screen and its manager exists
        if current_screen and hasattr(current_screen, 'manager'):
            current_screen.manager.current = 'main_menu'


class ExitButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ExitButton, self).__init__(**kwargs)
        self.normal_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_exit.png'
        self.highlighted_source = 'C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/icon_exit_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'right': 0.99, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True
        self.bind(on_release=self.exit_app)

        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def exit_app(self, instance):
        App.get_running_app().stop()


class RecommendationsScreen(Screen):
    def __init__(self, **kwargs):
        super(RecommendationsScreen, self).__init__(**kwargs)
        # Create a BoxLayout as the main container for the screen
        main_layout = BoxLayout(orientation='vertical', padding=[0, 10, 0, 10])

        # Images
        logo_image = Image(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/logo_spotamix.png',
            size_hint_y=None,
            height=Window.height * 0.1
        )
        name_image = Image(
            source='C:/Users/marta/PycharmProjects/Python-project-WUST-2023-develop/interface/resources/spotamix_name.png',
            size_hint_y=None,
            height=Window.height * 0.03
        )

        # Add images to the main layout
        main_layout.add_widget(Widget(size_hint_y=None, height=5))  # Spacer
        main_layout.add_widget(logo_image)
        main_layout.add_widget(Widget(size_hint_y=None, height=15))  # Spacer
        main_layout.add_widget(name_image)
        main_layout.add_widget(Widget(size_hint_y=None, height=20))  # Spacer

        # Add Back Button
        back_button = BackButton()
        self.add_widget(back_button)

        # Add Exit Button
        exit_button = ExitButton()
        self.add_widget(exit_button)

        # SongsRecycleView
        songs_view = SongsRecycleView(size_hint=(0.8, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.4})
        main_layout.add_widget(songs_view)

        # Spacer between recycle view and the button
        main_layout.add_widget(Widget(size_hint_y=None, height=50))

        # Playlist button
        playlist_button = PlaylistButton(size_hint=(None, None), size=(Window.width * 0.8, 60),
                                         pos_hint={'center_x': 0.5, 'center_y': 0.4})
        main_layout.add_widget(playlist_button)

        # Spacer between the button and the bottom of the screen
        main_layout.add_widget(Widget(size_hint_y=None, height=50))

        # Add the main layout to the screen
        self.add_widget(main_layout)