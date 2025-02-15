import pygame
from Utils import fmath
from typing import Callable, Tuple, List
import singletons
import singletons.SCamera
import singletons.SCameraDragController
from mouse_callback.MouseCallbackList import MouseCallbackList

class SMouse:
    def __init__(self):
        self.last_mouse_pressed_in = self.last_mouse_position = (0,0)
        self.is_pressed = False
        self.mouse_movement_delta = (0,0)
        self.drag_current_vel: List[float] = [0,0]
        self.drag_unlock = False
        self.drag_delta_threshold = 30

        self.mouse_position_in_world = (0,0)

        self.curr_mouse_position = pygame.mouse.get_pos()
        
        self.camera = singletons.SCamera.instance
        self.camera_drag_controller = singletons.SCameraDragController.instance

        self.mouse_callback_list: MouseCallbackList = None


    def update_based_on_event(self, event: pygame.event.Event):
        self.curr_mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEWHEEL:
            for c in self.mouse_callback_list.mousewheel:
                c(event.y)
             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for c in self.mouse_callback_list.pressed_left_in:
                c(self.curr_mouse_position)

            self.last_mouse_pressed_in = self.curr_mouse_position
            self.is_pressed = True

            self.camera_drag_controller.set_new_last_position()

            if self.camera_drag_controller.cam_is_floating():

                self.drag_unlock = True

                self.camera_drag_controller.stop_cam_floating()

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for c in self.mouse_callback_list.pressed_left_out:
                c(self.curr_mouse_position)

            self.is_pressed = False
            
            if fmath.get_vector_magnitude(self.drag_current_vel) >= self.camera_drag_controller.get_cam_velocity_magnitude_threshold() or self.drag_unlock:
                
                self.camera_drag_controller.start_cam_floating((-self.drag_current_vel[0], -self.drag_current_vel[1]))
                
                self.drag_current_vel[0] = 0
                self.drag_current_vel[1] = 0

            if self.drag_unlock == True:
                self.drag_unlock = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            for c in self.mouse_callback_list.pressed_right_in:
                c(self.curr_mouse_position)        
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
            for c in self.mouse_callback_list.pressed_right_out:
                c(self.curr_mouse_position)
        if event.type == pygame.MOUSEMOTION:
            self.mouse_movement_delta = (self.curr_mouse_position[0]-self.last_mouse_pressed_in[0], self.curr_mouse_position[1]-self.last_mouse_pressed_in[1])
            if self.is_pressed:

                if fmath.get_vector_magnitude(self.mouse_movement_delta) >= self.drag_delta_threshold or self.drag_unlock:
                    self.camera_drag_controller.update_cam_drag_position(self.mouse_movement_delta)
                    self.drag_unlock = True
        
        self.drag_current_vel = self.camera_drag_controller.calc_drag_current_velocity((self.curr_mouse_position[0]-self.last_mouse_position[0],self.curr_mouse_position[1]-self.last_mouse_position[1]))
        self.last_mouse_position = self.curr_mouse_position

instance: SMouse = None