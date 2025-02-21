from .. import dataset

def run_test():
    camera: dataset.SCamera = dataset.SCameraInstance
    assert camera is not None
    assert camera.map is not None
    assert camera.transform is not None
    assert camera.isometricMapRenderer is not None

    camera_drag_controller: dataset.SCameraDragController = dataset.SCameraDragControllerInstance
    assert camera_drag_controller is not None
    assert camera_drag_controller.cam is not None
    assert camera_drag_controller.mouse is not None

    transform: dataset.SIsometricTransform = dataset.SIsometricTransformInstance
    assert transform is not None
    assert transform.cam is not None
    assert transform.map is not None

    map: dataset.SMap = dataset.SMapInstance
    assert map is not None

    mouse: dataset.SMouse = dataset.SMouseInstance
    assert mouse is not None
    assert mouse.camera_drag_controller is not None

    state_machine: dataset.SStateMachine = dataset.StateMachineInstance
    assert state_machine is not None

    isometric_map_renderer: dataset.SIsometricMapRenderer = dataset.SIsometricMapRendererInstance
    assert isometric_map_renderer is not None
    assert isometric_map_renderer.cam is not None
    assert isometric_map_renderer.transform is not None
    assert isometric_map_renderer.map is not None
    