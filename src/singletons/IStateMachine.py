from GameState import GameState

class IStateMachine:
    def __init__(self):
        self.currentState: GameState = None

instance: IStateMachine = None