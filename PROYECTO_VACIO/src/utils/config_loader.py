import json
import random
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping, cast

CONFIG_FILE_PATH = Path(__file__).parent.parent.parent / "assets" / "cfg"
CONFIG_FILES = (
    "window", 
    "enemies",
    "level_01",
    "player",
    "bullet",
    "explosion", 
    "interface",
    "special_bullet"
)
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

def get_enemy_texture(enemy_name: str) -> str:
    enemy_mapping = get_enemy_by_name(enemy_name)
    _, enemy_data = _get_enemy_entry(enemy_mapping)
    return str(enemy_data["image"])

def get_enemy_sound(enemy_name: str) -> str:
    enemy_mapping = get_enemy_by_name(enemy_name)
    _, enemy_data = _get_enemy_entry(enemy_mapping)
    return str(enemy_data["sound"])

def _get_enemy_entry(enemy_mapping: Mapping[str, Any]) -> tuple[str, Mapping[str, Any]]:
    if len(enemy_mapping) != 1:
        raise ValueError("Enemy mapping must contain exactly one enemy entry.")

    enemy_name = next(iter(enemy_mapping))
    enemy_data = cast(Mapping[str, Any], enemy_mapping[enemy_name])
    return enemy_name, enemy_data

def get_hunter_config() -> Mapping[str, Any]:
    return get_enemy_by_name("Hunter")

def get_hunter_texture() -> str:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    return str(hunter_data["image"])

def get_hunter_chase_sound() -> str:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    return str(hunter_data["sound_chase"])

def get_hunter_velocity_chase() -> int:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    return int(hunter_data["velocity_chase"])

def get_hunter_velocity_return() -> int:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    return int(hunter_data["velocity_return"])

def get_hunter_chase_distance() -> int:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    return int(hunter_data["distance_start_chase"])

def get_hunter_return_distance() -> int:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    return int(hunter_data["distance_start_return"])

def get_hunter_number_frames() -> int:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    animations = cast(Mapping[str, Any], hunter_data["animations"])
    return int(animations["number_frames"])

def get_hunter_animations() -> dict:
    hunter_mapping = get_hunter_config()
    _, hunter_data = _get_enemy_entry(hunter_mapping)
    animations = cast(Mapping[str, Any], hunter_data["animations"])
    return dict(animations)

def get_enemy_name(enemy_mapping: Mapping[str, Any]) -> str:
    enemy_name, _ = _get_enemy_entry(enemy_mapping)
    return enemy_name


def get_enemy_config(enemy_mapping: Mapping[str, Any]) -> Mapping[str, Any]:
    _, enemy_data = _get_enemy_entry(enemy_mapping)
    return enemy_data

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

def is_smart_enemy(enemy_type: str) -> bool:
    return enemy_type == "Hunter"

def get_event_position(event_mapping: Mapping[LevelEventKey, bool]) -> tuple[int, int]:
    event, _ = _get_level_event_entry(event_mapping)
    position = event[2]
    return int(position[0]), int(position[1])


def set_event_triggered(event_mapping: Mapping[LevelEventKey, bool]) -> None:
    event, _ = _get_level_event_entry(event_mapping)
    event_mapping[event] = True
    
def get_explosion_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["explosion"])
    
def get_explosion_texture() -> str:
    explosion_config = get_explosion_config()
    explosion_texture = cast(Mapping[str, Any], explosion_config["image"])
    return str(explosion_texture)

def get_explosion_frames_count() -> int:
    explosion_config = get_explosion_config()
    explosion_texture = cast(Mapping[str, Any], explosion_config["animations"])
    return int(explosion_texture["number_frames"])

def get_explosion_animation() -> dict:
    explosion_config = get_explosion_config()
    explosion_animation = cast(Mapping[str, Any], explosion_config["animations"])
    return dict(explosion_animation)

def get_explosion_sound() -> str:
    explosion_config = get_explosion_config()
    explosion_sound = cast(Mapping[str, Any], explosion_config["sound"])
    return str(explosion_sound)

def get_player_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["player"])

def get_player_texture() -> str:
    player_config = get_player_config()
    texture = cast(Mapping[str, Any], player_config["image"])
    return str(texture)

def get_player_lifes() -> int:
    player_config = get_player_config()
    return int(player_config["lifes"])

def get_player_sound() -> str:
    player_config = get_player_config()
    sound = cast(Mapping[str, Any], player_config["sound"])
    return str(sound)

def get_player_win_sound() -> str:
    player_config = get_player_config()
    sound = cast(Mapping[str, Any], player_config["win_sound"])
    return str(sound)

def get_player_lose_sound() -> str:
    player_config = get_player_config()
    sound = cast(Mapping[str, Any], player_config["lose_sound"])
    return str(sound)

def get_player_animations() -> dict:
    player_config = get_player_config()
    animations = cast(Mapping[str, Any], player_config["animation"])
    return dict(animations)

def get_animation_index_by_name(animation_name: str, animations: dict) -> int:
    for index, animation in enumerate(animations):
        if animation.name == animation_name:
            return index
    raise ValueError(f"Animation '{animation_name}' not found")

def get_player_frames_count() -> int:
    animations = get_player_animations()
    return int(animations["number_frames"])

def get_player_velocity() -> int:
    player_config = get_player_config()
    return int(player_config["input_velocity"])

def get_player_spawn_position_config() -> tuple[int, int]:
    player_spawn_config = get_level_01_config()["player_spawn"]
    
    spawn = cast(Mapping[str, Any], player_spawn_config["position"])
    return int(spawn["x"]), int(spawn["y"])    

def get_level_bullet_limit() -> int:
    level_config = get_level_01_config()["player_spawn"]
    return int(level_config["max_bullets"])

def get_level_mine_limit() -> int:
    level_config = get_level_01_config()["player_spawn"]
    return int(level_config["max_mines"])

def get_bullet_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["bullet"])

def get_bullet_texture() -> str:
    bullet_config = get_bullet_config()
    texture = cast(Mapping[str, Any], bullet_config["image"])
    return str(texture)

def get_bullet_sound() -> str:
    bullet_config = get_bullet_config()
    sound = cast(Mapping[str, Any], bullet_config["sound"])
    return str(sound)

def get_bullet_velocity() -> int:
    bullet_config = get_bullet_config()
    return int(bullet_config["velocity"])

def get_interface_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["interface"])

def get_interface_font() -> str:
    interface_config = get_interface_config()
    font = cast(Mapping[str, Any], interface_config["font"])
    return str(font)

def get_interface_title_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    title_config = cast(Mapping[str, Any], interface_config["title"])
    return title_config

def get_interface_title_text() -> str:
    title_config = get_interface_title_config()
    return str(title_config["text"])

def get_interface_title_color() -> tuple[int, int, int]:
    title_config = get_interface_title_config()
    color = cast(Mapping[str, Any], title_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_title_size() -> int:
    title_config = get_interface_title_config()
    return int(title_config["size"])

def get_interface_instructions_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    instructions_config = cast(Mapping[str, Any], interface_config["instructions"])
    return instructions_config

def get_interface_instructions_text() -> str:
    instructions_config = get_interface_instructions_config()
    return str(instructions_config["text"])

def get_interface_instructions_color() -> tuple[int, int, int]:
    instructions_config = get_interface_instructions_config()
    color = cast(Mapping[str, Any], instructions_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_instructions_size() -> int:
    instructions_config = get_interface_instructions_config()
    return int(instructions_config["size"])

def get_interface_special_powers_label_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    label_config = cast(Mapping[str, Any], interface_config["special_powers_label"])
    return label_config

def get_interface_special_powers_label_text() -> str:
    label_config = get_interface_special_powers_label_config()
    return str(label_config["text"])

def get_interface_special_powers_label_color() -> tuple[int, int, int]:
    label_config = get_interface_special_powers_label_config()
    color = cast(Mapping[str, Any], label_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_special_powers_label_size() -> int:
    label_config = get_interface_special_powers_label_config()
    return int(label_config["size"])

def get_interface_load_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    load_config = cast(Mapping[str, Any], interface_config["load"])
    return load_config

def get_interface_load_text() -> str:
    load_config = get_interface_load_config()
    return str(load_config["text"])

def get_interface_load_color() -> tuple[int, int, int]:
    load_config = get_interface_load_config()
    color = cast(Mapping[str, Any], load_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_load_size() -> int:
    load_config = get_interface_load_config()
    return int(load_config["size"])

def get_interface_end_game_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    end_game_config = cast(Mapping[str, Any], interface_config["end_game"])
    return end_game_config

def get_interface_win_text() -> str:
    end_game_config = get_interface_end_game_config()
    return str(end_game_config["win"])

def get_interface_lose_text() -> str:
    end_game_config = get_interface_end_game_config()
    return str(end_game_config["lose"])

def get_interface_end_game_color() -> tuple[int, int, int]:
    end_game_config = get_interface_end_game_config()
    color = cast(Mapping[str, Any], end_game_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_end_game_size() -> int:
    end_game_config = get_interface_end_game_config()
    return int(end_game_config["size"])

def get_interface_pause_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    pause_config = cast(Mapping[str, Any], interface_config["pause"])
    return pause_config

def get_interface_pause_text() -> str:
    pause_config = get_interface_pause_config()
    return str(pause_config["text"])

def get_interface_pause_color() -> tuple[int, int, int]:
    pause_config = get_interface_pause_config()
    color = cast(Mapping[str, Any], pause_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_pause_size() -> int:
    pause_config = get_interface_pause_config()
    return int(pause_config["size"])

def get_interface_player_lifes_config() -> Mapping[str, Any]:
    interface_config = get_interface_config()
    lifes_config = cast(Mapping[str, Any], interface_config["player_lifes"])
    return lifes_config

def get_interface_player_lifes_text() -> str:
    lifes_config = get_interface_player_lifes_config()
    return str(lifes_config["text"])

def get_interface_player_lifes_color() -> tuple[int, int, int]:
    lifes_config = get_interface_player_lifes_config()
    color = cast(Mapping[str, Any], lifes_config["color"])
    return int(color["r"]), int(color["g"]), int(color["b"])

def get_interface_player_lifes_size() -> int:
    lifes_config = get_interface_player_lifes_config()
    return int(lifes_config["size"])

def get_special_bullet_config() -> Mapping[str, Any]:
    return cast(Mapping[str, Any], get_configurations()["special_bullet"])

def get_special_bullet_texture() -> str:
    special_bullet_config = get_special_bullet_config()
    texture = cast(Mapping[str, Any], special_bullet_config["image"])
    return str(texture)

def get_special_bullet_reload_time() -> float:
    special_bullet_config = get_special_bullet_config()
    return float(special_bullet_config["reload_time"])

def get_special_bullet_velocity() -> int:
    special_bullet_config = get_special_bullet_config()
    return int(special_bullet_config["velocity"])

def get_special_bullet_radius() -> int:
    special_bullet_config = get_special_bullet_config()
    return int(special_bullet_config["radius"])   

def get_special_bullet_sound() -> str:
    special_bullet_config = get_special_bullet_config()
    sound = cast(Mapping[str, Any], special_bullet_config["sound"])
    return str(sound) 