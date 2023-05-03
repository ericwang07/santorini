import copy
from CustomExceptions import InvalidMoveError, InvalidBuildError

class BlueFactory:
    def create_piece1(self, board):
        return PieceY(board)
    def create_piece2(self, board):
        return PieceZ(board)
    
class WhiteFactory:
    def create_piece1(self, board):
        return PieceA(board)
    def create_piece2(self, board):
        return PieceB(board)
    
class Piece:
    def __init__(self, board):    
        self._board = board
    
    def get_position(self):
        return self._position
    
    def change_position(self, direction):
        old_position = self._position.copy()
        new_position = self.project_position(direction)
        
        if self._board.check_movable(old_position, new_position):
            self._position = new_position
            self._board.update_board(self, new_position, old_position)        
        else:            
            raise InvalidMoveError() 
               
        return (self._position, old_position)
    
    def build_adjacent(self, direction):        
        structure_position = self.project_position(direction)

        if self._board.check_buildable(self._position, structure_position):
            self._board.build(structure_position)
        else:
            raise InvalidBuildError()   
    
    def create_memento(self):
        return PieceMemento(copy.deepcopy(self._position), copy.deepcopy(self._level))
    
    def project_position(self, direction):
        new_position = self._position.copy()
        
        if direction == "n":        
            new_position[0] -= 1        
        elif direction == "s":         
            new_position[0] += 1
        elif direction == "e":
            new_position[1] += 1
        elif direction == "w":
            new_position[1] -= 1
        elif direction == "ne":
            new_position[0] -= 1
            new_position[1] += 1
        elif direction == "se":
            new_position[0] += 1
            new_position[1] += 1
        elif direction == "sw":
            new_position[0] += 1
            new_position[1] -= 1
        elif direction == "nw":
            new_position[0] -= 1
            new_position[1] -= 1
        
        return new_position
        
class PieceY(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [1, 1]
    def __str__(self):
        return "Y"

class PieceZ(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [3, 3]
    def __str__(self):
        return "Z"
    
class PieceA(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [3, 1]
    def __str__(self):
        return "A"
    
class PieceB(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [1, 3]
    def __str__(self):
        return "B"

