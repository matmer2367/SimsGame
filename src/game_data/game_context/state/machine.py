from . import State

class StateMachine:
    def __init__(self,
                 currentState: State = None):
        self.currentState = currentState