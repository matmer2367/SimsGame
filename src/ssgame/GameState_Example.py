from .AIsometricSceneState import AIsometricSceneState
from typing import Tuple, List

from .GameObject import Person, GameObject
import pygame
from .map_gameObject_query import Map_GameObject_Query
from . import *

from mouse_callback.MouseCallbackList import MouseCallbackList

class GameState_Example(AIsometricSceneState):
    def __init__(self, screen):
        super().__init__(screen)
    
    def create_mouse_callback_list(self) -> MouseCallbackList:
        cbl =  super().create_mouse_callback_list()
        cbl.add_callbacks_to_listener(mouse_pressed_right_out_callback=self.mouse_pressed_right_out_event)

        camera_drag_controller = dataset.SCameraDragController()
        cbl.add_IMouseClickButtons_callbacks(camera_drag_controller)
        cbl.add_IMouseMotion_callbacks(camera_drag_controller)

        return cbl

    def mouse_pressed_right_out_event(self, pos: Tuple[float, float]):
        x, y = pos
        tx, ty = self.transform.get_transformed_isometric_world_position(x, y)

        tileSize = self.map.tile_size
        map_width = self.map.width
        map_height = self.map.height

        if 0 <= tx <= map_width*tileSize and 0 <= ty <= map_height*tileSize:
            self.game_objects.append(self.create_dummy_debug_person((tx, ty)))
    
    # game object creation functions
    def create_dummy_debug_person(self, pos: Tuple[float, float]):
        x, y = pos
        tileSize = self.map.tile_size
        object_rect_width = tileSize * .6
        object_rect = pygame.Surface((object_rect_width, 2*tileSize-object_rect_width/2))
        object_rect.fill((255,0,0))
        return Person(x, y, object_rect, -object_rect_width/2, -2*tileSize+object_rect_width/2, debug_draw_mode=True, selectable_hover_display=True)
    
    def update_keyboard_control(self):
        if dataset.SKeyboard.keys[pygame.K_UP]:
            self.cam.y -= self.cam.keyboard_movement_speed/self.cam.s
        if dataset.SKeyboard.keys[pygame.K_DOWN]:
            self.cam.y += self.cam.keyboard_movement_speed/self.cam.s
        if dataset.SKeyboard.keys[pygame.K_RIGHT]:
            self.cam.x += self.cam.keyboard_movement_speed/self.cam.s
        if dataset.SKeyboard.keys[pygame.K_LEFT]:
            self.cam.x -= self.cam.keyboard_movement_speed/self.cam.s

    def tick(self):
        pass

    def draw_at_tile_coordinate(self, x, y):
        tileSize = self.tileSize
        if self.mouse_pos_in_world[0]//tileSize == x and self.mouse_pos_in_world[1]//tileSize == y:
            self.transform.drawTransformedIsometricRect((255,255,255), x*tileSize, y*tileSize, tileSize, tileSize)            

    def draw_game_objects(self, draw_query: List[GameObject]):
        mouse_hover_highlight_object_index = -1
        # object selection identification
        for i in range(len(draw_query)):
            o = draw_query[i]
            if o.isInObjectBounds(self.curr_mouse_position):
                mouse_hover_highlight_object_index = i

        # draw all game objects
        for i in range(len(draw_query)):
            o: GameObject = draw_query[i]
            o.drawGameObject()
            if mouse_hover_highlight_object_index == i and o.selectable_hover_display:
                dx, dy = o.get_transformed_isometric_screen_drawing_surface_start_coordinate()
                sw, sh = self.transform.cam_size_conversion_tuple(o.getBoundingSurfaceDimenstion())
                pygame.draw.rect(self.screen, (255,255,255), (dx, dy, sw, sh), width=2)
    
    def render(self, screen: pygame.Surface):
        super().render(screen)