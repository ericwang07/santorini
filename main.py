import sys
from game import Game
from player import Player
from strategy import HumanStrategy, RandomStrategy, HeuristicStrategy
from memento import GameMemento, Caretaker


class GameManager():
    def __init__(self):
        self.game = Game() 
        self.turn = 1                
        self.pieces = self.game.get_pieces()
        white_pieces, blue_pieces = self.pieces[0], self.pieces[1]        
        
        self.white_player = Player(white_pieces)                        
        self.blue_player = Player(blue_pieces)
        self.white_strategy = None
        self.blue_strategy = None
        
        self.undo_redo = False
        self.score_display = False
        
        if sys.argv[1] == "human":                                    
            caretaker = Caretaker(self)
            self.white_strategy = HumanStrategy(caretaker)            
        elif sys.argv[1] == "random":            
            self.white_strategy = RandomStrategy()
        elif sys.argv[1] == "heuristic":            
            self.white_strategy = HeuristicStrategy()
                               
        if sys.argv[2] == "human":                        
            self.blue_strategy = HumanStrategy(caretaker)
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
                self.white_strategy.display_prompt(self)
            else:
                self.blue_strategy.display_prompt(self)
    
    # Public methods for interaction with the caretaker
    def set_game(self, game):
        self.game = game
    
    def set_turn(self, turn):
        self.turn = turn
        
    def set_white_player(self, player):
        self.white_player = player
        
    def set_blue_player(self, player):
        self.set_blue_player = player
        
    def save(self):
        return GameMemento(self.game, self.turn, self.white_player, self.blue_player)

    def restore(self, memento):
        self.game = memento.get_game()
        self.turn = memento.get_turn()
        self.white_player = memento.get_white_player()
        self.blue_player = memento.get_blue_player()

def main():    
    GameManager().run()

if __name__ == "__main__":
    main()