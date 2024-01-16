from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview.views import RecycleDataViewBehavior


class SongItem(RecycleDataViewBehavior, BoxLayout):
    title = StringProperty()
    artist = StringProperty()
    duration = StringProperty()
    play_button = StringProperty()

    def on_play_button_press(self):
        # Logic for when the play button is pressed
        print(f"Playing {self.title}")
