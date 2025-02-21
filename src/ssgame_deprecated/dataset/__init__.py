import pygame

from .SCamera import SCamera, instance as SCameraInstance
from .SCameraDragController import SCameraDragController, instance as SCameraDragControllerInstance
from .SIsometricMapRenderer import SIsometricMapRenderer, instance as SIsometricMapRendererInstance
from .SIsometricTransform import SIsometricTransform, instance as SIsometricTransformInstance, get_transformed_cam_on_screen_center, isometricTransform
from .SKeyboard import keys, update_keystates
from .SMap import SMap, instance as SMapInstance
from .SMouse import SMouse, instance as SMouseInstance
from .SStateMachine import SStateMachine, instance as StateMachineInstance

from .test_instances import run_test

def init(map_data, tile_Size, screen: pygame.Surface):
    global StateMachineInstance, SMapInstance, SCameraInstance, SIsometricTransformInstance, SCameraDragControllerInstance, SMouseInstance, SIsometricMapRendererInstance, SMouseInstance, SIsometricMapRendererInstance
    
    StateMachineInstance = SStateMachine()
    SMapInstance = SMap(map_data, tile_Size)
    SCameraInstance = SCamera(screen.get_width()/2,(screen.get_height()/2)+SMapInstance.height*SMapInstance.tile_size/2)
    SIsometricTransformInstance = SIsometricTransform(screen)
    SCameraDragControllerInstance = SCameraDragController()
    SMouseInstance = SMouse()
    SIsometricMapRendererInstance = SIsometricMapRenderer()
    SCameraInstance.transform = SIsometricTransformInstance
    SCameraInstance.map = SMapInstance
    SCameraInstance.isometricMapRenderer = SIsometricMapRendererInstance
    SCameraDragControllerInstance.mouse = SMouseInstance
    
    run_test()