import json
import os
from configparser import ConfigParser

from .. import USER_CONFIG_PATH, USER_DOWNLOADS_DIR, USER_WATCH_HISTORY


class Config(object):
    def __init__(self) -> None:
        self.configparser = ConfigParser(
            {
                "server": "",
                "continue_from_history": "False",
                "quality": "0",
                "auto_next": "True",
                "sort_by": "search match",
                "downloads_dir": USER_DOWNLOADS_DIR,
                "translation_type": "sub",
                "preferred_language": "romaji",
            }
        )
        self.configparser.add_section("stream")
        self.configparser.add_section("general")
        self.configparser.add_section("anilist")
        if not os.path.exists(USER_CONFIG_PATH):
            with open(USER_CONFIG_PATH, "w") as config:
                self.configparser.write(config)
        self.configparser.read(USER_CONFIG_PATH)

        # --- set defaults ---
        self.downloads_dir = self.get_downloads_dir()
        self.translation_type = self.get_translation_type()
        self.sort_by = self.get_sort_by()
        self.continue_from_history = self.get_continue_from_history()
        self.auto_next = self.get_auto_next()
        self.quality = self.get_quality()
        self.server = self.get_server()
        self.preferred_language = self.get_preferred_language()

        # ---- setup history ------
        if not os.path.exists(USER_WATCH_HISTORY):
            self.watch_history = {}
        else:
            with open(USER_WATCH_HISTORY, "r") as history:
                self.watch_history = json.load(history)

    def update_watch_history(self, title, episode):
        with open(USER_WATCH_HISTORY, "w") as history:
            self.watch_history[title] = episode
            json.dump(self.watch_history, history)

    def get_downloads_dir(self):
        return self.configparser.get("general", "downloads_dir")

    def get_preferred_language(self):
        return self.configparser.get("general", "preferred_language")

    def get_sort_by(self):
        return self.configparser.get("anilist", "sort_by")

    def get_continue_from_history(self):
        return self.configparser.getboolean("stream", "continue_from_history")

    def get_translation_type(self):
        return self.configparser.get("stream", "translation_type")

    def get_auto_next(self):
        return self.configparser.getboolean("stream", "auto_next")

    def get_quality(self):
        return self.configparser.getint("stream", "quality")

    def get_server(self):
        return self.configparser.get("stream", "server")

    def update_config(self, section: str, key: str, value: str):
        self.configparser.set(section, key, value)
        with open(USER_CONFIG_PATH, "w") as config:
            self.configparser.write(config)

    def __repr__(self):
        return f"Config(server:{self.get_server()},quality:{self.get_quality()},auto_next:{self.get_auto_next()},continue_from_history:{self.get_continue_from_history()},sort_by:{self.get_sort_by()},downloads_dir:{self.get_downloads_dir()})"

    def __str__(self):
        return self.__repr__()
