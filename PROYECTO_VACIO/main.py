#!/usr/bin/python3
"""Función Main"""

from src.engine.game_engine import GameEngine
from src.utils.config_loader import init_configurations

if __name__ == "__main__":
    init_configurations()
    engine = GameEngine()
    engine.run()
