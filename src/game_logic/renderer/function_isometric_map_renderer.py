import pygame

from game_data.game_context.world.map.map import Map
from game_data.rendering.sprite_sheet.sprite_sheet import SpriteSheet
from game_data.rendering.viewport.viewport_dimensions import ViewportDimensions
from game_logic.map.functions import get_tile_image_from_map_coordinate
from game_logic.math import isometric_transformations

from game_data.camera.transform import CameraTransform
from game_data.game_context.world.map.map_metadata import MapMetaData
from game_data.rendering.mip_mapping import MipMapping

def set_current_mip_map_image(mip_mapping: MipMapping, new_level: int):
    if new_level >= mip_mapping.max_level:
        return
    mip_mapping.current_level = new_level
    mip_mapping.current_buffer_image = mip_mapping.buffer_images[new_level]

def load_isometric_tile_texture(path, sheet_rows, sheet_cols, sheet_x_selector, sheet_y_selector) -> pygame.Surface:
    texture_sheet = pygame.image.load(path)
    texture = pygame.Surface((texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
    texture.blit(texture_sheet, (0,0), (sheet_x_selector*texture_sheet.get_width()/sheet_cols,sheet_y_selector*texture_sheet.get_height()/sheet_rows,texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
    texture.set_colorkey((0,0,0))
    return texture

def render_image_buffer_map(game_map: Map, mip_mapping: MipMapping, sprite_sheet: SpriteSheet):
    mip_mapping.buffer_images.clear()

    for i in range(1, mip_mapping.max_level+1):
        map_height = game_map.meta_data.height
        map_width = game_map.meta_data.width
        tileSize = game_map.meta_data.tile_size*i

        map_draw_w = tileSize*map_width*2
        map_draw_h = tileSize*map_height

        newImage = pygame.Surface((map_draw_w, map_draw_h), pygame.SRCALPHA)
        newImage.fill((0,0,0,0))

        for xp in range(map_width):
            for yp in range(map_height):
                dx, dy = isometric_transformations.isometricTransform((xp*tileSize, yp*tileSize))
                dx += tileSize*map_width
                image = get_tile_image_from_map_coordinate(xp, yp, sprite_sheet=sprite_sheet, map=game_map)
                scaled_image = pygame.transform.scale(image,(tileSize*2,tileSize))
                newImage.blit(scaled_image, (dx-tileSize, dy))

        mip_mapping.buffer_images.append(newImage)
    
    set_current_mip_map_image(0)

def render_map(camera_transform: CameraTransform, map_metadata: MapMetaData, mip_mapping: MipMapping, screen: pygame.Surface):
    cam_s = camera_transform.s
    
    map_height = map_metadata.height
    map_width = map_metadata.width
    tileSize = map_metadata.tile_size

    p1 = isometric_transformations.get_transformed_isometric_screen_position_from_tile_position(0, map_height, map_metadata=map_metadata, camera_transform=camera_transform, viewport_dimensions=ViewportDimensions(pixel_width=screen.get_width(), pixel_height=screen.get_height()))
    p2 = isometric_transformations.get_transformed_isometric_screen_position_from_tile_position(0, 0, map_metadata=map_metadata, camera_transform=camera_transform, viewport_dimensions=ViewportDimensions(pixel_width=screen.get_width(), pixel_height=screen.get_height())) 

    map_draw_x = p1[0]
    map_draw_y = p2[1]

    scaled_image = pygame.transform.scale(mip_mapping.current_buffer_image,(tileSize*map_width*2*cam_s,tileSize*map_height*cam_s))
    screen.blit(scaled_image, (map_draw_x, map_draw_y))