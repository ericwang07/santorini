import sys
import abc
import random
from CustomExceptions import InvalidBuildError, InvalidDirectionError, InvalidMoveError, InvalidWorkerError, DifferentColorWorkerError
from commands import MoveCommand, BuildCommand

class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def display_prompt(self, manager, score_display):
        pass
    def _check_game_end(self, manager):
        climb_winner = manager.board.check_climb_winner()
        if climb_winner:
            print(climb_winner + " has won")
            sys.exit(0)
        else:
            if manager.turn % 2 == 1:
                possible_actions = manager.board.generate_possible_actions("white")
                if not possible_actions:
                    print("blue has won")
                    sys.exit(0)                
            elif manager.turn % 2 == 0:
                possible_actions = manager.board.generate_possible_actions("blue")
                if not possible_actions:
                    print("white has won")
                    sys.exit(0)
        return possible_actions
    
class HumanStrategy(Strategy):
    def display_prompt(self, manager, score_display):
        print(manager.board)
                
        info_str = ""
        if manager.turn % 2 == 1:
            info_str += "Turn: " + str(manager.turn) + ", white (AB)"
            if score_display:
                info_str += manager.board.display_scores("white")
        else:
            info_str += "Turn: " + str(manager.turn) + ", blue (YZ)"
            if score_display:
                info_str += manager.board.display_scores("blue")        
        print(info_str)
        
        self._check_game_end(manager)
        
        piece_no = self._character_selection_prompt(manager.turn)
        
        while(True):            
            try:                            
                move_direction = self._move_prompt()                 
                if manager.turn % 2 == 1:                    
                    manager.white_player.move = MoveCommand(manager.white_player, piece_no, move_direction)
                    manager.white_player.move()    
                    # manager.white_player.move(piece_no, move_direction)                   
                else:
                    manager.blue_player.move = MoveCommand(manager.blue_player, piece_no, move_direction)
                    manager.blue_player.move()
                    # manager.blue_player.move(piece_no, move_direction)                
                break
            except InvalidDirectionError:                
                print("Not a valid direction")  
                continue
            except InvalidMoveError:
                print("Cannot move " + move_direction)
                continue
        
        while(True):                    
            try:                
                build_direction = self._build_prompt()
                if manager.turn % 2 == 1:
                    manager.white_player.build = BuildCommand(manager.white_player, piece_no, build_direction)
                    manager.white_player.build()    
                    # manager.white_player.build(piece_no, build_direction)                
                else:
                    manager.blue_player.build = BuildCommand(manager.blue_player, piece_no, build_direction)
                    manager.blue_player.build()
                    # manager.blue_player.build(piece_no, build_direction)                     
                break
            except InvalidDirectionError:                
                print("Not a valid direction")      
                continue    
            except InvalidBuildError:
                print("Cannot build " + build_direction)
                continue
        
        manager.turn += 1    
            
    def _character_selection_prompt(self, turn):                
        piece = None
        while not piece:
            print("Select a worker to move")            
            try:            
                dummy = input()
                if turn % 2 == 1:
                    if dummy == "Y" or dummy == "Z":
                        raise DifferentColorWorkerError()
                    elif dummy == "A" or dummy == "B":
                        piece = dummy                
                    else:
                        raise InvalidWorkerError()
                else:
                    if dummy == "A" or dummy == "B":
                        raise DifferentColorWorkerError()
                    elif dummy == "Y" or dummy == "Z":
                        piece = dummy                
                    else:
                        raise InvalidWorkerError()
            except DifferentColorWorkerError:
                print("That is not your worker")
            except InvalidWorkerError:
                print("Not a valid worker")        
        return 0 if (piece == "A" or piece == "Y") else 1
    
    def _move_prompt(self):                     
        print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")        
        move_direction = input()
        direction_choices = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
        if move_direction not in direction_choices:
            raise InvalidDirectionError()                            
                      
        return move_direction
                
    def _build_prompt(self):        
        print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
        build_direction = input()
        direction_choices = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
        if build_direction not in direction_choices:
            raise InvalidDirectionError()            
        
        return build_direction

class RandomStrategy(Strategy):
    def display_prompt(self, manager, score_display):
        print(manager.board)
        
        info_str = ""
        if manager.turn % 2 == 1:
            info_str += "Turn: " + str(manager.turn) + ", white (AB)"
            if score_display:
                info_str += manager.board.display_scores("white")
        else:
            info_str += "Turn: " + str(manager.turn) + ", blue (YZ)"
            if score_display:
                info_str += manager.board.display_scores("blue")        
        print(info_str)                             
        
        possible_actions = self._check_game_end(manager)
        
        (piece_letter, move_direction, build_direction) = random.choice(possible_actions)        
        
        if manager.turn % 2 == 1:
            piece_no = 0 if piece_letter == "A" else 1
        else:
            piece_no = 0 if piece_letter == "Y" else 1
        
        
        if manager.turn % 2 == 1:
            manager.white_player.move = MoveCommand(manager.white_player, piece_no, move_direction)
            manager.white_player.move()
            
            manager.white_player.build = BuildCommand(manager.white_player, piece_no, build_direction)
            manager.white_player.build()
            # manager.white_player.move(piece_no, move_direction)                            
            # manager.white_player.build(piece_no, build_direction)                        
        else:
            manager.blue_player.move = MoveCommand(manager.blue_player, piece_no, move_direction)
            manager.blue_player.move()
            
            manager.blue_player.build = BuildCommand(manager.blue_player, piece_no, build_direction)
            manager.blue_player.build()
            # manager.blue_player.move(piece_no, move_direction)          
            # manager.blue_player.build(piece_no, build_direction)                                    
        
        print(f"{piece_letter},{move_direction},{build_direction}")
                
        manager.turn += 1    
    
class HeuristicStrategy(Strategy):
    def display_prompt(self, manager, score_display):
        print(manager.board)
        
        info_str = ""
        if manager.turn % 2 == 1:
            info_str += "Turn: " + str(manager.turn) + ", white (AB)"
            if score_display:
                info_str += manager.board.display_scores("white")
        else:
            info_str += "Turn: " + str(manager.turn) + ", blue (YZ)"
            if score_display:
                info_str += manager.board.display_scores("blue")
        print(info_str)                         
        
        possible_actions = self._check_game_end(manager)
        
        if manager.turn % 2 == 1:            
            player = "white"
        else:            
            player = "blue"
            
        best_action = manager.board.choose_best_action(player, possible_actions)        
        
        (piece_letter, move_direction, build_direction) = best_action
                
        if manager.turn % 2 == 1:
            piece_no = 0 if piece_letter == "A" else 1
            # print("piece no: " + str(piece_no))
            manager.white_player.move(piece_no, move_direction)                
            manager.white_player.build(piece_no, build_direction)                        
        else:
            piece_no = 0 if piece_letter == "Y" else 1
            manager.blue_player.move(piece_no, move_direction)          
            manager.blue_player.build(piece_no, build_direction)                                                     
        
        print(f"{piece_letter},{move_direction},{build_direction}")
        manager.turn += 1    