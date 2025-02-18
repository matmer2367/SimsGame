import pygame
import game_data

from typing import List

class SIsometricMapRenderer:
    def __init__(self):
        self.cam = game_data.SCamera.instance
        self.map = game_data.SMap.instance
        self.transform = game_data.SIsometricTransform.instance

        self.tileSize = self.map.tile_size

        self.current_mip_map_level = 0
        self.current_mip_map_image = None

        self.map_draw_x = 0
        self.map_draw_y = 0
        self.map_draw_w = 0
        self.map_draw_h = 0

        self.MIP_MAP_LEVELS = 5
        self.map_buffer_images: List[pygame.Surface] = []

        self.isometric_textures_sprites = []
        self.grass_terrain = self.load_isometric_tile_texture("../res/sprites/terrain_sheet.png", 6, 3, 0, 0)

    def set_current_mip_map_image(self, level: int):
        if level >= self.MIP_MAP_LEVELS:
            return
        self.current_mip_map_level = level
        self.current_mip_map_image = self.map_buffer_images[level]
        self.map_draw_w = self.current_mip_map_image.get_width()
        self.map_draw_h = self.current_mip_map_image.get_height()

    def get_tile_image_from_map_coordinate(self, x, y):
        return self.isometric_textures_sprites[self.grass_terrain]

    def load_isometric_tile_texture(self, path, sheet_rows, sheet_cols, sheet_x_selector, sheet_y_selector) -> int:
        texture_sheet = pygame.image.load(path)
        texture = pygame.Surface((texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
        texture.blit(texture_sheet, (0,0), (sheet_x_selector*texture_sheet.get_width()/sheet_cols,sheet_y_selector*texture_sheet.get_height()/sheet_rows,texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
        texture.set_colorkey((0,0,0))
        self.isometric_textures_sprites.append(texture)
        return len(self.isometric_textures_sprites)-1

    def render_image_buffer_map(self):
        self.map_buffer_images.clear()

        for i in range(1, self.MIP_MAP_LEVELS+1):
            map_height = self.map.height
            map_width = self.map.width
            tileSize = self.map.tile_size*i

            map_draw_w = tileSize*map_width*2
            map_draw_h = tileSize*map_height

            newImage = pygame.Surface((map_draw_w, map_draw_h), pygame.SRCALPHA)
            newImage.fill((0,0,0,0))

            for xp in range(map_width):
                for yp in range(map_height):
                    dx, dy = game_data.SIsometricTransform.isometricTransform((xp*tileSize, yp*tileSize))
                    dx += tileSize*map_width
                    image = self.get_tile_image_from_map_coordinate(xp, yp)
                    scaled_image = pygame.transform.scale(image,(tileSize*2,tileSize))
                    newImage.blit(scaled_image, (dx-tileSize, dy))

            self.map_buffer_images.append(newImage)
        
        self.set_current_mip_map_image(0)

    def render_map(self, screen):
        cam_s = self.cam.s
        map_height = self.map.height
        map_width = self.map.width
        tileSize = self.map.tile_size

        p1 = self.transform.get_transformed_isometric_screen_position(0, self.map.height*self.tileSize)
        p2 = self.transform.get_transformed_isometric_screen_position(0, 0) 

        map_draw_x = p1[0]
        map_draw_y = p2[1]

        scaled_image = pygame.transform.scale(self.current_mip_map_image,(tileSize*map_width*2*cam_s,tileSize*map_height*cam_s))
        screen.blit(scaled_image, (map_draw_x, map_draw_y))

instance: SIsometricMapRenderer = None