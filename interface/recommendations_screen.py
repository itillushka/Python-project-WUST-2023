import webbrowser

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

    PlayButton:
        id: play_button_image
        source: root.play_button
        size_hint_x: None
        width: self.height
        on_press: root.on_play_button_press()
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


class SongItem(ButtonBehavior, BoxLayout):
    """
        A custom widget representing a song item, combining button behavior with a box layout.

        Attributes:
            title (StringProperty): The title of the song.
            artist (StringProperty): The artist of the song.
            duration (StringProperty): The duration of the song.
            play_button (StringProperty): Path to the play button image.

        Methods:
            on_play_button_press(): Handles the event when the play button is pressed.
        """
    title = StringProperty('')
    artist = StringProperty('')
    duration = StringProperty('')
    play_button = StringProperty(abs_path_to_res + 'icon_play_button.png')

    def on_play_button_press(self):
        """
        Handles the play button press event.

        This method is called when the play button in the song item is pressed.
        """

        print("The song is being played")


class PlayButton(ButtonBehavior, Image):
    """
    A custom play button widget, inheriting from ButtonBehavior and Image.

    This button changes its appearance when hovered over with the mouse.

    Methods:
        on_mouse_pos(*args): Handles the change of the button's appearance based on mouse position.
    """

    def __init__(self, **kwargs):
        """
        Initializes the PlayButton instance.

        Binds the necessary events for functionality.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(PlayButton, self).__init__(**kwargs)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        """
        Handles the mouse position event for hover effect.

        Changes the source of the button image when the mouse hovers over it.

        Args:
            *args: Variable length argument list, where the second argument
                   is expected to be the mouse position.
        """

        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = abs_path_to_res + 'icon_play_button_highlighted.png'
        else:
            self.source = abs_path_to_res + 'icon_play_button.png'


class SongsRecycleView(RecycleView):
    """
    A RecycleView widget customized for displaying a list of songs.

    This class handles the display and update of song information in a recycle view format.

    Methods:
        update_track_info(*args): Updates the track information in the view.
    """

    def __init__(self, **kwargs):
        super(SongsRecycleView, self).__init__(**kwargs)

        # Bind the update_track_info method to track info updates
        App.get_running_app().bind(track_info=self.update_track_info)

        # Initialize the view with current track information
        self.update_track_info()

    def update_track_info(self, *args):
        """
        Updates the track information in the view.

        Retrieves track information from the App instance and updates the view. If no
        track information is available, it displays an empty list.

        Args:
            *args: Additional arguments, not used in this method.
        """

        # Retrieve track information from the App instance
        if hasattr(App.get_running_app(), 'track_info') and App.get_running_app().track_info is not None:
            track_info = App.get_running_app().track_info
        else:
            track_info = []

        # Add play button icon to each track
        for i, track in enumerate(track_info):
            track['play_button'] = abs_path_to_res + 'icon_play_button.png'

        # Update the RecycleView data
        self.data = track_info

        # Set up the background for the RecycleView
        with Window.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            self.bg = Rectangle(
                source=(abs_path_to_res + 'spotamix_background_main.png'),
                size=(Window.width, Window.height))

        # Adjust size and position of the RecycleView
        self.size_hint = (0.8, 0.6)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.35}


class PlaylistButton(ButtonBehavior, FloatLayout):
    """
    A custom button widget for navigating to a Spotify playlist, combining button behavior with a float layout.

    Methods:
        on_mouse_pos(*args): Handles the change of the button's appearance based on mouse position.
        on_enter(): Changes the button's background to a highlighted version when hovered.
        on_leave(): Reverts the button's background to the default when not hovered.
        on_press(): Defines the action when the button is pressed.
    """

    def __init__(self, **kwargs):
        """
        Initializes the PlaylistButton instance.

        Sets up the button's size, position, background image, label, and binds the necessary events for functionality.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(PlaylistButton, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (Window.width * 0.8, 60)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.40}

        # Setup background image
        self.background_image = Image(
            source=(abs_path_to_res + 'button_background.png'),
            allow_stretch=True,
            keep_ratio=True,
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.40}
        )

        self.default_source = abs_path_to_res + 'button_background.png'
        self.highlight_source = abs_path_to_res + 'button_background_highlighted.png'
        self.add_widget(self.background_image)

        # Full path to the font file
        font_path = abs_path_to_res + 'AristaSans-OV314.ttf'

        # Setup label
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

        # Bind mouse events for hover effects
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        """
        Handles the mouse position event for hover effect.

        Args:
            *args: Variable length argument list, where the second argument
                   is expected to be the mouse position.
        """
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
        """
        Changes the button's background to the highlighted version when hovered.
        """
        self.background_image.source = self.highlight_source

    def on_leave(self):
        """
        Reverts the button's background to the default when not hovered.
        """
        self.background_image.source = self.default_source

    def on_press(self):
        """
        Defines the action to be taken when the button is pressed.

        Opens the Spotify playlist link in a web browser.
        """
        new_playlist_link = App.get_running_app().new_playlist_link
        webbrowser.open(new_playlist_link)
        print("Navigate to the spotify playlist.")


class BackButton(ButtonBehavior, Image):
    """
    A custom button widget designed to act as a back button.

    Inherits from ButtonBehavior and Image to provide interactive functionality.
    The button changes its appearance when hovered over and returns to the main
    menu when clicked.

    Attributes:
        normal_source (str): Path to the image for the button's normal state.
        highlighted_source (str): Path to the image for the button's highlighted state.
        size_hint (tuple): Size hint for the button's size.
        size (tuple): Size of the button in pixels.
        pos_hint (dict): Position hint for the button's position on the screen.
        keep_ratio (bool): Maintain the aspect ratio of the button's image.
        allow_stretch (bool): Allow stretching of the button's image.
    """

    def __init__(self, **kwargs):
        """
        Initializes the BackButton instance.

        Sets up the button with its normal and highlighted images, size, position,
        and binds the necessary events for functionality.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(BackButton, self).__init__(**kwargs)
        self.normal_source = abs_path_to_res + 'icon_go_back_button.png'
        self.highlighted_source = abs_path_to_res + 'icon_go_back_button_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'x': 0.01, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True
        self.bind(on_release=self.go_to_main_menu)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        """
        Handles the mouse position event for hover effect.

        Changes the source of the button image when the mouse hovers over it.

        Args:
            *args: Variable length argument list, where the second argument
                   is expected to be the mouse position.
        """
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def go_to_main_menu(self, instance):
        """
        Transitions to the main menu screen.

        This method is called when the back button is clicked. It navigates the user
        back to the main menu of the application.

        Args:
            instance: The instance of the button that was clicked.
        """
        current_screen = self.parent
        while current_screen and not isinstance(current_screen, Screen):
            current_screen = current_screen.parent

        if current_screen and hasattr(current_screen, 'manager'):
            current_screen.manager.current = 'main_menu'


class ExitButton(ButtonBehavior, Image):
    """
    A custom button widget designed to exit the application.

    Inherits from ButtonBehavior and Image. The button changes its appearance
    when hovered over and closes the application when clicked.

    Attributes:
        normal_source (str): Path to the image for the button's normal state.
        highlighted_source (str): Path to the image for the button's highlighted state.
        size_hint (tuple): Size hint for the button's size.
        size (tuple): Size of the button in pixels.
        pos_hint (dict): Position hint for the button's position on the screen.
        keep_ratio (bool): Maintain the aspect ratio of the button's image.
        allow_stretch (bool): Allow stretching of the button's image.
    """

    def __init__(self, **kwargs):
        """
        Initializes the ExitButton instance.

        Sets up the button with its normal and highlighted images, size, position,
        and binds the necessary events for functionality.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(ExitButton, self).__init__(**kwargs)
        self.normal_source = abs_path_to_res + 'icon_exit.png'
        self.highlighted_source = abs_path_to_res + 'icon_exit_highlighted.png'
        self.source = self.normal_source
        self.size_hint = (None, None)
        self.size = (50, 50)
        self.pos_hint = {'right': 0.99, 'top': 0.99}
        self.keep_ratio = True
        self.allow_stretch = True
        self.bind(on_release=self.exit_app)
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        """
        Handles the mouse position event for hover effect.

        Changes the source of the button image when the mouse hovers over it.

        Args:
            *args: Variable length argument list, where the second argument
                   is expected to be the mouse position.
        """

        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.source = self.highlighted_source
        else:
            self.source = self.normal_source

    def exit_app(self, instance):
        """
        Closes the application.

        This method is called when the exit button is clicked.

        Args:
            instance: The instance of the button that was clicked.
        """

        App.get_running_app().stop()


class RecommendationsScreen(Screen):
    """
    A screen class that displays recommendations.

    This class is responsible for setting up the recommendations screen, including
    the layout, images, buttons, and the song recycle view. It inherits from the
    Screen class of Kivy.

    Attributes:
        main_layout (BoxLayout): The main container for the screen elements.
    """

    def __init__(self, **kwargs):
        """
        Initializes the RecommendationsScreen instance.

        Sets up the main layout, adds images, buttons, and the songs recycle view
        to the layout.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the superclass.
        """

        super(RecommendationsScreen, self).__init__(**kwargs)

        # Main vertical layout
        main_layout = BoxLayout(orientation='vertical', padding=[0, 10, 0, 10])

        # Images
        logo_image = Image(
            source=(abs_path_to_res + 'logo_spotamix.png'),
            size_hint_y=None,
            height=Window.height * 0.1
        )
        name_image = Image(
            source=(abs_path_to_res + 'spotamix_name.png'),
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
