class CameraDragAttributes:
    def __init__(self,
                 current_velocity = [0,0],
                 camera_position_when_drag_started = [0,0]):
        self.current_velocity  = current_velocity
        self.camera_position_when_drag_started = camera_position_when_drag_started