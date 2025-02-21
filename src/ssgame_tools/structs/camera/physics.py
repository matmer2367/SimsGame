class CameraPhysicalAttributes:
    def __init__(self,
                 velocity = [0,0],
                 velocity_magnitude_threshold = .2,
                 velocity_friction_multiplier = 0.85,
                 ):
        self.velocity = velocity
        self.velocity_magnitude_threshold = velocity_magnitude_threshold
        self.velocity_friction_multiplier = velocity_friction_multiplier
        