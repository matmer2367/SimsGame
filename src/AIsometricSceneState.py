import pygame
import singletons.SIsometricTransform
import singletons.SMap as SMap
from typing import List, Tuple
from GameObject import GameObject, Person
from map_gameObject_query import Map_GameObject_Query
from Utils import fmath

import singletons.SCamera as SCamera
import singletons.SMouse
import singletons.SIsometricTransform as SIsometricTransform
import singletons.SIsometricMapRenderer as SIsometricMapRenderer

from singletons.SMouse import SMouse
import singletons

import singletons.SKeyboard as SKeyboard
from AState import AState

from mouse_callback.MouseCallbackList import MouseCallbackList

class AIsometricSceneState(AState):
    def __init__(self, screen):
        super().__init__(screen)
        self.map = SMap.instance
        self.tileSize = self.map.tile_size
        self.isometric_map_renderer = SIsometricMapRenderer.instance

        self.game_objects: List[GameObject] = []
        self.game_objects_map_query = Map_GameObject_Query(self.game_objects)

        self.isometric_map_renderer.render_image_buffer_map()

    def create_mouse_callback_list(self) -> MouseCallbackList:
        cbl =  super().create_mouse_callback_list()
        cbl.add_callbacks_to_listener(mousewheel_callback=self.cam.update_mousewheel_zoom)
        return cbl
    
    def draw_at_tile_coordinate(self, x, y):
        raise NotImplementedError(self.draw_at_tile_coordinate, self.__class__)

    def draw_game_objects(self, draw_query: Map_GameObject_Query):
        raise NotADirectoryError(self.draw_game_objects, self.__class__)

    def render(self, screen: pygame.Surface):
        
        self.game_objects_map_query.update()

        map_height = self.map.height
        map_width = self.map.width
        tileSize = self.map.tile_size

        screen.fill((10,5,10))

        self.isometric_map_renderer.render_map(screen)

        ulx = self.transform.get_transformed_isometric_world_position(0,0)[0]//self.tileSize
        ury = self.transform.get_transformed_isometric_world_position(screen.get_width(),0)[1]//self.tileSize
        drx = self.transform.get_transformed_isometric_world_position(screen.get_width(),screen.get_height())[0]//self.tileSize+1
        dly = self.transform.get_transformed_isometric_world_position(0,screen.get_height())[1]//self.tileSize+1

        xp_start = int(ulx if ulx >= 0 else 0)
        yp_start = int(ury if ury >= 0 else 0)

        xp_end = int(drx if drx <= map_width else map_width)
        yp_end = int(dly if dly <= map_height else map_height)

        for xp in range(xp_start, xp_end):
            for yp in range(yp_start, yp_end):
                if self.transform.isometric_rect_in_viewport(xp, yp, tileSize):
                    self.draw_at_tile_coordinate(xp, yp)
        
        game_objects_draw_query: List[GameObject] = self.game_objects_map_query.game_objects
        game_objects_draw_query.sort(key=lambda o: o.get_transformed_isometric_screen_pivot_coordinate()[1])
        self.draw_game_objects(game_objects_draw_query)