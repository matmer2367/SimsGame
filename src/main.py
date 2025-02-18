import pygame

from GameState_Example import GameState_Example

import Utils.file_load as file_load
import game_data

screen: pygame.Surface = None

def initialize_singletons():
    game_data.SStateMachine.instance = game_data.SStateMachine.SStateMachine()
    game_data.SMap.instance = game_data.SMap.SMap(file_load.load("../res/map.yaml")["map"], 10)
    game_data.SCamera.instance = game_data.SCamera.SCamera(screen.get_width()/2,(screen.get_height()/2)+game_data.SMap.instance.height*game_data.SMap.instance.tile_size/2)
    game_data.SIsometricTransform.instance = game_data.SIsometricTransform.SIsometricTransform(screen)
    game_data.SCameraDragController.instance = game_data.SCameraDragController.SCameraDragController()
    game_data.SMouse.instance = game_data.SMouse.SMouse()
    game_data.SIsometricMapRenderer.instance = game_data.SIsometricMapRenderer.SIsometricMapRenderer()

    game_data.SCamera.instance.transform = game_data.SIsometricTransform.instance
    game_data.SCamera.instance.map = game_data.SMap.instance
    game_data.SCamera.instance.isometricMapRenderer = game_data.SIsometricMapRenderer.instance

    game_data.SCameraDragController.instance.mouse = game_data.SMouse.instance

    game_data.test_instances.run()

def main():
    running_value = True

    # pygame setup
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    
    initialize_singletons()

    mouse = game_data.SMouse.instance
    state_machine = game_data.SStateMachine.instance

    #mouse.add_callbacks_to_listener(cam.update_mousewheel_zoom)
    state_machine.currentState = GameState_Example(screen)
    mouse.mouse_callback_list = state_machine.currentState.mouse_callback_list
    while running_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_value = False

            game_data.SKeyboard.update_keystates(event)
            mouse.update_based_on_event(event)

        state_machine.currentState.update()
        state_machine.currentState.render(screen)

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()