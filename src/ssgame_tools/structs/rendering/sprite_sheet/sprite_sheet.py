import pygame

from .meta_data import SpriteSheetMetaData

class SpriteSheet:
    def __init__(self,
                 path = "",
                 images_dict = {},
                 metadata: SpriteSheetMetaData = None):
        self.path = path
        self.images_dict = images_dict
        self.metadata = metadata