import math
import pygame

from game_data.game_context.world.game_map.map_metadata import MapMetaData
from game_data.rendering.viewport.viewport_dimensions import ViewportDimensions
from game_logic.math import isometric_transformations

from game_data.camera.movement_bounds import CameraMovementBounds
from game_data.camera.transform import CameraTransform
from game_data.camera.physics import CameraPhysicalAttributes
from game_data.camera.input_control_values import CameraInputControlValues

from . import physics
    
def keep_camera_in_bounds(map_metadata: MapMetaData, viewport_dimensions: ViewportDimensions, camera_transform: CameraTransform, camera_physical_attributes: CameraPhysicalAttributes, camera_movement_bounds: CameraMovementBounds):
    isometric_transformations.update_cam_restriction_box(map_metadata=map_metadata, camera_transform=camera_transform, camera_movement_bounds=camera_movement_bounds, viewport_dimensions=viewport_dimensions)
    screen_width = viewport_dimensions.pixel_width
    screen_height = viewport_dimensions.pixel_height

    if camera_transform.x+screen_width/camera_transform.s <= camera_movement_bounds.right/camera_transform.s:
        camera_physical_attributes.velocity[0] = 0
        camera_transform.x = (camera_movement_bounds.right-screen_width)/camera_transform.s

    if camera_transform.y+screen_height/camera_transform.s <= camera_movement_bounds.bottom/camera_transform.s:
        camera_physical_attributes.velocity[0] = 0
        camera_transform.y = (camera_movement_bounds.bottom-screen_height)/camera_transform.s

    if camera_transform.x >= camera_movement_bounds.left/camera_transform.s:
        camera_physical_attributes.velocity[0] = 0
        camera_transform.x = camera_movement_bounds.left/camera_transform.s

    if camera_transform.y >= camera_movement_bounds.up/camera_transform.s:
        camera_physical_attributes.velocity[0] = 0
        camera_transform.y = camera_movement_bounds.up/camera_transform.s

def update_physical_movement(camera_transform: CameraTransform, camera_physical_attributes: CameraPhysicalAttributes):
    if physics.isFloating(camera_physical_attributes=camera_physical_attributes):
        camera_transform.x += camera_physical_attributes.velocity[0]
        camera_physical_attributes.velocity[0] *= camera_physical_attributes.velocity_friction_multiplier

        camera_transform.y += camera_transform.velocity[1]
        camera_physical_attributes.velocity[1] *= camera_physical_attributes.velocity_friction_multiplier
    else:
        camera_physical_attributes.velocity = [0,0]

def update_mousewheel_zoom(zoom_factor: int, camera_transform: CameraTransform, camera_input_control_values: CameraInputControlValues):
    cam_zoom_multiplier = math.floor(camera_transform.s*.3)
    if cam_zoom_multiplier >= 1:
        camera_input_control_values.zoom_step_counter += zoom_factor*cam_zoom_multiplier
    else:
        camera_input_control_values.zoom_step_counter += zoom_factor

    if camera_input_control_values.zoom_step_counter < camera_input_control_values.scale_cap_min//camera_input_control_values.scale_step:
        camera_input_control_values.zoom_step_counter = camera_input_control_values.scale_cap_min//camera_input_control_values.scale_step
    if camera_input_control_values.zoom_step_counter > camera_input_control_values.scale_cap_max//camera_input_control_values.scale_step:
        camera_input_control_values.zoom_step_counter = camera_input_control_values.scale_cap_max//camera_input_control_values.scale_step
    
    camera_transform.s = camera_input_control_values.zoom_step_counter*camera_input_control_values.scale_step

def cam_size_conversion(self, x, y):
    return x*self.cam.s, y*self.cam.s

def cam_size_conversion_tuple(self, pos):
    x, y = pos
    return x*self.cam.s, y*self.cam.s