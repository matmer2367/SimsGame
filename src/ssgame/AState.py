import pygame
from . import dataset

import typing

from mouse_callback.MouseCallbackList import MouseCallbackList

class AState:
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface = screen
        self.cam = dataset.SCameraInstance
        self.transform = dataset.SIsometricTransformInstance
        
        self.mouse = dataset.SMouseInstance
        self.mouse_callback_list = self.create_mouse_callback_list()

        self.mouse_pos_in_world: typing.Tuple[float, float] = (0,0)
        self.curr_mouse_position = pygame.mouse.get_pos()

        self.next_state_inquiry: AState = None
    
    def create_mouse_callback_list(self) -> MouseCallbackList:
        return MouseCallbackList()

    def update_keyboard_control(self):
        pass

    def update_camera(self):
        self.cam.update_physical_movement()
        self.cam.keep_camera_in_bounds(self.screen)

    def update_mouse_position(self):
        self.curr_mouse_position = pygame.mouse.get_pos()
        self.mouse_pos_in_world = self.transform.get_transformed_isometric_world_position(self.curr_mouse_position[0],self.curr_mouse_position[1])

    def update(self):
        self.update_keyboard_control()
        self.update_camera()
        self.update_mouse_position()
    
    def render(self, screen: pygame.Surface):
        screen.fill((0,0,0))

    def set_next_state_inquiry(self, next_state):
        self.next_state_inquiry = next_state
    
    def remove_next_state_inquiry(self):
        self.next_state_inquiry = None