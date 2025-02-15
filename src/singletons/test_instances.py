import singletons
import singletons.ICamera
import singletons.ICameraDragController
import singletons.IMap
import singletons.IMouse
import singletons.IStateMachine
import singletons.IIsometricTransform

def run():
    camera: singletons.ICamera.ICamera = singletons.ICamera.instance
    assert camera is not None
    assert camera.map is not None
    assert camera.transform is not None

    camera_drag_controller: singletons.ICameraDragController.ICameraDragController = singletons.ICameraDragController.instance
    assert camera_drag_controller is not None
    assert camera_drag_controller.cam is not None

    transform: singletons.IIsometricTransform.IIsometricTransform = singletons.IIsometricTransform.instance
    assert transform is not None
    assert transform.cam is not None
    assert transform.map is not None

    map: singletons.IMap.IMap = singletons.IMap.instance
    assert map is not None

    mouse: singletons.IMouse.IMouse = singletons.IMouse.instance
    assert mouse is not None
    assert mouse.camera_drag_controller is not None
    assert mouse.camera is not None

    state_machine: singletons.IStateMachine = singletons.IStateMachine.instance
    assert state_machine is not None
    