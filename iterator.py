class SimBoardIterator:
    '''Iterator that iterates through the board, preventing the interface from seeing the details of iteration.
       Works to compute the center, height, and distance scores upon StopIteration.'''
    def __init__(self, pieces, board) -> None:
        self._board = board
        self._pieces = pieces
        self._x = 0
        self._y = 0
        self._height_score = 0
        self._center_score = 0
        self._distance_score = 0
        self._source1_pos = None
        self._source2_pos = None
        
    def __iter__(self):
        return self
        
    def __next__(self):
        if self._x >= len(self._board):
            raise StopIteration
        
        curr_cell = self._board[self._x][self._y]
        has_piece1 = curr_cell.has_piece(self._pieces[0])
        has_piece2 = curr_cell.has_piece(self._pieces[1])
        
        if has_piece1 or has_piece2:
            # Calculate the running center and height scores.
            if self._x == 2 and self._y == 2:
                self._center_score += 2
            elif self._x != 0 and self._x != 4 and self._y != 0 and self._y != 4:
                self._center_score += 1   
            
            self._height_score += curr_cell.get_level()    
            
            # Keep track of the updated source1 and source2 positions for distance score calculation
            if has_piece1:
                self._source1_pos = [self._x, self._y]
            elif has_piece2:
                self._source2_pos = [self._x, self._y]                        
                    
        self._y += 1
        if self._y >= len(self._board[self._x]):
            self._y = 0
            self._x += 1     
    
    def get_center_score(self):
        return self._center_score
    
    def get_height_score(self):
        return self._height_score
    
    def get_source1_position(self):
        return self._source1_pos
    
    def get_source2_position(self):
        return self._source2_pos