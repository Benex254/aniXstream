from kivy.properties import (
    ObjectProperty,
    StringProperty,
    BooleanProperty,
    ListProperty,
    NumericProperty,
)
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.behaviors import HoverBehavior

from .components import MediaPopup


class MediaCard(ButtonBehavior, HoverBehavior, MDBoxLayout):
    screen = ObjectProperty()
    anime_id = NumericProperty()
    title = StringProperty()
    is_play = ObjectProperty()
    trailer_url = StringProperty()
    episodes = StringProperty()
    favourites = StringProperty()
    popularity = StringProperty()
    media_status = StringProperty("Releasing")
    is_in_my_list = BooleanProperty(False)
    is_in_my_notify = BooleanProperty(False)
    genres = StringProperty()
    first_aired_on = StringProperty()
    description = StringProperty()
    producers = StringProperty()
    studios = StringProperty()
    next_airing_episode = StringProperty()
    tags = StringProperty()
    stars = ListProperty([0, 0, 0, 0, 0, 0])
    cover_image_url = StringProperty()
    preview_image = StringProperty()
    has_trailer_color = ListProperty([.5, .5, .5, .5])

    def __init__(self, trailer_url=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"

        if trailer_url:
            self.trailer_url = trailer_url
        self.adaptive_size = True

    def on_enter(self):
        def _open_popup(dt):
            if self.hovering:
                window = self.get_parent_window()
                if window:
                    for widget in window.children:  # type: ignore
                        if isinstance(widget, MediaPopup):
                            return
                    self.open()

        Clock.schedule_once(_open_popup, 5)

    def on_popup_open(self, popup: MediaPopup):
        popup.center = self.center

    def on_dismiss(self, popup: MediaPopup):
        popup.player.state = "stop"
        if popup.player._video:
            popup.player._video.unload()

    def set_preview_image(self, image):
        self.preview_image = image

    def set_trailer_url(self, trailer_url):
        self.trailer_url = trailer_url
        self.has_trailer_color = self.theme_cls.primaryColor

    def open(self, *_):
        popup = MediaPopup(self)
        popup.title = self.title
        popup.bind(on_dismiss=self.on_dismiss, on_open=self.on_popup_open)
        popup.open(self)

    # ---------------respond to user actions and call appropriate model-------------------------
    def on_is_in_my_list(self, instance, in_user_anime_list):
        if self.screen:
            if in_user_anime_list:
                self.screen.app.add_anime_to_user_anime_list(self.anime_id)
            else:
                self.screen.app.remove_anime_from_user_anime_list(self.anime_id)

    def on_trailer_url(self, *args):
        pass


class MediaCardsContainer(MDBoxLayout):
    container = ObjectProperty()
    list_name = StringProperty()