from game_data.user_input.mouse.buttons_state import MouseButtonsState
from game_data.camera.physics import CameraPhysicalAttributes
from game_data.camera.transform import CameraTransform
from game_data.camera.drag import CameraDragAttributes
from game_logic.camera.physics import isFloating
from game_logic.math import vector

from game_constants import camera

def pressed_left_in(self, camera_transform: CameraTransform, camera_drag_attributes: CameraDragAttributes, camera_physical_attributes: CameraPhysicalAttributes) -> None:
    camera_drag_attributes.camera_position_when_drag_started[0] = camera_transform.x
    camera_drag_attributes.camera_position_when_drag_started[1] = camera_transform.y

    camera_physical_attributes.velocity[0] = 0
    camera_physical_attributes.velocity[1] = 0

def pressed_left_out(camera_drag_attributes: CameraDragAttributes, camera_physical_attributes: CameraPhysicalAttributes) -> None:
    if isFloating(camera_physical_attributes=camera_physical_attributes):
        camera_physical_attributes.velocity[0] = -camera_drag_attributes.drag_current_vel[0]
        camera_physical_attributes.velocity[1] = -camera_drag_attributes.drag_current_vel[1]

        camera_drag_attributes.drag_current_vel[0] = 0
        camera_drag_attributes.drag_current_vel[1] = 0

def mouse_motion(positional_delta, movement_delta, camera_drag_attributes: CameraDragAttributes, camera_transform: CameraTransform, mouse_button_state: MouseButtonsState) -> None:
    if mouse_button_state.left_button_pressed:
        camera_drag_attributes.drag_current_vel = [movement_delta[0]/camera_transform.s, movement_delta[1]/camera_transform.s]
        if vector.vector_magnitude_is_over_threshold(positional_delta, camera.DRAG_DELTA_THRESHOLD):
            camera_transform.x = camera_drag_attributes.camera_position_when_drag_started[0]-positional_delta[0]/camera_transform.s
            camera_transform.y = camera_drag_attributes.camera_position_when_drag_started[1]-positional_delta[1]/camera_transform.s