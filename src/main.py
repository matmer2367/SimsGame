import pygame

from GameState_Example import GameState_Example

import game_file
import singletons
import singletons.SCamera
import singletons.SMap
import singletons.SMouse
import singletons.SStateMachine
import singletons.SIsometricTransform
import singletons.SKeyboard as SKeyboard
import singletons.test_instances

screen: pygame.Surface = None

def initialize_singletons():
    singletons.SStateMachine.instance = singletons.SStateMachine.SStateMachine()
    singletons.SMap.instance = singletons.SMap.SMap(game_file.load("../res/map.yaml")["map"], 10)
    singletons.SCamera.instance = singletons.SCamera.SCamera(screen.get_width()/2,(screen.get_height()/2)+singletons.SMap.instance.height*singletons.SMap.instance.tile_size/2)
    singletons.SIsometricTransform.instance = singletons.SIsometricTransform.SIsometricTransform(screen)
    singletons.SCameraDragController.instance = singletons.SCameraDragController.SCameraDragController()
    singletons.SMouse.instance = singletons.SMouse.SMouse()

    singletons.SCamera.instance.transform = singletons.SIsometricTransform.instance
    singletons.SCamera.instance.map = singletons.SMap.instance

    singletons.test_instances.run()

def main():
    running_value = True

    # pygame setup
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    
    initialize_singletons()

    mouse = singletons.SMouse.instance
    state_machine = singletons.SStateMachine.instance

    #mouse.add_callbacks_to_listener(cam.update_mousewheel_zoom)
    state_machine.currentState = GameState_Example(screen)
    mouse.mouse_callback_list = state_machine.currentState.mouse_callback_list

    while running_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_value = False

            SKeyboard.update_keystates(event)
            singletons.SMouse.instance.update_based_on_event(event)

        state_machine.currentState.state_update()
        state_machine.currentState.state_render()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()