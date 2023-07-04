from CustomExceptions import InvalidBuildError, InvalidMoveError
class MoveCommand:
    def __init__(self, game, player, piece_no, direction):
        self._game = game
        self._player = player 
        self._piece_no = piece_no
        self._direction = direction        
        
    def __call__(self):                
        piece = self._player.get_piece(self._piece_no)
        try:            
            old_pos = piece.get_position()
            new_pos = self._game.check_movable(old_pos, self._direction)
            if new_pos:                
                piece.set_position(new_pos)                
                self._game.update_board(piece, new_pos, old_pos)                        
            else:            
                raise InvalidMoveError() 
        except InvalidMoveError:
            raise
    
class BuildCommand:
    def __init__(self, game, player, piece_no, direction):
        self._game = game
        self._player = player
        self._piece_no = piece_no
        self._direction = direction    
    
    def __call__(self):
        piece = self._player.get_piece(self._piece_no)
        try:
            self._game.build_adjacent(piece, self._direction)
        except InvalidBuildError:
            raise