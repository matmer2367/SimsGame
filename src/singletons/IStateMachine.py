from AIsometricSceneState import AIsometricSceneState

class IStateMachine:
    def __init__(self):
        self.currentState: AIsometricSceneState = None

instance: IStateMachine = None