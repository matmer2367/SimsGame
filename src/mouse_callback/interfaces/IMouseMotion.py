from typing import Tuple

class IMouseMotion:
    def mouse_motion(self, positional_delta: Tuple[int, int]) -> None:
        raise NotImplementedError(self.mouse_motion, self.__class__)