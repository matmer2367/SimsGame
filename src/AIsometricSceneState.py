import pygame
import singletons.IMap as IMap
from typing import List, Tuple
from GameObject import GameObject, Person
from map_gameObject_query import Map_GameObject_Query
from Utils import fmath

import singletons.ICamera as ICamera
import singletons.IMouse
import singletons.IIsometricTransform as IIsometricTransform

from singletons.IMouse import IMouse
import singletons

import singletons.IKeyboard as IKeyboard
from AState import AState

from MouseCallbackList import MouseCallbackList

class AIsometricSceneState(AState):
    def __init__(self, screen):
        super().__init__(screen)
        self.map = IMap.instance
        self.tileSize = self.map.tile_size

        self.game_objects: List[GameObject] = []
        self.game_objects_map_query = Map_GameObject_Query(self.game_objects)

    def create_mouse_callback_list(self) -> MouseCallbackList:
        cbl = MouseCallbackList()
        cbl.add_callbacks_to_listener(mousewheel_callback=self.cam.update_mousewheel_zoom)
        return cbl

    def get_tile_image_from_map_coordinate(self, x, y):
        raise NotImplementedError(self.get_tile_image_from_map_coordinate, self.__class__)
    
    def draw_at_tile_coordinate(self, x, y):
        raise NotImplementedError(self.draw_at_tile_coordinate, self.__class__)

    def draw_game_objects(self, draw_query: Map_GameObject_Query):
        raise NotADirectoryError(self.draw_game_objects, self.__class__)

    def concrete_render(self, screen: pygame.Surface):
        screen.fill((10,5,10))
        self.game_objects_map_query.update()
        game_objects_draw_query: List[GameObject] = []

        map_height = self.map.height
        map_width = self.map.width
        tileSize = self.map.tile_size

        cam_s = self.cam.s

        # Map Draw
        yp_start = 0
        xp_start = 0
        xp = xp_start
        yp = yp_start
        yp_movement = True
        for i in range(map_width*map_height):
            if self.transform.isometric_rect_in_viewport((xp*tileSize, yp*tileSize, tileSize, tileSize)):
                dx, dy = self.transform.get_transformed_isometric_screen_position(xp*tileSize, yp*tileSize)
                self.screen.blit(pygame.transform.scale(self.get_tile_image_from_map_coordinate(xp, yp),(tileSize*2*cam_s,tileSize*cam_s)), (dx-tileSize*cam_s, dy))
                
                for go in self.game_objects_map_query.get_object_list_at(xp, yp):
                    game_objects_draw_query.append(go)
                
                self.draw_at_tile_coordinate(xp, yp)

            if yp >= map_height-1:
                yp_movement = False
            if yp_movement:
                if yp <= 0 or xp >= map_width-1:
                    yp_start += 1
                    yp = yp_start
                    xp = 0
                else:
                    xp += 1
                    yp -= 1
            else:
                if yp <= 0 or xp >= map_width-1:
                    xp_start += 1
                    xp = xp_start
                    yp = map_height-1
                else:
                    xp += 1
                    yp -= 1
            
        # game objects for drawing in chronological order
        game_objects_draw_query.sort(key=lambda o: o.get_transformed_isometric_screen_pivot_coordinate()[1])
        self.draw_game_objects(game_objects_draw_query)
        

