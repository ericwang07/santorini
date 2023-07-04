import random
import copy
from pieces import BlueFactory, WhiteFactory
from CustomExceptions import InvalidBuildError
from iterator import SimBoardIterator
from cell import Cell

class Game():
    def __init__(self) -> None:
        self._blue_factory = BlueFactory()
        self._white_factory = WhiteFactory()
        self._blue_pieces = [self._blue_factory.create_piece1(),
                             self._blue_factory.create_piece2()]
        self._white_pieces = [self._white_factory.create_piece1(),
                             self._white_factory.create_piece2()]        
        self._board = []             
        
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
            self._board.append(row) 
    
    def update_board(self, piece, new_pos, old_pos):
        '''Reflects a piece's movement on the board.'''
        # Put the piece on its new position
        (new_x, new_y) = new_pos
        self._board[new_x][new_y].update_piece(piece)
        
        # Remove the piece from its previous position
        (old_x, old_y) = old_pos
        self._board[old_x][old_y].update_piece()
    
    def build_adjacent(self, piece, direction):
        '''Builds a given piece in a given direction. Raises an exception if not buildable.'''     
        piece_pos = piece.get_position()              
        if self._check_buildable(None, piece_pos, direction):
            build_pos = self.project_direction(piece_pos, direction)
            (build_x, build_y) = build_pos
            self._board[build_x][build_y].raise_level()            
        else:
            raise InvalidBuildError() 
    
    def choose_best_action(self, player, actions):
        '''Calculates the move scores of each action and returns the action with the highest score.'''
        
        pieces = player.get_pieces()
            
        best_actions = []
        max_move_score = 0
                
        for action in actions:           
            sim_board = self._generate_simulation(pieces, action)                                
            move_score = self._calculate_move_score(pieces, sim_board)                                                
            if move_score == max_move_score:
                best_actions.append(action)                
            elif move_score > max_move_score:                                
                best_actions = []
                max_move_score = move_score
                best_actions.append(action)                        
        
        # There could be multiple actions with the same highest move score. In this case, choose one randomly.
        random_best_action = random.choice(best_actions)
        
        return random_best_action
    
    def generate_possible_actions(self, player):
        '''Cycles through all possible actions (move + build) and returns a set of all possible move and build directions'''        
            
        possible_actions = [] # tuple of move and build direction combo
        pieces = player.get_pieces()
              
        for piece in pieces:            
            piece_pos = piece.get_position()            
            for direction in ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw']:                
                new_pos = self.check_movable(piece_pos, direction)
                if new_pos:
                    possible_move = direction
                    possible_builds = self._generate_possible_builds(piece_pos, new_pos)
                    if possible_builds:
                        for possible_build in possible_builds:                                
                            possible_actions.append([str(piece), possible_move, possible_build])                                                   
        return possible_actions
    
    def project_direction(self, pos, direction):
        '''Returns the new position after a simulation of a movement'''
        new_position = copy.copy(pos)                
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
    
    def check_climb_winner(self):
        '''Returns the player who has reached a level-3 structure, or None if there is no winner'''
        pieces = self._blue_pieces + self._white_pieces        
        for piece in pieces:
            (piece_x, piece_y) = piece.get_position()
            occupied_cell = self._board[piece_x][piece_y]
            if occupied_cell.is_max_climb_height():
                return "white" if piece in self._white_pieces else "blue"
        return None

    def display_scores(self, player):
        '''Displays the current formatted height, center, and distance scores.'''
        pieces = player.get_pieces()

        hcd_scores = self._calculate_hcd_scores(pieces, self._board)
        return ", " + str(hcd_scores) 
    
    def check_movable(self, old_pos, direction):
        '''Checks if the direction is movable from the current position.
           Made public to allow for the piece to move itself and then the board to update itself.'''
        new_pos = self.project_direction(old_pos, direction)
        (old_x, old_y) = old_pos
        (new_x, new_y) = new_pos        
        
        if not (0 <= new_x < 5) or not ((0 <= new_y < 5)):
            return None
        
        old_cell = self._board[old_x][old_y]
        new_cell = self._board[new_x][new_y]
        
        if old_cell.is_reachable(new_cell) and new_cell.is_unoccupied():
            return new_pos
        else:
            return None
        
    def get_pieces(self):
        '''Getter function to return the pieces for Player construction.'''
        return [self._white_pieces, self._blue_pieces]
    
    def _check_buildable(self, old_pos, pos, direction):
        '''Checks if a direction is buildable from a post-move position.
           Takes in the position pre-move to allow for edge case.'''
        build_pos = self.project_direction(pos, direction)
        (build_x, build_y) = build_pos
        
        if not (0 <= build_x < 5) or not ((0 <= build_y < 5)):
            return False
        
        build_cell = self._board[build_x][build_y]
        
        # edge case for when the piece wants to build in the position it just left
        # treat it as unoccupied
        if old_pos and old_pos == build_pos and not build_cell.is_max_height():
            return True                    
        
        if build_cell.is_unoccupied() and not build_cell.is_max_height():
            return True
        else:
            return False
    
    def _generate_possible_builds(self, old_pos, pos):
        '''Generates all possible build directions from the current position.
           Takes in pre-move position for _check_buildable edge case.'''        
        possible_builds = []
        
        for direction in ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw']:
            if self._check_buildable(old_pos, pos, direction):
                possible_builds.append(direction)
        return possible_builds
            
    def _generate_simulation(self, pieces, action):
        '''Generates a simulation of the pieces where they are moved on the board, but their internal states are unchanged.'''
        sim_board = copy.deepcopy(self._board)
        (piece_letter, move_direction, build_direction) = action
        
        if piece_letter == "A" or piece_letter == "Y":
            piece_no = 0
        else:
            piece_no = 1
        
        piece = pieces[piece_no]
        piece_pos = piece.get_position()
        (old_x, old_y) = piece_pos
        
        projected_position = self.project_direction(piece_pos, move_direction)
        (projected_x, projected_y) = projected_position
        
        sim_board[projected_x][projected_y].update_piece(piece)
                        
        sim_board[old_x][old_y].update_piece()
        
        return sim_board               
    
    def _calculate_hcd_scores(self, pieces, sim_board):      
        '''Calculates the height, center, and distance scores and returns it as a tuple.'''          
        height_score = 0
        center_score = 0
        
        source_pieces = pieces  
        if source_pieces == self._white_pieces:
            sink_pieces = self._blue_pieces
        else:
            sink_pieces = self._white_pieces
        
        iterator = SimBoardIterator(pieces, sim_board)
        while True:
            try:
                next(iterator)
            except StopIteration:
                height_score += iterator.get_height_score()
                center_score += iterator.get_center_score()
                source1_pos = iterator.get_source1_position()
                source2_pos = iterator.get_source2_position()
                break
        
        sink1_pos =  sink_pieces[0].get_position()
        sink2_pos =  sink_pieces[1].get_position()
        
        dist_to_sink1 = min(self._distance(source1_pos, sink1_pos), self._distance(source2_pos, sink1_pos))
        dist_to_sink2 = min(self._distance(source1_pos, sink2_pos), self._distance(source2_pos, sink2_pos))
        
        distance_score = dist_to_sink1 + dist_to_sink2
        distance_score = 8 - distance_score              
        
        return (height_score, center_score, distance_score)
    
    def _calculate_move_score(self, pieces, sim_board):        
        '''Calculates the move score based on the height, center, and distance scores.'''        
        c1, c2, c3 = 3, 2, 1
        (height_score, center_score, distance_score) = self._calculate_hcd_scores(pieces, sim_board)
        return c1*height_score + c2*center_score + c3*distance_score
    
    def _distance(self, pos1, pos2):
        '''Uses the Chebyshev distance formula to calculate the distance between two positions on the board.'''
        return max(abs(pos1[0] - pos2[0]), abs(pos1[1] - pos2[1]))
    
    def __repr__(self) -> str:
        output_table = ""
        for row in self._board:
            formatted_row = "|"
            for col in row:
                formatted_row += str(col)
                formatted_row += "|"
            formatted_row += "\n"
            output_table += "+--+--+--+--+--+\n"
            output_table += formatted_row
        output_table += "+--+--+--+--+--+"
        return output_table
       