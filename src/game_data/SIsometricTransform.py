import pygame
import game_data


def get_transformed_cam_on_screen_center(screen_width, screen_height, pcam_x, pcam_y, scale, x, y, width, height):
    return (scale*x+(screen_width/2)*(scale+1)-scale*pcam_x, scale*y+(screen_height/2)*(scale+1)-scale*pcam_y, width*scale, height*scale)

def isometricTransform(pos):
    x, y = pos
    return (x-y, .5*(x+y))

class SIsometricTransform:
    def __init__(self, screen) -> None:
        self.screen: pygame.Surface = screen
        self.cam: game_data.SCamera.SCamera = game_data.SCamera.instance
        self.map: game_data.SMap.SMap = game_data.SMap.instance

    def rect_in_viewport(self, rect_data) -> bool:
        x1 = rect_data[0]
        y1 = rect_data[1]
        x2 = x1+rect_data[2]
        y2 = y1+rect_data[3]
        return not (y2 <= 0 or y1 >= self.screen.get_height() or x2 <= 0 or x1 >= self.screen.get_width()) 

    # Camera Methods
    def get_camera_bounding_box_for_its_current_scale(self):
        cam_x, cam_y = self.cam.x, self.cam.y
        self.cam.x = 0
        self.cam.y = 0

        map_width = self.map.width
        map_height = self.map.height
        tileSize = self.map.tile_size

        cam_border_left_x = self.get_transformed_isometric_screen_position((map_width-1)*tileSize, 0)[0]
        cam_border_left_y = self.get_transformed_isometric_screen_position((map_width-1)*tileSize, (map_height-1)*tileSize)[1]

        cam_border_right_x = self.get_transformed_isometric_screen_position(0, (map_height-1)*tileSize)[0]
        cam_border_right_y = self.get_transformed_isometric_screen_position(1*tileSize, 1*tileSize)[1]

        self.cam.x = cam_x
        self.cam.y = cam_y

        return cam_border_left_x, cam_border_left_y, cam_border_right_x, cam_border_right_y

    def isometric_rect_in_viewport(self, x, y, tileSize):
        dx, dy = self.get_transformed_isometric_screen_position(x*tileSize, y*tileSize)
        cam_s = self.cam.s
        dx_draw, dy_draw = dx-tileSize*cam_s, dy
        dw_draw, dh_draw = tileSize*2*cam_s, tileSize*cam_s

        return self.rect_in_viewport((dx_draw, dy_draw, dw_draw, dh_draw))

    def isometric_rect_in_viewport_polygon_calculation(self, rect_data):
        ''' VERY INTENSIVE CALCULATION '''
        x = rect_data[0]
        y = rect_data[1]
        w = rect_data[2]
        h = rect_data[3]
        p1x, p1y = (x, y)
        p2x, p2y = (x+w, y)
        p3x, p3y = (x+w, y+h)
        p4x, p4y = (x, y+h)
        
        t1x, t1y = self.get_transformed_isometric_screen_position(p1x, p1y)
        t2x, t2y = self.get_transformed_isometric_screen_position(p2x, p2y)
        t3x, t3y = self.get_transformed_isometric_screen_position(p3x, p3y)
        t4x, t4y = self.get_transformed_isometric_screen_position(p4x, p4y)

        cam_s = self.cam.s
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        b1 = 0-h*cam_s <= t1x <= screen_width+h*cam_s and 0-h*cam_s*2 <= t1y <= screen_height+h*cam_s*2
        b2 = 0-h*cam_s <= t2x <= screen_width+h*cam_s and 0-h*cam_s*2 <= t2y <= screen_height+h*cam_s*2
        b3 = 0-h*cam_s <= t3x <= screen_width+h*cam_s and 0-h*cam_s*2 <= t3y <= screen_height+h*cam_s*2
        b4 = 0-h*cam_s <= t4x <= screen_width+h*cam_s and 0-h*cam_s*2 <= t4y <= screen_height+h*cam_s*2

        return b1 or b2 or b3 or b4
    
    def isInScreenViewPort(self, x, y):
        tx, ty = self.get_transformed_isometric_screen_position(x,y)
        return 0 <= tx <= self.screen.get_width() and 0 <= ty <= self.screen.get_height()
    
    # Draw Stuff Methods ###############################################
    def drawTransformedIsometricRect(self, color, x, y, w, h):
        if not (self.isInScreenViewPort(x,y) or self.isInScreenViewPort(x+w,y) or self.isInScreenViewPort(x,y+h) or self.isInScreenViewPort(x+w, y+h)):
            return
        polygonPoints = []
        for i in range(4):
            polygonPoints.append(self.get_transformed_isometric_screen_position(x, y))
            polygonPoints.append(self.get_transformed_isometric_screen_position(x+w, y))
            polygonPoints.append(self.get_transformed_isometric_screen_position(x+w, y+h))
            polygonPoints.append(self.get_transformed_isometric_screen_position(x, y+h))

            pygame.draw.polygon(self.screen, color, polygonPoints)

    # Get transformd Coordinates ##################################
    def get_transformed_isometric_world_position(self, x, y):
        cam_s = self.cam.s
        cam_x = self.cam.x
        cam_y = self.cam.y
        
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        tx = (screen_width/2)*(cam_s+1)-cam_s*cam_x
        ty = (screen_height/2)*(cam_s+1)-cam_s*cam_y
        m = (x-tx)/cam_s
        w = 2*(y-ty)/cam_s
        rx = (m+w)/2
        return (rx, w-rx)

    def get_transformed_isometric_screen_position(self, x, y):
        cam_s = self.cam.s
        cam_x = self.cam.x
        cam_y = self.cam.y

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        return (cam_s*(x-y)+(screen_width/2)*(cam_s+1)-cam_s*cam_x,(cam_s/2)*(x+y)+(screen_height/2)*(cam_s+1)-cam_s*cam_y)

    def get_transformed_scaled_position(self, x, y):
        return get_transformed_cam_on_screen_center(self.screen.get_width(), self.screen.get_height(), self.cam.x, self.cam.y, self.cam.s, x, y, 1, 1)[:3]

    # Old Methods ######################################################
    def get_transformed_rect_position(self, x, y, w, h):
        return get_transformed_cam_on_screen_center(self.screen.get_width(), self.screen.get_height(), self.cam.x, self.cam.y, self.cam.s, x, y, w, h)
    
    def get_transformed_position(self, x, y):
        return get_transformed_cam_on_screen_center(self.screen.get_width(), self.screen.get_height(), self.cam.x, self.cam.y, self.cam.s, x, y, 0, 0)[:2]
    
    # conversion ############################################################
    def cam_size_conversion(self, x, y):
        return x*self.cam.s, y*self.cam.s
    
    def cam_size_conversion_tuple(self, pos):
        x, y = pos
        return x*self.cam.s, y*self.cam.s

    def convert_to_screen_position(self, world_x, world_y):
        cam_s = self.cam.s
        cam_x = self.cam.x
        cam_y = self.cam.y

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        return (cam_s*(world_x+(screen_width/2-cam_x))+(screen_width/2), cam_s*(world_y+(screen_height/2-cam_y))+(screen_height/2))

    def convert_to_world_position(self, screen_x, screen_y):
        cam_s = self.cam.s
        cam_x = self.cam.x
        cam_y = self.cam.y

        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        return (((screen_x-screen_width/2)/cam_s)-(screen_width/2-cam_x), ((screen_y-screen_height/2)/cam_s)-(screen_height/2-cam_y))

instance: SIsometricTransform = None