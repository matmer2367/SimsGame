import singletons

from typing import Tuple, List

import singletons.SCamera

class SCameraDragController:
    def __init__(self):
        self.cam = singletons.SCamera.instance
    
    def set_new_last_position(self) -> None:
        self.cam.last_position[0] = self.cam.x
        self.cam.last_position[1] = self.cam.y
    
    def cam_is_floating(self) -> bool:
        return self.cam.is_floating
    
    def stop_cam_floating(self) -> None:
        self.cam.is_floating = False
        self.cam.velocity[0] = 0
        self.cam.velocity[1] = 0
    
    def get_cam_velocity_magnitude_threshold(self) -> float:
        return self.cam.velocity_magnitude_threshold
    
    def start_cam_floating(self, velocity: Tuple[float, float]) -> None:
        self.cam.is_floating = True
        self.cam.velocity[0] = velocity[0]
        self.cam.velocity[1] = velocity[1]
    
    def update_cam_drag_position(self, last_to_current_position_delta: Tuple[float, float]) -> None:
        self.cam.x = self.cam.last_position[0]-last_to_current_position_delta[0]/self.cam.s
        self.cam.y = self.cam.last_position[1]-last_to_current_position_delta[1]/self.cam.s

    def calc_drag_current_velocity(self, velocity: Tuple[float, float]) -> List[float]:
        return [velocity[0]/self.cam.s, velocity[1]/self.cam.s]

instance: SCameraDragController = None