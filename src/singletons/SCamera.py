from Utils import fmath
import math
from typing import List

import singletons
import singletons.SIsometricMapRenderer
import singletons.SMap
import singletons.SIsometricTransform

class SCamera:
    def __init__(self, x, y, s = 1) -> None:
        self.transform: singletons.SIsometricTransform.SIsometricTransform = singletons.SIsometricTransform.instance
        self.map: singletons.SMap.SMap = singletons.SMap.instance
        self.isometricMapRenderer: singletons.SIsometricMapRenderer.SIsometricMapRenderer = singletons.SIsometricMapRenderer.instance

        self.reset_value_x = x
        self.reset_value_y = y
        self.reset_value_s = s

        self.x = x
        self.y = y

        self.last_position: List[float] = [0,0]
        self.velocity = [0,0]
        self.velocity_magnitude_threshold = .2
        self.velocity_friction_multiplier = 0.85
        self.is_floating = False
        self.scale_step = s
        self.keyboard_movement_speed = 6
        self.scale_cap_min, self.scale_cap_max = 1, 30
        self.ZOOM_STEP_COUNTER = (self.scale_cap_max-self.scale_cap_min)//15
        self.s = self.ZOOM_STEP_COUNTER*self.scale_step

        self.cam_border_left_x, self.cam_border_left_y, self.cam_border_right_x, self.cam_border_right_y = 0,0,0,0

    def reset(self):
        self.x = self.reset_value_x
        self.y = self.reset_value_y
        self.s = self.reset_value_s

        self.last_position[0]= 0
        self.last_position[1]= 0

        self.velocity[0] = 0
        self.velocity[1] = 1
        
        self.velocity_magnitude_threshold = .2
        self.velocity_friction_multiplier = 0.85
        self.is_floating = False
        self.scale_step = self.s
        self.keyboard_movement_speed = 6
        self.scale_cap_min, self.scale_cap_max = 1, 30
        self.ZOOM_STEP_COUNTER = (self.scale_cap_max-self.scale_cap_min)//15
        self.s = self.ZOOM_STEP_COUNTER*self.scale_step

        self.cam_border_left_x, self.cam_border_left_y, self.cam_border_right_x, self.cam_border_right_y = 0,0,0,0

    def update_bounding_box_for_its_current_scale(self):
        self.cam_border_left_x, self.cam_border_left_y, self.cam_border_right_x, self.cam_border_right_y = self.transform.get_camera_bounding_box_for_its_current_scale()
     
    def keep_camera_in_bounds(self, screen):
        self.update_bounding_box_for_its_current_scale()

        if self.x+screen.get_width()/self.s <= self.cam_border_right_x/self.s:
            self.velocity[0] = 0
            self.x = (self.cam_border_right_x-screen.get_width())/self.s

        if self.y+screen.get_height()/self.s <= self.cam_border_right_y/self.s:
            self.velocity[0] = 0
            self.y = (self.cam_border_right_y-screen.get_height())/self.s

        if self.x >= self.cam_border_left_x/self.s:
            self.velocity[0] = 0
            self.x = self.cam_border_left_x/self.s

        if self.y >=  self.cam_border_left_y/self.s:
            self.velocity[0] = 0
            self.y = self.cam_border_left_y/self.s
    
    def update_physical_movement(self):
        if self.is_floating:
            self.x += self.velocity[0]
            self.velocity[0] *= self.velocity_friction_multiplier

            self.y += self.velocity[1]
            self.velocity[1] *= self.velocity_friction_multiplier

            if fmath.get_vector_magnitude(self.velocity) <= self.velocity_magnitude_threshold:
                self.velocity = [0,0]
                self.is_floating = False
    
    def update_mousewheel_zoom(self, zoom_factor):
        cam_zoom_multiplier = math.floor(self.s*.3)
        if cam_zoom_multiplier >= 1:
            self.ZOOM_STEP_COUNTER += zoom_factor*cam_zoom_multiplier
        else:
            self.ZOOM_STEP_COUNTER += zoom_factor

        if self.ZOOM_STEP_COUNTER < self.scale_cap_min//self.scale_step:
            self.ZOOM_STEP_COUNTER = self.scale_cap_min//self.scale_step
        if self.ZOOM_STEP_COUNTER > self.scale_cap_max//self.scale_step:
            self.ZOOM_STEP_COUNTER = self.scale_cap_max//self.scale_step
        
        self.s = self.ZOOM_STEP_COUNTER*self.scale_step

        print(self.s)
        self.isometricMapRenderer.set_current_mip_map_image(self.s-1)

instance: SCamera = None