import pygame
import keyboard

from GameState import GameState

import game_file
import singletons
import singletons.ICamera
import singletons.IMap
import singletons.IMouse
import singletons.ITransform
import singletons.test_instances

def main():
    running_value = True

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE, vsync=1)
    clock = pygame.time.Clock()
    
    singletons.IMap.instance = singletons.IMap.IMap(game_file.load("../res/map.yaml")["map"], 10)
    singletons.ICamera.instance = singletons.ICamera.ICamera(screen.get_width()/2,(screen.get_height()/2)+singletons.IMap.instance.height*singletons.IMap.instance.tile_size/2)
    singletons.ITransform.instance = singletons.ITransform.ITransform(screen)
    singletons.ICameraDragController.instance = singletons.ICameraDragController.ICameraDragController()
    singletons.IMouse.instance = singletons.IMouse.IMouse()

    singletons.ICamera.instance.transform = singletons.ITransform.instance
    singletons.ICamera.instance.map = singletons.IMap.instance

    singletons.test_instances.run()

    game_state = GameState(screen)

    while running_value:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_value = False

            keyboard.update_keystates(event)
            game_state.check_events(event)

        game_state.update()
        game_state.render()

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()