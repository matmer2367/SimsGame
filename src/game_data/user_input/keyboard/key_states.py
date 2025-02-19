import pygame

class KeyStates:
    def __init__(self):
        self.keys = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
            pygame.K_PLUS: False,
            pygame.K_MINUS: False
        }
