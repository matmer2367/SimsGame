from game_constants.rendering.sprite_sheet import GRASS_IMAGE
from structs.game_context.world.game_map.map import Map
from structs.rendering.sprite_sheet.sprite_sheet import SpriteSheet

def get_tile_image_from_map_coordinate(xp, yp, sprite_sheet: SpriteSheet, map: Map):
    #TODO
    return sprite_sheet.images[GRASS_IMAGE]