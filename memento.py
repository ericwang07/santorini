from copy import deepcopy

class Memento:
    pass
    
class GameMemento(Memento):
    def __init__(self, game, turn, white_player, blue_player) -> None:
        self._game = deepcopy(game)
        self._turn = deepcopy(turn)
        self._white_player = deepcopy(white_player)
        self._blue_player = deepcopy(blue_player)        
                
    def get_game(self):
        return self._game
    
    def get_turn(self):
        return self._turn
    
    def get_white_player(self):
        return self._white_player

    def get_blue_player(self):
        return self._blue_player
    
class Caretaker:
    def __init__(self, manager) -> None:
        self._originator = manager
        self._history = []
        self._undo_history = []
    
    def backup(self):
        '''Saves the current state of the game and adds it to the history'''
        self._history.append(self._originator.save())
    
    def undo(self):
        '''Reverses the game state to the most recent state (before the current)'''
        if not len(self._history):
            return 
        
        memento = self._history.pop()
        self._undo_history.append(self._originator.save())
        
        try:
            self._originator.restore(memento)
        except Exception:
            self.undo()
    
    def redo(self):
        '''Restores an undone state.'''
        if not len(self._undo_history):
            return
        
        recovered_memento = self._undo_history.pop()
        
        try:
            self._originator.restore(recovered_memento)
        except Exception:
            self.redo()