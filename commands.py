from CustomExceptions import InvalidBuildError, InvalidMoveError
class MoveCommand:
    def __init__(self, player, piece_no, direction):
        self._player = player
        self._piece_no = piece_no
        self._direction = direction
        self.memento = None
        
    def __call__(self):
        piece = self._player.get_piece(self._piece_no)
        try:
            piece.change_position(self._direction)
        except InvalidMoveError:
            raise
    
class BuildCommand:
    def __init__(self, player, piece_no, direction):
        self._player = player
        self._piece_no = piece_no
        self._direction = direction
        self.memento = None
    
    def __call__(self):
        piece = self._player.get_piece(self._piece_no)
        try:
            piece.build_adjacent(self._direction)
        except InvalidBuildError:
            raise

