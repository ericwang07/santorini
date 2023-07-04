class Player:
    '''Moves on the board are made through this class through the Move and Build commands.'''
    def __init__(self, pieces) -> None:        
        self._pieces = pieces # players are defined by the pieces they are given
    
    # used for the command
    def get_piece(self, piece_no):
        return self._pieces[piece_no]

    def get_pieces(self):
        return self._pieces
  