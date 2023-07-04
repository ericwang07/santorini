import abc

class PieceFactory(abc.ABC):
    @abc.abstractmethod
    def create_piece1(self):
        pass
    
    @abc.abstractmethod
    def create_piece2(self):
        pass
        
class BlueFactory:
    def create_piece1(self):
        return PieceY()
    def create_piece2(self):
        return PieceZ()
    
class WhiteFactory:
    def create_piece1(self):
        return PieceA()
    def create_piece2(self):
        return PieceB()

class Piece:
    def __init__(self):    
        self._position = None
    
    def get_position(self):
        return self._position
    
    def set_position(self, position):
        self._position = position    
        
class PieceY(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [1, 1]
    def __str__(self):
        return "Y"

class PieceZ(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [3, 3]
    def __str__(self):
        return "Z"
    
class PieceA(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [3, 1]
    def __str__(self):
        return "A"
    
class PieceB(Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._position = [1, 3]
    def __str__(self):
        return "B"

