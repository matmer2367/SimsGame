import pygame

import game_data

class GameObject:
    def __init__(self, x, y, surface, draw_offset_x = 0, draw_offset_y = 0, debug_draw_mode = False, debug_draw_pivot_color = (0,0,0), selectable_hover_display = False) -> None:
        self.x_pivot = x
        self.y_pivot = y
        self.draw_surface: pygame.Surface = surface
        self.draw_offset_x = draw_offset_x
        self.draw_offset_y = draw_offset_y

        self.debug_draw_mode = debug_draw_mode
        self.debug_draw_pivot_color = debug_draw_pivot_color

        self.last_x_transformed_pivot = self.x_pivot
        self.last_y_transformed_pivot = self.y_pivot
        self.last_x_transformed_draw_offset = self.draw_offset_x
        self.last_y_transformed_draw_offset = self.draw_offset_y

        self.selectable_hover_display = selectable_hover_display

        self.transform = game_data.SIsometricTransform.instance
        self.cam = game_data.SCamera.instance
    
    def get_transformed_isometric_screen_pivot_coordinate(self):
        return self.transform.get_transformed_isometric_screen_position(self.x_pivot, self.y_pivot)
    
    def get_transformed_isometric_screen_drawing_surface_start_coordinate(self):
        px, py = self.get_transformed_isometric_screen_pivot_coordinate()
        sox, soy = self.transform.cam_size_conversion(self.draw_offset_x, self.draw_offset_y)
        return px+sox, py+soy
    
    def isInObjectBounds(self, checkScreenCoord):
        x, y = checkScreenCoord
        rx, ry = self.getPivotPos()
        w, h = self.getBoundingSurfaceDimenstion()
        trectx, trecty = self.transform.get_transformed_isometric_screen_position(rx, ry)

        cam_s = self.cam.s

        return trectx+self.draw_offset_x*cam_s <= x <= trectx+self.draw_offset_x*cam_s+w*cam_s and trecty+self.draw_offset_y*cam_s <= y <= trecty+self.draw_offset_y*cam_s+h*cam_s
    
    def drawGameObject(self):
        dx, dy = self.x_pivot, self.y_pivot
        surfw, surfh = self.draw_surface.get_width(), self.draw_surface.get_height()
        tx, ty = self.transform.get_transformed_isometric_screen_position(dx, dy)
        self.transform.screen.blit(pygame.transform.scale(self.draw_surface, (surfw*self.cam.s, surfh*self.cam.s)), (tx+self.draw_offset_x*self.cam.s, ty+self.draw_offset_y*self.cam.s))
        if self.debug_draw_mode:
            pygame.draw.circle(self.transform.screen, self.debug_draw_pivot_color, (tx, ty), self.cam.s*surfw*.2)

    def getDrawCoordinate(self):
        return self.x_pivot + self.draw_offset_x, self.y_pivot + self.draw_offset_y
    
    def getPivotPos(self):
        return self.x_pivot, self.y_pivot
    
    def getBoundingSurfaceDimenstion(self):
        return self.draw_surface.get_width(), self.draw_surface.get_height()

    def move(self, x_off, y_off):
        self.x_pivot += x_off
        self.y_pivot += y_off
    
    def displayOnScreen(screen):
        pass
        #transform.drawGameObject(object)
        #px, py = object.getPivotPos()
        #if transform.isInObjectBounds(curr_mouse_position, object):
            #dx, dy = object.get_transformed_isometric_screen_drawing_surface_start_coordinate(transform)
            #sw, sh = transform.cam_size_conversion_tuple(object.getBoundingSurfaceDimenstion())
            #pygame.draw.rect(screen, (255,255,255), (dx, dy, sw, sh), width=2)

class Person(GameObject):
    def __init__(self, x, y, surface, draw_offset_x=0, draw_offset_y=0, debug_draw_mode=False, debug_draw_pivot_color=(0, 200, 0), selectable_hover_display=False) -> None:
        super().__init__(x, y, surface, draw_offset_x, draw_offset_y, debug_draw_mode, debug_draw_pivot_color, selectable_hover_display)