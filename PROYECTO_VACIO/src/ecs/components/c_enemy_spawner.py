from src.utils.config_loader import LevelEventState


class CEnemySpawner:
    def __init__(self, spawn_events: list[LevelEventState]) -> None:
        self.spawn_events = spawn_events