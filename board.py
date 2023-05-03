import abc
import random
import copy
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
        self._hcd_scores = None
        
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
    
    def check_buildable(self, old_move_pos, build_pos):
        (build_x, build_y) = build_pos              
        
        if not (0 <= build_x < 5) or not ((0 <= build_y < 5)):
            return False
        
        build_cell = self._cells[build_x][build_y]
        
        # edge case for when the piece wants to build in the position it just left
        # treat it as unoccupied
        if old_move_pos == build_pos and not build_cell.is_max_height():
            return True                    
        
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
            if occupied_cell.is_max_climb_height():
                return "white" if piece in self._white_pieces else "blue"
        return None    
    
    def generate_possible_actions(self, player):
        '''Cycles through all possible moves and returns a set of all possible move and build directions'''
        
        possible_actions = [] # tuple of move and build direction combo
        if player == "white":
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
                    if self.check_movable(piece_pos, projected_pos):
                        possible_move = self._convert_direction(x_shift, y_shift)
                        possible_builds = self._generate_possible_builds(piece_pos, projected_pos)
                        if possible_builds:
                            for possible_build in possible_builds:                                
                                possible_actions.append([str(piece), possible_move, possible_build])                                   
        # print("possible actions: " + str(possible_actions) + "\n")
        return possible_actions
    
    def choose_best_action(self, player, actions):
        if player == "white":
            pieces = self._white_pieces
        else:
            pieces = self._blue_pieces
        
        best_actions = []
        max_move_score = 0
        
        # print("original: " + str(self._cells))
        for action in actions:   
            # print(action)                                 
            sim_cells = self._generate_simulation(pieces, action)                                
            move_score = self._calculate_move_score(pieces, sim_cells)                        
            if move_score == max_move_score:
                best_actions.append(action)                
            elif move_score > max_move_score:
                # print("update move score: " + str(move_score))
                best_actions = []
                max_move_score = move_score
                best_actions.append(action)                        
        
        random_best_action = random.choice(best_actions)
        
        return random_best_action

    def display_scores(self, color):
        if color == "white":
            pieces = self._white_pieces
        else:
            pieces = self._blue_pieces
                    
        hcd_scores = self._calculate_hcd_scores(pieces)
        return ", " + str(hcd_scores) 
            
    def _generate_simulation(self, pieces, action):
        sim_cells = copy.deepcopy(self._cells)
        (piece_letter, move_direction, build_direction) = action
        
        if piece_letter == "A" or piece_letter == "Y":
            piece_no = 0
        else:
            piece_no = 1
        
        piece = pieces[piece_no]
        (old_x, old_y) = piece.get_position()
        
        projected_position = piece.project_position(move_direction)
        (projected_x, projected_y) = projected_position
        
        sim_cells[projected_x][projected_y].update_cell_piece(piece)
                        
        sim_cells[old_x][old_y].update_cell_piece()
        
        return sim_cells               
    
    def _calculate_move_score(self, pieces, sim_cells):
        c1, c2, c3 = 3, 2, 1
        height_score = self._calculate_height_score(pieces, sim_cells)
        center_score = self._calculate_center_score(pieces, sim_cells)
        distance_score = self._calculate_distance_score(pieces, sim_cells)
        
        # print(height_score, center_score, distance_score)
        
        return c1*height_score + c2*center_score + c3*distance_score
    
    def _calculate_hcd_scores(self, pieces):        
        height_score = self._calculate_height_score(pieces, self._cells)
        center_score = self._calculate_center_score(pieces, self._cells)
        distance_score = self._calculate_distance_score(pieces, self._cells)
        hcd_score = (height_score, center_score, distance_score)
        return hcd_score
    
    def _calculate_height_score(self, pieces, sim_cells):                
        # print("simulated :" + str(sim_cells))            
        height_score = 0
        for piece in pieces:
            for x in range(len(sim_cells)):
                for y in range(len(sim_cells)):                                        
                    if sim_cells[x][y].has_piece(piece):                                                
                        piece_cell = sim_cells[x][y]
                        # print("found " + str(piece) + f" at {x},{y}")
                        height_score += piece_cell.get_level()                            
        return height_score    

    def _calculate_center_score(self, pieces, sim_cells):        
        center_score = 0
        for piece in pieces:
            for x in range(len(sim_cells)):
                for y in range(len(sim_cells)):
                    if sim_cells[x][y].has_piece(piece):
                        # print("found " + str(piece) + f" at {x},{y}")
                        if x == 2 and y == 2:
                            center_score += 2
                        elif x != 0 and x != 4 and y != 0 and y != 4:
                            center_score += 1        
                        
        # print(center_score)
        return center_score
    
    def _calculate_distance_score(self, pieces, sim_cells):
        source_pieces = pieces
        if source_pieces == self._white_pieces:
            sink_pieces = self._blue_pieces
        else:
            sink_pieces = self._white_pieces
        
        # must look for positions of the sources in the simulation because the pieces' positions are unchanged
        # the "simulated" new position only applies to one of the sources, so we must check both
        # source1_pos = None
        # source2_pos = None
        
        for x in range(len(sim_cells)):
            for y in range(len(sim_cells)):                 
                curr_cell = sim_cells[x][y]                                                   
                if curr_cell.has_piece(source_pieces[0]):                    
                    source1_pos = [x, y]                    
                elif curr_cell.has_piece(source_pieces[1]):                    
                    source2_pos = [x, y]
                    
                    
        sink1_pos =  sink_pieces[0].get_position()
        sink2_pos =  sink_pieces[1].get_position()
        
        dist_to_sink1 = min(self._distance(source1_pos, sink1_pos), self._distance(source2_pos, sink1_pos))
        dist_to_sink2 = min(self._distance(source1_pos, sink2_pos), self._distance(source2_pos, sink2_pos))
        
        distance_score = dist_to_sink1 + dist_to_sink2
        adjusted_distance_score = 8 - distance_score
        
        return adjusted_distance_score
    
    def _distance(self, pos1, pos2):
        # use the Chebyshev distance
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
        
    def _generate_possible_builds(self, old_pos, pos):
        (x, y) = pos
        possible_builds = []
        for x_shift in [-1, 0, 1]:
            for y_shift in [-1, 0, 1]:
                if x_shift == 0 and y_shift == 0:
                    continue
                projected_pos = [x + x_shift, y + y_shift]                
                if self.check_buildable(old_pos, projected_pos):
                    possible_build = self._convert_direction(x_shift, y_shift)
                    possible_builds.append(possible_build)
        return possible_builds
        
    def _convert_direction(self, x, y):
        direction = ""
        if x == 1:
            direction += "s"
        elif x == -1:
            direction += "n"
        if y == 1:
            direction += "e"
        elif y == -1:
            direction += "w"
        
        return direction
    
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
    
    def get_level(self):
        return self._level 
    
    def raise_level(self):
        self._level += 1

    def has_piece(self, piece):
        return str(self._piece) == str(piece)
                    
    def is_unoccupied(self):
        return (self._piece == None)
    
    def is_max_height(self):
        return self._level == 4
    
    def is_max_climb_height(self):
        return self._level == 3
    
    def is_reachable(self, other):        
        return self._level >= other._level - 1



    
# class SantoriniState(metaclass=abc.ABCMeta):
#     @abc.abstractmethod
#     def 