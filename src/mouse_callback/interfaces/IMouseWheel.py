class IMouseWheel:
    def mouse_wheel(self, y: int) -> None:
        raise NotImplementedError(self.mouse_wheel, self.__class__)