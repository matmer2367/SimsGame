import game_data

def run():
    camera: game_data.SCamera.SCamera = game_data.SCamera.instance
    assert camera is not None
    assert camera.map is not None
    assert camera.transform is not None
    assert camera.isometricMapRenderer is not None

    camera_drag_controller: game_data.SCameraDragController.SCameraDragController = game_data.SCameraDragController.instance
    assert camera_drag_controller is not None
    assert camera_drag_controller.cam is not None
    assert camera_drag_controller.mouse is not None

    transform: game_data.SIsometricTransform.SIsometricTransform = game_data.SIsometricTransform.instance
    assert transform is not None
    assert transform.cam is not None
    assert transform.map is not None

    map: game_data.SMap.SMap = game_data.SMap.instance
    assert map is not None

    mouse: game_data.SMouse.SMouse = game_data.SMouse.instance
    assert mouse is not None
    assert mouse.camera_drag_controller is not None

    state_machine: game_data.SStateMachine.SStateMachine = game_data.SStateMachine.instance
    assert state_machine is not None

    isometric_map_renderer: game_data.SIsometricMapRenderer.SIsometricMapRenderer = game_data.SIsometricMapRenderer.instance
    assert isometric_map_renderer is not None
    assert isometric_map_renderer.cam is not None
    assert isometric_map_renderer.transform is not None
    assert isometric_map_renderer.map is not None
    