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

        self.game_objects: List[GameObject] = []
        self.game_objects_map_query = Map_GameObject_Query(self.game_objects)

        self.map_draw_x = 0
        self.map_draw_y = 0
        self.map_draw_w = 0
        self.map_draw_h = 0
        self.map_buffer_image: pygame.Surface = pygame.Surface((0,0))

    def load_sprites(self):
        raise NotImplementedError(self.load_sprites, self.__class__)

    def render_image_buffer_map(self):
        map_height = self.map.height
        map_width = self.map.width
        tileSize = self.map.tile_size

        self.map_draw_w = tileSize*map_width*2
        self.map_draw_h = tileSize*map_height

        self.map_buffer_image = pygame.Surface((self.map_draw_w, self.map_draw_h))

        for xp in range(map_width):
            for yp in range(map_height):
                dx, dy = singletons.SIsometricTransform.isometricTransform((xp*tileSize, yp*tileSize))
                dx += tileSize*map_width
                image = self.get_tile_image_from_map_coordinate(xp, yp)
                scaled_image = pygame.transform.scale(image,(tileSize*2,tileSize))
                self.map_buffer_image.blit(scaled_image, (dx-tileSize, dy))

    def create_mouse_callback_list(self) -> MouseCallbackList:
        cbl =  super().create_mouse_callback_list()
        cbl.add_callbacks_to_listener(mousewheel_callback=self.cam.update_mousewheel_zoom)
        return cbl

    def get_tile_image_from_map_coordinate(self, x, y):
        raise NotImplementedError(self.get_tile_image_from_map_coordinate, self.__class__)
    
    def draw_at_tile_coordinate(self, x, y):
        raise NotImplementedError(self.draw_at_tile_coordinate, self.__class__)

    def draw_game_objects(self, draw_query: Map_GameObject_Query):
        raise NotADirectoryError(self.draw_game_objects, self.__class__)

    def render(self, screen: pygame.Surface):
        
        self.game_objects_map_query.update()

        map_height = self.map.height
        map_width = self.map.width
        tileSize = self.map.tile_size

        cam_s = self.cam.s

        # Map Draw
        ulx = self.transform.get_transformed_isometric_world_position(0,0)[0]//self.tileSize
        ury = self.transform.get_transformed_isometric_world_position(screen.get_width(),0)[1]//self.tileSize
        drx = self.transform.get_transformed_isometric_world_position(screen.get_width(),screen.get_height())[0]//self.tileSize+1
        dly = self.transform.get_transformed_isometric_world_position(0,screen.get_height())[1]//self.tileSize+1

        xp_start = int(ulx if ulx >= 0 else 0)
        yp_start = int(ury if ury >= 0 else 0)

        xp_end = int(drx if drx <= map_width else map_width)
        yp_end = int(dly if dly <= map_height else map_height)

        screen.fill((10,5,10))

        p1 = self.transform.get_transformed_isometric_screen_position(0, self.map.height*self.tileSize)
        p2 = self.transform.get_transformed_isometric_screen_position(0, 0) 

        map_draw_x = p1[0]-self.tileSize
        map_draw_y = p2[1]

        scaled_image = pygame.transform.scale(self.map_buffer_image,(self.map_draw_w*cam_s,self.map_draw_h*cam_s))
        screen.blit(scaled_image, (map_draw_x, map_draw_y))

        #for xp in range(xp_start, xp_end):
        #    for yp in range(yp_start, yp_end):
        #        if self.transform.isometric_rect_in_viewport(xp, yp, tileSize):
        #            dx, dy = self.transform.get_transformed_isometric_screen_position(xp*tileSize, yp*tileSize)
        #            image = self.get_tile_image_from_map_coordinate(xp, yp)
        #            scaled_image = pygame.transform.scale(image,(tileSize*2*cam_s,tileSize*cam_s))
        #           self.screen.blit(scaled_image, (dx-tileSize*cam_s, dy))
        #           self.draw_at_tile_coordinate(xp, yp)

        game_objects_draw_query: List[GameObject] = []
        for xp in range(xp_start, xp_end):
            for yp in range(yp_start, yp_end):
                if self.transform.isometric_rect_in_viewport(xp, yp, tileSize):
                    for go in self.game_objects_map_query.get_object_list_at(xp, yp):
                        game_objects_draw_query.append(go)
                    game_objects_draw_query.sort(key=lambda o: o.get_transformed_isometric_screen_pivot_coordinate()[1])
                    self.draw_game_objects(game_objects_draw_query)
                    game_objects_draw_query.clear()