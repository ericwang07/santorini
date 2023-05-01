import sys
import abc
from board import Board
from player import WhiteHumanPlayer, BlueHumanPlayer
from CustomExceptions import DifferentColorWorkerError, InvalidDirectionError, InvalidWorkerError, InvalidBuildError, InvalidMoveError

class GameManager():
    def __init__(self):
        self.board = Board() 
        self.turn = 1
        self.white_strategy = None
        self.blue_strategy = None
        self.state = None
        
        # state will depend on argv[1] and 2
        
        self.state = HumanWhiteTurn()
        
        if sys.argv[1] == "human":            
            self.white_player = WhiteHumanPlayer(self.board)
            self.white_strategy = HumanWhiteTurn()
            self.state = self.white_strategy
        # elif sys.argv[1] == "random":
        #     self.white_player = WhiteRandomPlayer(self.board)
                               
        if sys.argv[2] == "human":            
            self.blue_player = BlueHumanPlayer(self.board)
            self.blue_strategy = HumanBlueTurn()
        
        if sys.argv[3] == "on":
            self.undo_redo = True
        elif sys.argv[3] == "off":
            self.undo_redo = False
        else:
            raise Exception("Undo/Redo only takes 'on' or 'off'.")
        
        if sys.argv[4] == "on":
            self.score_display = True
        elif sys.argv[4] == "off":
            self.score_display = False
        else:
            raise Exception("Score display only takes 'on' or 'off'.")                                                

    def run(self):        
        while(True):
            self.state.display_prompt(self)
        
        # while(True):
        #     self._start_turn()


class GameState(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def display_prompt():
        pass
    
class HumanTurn(GameState):
    def _move_prompt(self):                     
        print("Select a direction to move (n, ne, e, se, s, sw, w, nw)")        
        move_direction = input()
        if move_direction not in ["n", "ne", "e", "se", "s", "sw", "w", "nw"]:
            raise InvalidDirectionError()                            
                      
        return move_direction
                
    def _build_prompt(self):        
        print("Select a direction to build (n, ne, e, se, s, sw, w, nw)")
        build_direction = input()
        if build_direction not in ["n", "ne", "e", "se", "s", "sw", "w", "nw"]:
            raise InvalidDirectionError()            
        
        return build_direction
            
        
class HumanWhiteTurn(HumanTurn):
    def display_prompt(self, manager):
        print(manager.board)
        print("Turn: " + str(manager.turn) + ", white (AB)")                             
        self._check_winner(manager)
        
        piece = self._character_selection_prompt()
        
        while(True):            
            try:                            
                move_direction = self._move_prompt()        
                manager.white_player.move(piece, move_direction)                
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
                manager.white_player.build(piece, build_direction)
                break
            except InvalidDirectionError:                
                print("Not a valid direction")      
                continue    
            except InvalidBuildError:
                print("Cannot build " + build_direction)
                continue
                
                
        manager.turn += 1
        manager.state = manager.blue_strategy
    
    def _check_winner(self, manager):
        winner = manager.board.check_climb_winner()
        if winner:
            print(winner + "has won")
            sys.exit(0)
        else:
            if not manager.board.check_possible_moves("white"):
                print("blue has won")
                sys.exit(0)
            
    def _character_selection_prompt(self):        
        # enter assert statements for input validation
        piece = None
        while not piece:
            print("Select a worker to move")
            try:            
                dummy = input()
                if dummy == "Y" or dummy == "Z":
                    raise DifferentColorWorkerError()
                elif dummy == "A" or dummy == "B":
                    piece = dummy                
                else:
                    raise InvalidWorkerError()
            except DifferentColorWorkerError:
                print("That is not your worker")
            except InvalidWorkerError:
                print("Not a valid worker")
        return piece


class HumanBlueTurn(HumanTurn):
    def display_prompt(self, manager):
        print(manager.board)
        print("Turn: " + str(manager.turn) + ", blue (YZ)")                             
        self._check_winner(manager)
        
        piece = self._character_selection_prompt()        
                   
        while(True):            
            try:                            
                move_direction = self._move_prompt()        
                manager.blue_player.move(piece, move_direction)                
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
                manager.blue_player.build(piece, build_direction)
                break
            except InvalidDirectionError:                
                print("Not a valid direction")      
                continue    
            except InvalidBuildError:
                print("Cannot build " + build_direction)
                continue
        
        manager.turn += 1
        manager.state = manager.white_strategy
        
    def _check_winner(self, manager):
        winner = manager.board.check_climb_winner()
        if winner:
            print(winner + "has won")
            sys.exit(0)
        else:
            if not manager.board.check_possible_moves("blue"):
                print("white has won")
                sys.exit(0)
            
        
    def _character_selection_prompt(self):
        piece = None
        while not piece:
            print("Select a worker to move")
            try:            
                dummy = input()
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
        return piece
    
       
        
    
            
if __name__ == "__main__":
    GameManager().run()