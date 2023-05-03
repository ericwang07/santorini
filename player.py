import abc
import sys
from CustomExceptions import InvalidBuildError, InvalidMoveError 

class Player:
    def __init__(self, pieces) -> None:        
        self._pieces = pieces # players are defined by the pieces they are given
    
    def move(self, piece_no, move_direction):
        selected_piece = self._pieces[piece_no] 
        try:
            selected_piece.change_position(move_direction)
        except InvalidMoveError:
            raise          
    
    def build(self, piece_no, build_direction):
        selected_piece = self._pieces[piece_no] 
        try:
            selected_piece.build_adjacent(build_direction)
        except InvalidBuildError:
            raise
    
    # used for the command
    def get_piece(self, piece_no):
        return self._pieces[piece_no]

    def get_piece_positions(self):
        positions = []
        for piece in self._pieces:
            positions.append(piece.get_position())
        
        return positions


# class HumanPlayer:
#     def __init__(self, board):                        
#         self._board = board        
                    
# class WhiteHumanPlayer(HumanPlayer):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         self._pieces = self._board.get_pieces()[0]
    
#     def move(self, piece_code, move_direction):        
#         # move the piece
#         if piece_code == "A":
#             selected_piece = self._pieces[0]
#         elif piece_code == "B":
#             selected_piece = self._pieces[1]                                
#         try:
#             selected_piece.change_position(move_direction)
#         except InvalidMoveError:
#             raise                                
#         # self._board.update_board(selected_piece, new_position, old_position)        
        
#     def build(self, piece_code, build_direction):
#         # build at an adjacent position
#         if piece_code == "A":
#             selected_piece = self._pieces[0]
#         elif piece_code == "B":
#             selected_piece = self._pieces[1]   
#         try:
#             selected_piece.build_adjacent(build_direction)
#         except InvalidBuildError:
#             raise
        
# class BlueHumanPlayer(HumanPlayer):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)
#         self._pieces = self._board.get_pieces()[1]
        
#     def move(self, piece_code, move_direction):        
#         if piece_code == "Y":
#             selected_piece = self._pieces[0]
#         elif piece_code == "Z":
#             selected_piece = self._pieces[1]        
                
#         try:
#             selected_piece.change_position(move_direction)
#         except InvalidMoveError:
#             raise        
                
#         # self._board.update_board(selected_piece, new_position, old_position)

#     def build(self, piece_code, build_direction):
#         # build at an adjacent position
#         if piece_code == "Y":
#             selected_piece = self._pieces[0]
#         elif piece_code == "Z":
#             selected_piece = self._pieces[1]   
            
#         try:
#             selected_piece.build_adjacent(build_direction)
#         except InvalidBuildError:
#             raise
    
# class RandomPlayer:
#     def __init__(self, board):                        
#         self._board = board  
        
# class WhiteRandomPlayer(RandomPlayer):
    

    
        
# class MoveCommand:
#     def __init__(self, piece, move_direction, build_direction, player) -> None:
#         self._player = player
#         self._piece = piece
#         self._move_direction = move_direction
#         self._build_direction = build_direction
        

#     def __call__(self): 
#         (new_position, old_position) = self._piece.change_position()
        
#         self._player._board.update_board(self._piece, new_position, old_position)
        
    