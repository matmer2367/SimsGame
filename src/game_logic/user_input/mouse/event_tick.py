import pygame
from game_data.user_input.mouse.callback_list import MouseCallbackList
from game_data.user_input.mouse.positional_attributes import MousePositionalAttributes

def update_based_on_event(event: pygame.event.Event,
                          mouse_callback_list: MouseCallbackList,
                          mouse_positional_attributes: MousePositionalAttributes):
    curr_mouse_position = pygame.mouse.get_pos()

    if event.type == pygame.MOUSEWHEEL:
        for c in mouse_callback_list.mousewheel:
            c(event.y)
            
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        for c in mouse_callback_list.pressed_left_in:
            c(curr_mouse_position)
        mouse_positional_attributes.last_left_button_pressed_in_position = curr_mouse_position

    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        for c in mouse_callback_list.pressed_left_out:
            c(curr_mouse_position)

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_RIGHT:
        for c in mouse_callback_list.pressed_right_in:
            c(curr_mouse_position)
        mouse_positional_attributes.last_right_button_pressed_in_position = curr_mouse_position

    if event.type == pygame.MOUSEBUTTONUP and event.button == pygame.BUTTON_RIGHT:
        for c in mouse_callback_list.pressed_right_out:
            c(curr_mouse_position)

    if event.type == pygame.MOUSEMOTION:
        drag_movement_delta = (curr_mouse_position[0]-mouse_positional_attributes.last_left_button_pressed_in_position[0], curr_mouse_position[1]-mouse_positional_attributes.last_left_button_pressed_in_position[1])
        movement_delta = (curr_mouse_position[0]-mouse_positional_attributes.last_mouse_position[0], curr_mouse_position[1]-mouse_positional_attributes.last_mouse_position[1])
        for c in mouse_callback_list.mouse_motion:
            c(drag_movement_delta, movement_delta)
    
    mouse_positional_attributes.last_mouse_position = curr_mouse_position