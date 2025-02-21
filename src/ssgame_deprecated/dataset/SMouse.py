import pygame
from ..Utils import fmath
from typing import Callable, Tuple, List
from .. import dataset
from ..mouse_callback.MouseCallbackList import MouseCallbackList

class SMouse:
    def __init__(self):
        self.camera_drag_controller = dataset.SCameraDragControllerInstance
        
        self.mouse_position_in_world = (0,0)
        self.last_left_button_pressed_in_position = self.last_right_button_pressed_in_position = self.last_mouse_position = (0,0)

        self.mouse_callback_list: MouseCallbackList = None

    def update_based_on_event(self, event: pygame.event.Event):
        curr_mouse_position = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEWHEEL:
            for c in self.mouse_callback_list.mousewheel:
                c(event.y)
             
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for c in self.mouse_callback_list.pressed_left_in:
                c(curr_mouse_position)
            self.last_left_button_pressed_in_position = curr_mouse_position

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            for c in self.mouse_callback_list.pressed_left_out:
                c(curr_mouse_position)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
            for c in self.mouse_callback_list.pressed_right_in:
                c(curr_mouse_position)
            self.last_right_button_pressed_in_position = curr_mouse_position

        if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
            for c in self.mouse_callback_list.pressed_right_out:
                c(curr_mouse_position)

        if event.type == pygame.MOUSEMOTION:
            drag_movement_delta = (curr_mouse_position[0]-self.last_left_button_pressed_in_position[0], curr_mouse_position[1]-self.last_left_button_pressed_in_position[1])
            movement_delta = (curr_mouse_position[0]-self.last_mouse_position[0], curr_mouse_position[1]-self.last_mouse_position[1])
            for c in self.mouse_callback_list.mouse_motion:
                c(drag_movement_delta, movement_delta)
        
        self.last_mouse_position = curr_mouse_position

instance: SMouse = None