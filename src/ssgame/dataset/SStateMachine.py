from .. import AState

class SStateMachine:
    def __init__(self, currentState = None):
        self.currentState: AState = currentState

instance: SStateMachine = None