import pygame
import singletons
import singletons.ICamera
import singletons.IMouse
import singletons.IIsometricTransform

import typing

import MouseCallbackList

class AState:
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.cam = singletons.ICamera.instance
        self.transform = singletons.IIsometricTransform.instance
        
        self.mouse = singletons.IMouse.instance
        self.mouse_callback_list = self.create_mouse_callback_list()

        self.mouse_pos_in_world: typing.Tuple[float, float] = (0,0)
        self.curr_mouse_position = pygame.mouse.get_pos()

        self.next_state_inquiry: AState = None
    
    def create_mouse_callback_list(self) -> MouseCallbackList:
        raise NotImplementedError(self.initialize_mouse_callback_list, self.__class__)

    def concrete_update_keyboard_control(self):
        pass

    def concrete_update_camera(self):
        raise NotImplementedError(self.concrete_update_camera, self.__class__)

    def default_update_camera(self):
        self.cam.update_physical_movement()
        self.cam.keep_camera_in_bounds(self.screen)

    def update_mouse_position(self):
        self.curr_mouse_position = self.mouse.curr_mouse_position
        self.mouse_pos_in_world = self.transform.get_transformed_isometric_world_position(self.curr_mouse_position[0],self.curr_mouse_position[1])

    def tick(self):
        raise NotImplementedError(self.tick, self.__class__)

    def state_update(self):
        self.concrete_update_keyboard_control()
        self.concrete_update_camera()
        self.update_mouse_position()
        self.tick()
    
    def state_render(self):
        self.concrete_render(self.screen)

    def concrete_render(self, screen: pygame.Surface):
        raise NotImplementedError(self.concrete_render, self.__class__)

    def set_inquiry_next_state(self, next_state):
        self.next_state_inquiry = next_state
    
    def remove_next_state_inquiry(self):
        self.next_state_inquiry = None