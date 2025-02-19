class CameraInputControlValues:
    def __init__(self,
                 scale_step = 1,
                 keyboard_movement_speed = 1,
                 scale_cap_min = 1,
                 scale_cap_max = 30):
        self.scale_step = scale_step
        self.keyboard_movement_speed = keyboard_movement_speed
        self.scale_cap_min = scale_cap_min
        self.scale_cap_max = scale_cap_max

        self.zoom_step_counter = (self.scale_cap_max-self.scale_cap_min)//15