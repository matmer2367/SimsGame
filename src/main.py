import pygame

from Utils import file_load

import ssgame_deprecated

import ssgame_tools

def main_deprecated():
    running_value = True

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    
    ssgame_deprecated.init(file_load.load("../res/map.yaml")["map"], 10, screen)

    mouse = ssgame_deprecated.dataset.SMouseInstance
    state_machine = ssgame_deprecated.dataset.StateMachineInstance

    #mouse.add_callbacks_to_listener(cam.update_mousewheel_zoom)
    state_machine.currentState =ssgame_deprecated.GameState_Example(screen)
    mouse.mouse_callback_list = state_machine.currentState.mouse_callback_list
    while running_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_value = False

            ssgame_deprecated.dataset.SKeyboard.update_keystates(event)
            mouse.update_based_on_event(event)

        state_machine.currentState.update()
        state_machine.currentState.render(screen)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main_deprecated()