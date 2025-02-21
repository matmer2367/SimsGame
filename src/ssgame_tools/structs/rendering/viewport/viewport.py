from ssgame_tools.structs.camera.movement_bounds import CameraMovementBounds
from ssgame_tools.structs.camera.transform import CameraTransform
from .viewport_dimensions import ViewportDimensions


class ViewPort:
    def __init__(self,
                 dimensions: ViewportDimensions = None,
                 camera_transform: CameraTransform = None,
                 camera_movement_bounds: CameraMovementBounds = None):
        self.dimensions = dimensions
        self.camera_transform = camera_transform
        self.camera_movement_bounds = camera_movement_bounds