import pygame
import singletons.IMap as IMap
from typing import List, Tuple
from GameObject import GameObject, Person
from map_gameObject_query import Map_GameObject_Query
from Utils import fmath

import singletons.ICamera as ICamera
import singletons.ITransform as ITransform

from mouse import Mouse
import singletons

import keyboard

class GameState:
    def __init__(self, screen):
        self.screen: pygame.Surface = screen
        # map
        self.map = IMap.instance
        self.map_data = self.map.data
        self.map_height, self.map_width = self.map.height, self.map.width
        self.tileSize = self.map.tile_size

        self.game_objects: List[GameObject] = []
        self.game_objects_map_query = Map_GameObject_Query(self.game_objects)

        # transform
        self.cam = ICamera.instance
        self.transform = ITransform.instance
        #self.cam = Camera(screen.get_width()/2,(screen.get_height()/2)+self.map_height*self.tileSize/2)
        #self.transform = transform.create(screen, self.cam)

        self.mouse = Mouse(self.cam.update_mousewheel_zoom,
                           self.mouse_pressed_left_in_event,
                           self.mouse_pressed_left_out_event,
                           self.mouse_pressed_right_in_event,
                           self.mouse_pressed_right_out_event)
        
        self.mouse_pos_in_world: Tuple[float, float] = (0,0)

        # isometric textures list setup
        self.isometric_textures_sprites = []

        self.grass_terrain = self.load_isometric_tile_texture("../res/sprites/terrain_sheet.png", 6, 3, 0, 0)

        # mouse
        self.curr_mouse_position = pygame.mouse.get_pos()

    # mouse callback functions
    def mouse_pressed_left_in_event(self, pos: Tuple[float, float]):
        x, y = pos

    def mouse_pressed_left_out_event(self, pos: Tuple[float, float]):
        x, y = pos

    def mouse_pressed_right_in_event(self, pos: Tuple[float, float]):
        x, y = pos

    def mouse_pressed_right_out_event(self, pos: Tuple[float, float]):
        x, y = pos
        tx, ty = self.transform.get_transformed_isometric_world_position(x, y)
        if 0 <= tx <= self.map_width*self.tileSize and 0 <= ty <= self.map_height*self.tileSize:
            self.game_objects.append(self.create_dummy_debug_person((tx, ty)))

    # game object creation functions
    def create_dummy_debug_person(self, pos: Tuple[float, float]):
        x, y = pos
        object_rect_width = self.tileSize * .6
        object_rect = pygame.Surface((object_rect_width, 2*self.tileSize-object_rect_width/2))
        object_rect.fill((255,0,0))
        return Person(x, y, object_rect, -object_rect_width/2, -2*self.tileSize+object_rect_width/2, debug_draw_mode=True, selectable_hover_display=True)

    def load_isometric_tile_texture(self, path, sheet_rows, sheet_cols, sheet_x_selector, sheet_y_selector) -> int:
        texture_sheet = pygame.image.load(path)
        texture = pygame.Surface((texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
        texture.blit(texture_sheet, (0,0), (sheet_x_selector*texture_sheet.get_width()/sheet_cols,sheet_y_selector*texture_sheet.get_height()/sheet_rows,texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
        texture.set_colorkey((0,0,0))
        self.isometric_textures_sprites.append(texture)
        return len(self.isometric_textures_sprites)-1
    
    def check_events(self, event):
        self.mouse.update_based_on_event(event)

    def keyboard_control_update(self):
        if keyboard.keys[pygame.K_UP]:
            self.cam.y -= self.cam_keyboard_movement_speed/self.cam.s
        if keyboard.keys[pygame.K_DOWN]:
            self.cam.y += self.cam_keyboard_movement_speed/self.cam.s
        if keyboard.keys[pygame.K_RIGHT]:
            self.cam.x += self.cam_keyboard_movement_speed/self.cam.s
        if keyboard.keys[pygame.K_LEFT]:
            self.cam.x -= self.cam_keyboard_movement_speed/self.cam.s

    def update_camera(self):
        self.cam.update_physical_movement()
        self.cam.keep_camera_in_bounds(self.screen)

    def update_mouse_position(self):
        curr_mouse_position = self.mouse.curr_mouse_position
        self.mouse_pos_in_world = self.transform.get_transformed_isometric_world_position(curr_mouse_position[0],curr_mouse_position[1])

    def update(self):
        self.keyboard_control_update()
        self.update_camera()
        self.update_mouse_position()
    
    def render(self):
        self.game_objects_map_query.update()
        self.screen.fill((10,5,10))
        game_objects_draw_query: List[GameObject] = []

        # Map Draw
        yp_start = 0
        xp_start = 0
        xp = xp_start
        yp = yp_start
        yp_movement = True
        for i in range(self.map_width*self.map_height):
            if self.transform.isometric_rect_in_viewport((xp*self.tileSize, yp*self.tileSize, self.tileSize, self.tileSize)):
                # MAP TILE SELECTION PART ##########################################################################################################
                dx, dy = self.transform.get_transformed_isometric_screen_position(xp*self.tileSize, yp*self.tileSize)
                self.screen.blit(pygame.transform.scale(self.isometric_textures_sprites[self.grass_terrain],(self.tileSize*2*self.cam.s,self.tileSize*self.cam.s)), (dx-self.tileSize*self.cam.s, dy))
                
                if self.mouse_pos_in_world[0]//self.tileSize == xp and self.mouse_pos_in_world[1]//self.tileSize == yp:
                        self.transform.drawTransformedIsometricRect((255,255,255), xp*self.tileSize, yp*self.tileSize, self.tileSize, self.tileSize)
                
                for go in self.game_objects_map_query.get_object_list_at(xp, yp):
                    game_objects_draw_query.append(go)
            
            if yp >= self.map_height-1:
                yp_movement = False
            if yp_movement:
                if yp <= 0 or xp >= self.map_width-1:
                    yp_start += 1
                    yp = yp_start
                    xp = 0
                else:
                    xp += 1
                    yp -= 1
            else:
                if yp <= 0 or xp >= self.map_width-1:
                    xp_start += 1
                    xp = xp_start
                    yp = self.map_height-1
                else:
                    xp += 1
                    yp -= 1
        
        # game objects for drawing in chronological order
        game_objects_draw_query.sort(key=lambda o: o.get_transformed_isometric_screen_pivot_coordinate()[1])
        
        mouse_hover_highlight_object_index = -1
        # object selection identification
        for i in range(len(game_objects_draw_query)):
            o = game_objects_draw_query[i]
            if o.isInObjectBounds(self.curr_mouse_position):
                mouse_hover_highlight_object_index = i

        # draw all game objects
        for i in range(len(game_objects_draw_query)):
            o: GameObject = game_objects_draw_query[i]
            o.drawGameObject()
            if mouse_hover_highlight_object_index == i and o.selectable_hover_display:
                dx, dy = o.get_transformed_isometric_screen_drawing_surface_start_coordinate()
                sw, sh = self.transform.cam_size_conversion_tuple(o.getBoundingSurfaceDimenstion())
                pygame.draw.rect(self.screen, (255,255,255), (dx, dy, sw, sh), width=2)
