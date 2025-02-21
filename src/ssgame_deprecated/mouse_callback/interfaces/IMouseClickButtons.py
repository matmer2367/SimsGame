class IMouseClickButtons:
    def pressed_right_in(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError(self.pressed_right_in, self.__class__)
    
    def pressed_right_out(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError(self.pressed_right_out, self.__class__)
    

    def pressed_left_in(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError(self.pressed_left_in, self.__class__)
    
    def pressed_left_out(self, pos: tuple[int, int]) -> None:
        raise NotImplementedError(self.pressed_left_out, self.__class__)