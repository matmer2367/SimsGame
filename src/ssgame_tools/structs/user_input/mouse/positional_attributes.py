class MousePositionalAttributes:
    def __init__(self,
                 mouse_position_in_world = [0,0],
                 last_left_button_pressed_in_position = [0,0],
                 last_right_button_pressed_in_position = [0,0],
                 last_mouse_position = [0,0]):
        self.mouse_position_in_world = mouse_position_in_world
        self.last_left_button_pressed_in_position = last_left_button_pressed_in_position
        self.last_right_button_pressed_in_position = last_right_button_pressed_in_position
        self.last_mouse_position = last_mouse_position