import pygame

from game_data.user_input.keyboard.key_states import KeyStates

def update_keystates(keys: KeyStates, event: pygame.event):
    if event.type == pygame.KEYDOWN:
        for key in keys.keys():
            if event.key == key:
                keys[key] = True
    if event.type == pygame.KEYUP:
        for key in keys.keys():
            if event.key == key:
                keys[key] = False