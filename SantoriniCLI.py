import sys
from board import Board
from player import Player
from strategy import HumanStrategy, RandomStrategy, HeuristicStrategy

class GameManager():
    def __init__(self):
        self.board = Board() 
        self.turn = 1                
        pieces = self.board.get_pieces()
        white_pieces, blue_pieces = pieces[0], pieces[1]        
        self.white_player = Player(white_pieces)
        self.blue_player = Player(blue_pieces)
        
        if sys.argv[1] == "human":                                    
            self.white_strategy = HumanStrategy()            
        elif sys.argv[1] == "random":            
            self.white_strategy = RandomStrategy()
        elif sys.argv[1] == "heuristic":            
            self.white_strategy = HeuristicStrategy()
                               
        if sys.argv[2] == "human":                        
            self.blue_strategy = HumanStrategy()
        elif sys.argv[2] == "random":            
            self.blue_strategy = RandomStrategy()
        elif sys.argv[2] == "heuristic":
            self.blue_strategy = HeuristicStrategy()
        
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
            if self.turn % 2 == 1:
                self.white_strategy.display_prompt(self, self.score_display)
            else:
                self.blue_strategy.display_prompt(self, self.score_display)


            
if __name__ == "__main__":
    GameManager().run()