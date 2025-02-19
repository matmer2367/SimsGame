import pygame

def load_isometric_tile_texture(path, sheet_rows, sheet_cols, sheet_x_selector, sheet_y_selector, color_key = (0,0,0)):
        texture_sheet = pygame.image.load(path)
        texture = pygame.Surface((texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
        texture.blit(texture_sheet, (0,0), (sheet_x_selector*texture_sheet.get_width()/sheet_cols,sheet_y_selector*texture_sheet.get_height()/sheet_rows,texture_sheet.get_width()/sheet_cols, texture_sheet.get_height()/sheet_rows))
        texture.set_colorkey(color_key)
        return texture