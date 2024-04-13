class CMetadata:
    def __init__(self, name: str, spawn_time: int):
        self.name = name
        self.spawn_time = spawn_time
        self._is_spawned = False

    @property
    def is_spawned(self) -> bool:
        return self._is_spawned

    @is_spawned.setter
    def is_spawned(self, value: bool):
        self._is_spawned = value
