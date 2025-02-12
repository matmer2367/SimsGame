import pygame
from Utils import fmath
import math
from typing import Callable, Tuple, List
import singletons
import singletons.ICameraDragController

class Mouse:
    def __init__(self, mousewheel_callback: Callable[[int],None],
                 mouse_pressed_left_in_callback: Callable[[Tuple[int, int]],None],
                 mouse_pressed_left_out_callback: Callable[[Tuple[int, int]],None],
                 mouse_pressed_right_in_callback: Callable[[Tuple[int, int]],None],
                 mouse_pressed_right_out_callback: Callable[[Tuple[int, int]],None]):
        
        self.last_mouse_pressed_in = self.last_mouse_position = (0,0)
        self.is_pressed = False
        self.drag_delta = (0,0)
        self.drag_current_vel: List[float] = [0,0]
        self.drag_unlock = False
        self.drag_delta_threshold = 30
        self.event_valid = False

        self.mouse_position_in_world = (0,0)

        self.mousewheel_callback = mousewheel_callback

        self.curr_mouse_position = pygame.mouse.get_pos()

        self.mouse_pressed_left_in_callback = mouse_pressed_left_in_callback
        self.mouse_pressed_left_out_callback = mouse_pressed_left_out_callback
        self.mouse_pressed_right_in_callback = mouse_pressed_right_in_callback
        self.mouse_pressed_right_out_callback = mouse_pressed_right_out_callback

        self.camera_drag_controller = singletons.ICameraDragController.instance

    def update_based_on_event(self, event: pygame.event.Event):
        self.curr_mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEWHEEL:
            self.mousewheel_callback(event.y)
             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.last_mouse_pressed_in = self.curr_mouse_position
            self.is_pressed = True

            if self.camera_drag_controller is not None:
                self.camera_drag_controller.set_new_last_position()
                    #self.cam.position_when_last_mouse_pressed = (self.cam.x, self.cam.y)

                if self.camera_drag_controller.cam_is_floating():
                        #self.cam.is_floating:

                    self.drag_unlock = True

                    self.camera_drag_controller.stop_cam_floating()
                        #self.cam.is_floating = False
                        #self.cam.velocity = [0,0]
                else:
                    self.mouse_pressed_left_in_callback(self.curr_mouse_position)
            else:
                self.mouse_pressed_left_in_callback(self.curr_mouse_position)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.event_valid = False
            self.is_pressed = False
            
            if self.camera_drag_controller is not None:
                if fmath.get_vector_magnitude(self.drag_current_vel) >= self.camera_drag_controller.get_cam_velocity_magnitude_threshold() or self.drag_unlock:
                    #if fmath.get_vector_magnitude(self.drag_current_vel) >= self.cam.velocity_magnitude_threshold or self.drag_unlock:
                    
                    self.camera_drag_controller.start_cam_floating((-self.drag_current_vel[0], -self.drag_current_vel[1]))
                        #self.cam.is_floating = True
                        #self.cam.velocity[0] = -self.drag_current_vel[0]
                        #self.cam.velocity[1] = -self.drag_current_vel[1]
                    
                    self.drag_current_vel[0] = 0
                    self.drag_current_vel[1] = 0
                else:
                    self.event_valid = True

                if self.drag_unlock == True:
                    self.drag_unlock = False
                    self.event_valid = False
            
            if self.event_valid or self.camera_drag_controller is None:
                self.mouse_pressed_left_out_callback(self.curr_mouse_position)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            self.mouse_pressed_right_in_callback(self.curr_mouse_position)        
        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
            self.mouse_pressed_right_out_callback(self.curr_mouse_position)
        if event.type == pygame.MOUSEMOTION:
            if self.is_pressed:
                self.drag_delta = (self.curr_mouse_position[0]-self.last_mouse_pressed_in[0], self.curr_mouse_position[1]-self.last_mouse_pressed_in[1])

                if self.camera_drag_controller is not None and (fmath.get_vector_magnitude(self.drag_delta) >= self.drag_delta_threshold or self.drag_unlock):
                    self.camera_drag_controller.update_cam_drag_position(self.drag_delta)
                        #self.cam.x = self.cam.position_when_last_mouse_pressed[0]-self.drag_delta[0]/self.cam.s
                        #self.cam.y = self.cam.position_when_last_mouse_pressed[1]-self.drag_delta[1]/self.cam.s
                    self.drag_unlock = True
        
        if self.camera_drag_controller is not None:
            self.drag_current_vel = self.camera_drag_controller.calc_drag_current_velocity((self.curr_mouse_position[0]-self.last_mouse_position[0],self.curr_mouse_position[1]-self.last_mouse_position[1]))
                #self.drag_current_vel = ((curr_mouse_position[0]-self.last_mouse_position[0])/self.cam.s, (curr_mouse_position[1]-self.last_mouse_position[1])/self.cam.s)
        self.last_mouse_position = self.curr_mouse_position