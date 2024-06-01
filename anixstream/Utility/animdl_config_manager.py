from typing import TypedDict
import plyer
import os

from .yaml_parser import YamlParser


class AnimdlConfig(TypedDict):
    default_player: str
    default_provider: str
    quality_string: str

 
if local_data_path:=os.getenv("LOCALAPPDATA"):
    config_dir = os.path.join(local_data_path,".config")
    if not os.path.exists(config_dir):
        os.mkdir(config_dir)
    animdl_config_folder_location = os.path.join(config_dir, "animdl")
else:
    user_profile_path = plyer.storagepath.get_home_dir()  # type: ignore
    animdl_config_folder_location = os.path.join(user_profile_path, ".animdl")
    if not os.path.exists(animdl_config_folder_location):
        os.mkdir(animdl_config_folder_location)

animdl_config_location = os.path.join(animdl_config_folder_location, "config.yml")
# print(animdl_config_location)
animdl_config = YamlParser(
    animdl_config_location,
    {"default_player": "mpv", "default_provider": "allanime", "quality_string": "best"},
    AnimdlConfig,
)


def update_animdl_config(field_to_update: str, value):
    current_data = animdl_config.data
    current_data[f"{field_to_update}"] = value
    animdl_config.write(current_data)


def get_animdl_config() -> AnimdlConfig:
    return animdl_config.data