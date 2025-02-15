from typing import List,Callable,Tuple
from mouse_callback.interfaces.IMouseClickButtons import IMouseClickButtons
from mouse_callback.interfaces.IMouseWheel import IMouseWheel
from mouse_callback.interfaces.IMouseMotion import IMouseMotion

class MouseCallbackList:
    def __init__(self) -> None:
        self.mousewheel: List[Callable] = []
        self.pressed_left_in: List[Callable] = []
        self.pressed_left_out: List[Callable] = []
        self.pressed_right_in: List[Callable] = []
        self.pressed_right_out: List[Callable] = []
        self.mouse_motion: List[Callable] = []
    
    def add_callbacks_to_listener(self,
                mousewheel_callback: Callable[[int],None] = None,
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
    
    def add_IMouseClickButtons_callbacks(self, callbacks: IMouseClickButtons):
        self.add_callbacks_to_listener(
            mouse_pressed_left_in_callback=callbacks.pressed_left_in,
            mouse_pressed_left_out_callback=callbacks.pressed_left_out,
            mouse_pressed_right_in_callback=callbacks.pressed_right_in,
            mouse_pressed_right_out_callback=callbacks.pressed_right_out
        )
    
    def add_IMouseWheel_callbacks(self, callbacks: IMouseWheel):
        self.add_callbacks_to_listener(
            mouse_motion_callback=callbacks.mouse_wheel
        )
    
    def add_IMouseMotion_callbacks(self, callbacks: IMouseMotion):
        self.add_callbacks_to_listener(
            mouse_motion_callback=callbacks.mouse_motion
        )