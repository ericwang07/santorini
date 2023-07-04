import sys
import abc
import random
from CustomExceptions import InvalidBuildError, InvalidDirectionError, InvalidMoveError, InvalidWorkerError, DifferentColorWorkerError
from commands import MoveCommand, BuildCommand

class Strategy(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def display_prompt(self, manager):        
        pass
    
    def _show_turn_info(self, manager):
        '''Displays the turn count, the current active player, and their pieces.'''
        print(manager.game)
                
        info_str = ""
        if manager.turn % 2 == 1:
            info_str += "Turn: " + str(manager.turn) + ", white (AB)"
            if manager.score_display:
                info_str += manager.game.display_scores(manager.white_player)
        else:
            info_str += "Turn: " + str(manager.turn) + ", blue (YZ)"
            if manager.score_display:
                info_str += manager.game.display_scores(manager.blue_player)        
        print(info_str)
    
    def _check_game_end(self, manager):
        '''Checks for a game winner through two ways: climbing and no possible actions.'''
        climb_winner = manager.game.check_climb_winner()
        if climb_winner:
            print(climb_winner + " has won")
            sys.exit(0)
        else:
            if manager.turn % 2 == 1:
                possible_actions = manager.game.generate_possible_actions(manager.white_player)
                if not possible_actions:
                    print("blue has won")
                    sys.exit(0)                
            elif manager.turn % 2 == 0:
                possible_actions = manager.game.generate_possible_actions(manager.blue_player)
                if not possible_actions:
                    print("white has won")
                    sys.exit(0)
        return possible_actions
    
    def _unvalidated_move_and_build(self, manager, piece_letter, move_direction, build_direction):
        '''Move and build commands for Random and Heuristic strategies.'''
        if manager.turn % 2 == 1:
            piece_no = 0 if piece_letter == "A" else 1
        else:
            piece_no = 0 if piece_letter == "Y" else 1
        if manager.turn % 2 == 1:
            piece_no = 0 if piece_letter == "A" else 1
            # print("piece no: " + str(piece_no))
            manager.white_player.move = MoveCommand(manager.game, manager.white_player, piece_no, move_direction)
            manager.white_player.move()
            
            manager.white_player.build = BuildCommand(manager.game, manager.white_player, piece_no, build_direction)
            manager.white_player.build()
        else:
            piece_no = 0 if piece_letter == "Y" else 1
            manager.blue_player.move = MoveCommand(manager.game, manager.blue_player, piece_no, move_direction)
            manager.blue_player.move()
            
            manager.blue_player.build = BuildCommand(manager.game, manager.blue_player, piece_no, build_direction)
            manager.blue_player.build()

class HumanStrategy(Strategy):
    def __init__(self, caretaker) -> None:
        super().__init__()
        # caretaker used to support undo/redo functionality
        self._caretaker = caretaker
        
    def display_prompt(self, manager):
        '''Displays a series of prompts that ask the user for piece, move, and build information.'''
        self._show_turn_info(manager)        
        self._check_game_end(manager)
        
        if self._undo_redo_prompt(manager) == True:
            return       
        
        piece_no = self._character_selection_prompt(manager.turn)

        self._caretaker.backup()

        self._move_prompt(manager, piece_no)
        self._build_prompt(manager, piece_no) 
        
        manager.turn += 1
            
    def _character_selection_prompt(self, turn):  
        '''Asks the user to select a worker to move. Includes input validation.'''              
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
    
    def _move_prompt(self, manager, piece_no):       
        '''Asks the user to select a direction to move. Includes input validation.'''                                    
        while(True):            
            try:                            
                print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")        
                move_direction = input()
                direction_choices = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]                
                if move_direction not in direction_choices:
                    raise InvalidDirectionError()                               
                if manager.turn % 2 == 1:                    
                    manager.white_player.move = MoveCommand(manager.game, manager.white_player, piece_no, move_direction)
                    manager.white_player.move()    
                    # manager.white_player.move(piece_no, move_direction)                   
                else:
                    manager.blue_player.move = MoveCommand(manager.game, manager.blue_player, piece_no, move_direction)
                    manager.blue_player.move()
                    # manager.blue_player.move(piece_no, move_direction)                
                break
            except InvalidDirectionError:                
                print("Not a valid direction")  
                continue
            except InvalidMoveError:
                print("Cannot move " + move_direction)
                continue
                   
    def _build_prompt(self, manager, piece_no):   
        '''Asks the user to select a direction to build. Includes input validation.'''         
        while(True):                    
            try:                
                print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
                build_direction = input()
                direction_choices = ["n", "s", "e", "w", "ne", "nw", "se", "sw"]
                if build_direction not in direction_choices:
                    raise InvalidDirectionError()
                if manager.turn % 2 == 1:
                    manager.white_player.build = BuildCommand(manager.game, manager.white_player, piece_no, build_direction)
                    manager.white_player.build()    
                    # manager.white_player.build(piece_no, build_direction)                
                else:
                    manager.blue_player.build = BuildCommand(manager.game, manager.blue_player, piece_no, build_direction)
                    manager.blue_player.build()
                    # manager.blue_player.build(piece_no, build_direction)                     
                break
            except InvalidDirectionError:                
                print("Not a valid direction")      
                continue    
            except InvalidBuildError:
                print("Cannot build " + build_direction)
                continue
    
    def _undo_redo_prompt(self, manager):
        '''Asks the user if they want to undo or redo a previous game setate.'''
        if manager.undo_redo:
            print("undo, redo, or next")
            while(True):
                response = input()
                if response == "undo":
                    self._caretaker.undo()
                    return True
                elif response == "redo":
                    self._caretaker.redo()
                    return True
                elif response == "next":
                    break
                else:
                    print("Please enter a valid option.")
            return False

class RandomStrategy(Strategy):
    def display_prompt(self, manager):        
        '''Generates all possible choices and chooses a random action (move and buiild) to execute.'''
        self._show_turn_info(manager)                             
        possible_actions = self._check_game_end(manager)
        
        (piece_letter, move_direction, build_direction) = random.choice(possible_actions)        
        
        self._unvalidated_move_and_build(manager, piece_letter, move_direction, build_direction)
                
        print(f"{piece_letter},{move_direction},{build_direction}")                
        manager.turn += 1    
    
class HeuristicStrategy(Strategy):    
    def display_prompt(self, manager):
        '''Generates all possible choices and chooses the best action (move and buiild) to execute.'''
        self._show_turn_info(manager)                                 
        possible_actions = self._check_game_end(manager)
        
        if manager.turn % 2 == 1:            
            player = manager.white_player
        else:            
            player = manager.blue_player
        
        # Selects the best action of all the possible actions 
        best_action = manager.game.choose_best_action(player, possible_actions)        
                
        (piece_letter, move_direction, build_direction) = best_action
                
        self._unvalidated_move_and_build(manager, piece_letter, move_direction, build_direction)                                                    
        
        print(f"{piece_letter},{move_direction},{build_direction}")
        manager.turn += 1    