import pygame

class MipMapping:
    def __init__(self,
                 max_level = 0,
                 start_level = 0):
        self.max_level = max_level

        self.current_level = start_level
        self.current_buffer_image = None
        self.buffer_images: pygame.Surface = []