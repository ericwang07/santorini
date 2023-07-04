class Cell():
    def __init__(self, piece=None) -> None:
        self._level = 0
        self._piece = piece
        
    def __repr__(self) -> str:
        if self._piece is None:
            return str(self._level) + " "    
        return str(self._level) + str(self._piece)
    
    def update_piece(self, piece=None):        
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
