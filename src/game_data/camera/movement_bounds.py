class CameraMovementBounds:
    def __init__(self,
                 left = 0,      #x old: left x
                 up = 0,        #y old: left y
                 right = 0,     #x old: right x
                 bottom = 0):   #y old: right y
        self.left = left
        self.up = up
        self.right = right
        self.bottom = bottom