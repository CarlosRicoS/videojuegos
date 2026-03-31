import json
import random
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, cast

CONFIG_FILE_PATH = Path(__file__).parent.parent.parent / "assets" / "cfg"
CONFIG_FILES = (
    "window", 
    "enemies",
    "level_01")
_CONFIG_STATE: Mapping[str, Any] | None = None

LevelEventKey = tuple[float, str, tuple[int, int]]
LevelEventState = dict[LevelEventKey, bool]


def _freeze(value: Any) -> Any:
    """Recursively convert structures into immutable equivalents."""
    if isinstance(value, dict):
        frozen_dict = {k: _freeze(v) for k, v in value.items()}
        return MappingProxyType(frozen_dict)
    if isinstance(value, list):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, tuple):
        return tuple(_freeze(item) for item in value)
    return value


def read_config_file(file_name: str) -> dict[str, Any]:
    try:
        with (CONFIG_FILE_PATH / f"{file_name}.json").open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise RuntimeError(f"Config file not found: {file_name}.json")
    except json.JSONDecodeError:
        raise RuntimeError(f"Invalid JSON in config file: {file_name}.json")


def init_configurations() -> None:
    global _CONFIG_STATE
    if _CONFIG_STATE is not None:
        return

    configs: dict[str, Any] = {}
    for config_file in CONFIG_FILES:
        configs[config_file] = read_config_file(config_file)

    _CONFIG_STATE = cast(Mapping[str, Any], _freeze(configs))


def get_configurations() -> Mapping[str, Any]:
    if _CONFIG_STATE is None:
        raise RuntimeError(
            "Configurations not initialized. Call init_configurations() from main.py first."
        )
    return _CONFIG_STATE


def load_configurations() -> Mapping[str, Any]:
    """Backward-compatible accessor that initializes on first call."""
    init_configurations()
    return get_configurations()


def get_window_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["window"])


def get_window_title() -> str:
    return str(get_window_config()["title"])


def get_window_size() -> tuple[int, int]:
    size = cast(Mapping[str, Any], get_window_config()["size"])
    return int(size["w"]), int(size["h"])


def get_framerate() -> int:
    return int(get_window_config()["framerate"])


def get_bg_color() -> tuple[int, int, int]:
    bg_color = cast(Mapping[str, Any], get_window_config()["bg_color"])
    return int(bg_color["r"]), int(bg_color["g"]), int(bg_color["b"])


def get_enemies_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["enemies"])


def get_enemy_list() -> list[Mapping[str, Any]]:
    enemies_config = get_enemies_config()
    return [
        cast(Mapping[str, Any], MappingProxyType({enemy_type: enemy_config}))
        for enemy_type, enemy_config in enemies_config.items()
    ]


def get_enemy_by_name(enemy_name: str) -> Mapping[str, Any]:
    for enemy_mapping in get_enemy_list():
        if get_enemy_name(enemy_mapping) == enemy_name:
            return enemy_mapping
    raise KeyError(f"Enemy not found: {enemy_name}")


def _get_enemy_entry(enemy_mapping: Mapping[str, Any]) -> tuple[str, Mapping[str, Any]]:
    if len(enemy_mapping) != 1:
        raise ValueError("Enemy mapping must contain exactly one enemy entry.")

    enemy_name = next(iter(enemy_mapping))
    enemy_data = cast(Mapping[str, Any], enemy_mapping[enemy_name])
    return enemy_name, enemy_data


def get_enemy_name(enemy_mapping: Mapping[str, Any]) -> str:
    enemy_name, _ = _get_enemy_entry(enemy_mapping)
    return enemy_name


def get_enemy_config(enemy_mapping: Mapping[str, Any]) -> Mapping[str, Any]:
    _, enemy_data = _get_enemy_entry(enemy_mapping)
    return enemy_data


def get_enemy_size(enemy_mapping: Mapping[str, Any]) -> tuple[int, int]:
    enemy_data = get_enemy_config(enemy_mapping)
    size = cast(Mapping[str, Any], enemy_data["size"])
    return int(size["x"]), int(size["y"])


def get_enemy_color(enemy_mapping: Mapping[str, Any]) -> tuple[int, int, int]:
    enemy_data = get_enemy_config(enemy_mapping)
    color = cast(Mapping[str, Any], enemy_data["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])


def get_enemy_velocity_min(enemy_mapping: Mapping[str, Any]) -> int:
    enemy_data = get_enemy_config(enemy_mapping)
    return int(enemy_data["velocity_min"])


def get_enemy_velocity_max(enemy_mapping: Mapping[str, Any]) -> int:
    enemy_data = get_enemy_config(enemy_mapping)
    return int(enemy_data["velocity_max"])


def get_enemy_velocity_range(enemy_mapping: Mapping[str, Any]) -> tuple[int, int]:
    velocity_min = get_enemy_velocity_min(enemy_mapping)
    velocity_max = get_enemy_velocity_max(enemy_mapping)
    speed_min = min(abs(velocity_min), abs(velocity_max))
    speed_max = max(abs(velocity_min), abs(velocity_max))

    vel_x = random.randint(speed_min, speed_max) * random.choice((-1, 1))
    vel_y = random.randint(speed_min, speed_max) * random.choice((-1, 1))
    return (
        vel_x,
        vel_y,
    )


def get_level_01_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["level_01"])


def get_level_01_events() -> list[LevelEventState]:
    level_config = get_level_01_config()
    events = cast(tuple[Any, ...], level_config["enemy_spawn_events"])

    parsed_events: list[LevelEventState] = []
    for event in events:
        event_mapping = cast(Mapping[str, Any], event)
        position = cast(Mapping[str, Any], event_mapping["position"])
        event_tuple = (
            float(event_mapping["time"]),
            str(event_mapping["enemy_type"]),
            (int(position["x"]), int(position["y"])),
        )
        parsed_events.append({event_tuple: False})

    parsed_events.sort(key=lambda event_state: next(iter(event_state))[0])
    return parsed_events


def _get_level_event_entry(
    event_mapping: Mapping[LevelEventKey, bool],
) -> tuple[LevelEventKey, bool]:
    if len(event_mapping) != 1:
        raise ValueError("Event mapping must contain exactly one event entry.")

    event = next(iter(event_mapping))
    return event, bool(event_mapping[event])


def get_event_time(event_mapping: Mapping[LevelEventKey, bool]) -> float:
    event, _ = _get_level_event_entry(event_mapping)
    return float(event[0])


def get_event_enemy_type(event_mapping: Mapping[LevelEventKey, bool]) -> str:
    event, _ = _get_level_event_entry(event_mapping)
    return str(event[1])


def get_event_position(event_mapping: Mapping[LevelEventKey, bool]) -> tuple[int, int]:
    event, _ = _get_level_event_entry(event_mapping)
    position = event[2]
    return int(position[0]), int(position[1])


def set_event_triggered(event_mapping: Mapping[LevelEventKey, bool]) -> None:
    event, _ = _get_level_event_entry(event_mapping)
    event_mapping[event] = True
