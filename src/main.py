import pygame

from GameState_Example import GameState_Example

import game_file
import singletons
import singletons.ICamera
import singletons.IMap
import singletons.IMouse
import singletons.IStateMachine
import singletons.IIsometricTransform
import singletons.IKeyboard as IKeyboard
import singletons.test_instances

screen: pygame.Surface = None

def initialize_singletons():
    singletons.IStateMachine.instance = singletons.IStateMachine.IStateMachine()
    singletons.IMap.instance = singletons.IMap.IMap(game_file.load("../res/map.yaml")["map"], 10)
    singletons.ICamera.instance = singletons.ICamera.ICamera(screen.get_width()/2,(screen.get_height()/2)+singletons.IMap.instance.height*singletons.IMap.instance.tile_size/2)
    singletons.IIsometricTransform.instance = singletons.IIsometricTransform.IIsometricTransform(screen)
    singletons.ICameraDragController.instance = singletons.ICameraDragController.ICameraDragController()
    singletons.IMouse.instance = singletons.IMouse.IMouse()

    singletons.ICamera.instance.transform = singletons.IIsometricTransform.instance
    singletons.ICamera.instance.map = singletons.IMap.instance

    singletons.test_instances.run()

def main():
    running_value = True

    # pygame setup
    pygame.init()
    global screen
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    
    initialize_singletons()

    mouse = singletons.IMouse.instance
    cam = singletons.ICamera.instance
    state_machine = singletons.IStateMachine.instance

    #mouse.add_callbacks_to_listener(cam.update_mousewheel_zoom)
    state_machine.currentState = GameState_Example(screen)
    mouse.mouse_callback_list = state_machine.currentState.mouse_callback_list

    while running_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_value = False

            IKeyboard.update_keystates(event)
            singletons.IMouse.instance.update_based_on_event(event)

        state_machine.currentState.state_update()
        state_machine.currentState.state_render()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()