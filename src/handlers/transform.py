import pygame
from singletons.ICamera import ICamera

def get_transformed_cam_on_screen_center(screen_width, screen_height, pcam_x, pcam_y, scale, x, y, width, height):
    return (scale*x+(screen_width/2)*(scale+1)-scale*pcam_x, scale*y+(screen_height/2)*(scale+1)-scale*pcam_y, width*scale, height*scale)

def isometricTransform(pos):
    x, y = pos
    return (x-y, .5*(x+y))

class Transform:
    def __init__(self, screen, cam=None) -> None:
        self.screen: pygame.Surface = screen
        self.cam: ICamera = cam

    # Camera Methods
    def get_camera_bounding_box_for_its_current_scale(self, map_width, map_height, tileSize):
        cam_x, cam_y = self.cam.x, self.cam.y
        self.cam.x = 0
        self.cam.y = 0

        cam_border_left_x = self.get_transformed_isometric_screen_position((map_width-1)*tileSize, 0)[0]
        cam_border_left_y = self.get_transformed_isometric_screen_position((map_width-1)*tileSize, (map_height-1)*tileSize)[1]

        cam_border_right_x = self.get_transformed_isometric_screen_position(0, (map_height-1)*tileSize)[0]
        cam_border_right_y = self.get_transformed_isometric_screen_position(1*tileSize, 1*tileSize)[1]

        self.cam.x = cam_x
        self.cam.y = cam_y

        return cam_border_left_x, cam_border_left_y, cam_border_right_x, cam_border_right_y

    def isometric_rect_in_viewport(self, rect_data):
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

        b1 = 0-h*self.cam.s <= t1x <= self.screen.get_width()+h*self.cam.s and 0-h*self.cam.s*2 <= t1y <= self.screen.get_height()+h*self.cam.s*2
        b2 = 0-h*self.cam.s <= t2x <= self.screen.get_width()+h*self.cam.s and 0-h*self.cam.s*2 <= t2y <= self.screen.get_height()+h*self.cam.s*2
        b3 = 0-h*self.cam.s <= t3x <= self.screen.get_width()+h*self.cam.s and 0-h*self.cam.s*2 <= t3y <= self.screen.get_height()+h*self.cam.s*2
        b4 = 0-h*self.cam.s <= t4x <= self.screen.get_width()+h*self.cam.s and 0-h*self.cam.s*2 <= t4y <= self.screen.get_height()+h*self.cam.s*2

        #b1 = -100 <= t1x <= self.screen.get_width()+200 and -100 <= t1y <= self.screen.get_height()+200
        #b2 = -100 <= t2x <= self.screen.get_width()+200 and -100 <= t2y <= self.screen.get_height()+200
        #b3 = -100 <= t3x <= self.screen.get_width()+200 and -100 <= t3y <= self.screen.get_height()+200
        #b4 = -100 <= t4x <= self.screen.get_width()+200 and -100 <= t4y <= self.screen.get_height()+200

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
        tx = (self.screen.get_width()/2)*(self.cam.s+1)-self.cam.s*self.cam.x
        ty = (self.screen.get_height()/2)*(self.cam.s+1)-self.cam.s*self.cam.y
        m = (x-tx)/self.cam.s
        w = 2*(y-ty)/self.cam.s
        rx = (m+w)/2
        return (rx, w-rx)

    def get_transformed_isometric_screen_position(self, x, y):
        return (self.cam.s*(x-y)+(self.screen.get_width()/2)*(self.cam.s+1)-self.cam.s*self.cam.x,(self.cam.s/2)*(x+y)+(self.screen.get_height()/2)*(self.cam.s+1)-self.cam.s*self.cam.y)

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
        return (self.cam.s*(world_x+(self.screen.get_width()/2-self.cam.x))+(self.screen.get_width()/2), self.cam.s*(world_y+(self.screen.get_height()/2-self.cam.y))+(self.screen.get_height()/2))

    def convert_to_world_position(self, screen_x, screen_y):
        return (((screen_x-self.screen.get_width()/2)/self.cam.s)-(self.screen.get_width()/2-self.cam.x), ((screen_y-self.screen.get_height()/2)/self.cam.s)-(self.screen.get_height()/2-self.cam.y))