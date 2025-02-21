import pygame

#keyboard setup
keys = {
    pygame.K_UP: False,
    pygame.K_DOWN: False,
    pygame.K_LEFT: False,
    pygame.K_RIGHT: False,
    pygame.K_PLUS: False,
    pygame.K_MINUS: False
}

def update_keystates(event: pygame.event):
    if event.type == pygame.KEYDOWN:
        for key in keys.keys():
            if event.key == key:
                keys[key] = True
    if event.type == pygame.KEYUP:
        for key in keys.keys():
            if event.key == key:
                keys[key] = False