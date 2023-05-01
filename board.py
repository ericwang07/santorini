import abc
from pieces import BlueFactory, WhiteFactory

class Board():
    def __init__(self) -> None:
        self._blue_factory = BlueFactory()
        self._white_factory = WhiteFactory()
        self._blue_pieces = [self._blue_factory.create_piece1(self),
                             self._blue_factory.create_piece2(self)]
        self._white_pieces = [self._white_factory.create_piece1(self),
                             self._white_factory.create_piece2(self)]        
        
        self._cells = []     
        
        for i in range(5):
            row = []
            for j in range(5):
                if i == 1 and j == 1:
                    row.append(Cell(self._blue_pieces[0]))
                elif i == 1 and j == 3:
                    row.append(Cell(self._white_pieces[1]))    
                elif i == 3 and j == 1:
                    row.append(Cell(self._white_pieces[0]))
                elif i == 3 and j == 3:
                    row.append(Cell(self._blue_pieces[1]))
                else:
                    row.append(Cell())
            self._cells.append(row)
    
    def get_pieces(self):
        return [self._white_pieces, self._blue_pieces]
    
    def update_board(self, piece, new_pos, old_pos):
        (new_x, new_y) = new_pos
        self._cells[new_x][new_y].update_cell_piece(piece)
        
        (old_x, old_y) = old_pos
        self._cells[old_x][old_y].update_cell_piece()
    
    def build(self, build_pos):
        (build_x, build_y) = build_pos
        self._cells[build_x][build_y].raise_level()

    def check_movable(self, old_pos, new_pos):                
        (old_x, old_y) = old_pos
        (new_x, new_y) = new_pos
        
        if not (0 <= new_x < 5) or not ((0 <= new_y < 5)):
            return False
        
        old_cell = self._cells[old_x][old_y]
        new_cell = self._cells[new_x][new_y]
        
        if old_cell.is_reachable(new_cell) and new_cell.is_unoccupied():
            return True
        else:
            return False
    
    def check_buildable(self, build_pos):
        (build_x, build_y) = build_pos              
        
        if not (0 <= build_x < 5) or not ((0 <= build_y < 5)):
            return False
          
        build_cell = self._cells[build_x][build_y]
        
        if build_cell.is_unoccupied() and not build_cell.is_max_height():
            return True
        else:
            return False
    
    def check_climb_winner(self):
        '''Returns the player who has won, or None if there is no winner'''
        pieces = self._blue_pieces + self._white_pieces        
        for piece in pieces:
            (piece_x, piece_y) = piece.get_position()
            occupied_cell = self._cells[piece_x][piece_y]
            if occupied_cell.is_max_height():
                return "white" if piece in self._white_pieces else "blue"
        return None
    
    def check_possible_moves(self, curr_player):
        if curr_player == "white":
            pieces = self._white_pieces
        else:
            pieces = self._blue_pieces        
        for piece in pieces:            
            piece_pos = piece.get_position()
            (piece_x, piece_y) = piece_pos
            for x_shift in [-1, 0, 1]:
                for y_shift in [-1, 0, 1]:
                    if x_shift == 0 and y_shift == 0:
                        continue
                    projected_pos = [piece_x + x_shift, piece_y + y_shift]                    
                    if self.check_movable(piece_pos, projected_pos) and self._check_possible_builds(projected_pos):                        
                        return True        
        return False
    
    def _check_possible_builds(self, pos):
        (x, y) = pos
        for x_shift in [-1, 0, 1]:
            for y_shift in [-1, 0, 1]:
                if x_shift == 0 and y_shift == 0:
                    continue
                projected_pos = [x + x_shift, y + y_shift]                
                if self.check_buildable(projected_pos):
                    return True
        return False
    
        
    def __repr__(self) -> str:
        output_table = ""
        for row in self._cells:
            formatted_row = "|"
            for col in row:
                formatted_row += str(col)
                formatted_row += "|"
            formatted_row += "\n"
            output_table += "+--+--+--+--+--+\n"
            output_table += formatted_row
        output_table += "+--+--+--+--+--+"
        return output_table
       
class Cell():
    def __init__(self, piece=None) -> None:
        self._level = 0
        self._piece = piece
        
    def __repr__(self) -> str:
        if self._piece is None:
            return str(self._level) + " "    
        return str(self._level) + str(self._piece)
    
    def update_cell_piece(self, piece=None):        
        self._piece = piece
    
    def raise_level(self):
        self._level += 1
                    
    def is_unoccupied(self):
        return (self._piece == None)
    
    def is_max_height(self):
        return self._level == 3
    
    def is_reachable(self, other):        
        return self._level >= other._level - 1



    
# class SantoriniState(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def 