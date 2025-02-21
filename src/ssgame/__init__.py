import pygame

from . import dataset
from .AIsometricSceneState import AIsometricSceneState
from .AState import AState
from .GameObject import GameObject
from .GameState_Example import GameState_Example
from .map_gameObject_query import Map_GameObject_Query

def init(map_data, tile_Size, screen: pygame.Surface):
    global dataset
    dataset.init(map_data, tile_Size, screen)