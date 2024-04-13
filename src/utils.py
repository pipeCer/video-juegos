import json

FILE_PATH_MAP = {
    "window": "./assets/cfg/window.json",
    "level": "./assets/cfg/level_01.json",
    "enemies": "./assets/cfg/enemies.json",
    "player": "./assets/cfg/player.json",
    "bullet": "./assets/cfg/bullet.json",
}


class JSONObject(object):
    def __init__(self, d):
        self.__dict__ = d
        for key, value in self.__dict__.items():
            if isinstance(value, dict):
                self.__dict__[key] = JSONObject(value)


def read_json(config_name):
    file_path = FILE_PATH_MAP[config_name]
    with open(file_path, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            return [JSONObject(item) for item in data]
        return JSONObject(data)


def validate_position(x, y, bounds_size, offset):
    x = x if x > 0 else 0
    y = y if y > 0 else 0
    x = x if x < bounds_size[0] - offset[0] else bounds_size[0] - offset[0]
    y = y if y < bounds_size[1] - offset[1] else bounds_size[1] - offset[1]
    return x, y
