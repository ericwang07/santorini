from board import Board
from pieces import BlueFactory, WhiteFactory
class SantoriniSet:
    def __init__(self):        
        
        self._board = Board(self._blue_pieces, self._white_pieces)
        
    def display_board(self):
        return self._board
    # def update(self, piece, move_direction, build_direction):
    #     if self._turn_count % 2 == 1:            
    #         if piece == "A":
    #             self._white_pieces[0].move()
    #         if piece == "B":
    def get_pieces(self):
        return [self._white_pieces, self._blue_pieces]
    