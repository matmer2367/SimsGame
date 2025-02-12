import pygame
from Utils import fmath
from typing import Callable, Tuple, List
import singletons
import singletons.ICamera
import singletons.ICameraDragController

class IMouse:
    def __init__(self):
        
        self.last_mouse_pressed_in = self.last_mouse_position = (0,0)
        self.is_pressed = False
        self.drag_delta = (0,0)
        self.drag_current_vel: List[float] = [0,0]
        self.drag_unlock = False
        self.drag_delta_threshold = 30
        self.event_valid = False

        self.mouse_position_in_world = (0,0)

        self.curr_mouse_position = pygame.mouse.get_pos()
        
        self.camera = singletons.ICamera.instance
        self.camera_drag_controller = singletons.ICameraDragController.instance

        # Default mouse_wheelcallback
        self.mousewheel_callback = self.camera.update_mousewheel_zoom

        self.mouse_pressed_left_in_callback = None
        self.mouse_pressed_left_out_callback = None
        self.mouse_pressed_right_in_callback = None
        self.mouse_pressed_right_out_callback = None


    def set_callbacks(self,
                 mouse_pressed_left_in_callback: Callable[[Tuple[int, int]],None] = None,
                 mouse_pressed_left_out_callback: Callable[[Tuple[int, int]],None] = None,
                 mouse_pressed_right_in_callback: Callable[[Tuple[int, int]],None] = None,
                 mouse_pressed_right_out_callback: Callable[[Tuple[int, int]],None] = None):
        self.mouse_pressed_left_in_callback = mouse_pressed_left_in_callback
        self.mouse_pressed_left_out_callback = mouse_pressed_left_out_callback
        self.mouse_pressed_right_in_callback = mouse_pressed_right_in_callback
        self.mouse_pressed_right_out_callback = mouse_pressed_right_out_callback

    def update_based_on_event(self, event: pygame.event.Event):
        self.curr_mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEWHEEL:
            if self.mousewheel_callback is not None:
                self.mousewheel_callback(event.y)
             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.last_mouse_pressed_in = self.curr_mouse_position
            self.is_pressed = True

            self.camera_drag_controller.set_new_last_position()

            if self.camera_drag_controller.cam_is_floating():

                self.drag_unlock = True

                self.camera_drag_controller.stop_cam_floating()
            else:
                if self.mouse_pressed_left_in_callback is not None:
                    self.mouse_pressed_left_in_callback(self.curr_mouse_position)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.event_valid = False
            self.is_pressed = False
            
            if fmath.get_vector_magnitude(self.drag_current_vel) >= self.camera_drag_controller.get_cam_velocity_magnitude_threshold() or self.drag_unlock:
                
                self.camera_drag_controller.start_cam_floating((-self.drag_current_vel[0], -self.drag_current_vel[1]))
                
                self.drag_current_vel[0] = 0
                self.drag_current_vel[1] = 0
            else:
                self.event_valid = True

            if self.drag_unlock == True:
                self.drag_unlock = False
                self.event_valid = False
            
            if self.event_valid:
                if self.mouse_pressed_left_out_callback is not None:
                    self.mouse_pressed_left_out_callback(self.curr_mouse_position)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            if self.mouse_pressed_right_in_callback is not None:
                self.mouse_pressed_right_in_callback(self.curr_mouse_position)        
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
            if self.mouse_pressed_right_out_callback is not None:
                self.mouse_pressed_right_out_callback(self.curr_mouse_position)
        if event.type == pygame.MOUSEMOTION:
            if self.is_pressed:
                self.drag_delta = (self.curr_mouse_position[0]-self.last_mouse_pressed_in[0], self.curr_mouse_position[1]-self.last_mouse_pressed_in[1])

                if fmath.get_vector_magnitude(self.drag_delta) >= self.drag_delta_threshold or self.drag_unlock:
                    self.camera_drag_controller.update_cam_drag_position(self.drag_delta)
                    self.drag_unlock = True
        
        self.drag_current_vel = self.camera_drag_controller.calc_drag_current_velocity((self.curr_mouse_position[0]-self.last_mouse_position[0],self.curr_mouse_position[1]-self.last_mouse_position[1]))
        self.last_mouse_position = self.curr_mouse_position

instance: IMouse = None