from ..Utils import fmath
import math
from typing import List

from .. import dataset

class SCamera:
    def __init__(self, x, y, s = 1) -> None:
        self.transform: dataset.SIsometricTransform = dataset.SIsometricTransformInstance
        self.map: dataset.SMap = dataset.SMapInstance
        self.isometricMapRenderer: dataset.SIsometricMapRenderer = dataset.SIsometricMapRendererInstance

        self.x = x#
        self.y = y#
        self.s = s#

        
        self.velocity = [0,0]#
        self.velocity_magnitude_threshold = .2#
        self.velocity_friction_multiplier = 0.85#
        self.is_floating = False#
        self.scale_step = 1#
        self.keyboard_movement_speed = 6#
        self.scale_cap_min, self.scale_cap_max = 1, 30#
        self.zoom_step_counter = (self.scale_cap_max-self.scale_cap_min)//15#

        # \/
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

        if self.y >= self.cam_border_left_y/self.s:
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
            self.zoom_step_counter += zoom_factor*cam_zoom_multiplier
        else:
            self.zoom_step_counter += zoom_factor

        if self.zoom_step_counter < self.scale_cap_min//self.scale_step:
            self.zoom_step_counter = self.scale_cap_min//self.scale_step
        if self.zoom_step_counter > self.scale_cap_max//self.scale_step:
            self.zoom_step_counter = self.scale_cap_max//self.scale_step
        
        self.s = self.zoom_step_counter*self.scale_step

        self.isometricMapRenderer.set_current_mip_map_image(self.s-1)

instance: SCamera = None