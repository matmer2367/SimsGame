from .. import dataset

from ..Utils import fmath
from typing import Tuple, List


from mouse_callback.interfaces.IMouseClickButtons import IMouseClickButtons
from mouse_callback.interfaces.IMouseMotion import IMouseMotion

class SCameraDragController(IMouseClickButtons, IMouseMotion):
    def __init__(self):
        self.cam = dataset.SCameraInstance
        self.mouse = dataset.SMouseInstance
        
        self.camera_position_when_drag_started: List[float] = [0,0]
        self.left_button_pressed = False
        self.drag_current_vel: List[float] = [0,0]

        self.DRAG_DELTA_THRESHOLD = 30
    
    def pressed_left_in(self, pos: Tuple[int]) -> None:
        self.left_button_pressed = True

        self.camera_position_when_drag_started[0] = self.cam.x
        self.camera_position_when_drag_started[1] = self.cam.y

        self.cam.is_floating = False
        self.cam.velocity[0] = 0
        self.cam.velocity[1] = 0

    def pressed_left_out(self, pos: Tuple[int]) -> None:
        self.left_button_pressed = False
            
        if fmath.get_vector_magnitude(self.drag_current_vel) >= self.cam.velocity_magnitude_threshold:
            self.cam.is_floating = True
            self.cam.velocity[0] = -self.drag_current_vel[0]
            self.cam.velocity[1] = -self.drag_current_vel[1]

            self.drag_current_vel[0] = 0
            self.drag_current_vel[1] = 0

    def pressed_right_in(self, pos: Tuple[int]) -> None:
        pass

    def pressed_right_out(self, pos: Tuple[int]) -> None:
        pass

    def mouse_motion(self, positional_delta: Tuple[int, int], movement_delta: Tuple[int, int]) -> None:
        if self.left_button_pressed:
            self.drag_current_vel = [movement_delta[0]/self.cam.s, movement_delta[1]/self.cam.s]
            if fmath.get_vector_magnitude(positional_delta) >= self.DRAG_DELTA_THRESHOLD:
                self.cam.x = self.camera_position_when_drag_started[0]-positional_delta[0]/self.cam.s
                self.cam.y = self.camera_position_when_drag_started[1]-positional_delta[1]/self.cam.s

instance: SCameraDragController = None