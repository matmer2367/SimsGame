import singletons
import singletons.SCamera
import singletons.SCameraDragController
import singletons.SMap
import singletons.SMouse
import singletons.SStateMachine
import singletons.SIsometricTransform

def run():
    camera: singletons.SCamera.SCamera = singletons.SCamera.instance
    assert camera is not None
    assert camera.map is not None
    assert camera.transform is not None

    camera_drag_controller: singletons.SCameraDragController.SCameraDragController = singletons.SCameraDragController.instance
    assert camera_drag_controller is not None
    assert camera_drag_controller.cam is not None
    assert camera_drag_controller.mouse is not None

    transform: singletons.SIsometricTransform.SIsometricTransform = singletons.SIsometricTransform.instance
    assert transform is not None
    assert transform.cam is not None
    assert transform.map is not None

    map: singletons.SMap.SMap = singletons.SMap.instance
    assert map is not None

    mouse: singletons.SMouse.SMouse = singletons.SMouse.instance
    assert mouse is not None
    assert mouse.camera_drag_controller is not None

    state_machine: singletons.SStateMachine = singletons.SStateMachine.instance
    assert state_machine is not None
    