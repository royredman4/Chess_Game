
try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import os

from Game_Initialization import Chess_Matrix, Board_Colors
from Chess_Movement import Show_Hide_Movement
Infinite_Movement = 1000



class Chess_Piece_Movement:
    
    def __init__(self, color, movements, piece_coordinates):
        self.movement = movements
        self.color = color
        self.piece_coordinates = piece_coordinates
        self.movement_coordinates = None
        self.update_move_coordinates(piece_coordinates[:])
        self.OutOfBounds = False
        self.IsBlocked = False
        
    def update_move_coordinates(self, current_coords):
        for move in self.movement:
            for direction in move:
                if ("North" in direction):
                    current_coords[1] += move[direction]
                if("South" in direction):
                    current_coords[1] -= move[direction]
                if("East" in direction):
                    current_coords[0] += move[direction]
                if ("West" in direction):
                    current_coords[0] -= move[direction]
                    
        self.movement_coordinates = current_coords
        x,y = current_coords
        self.OutOfBounds = self.Is_OutOfBounds()
        self.IsBlocked = self.Is_Blocked()
                
    def Is_OutOfBounds(self):
        x,y = self.movement_coordinates
        if (0 <= x < 8):
            if (0 <= y < 8):
                return False
        return True         

    def Is_Blocked(self):
        x,y = self.movement_coordinates
        IsBlocked = False
        isOccupied = Chess_Matrix[x][y]
        if (isOccupied == None):
            return False
        elif (isOccupied.color() != self.color()):
            return False
        else:
            IsBlocked = True
            return True
        
        
        
    def show_move(self):
        self.update_move_coordinates(self.piece_coordinates[:])
        if (self.OutOfBounds or self.IsBlocked):
            return False
        
        else:
            x,y = self.movement_coordinates
            Board_Colors[x][y].Set_Color("yellow")
            return True  
    
    def hide_move(self):
        x,y = self.movement_coordinates
        Board_Colors[x][y].Reset_Color()
    
    
class Chess_Piece:
    def __init__(self, name, color, coordinates, canvas):
        self.Piece_name = name
        self.color = color
        self.Movements_Shown = False
        
        if (self.color == "Black"):
            self.negate_coordinates = True
        else:
            self.negate_coordinates = False
            
        self.coordinates = coordinates
        self.canvas = canvas
        self.image = None
        self.img_Obj = None
        self.Create_Piece()
        
        
        self.moves = {"North":[],"East":[],"South":[],"West":[],
                  "NorthEast":[],"NorthWest":[], "SouthEast":[],"SouthWest":[]}
        self.move_counts = 0
        
    def Create_Piece(self):
        x,y = self.coordinates
        img_location = os.getcwd() + "/Chess_Pieces/%s_Pieces/%s_%s.GIF" %(self.color, self.color, self.Piece_name)
        self.image = PhotoImage(file=img_location)
        self.img_Obj = self.canvas.create_image((30+(x *60)), 450-(y * 60), image = self.image)
        
    def Remove_Piece(self):
        print("Deleting Piece Image")
        self.canvas.delete(self.img_Obj)
        
    def Move_Piece(self, new_x, new_y):
        x = (new_x - self.coordinates[0]) * 60
        y = (self.coordinates[1] - new_y) * 60
        print("Moving x by %d and y by %d" % (x, y))
        self.canvas.move(self.img_Obj, x, y)

        self.coordinates = [new_x, new_y]
    
    
    def add_move(self, direction, piece_movements):
        if (len(piece_movements) == 1 and piece_movements[0].values()[0] == Infinite_Movement):
            direction = piece_movements[0].keys()[0]
            for i in range(1,8):
                self.add_move(direction, [{direction:i}])
            
        if self.negate_coordinates:
            for movement in piece_movements:
                for direction in movement:
                    movement[direction] *= -1
                
        self.moves[direction].append(Chess_Piece_Movement(self.color, piece_movements, self.coordinates))
    
    def show_movements(self):
        for direction in self.moves.keys():
            for coordinate in direction:
                coordinate.show_move()
                
        self.Movements_Shown = True
            
    def hide_movements(self):
        for direction in self.moves.keys():
            for coordinate in direction:
                coordinate.hide_move()
                
        self.Movements_Shown = False
    
class Pawn(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "Pawn", color, coordinates, canvas)
        self.Special_Moves = self.moves.copy()
        
        self.add_move("North", [{"North":1}])
        
        if(color is "Black"):
            multiplier = -1
        else:
            multiplier = 1
            
        self.Special_Moves["NorthEast"].append(Chess_Piece_Movement(color, [{"North":1*multiplier}, {"East":1*multiplier}], coordinates))
        self.Special_Moves["NorthWest"].append(Chess_Piece_Movement(color, [{"North":1*multiplier}, {"West":1*multiplier}], coordinates))
        self.Special_Moves["North"].append(Chess_Piece_Movement(color, [{"North":2*multiplier}], coordinates))
        
        
        

class Rook(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "Rook", color, coordinates, canvas)
        self.add_move("North", [{"North":Infinite_Movement}])
        self.add_move("East", [{"East":Infinite_Movement}])
        self.add_move("South", [{"South":Infinite_Movement}])
        self.add_move("West", [{"West":Infinite_Movement}])
        
        

class Knight(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "Knight", color, coordinates, canvas)
        self.add_move("North", [{"North":2}, {"East":1}])
        self.add_move("North", [{"North":2}, {"West":1}])
        self.add_move("East", [{"East":2}, {"North":1}])
        self.add_move("East", [{"East":2}, {"South":1}])
        self.add_move("South", [{"South":2}, {"East":1}])
        self.add_move("South", [{"South":2}, {"West":1}])
        self.add_move("West", [{"West":2}, {"North":1}])
        self.add_move("West", [{"West":2}, {"South":1}])
        
        
class Bishop(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "Bishop", color, coordinates, canvas)
        self.add_move("NorthEast", [{"NorthEast":Infinite_Movement}])
        self.add_move("NorthWest", [{"NorthWest":Infinite_Movement}])
        self.add_move("SouthEast", [{"SouthEast":Infinite_Movement}])
        self.add_move("SouthWest", [{"SouthWest":Infinite_Movement}])
        
        
class Queen(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "Queen", color, coordinates, canvas)
        self.add_move("North", [{"North":Infinite_Movement}])
        self.add_move("East", [{"East":Infinite_Movement}])
        self.add_move("South", [{"South":Infinite_Movement}])
        self.add_move("West", [{"West":Infinite_Movement}])
        self.add_move("NorthEast", [{"NorthEast":Infinite_Movement}])
        self.add_move("NorthWest", [{"NorthWest":Infinite_Movement}])
        self.add_move("SouthEast", [{"SouthEast":Infinite_Movement}])
        self.add_move("SouthWest", [{"SouthWest":Infinite_Movement}])
        
        
class King(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "King", color, coordinates, canvas)
        self.add_move("North", [{"North":1}])
        self.add_move("East", [{"East":1}])
        self.add_move("South", [{"South":1}])
        self.add_move("West", [{"West":1}])
        self.add_move("NorthEast", [{"NorthEast":1}])
        self.add_move("NorthWest", [{"NorthWest":1}])
        self.add_move("SouthEast", [{"SouthEast":1}])
        self.add_move("SouthWest", [{"SouthWest":1}])
        
        