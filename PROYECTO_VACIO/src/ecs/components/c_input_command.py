from enum import Enum


class CInputCommand:
    def __init__(self, name: str, key: int) -> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NA,
        self.trigger_position = None
        

class CommandPhase(Enum):
    NA = 0
    START = 1
    END = 2