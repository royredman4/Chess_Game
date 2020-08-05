
Infinite_Movement = 1000

class Chess_Piece_Movement:
    
    def __init__(self, movements):
        movement = movements
    
    def move(self):
        pass
    
    def show_move(self):
        pass
    
    
class Chess_Piece:
    def __init__(self, name):
        piece_name = name
        moves = {"North":[],"East":[],"South":[],"West":[],
                  "NorthEast":[],"NorthWest":[], "SouthEast":[],"SouthWest":[]}
        move_counts = 0
        
        
    def add_move(self, direction, piece_movement):
        moves[direction].append(Chess_Piece_Movement(piece_movement))
    
    def show_movements(self):
        for direction in moves.keys():
            for coordinate in direction:
                coordinate.show_move()
            
    
    
class Pawn(Chess_Piece):
    def __init__(self):
        Chess_Piece.__init__(self, "Pawn")
        Special_Moves = moves.copy()
        
        add_move("North", [{"North":1}])
        
        Special_Moves["NorthEast"].append(Chess_Piece_Movement([{"North":1}, {"East":1}]))
        Special_Moves["NorthEast"].append(Chess_Piece_Movement([{"North":1}, {"East":1}]))
        Special_Moves["North"].append(Chess_Piece_Movement([{"North":2}]))
        
        
        

class Rook(Chess_Piece):
    def __init__(self):
        Chess_Piece.__init__(self, "Rook")
        add_move("North", [{"North":Infinite_Movement}])
        add_move("East", [{"East":Infinite_Movement}])
        add_move("South", [{"South":Infinite_Movement}])
        add_move("West", [{"West":Infinite_Movement}])
        

class Knight(Chess_Piece):
    def __init__(self):
        Chess_Piece.__init__(self, "Knight")
        add_move("North", [{"North":2}, {"East":1}])
        add_move("North", [{"North":2}, {"West":1}])
        add_move("East", [{"East":2}, {"North":1}])
        add_move("East", [{"East":2}, {"South":1}])
        add_move("South", [{"South":2}, {"East":1}])
        add_move("South", [{"South":2}, {"West":1}])
        add_move("West", [{"West":2}, {"North":1}])
        add_move("West", [{"West":2}, {"South":1}])
        
        
class Bishop(Chess_Piece):
    def __init__(self):
        Chess_Piece.__init__(self, "Bishop")
        add_move("NorthEast", [{"NorthEast":Infinite_Movement}])
        add_move("NorthWest", [{"NorthWest":Infinite_Movement}])
        add_move("SouthEast", [{"SouthEast":Infinite_Movement}])
        add_move("SouthWest", [{"SouthWest":Infinite_Movement}])
        
class Queen(Chess_Piece):
    def __init__(self):
        Chess_Piece.__init__(self, "Queen")
        add_move("North", [{"North":Infinite_Movement}])
        add_move("East", [{"East":Infinite_Movement}])
        add_move("South", [{"South":Infinite_Movement}])
        add_move("West", [{"West":Infinite_Movement}])
        add_move("NorthEast", [{"NorthEast":Infinite_Movement}])
        add_move("NorthWest", [{"NorthWest":Infinite_Movement}])
        add_move("SouthEast", [{"SouthEast":Infinite_Movement}])
        add_move("SouthWest", [{"SouthWest":Infinite_Movement}])
        
class King(Chess_Piece):
    def __init__(self):
        Chess_Piece.__init__(self, "King")
        add_move("North", [{"North":1}])
        add_move("East", [{"East":1}])
        add_move("South", [{"South":1}])
        add_move("West", [{"West":1}])
        add_move("NorthEast", [{"NorthEast":1}])
        add_move("NorthWest", [{"NorthWest":1}])
        add_move("SouthEast", [{"SouthEast":1}])
        add_move("SouthWest", [{"SouthWest":1}])
        
        