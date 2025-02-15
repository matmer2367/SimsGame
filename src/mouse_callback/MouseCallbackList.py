from typing import List,Callable,Tuple

class MouseCallbackList:
    def __init__(self) -> None:
        self.mousewheel: List[Callable] = []
        self.pressed_left_in: List[Callable] = []
        self.pressed_left_out: List[Callable] = []
        self.pressed_right_in: List[Callable] = []
        self.pressed_right_out: List[Callable] = []
        self.mouse_motion: List[Callable] = []
    
    def add_callbacks_to_listener(self,
                mousewheel_callback: Callable[[Tuple[int, int]],None] = None,
                mouse_pressed_left_in_callback: Callable[[Tuple[int, int]],None] = None,
                mouse_pressed_left_out_callback: Callable[[Tuple[int, int]],None] = None,
                mouse_pressed_right_in_callback: Callable[[Tuple[int, int]],None] = None,
                mouse_pressed_right_out_callback: Callable[[Tuple[int, int]],None] = None,
                mouse_motion_callback: Callable[[Tuple[int, int]],None] = None):
        if mousewheel_callback is not None:
            self.mousewheel.append(mousewheel_callback)
        if mouse_pressed_left_in_callback is not None:
            self.pressed_left_in.append(mouse_pressed_left_in_callback)
        if mouse_pressed_left_out_callback is not None:
            self.pressed_left_out.append(mouse_pressed_left_out_callback)
        if mouse_pressed_right_in_callback is not None:
            self.pressed_right_in.append(mouse_pressed_right_in_callback)
        if mouse_pressed_right_out_callback is not None:
            self.pressed_right_out.append(mouse_pressed_right_out_callback)
        if mouse_motion_callback is not None:
            self.mouse_motion.append(mouse_motion_callback)