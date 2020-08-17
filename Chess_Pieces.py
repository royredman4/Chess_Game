try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import os
import copy

from Game_Initialization import Chess_Matrix, Board_Colors, White_Attack_Layout, Black_Attack_Layout
Infinite_Movement = 1000

White_King = None
Black_King = None


class Chess_Piece_Movement:
    
    def __init__(self, chess_piece, movements, piece_coordinates):
        self.movement = movements
        self.chess_piece = chess_piece    
        self.piece_coordinates = piece_coordinates
        
        self.movement_coordinates = None
        self.update_move_coordinates(piece_coordinates[:])
        self.OutOfBounds = False
        self.IsBlocked = False
        self.EnemyHit = False
        
    def update_move_coordinates(self, current_coords=None):
        if current_coords == None:
            current_coords = self.piece_coordinates[:]
            
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
        
        if (not self.Is_OutOfBounds()):
            if (not self.Is_Blocked()):
                return self
        else:
            self.IsBlocked = True
              
    def Is_OutOfBounds(self):
        x,y = self.movement_coordinates
        self.OutOfBounds = True
        
        if (0 <= x < 8):
            if (0 <= y < 8):
                self.OutOfBounds = False
                
        return self.OutOfBounds
        

    def Is_Blocked(self):
        x,y = self.movement_coordinates
        self.IsBlocked = False
        self.EnemyHit = False
        
        isOccupied = Chess_Matrix[x][y]    
            
        if (isOccupied == None):
            self.IsBlocked = False
            
        elif (isOccupied.color != self.chess_piece.color):
            self.IsBlocked = False
            self.EnemyHit = True
            
        else:
            self.IsBlocked = True
            
        return self.IsBlocked
        
        
        
    def show_move(self):
        #self.update_move_coordinates(self.piece_coordinates[:])
        if (self.OutOfBounds or self.IsBlocked):
            return False
        
        else:
            x,y = self.movement_coordinates
            Board_Colors[x][y].Set_Color("yellow")
            return True  
    
    def hide_move(self):
        x,y = self.movement_coordinates
        Board_Colors[x][y].Reset_Color()
    

'''
The default layout for all chess pieces.
'''
class Chess_Piece:
    def __init__(self, name, color, coordinates, canvas):
        self.Piece_name = name
        self.color = color
        self.movement_counter = 0
        self.Movements_Shown = False
        self.possible_moves = []
        
        
        if (self.color == "Black"):
            self.negate_coordinates = True
            self.attack_board = Black_Attack_Layout
        else:
            self.negate_coordinates = False
            self.attack_board = White_Attack_Layout
            
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
        print("Deleting Piece Image for {}:{}".format(self.color, self.Piece_name))
        self.canvas.delete(self.img_Obj)
        
    def Move_Piece(self, new_x, new_y):
        Chess_Matrix[self.coordinates[0]][self.coordinates[1]] = None
        enemy = Chess_Matrix[new_x][new_y]
        if (enemy and enemy.color != self.color):
            enemy.Remove_Piece()
            
        x = (new_x - self.coordinates[0]) * 60
        y = (self.coordinates[1] - new_y) * 60
        print("Moving x by %d and y by %d" % (x, y))
        self.canvas.move(self.img_Obj, x, y)

        self.coordinates[0], self.coordinates[1] = new_x, new_y
        Chess_Matrix[new_x][new_y] = self
        self.movement_counter += 1
        
        self.hide_movements()
        del self.possible_moves[:]
        self.Movements_Shown = False
        
        self.update_moves_list()
    
    def Move_Chosen(self, x,y):
        for movement in self.possible_moves:
            if movement.movement_coordinates == [x,y]:
                return True
            
        return False
    
    def update_moves_list(self):
        del self.possible_moves[:]
        for movement in self.moves:
            if (len(self.moves[movement]) == 0):
                continue
            for move in self.moves[movement]:         
                potential_move = move.update_move_coordinates()
                if potential_move:
                    self.possible_moves.append(potential_move)
                    x,y = potential_move.movement_coordinates
                    self.attack_board[x][y] = potential_move
                    if potential_move.EnemyHit:
                        break
                else:
                    break
    def enemy_present(self, coordinates):
        x,y = coordinates
        possible_enemy = Chess_Matrix[x][y]
        if (isinstance(possible_enemy, Chess_Piece) and possible_enemy.color != self.color):
            return True
        return False
        
    def add_move(self, direction, piece_movements):
        if (len(piece_movements) == 1 and piece_movements[0].values()[0] == Infinite_Movement):
            direction = piece_movements[0].keys()[0]
            
            for i in range(1,8):
                self.add_move(direction, [{direction:i}])
            return
            
        if self.negate_coordinates:
            for movement in piece_movements:
                for direction in movement:
                    movement[direction] *= -1
                
        self.moves[direction].append(Chess_Piece_Movement(self, piece_movements, self.coordinates))
    
    def show_movements(self):
        for move in self.possible_moves:
            move.show_move()
                
        self.Movements_Shown = True
            
    def hide_movements(self):
        for move in self.possible_moves:
            move.hide_move()
                
        self.Movements_Shown = False
    
    
    
class Pawn(Chess_Piece):
    def __init__(self, color, coordinates, canvas):
        Chess_Piece.__init__(self, "Pawn", color, coordinates, canvas)

        self.backup_moves = copy.deepcopy(self.moves)
        
    
        
    def update_moves_list(self):
        if(self.negate_coordinates):
            multiplier = -1
        else:
            multiplier = 1
            
        self.moves = copy.deepcopy(self.backup_moves)
        x,y = self.coordinates
        
        if (self.enemy_present([x,y+multiplier]) == False):
            self.add_move("North", [{"North":1}])
        
        if (self.enemy_present([x+multiplier,y+multiplier])):
            self.add_move("NorthEast", [{"North":1}, {"East":1}])
            
        if (self.enemy_present([x-multiplier,y+multiplier])):
            self.add_move("NorthWest", [{"North":1}, {"West":1}])
        
        
        if (self.movement_counter > 0):
            Chess_Piece.update_moves_list(self)
        else:
            if (self.enemy_present([x,y+(2*multiplier)]) == False and len(self.moves["North"]) == 1):
                self.add_move("North", [{"North":2}])
                
            Chess_Piece.update_moves_list(self)
            self.moves = copy.deepcopy(self.backup_moves)
        

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
        
    def update_moves_list(self):
        del self.possible_moves[:]
        for movement in self.moves:
            if (len(self.moves[movement]) == 0):
                continue
            for move in self.moves[movement]:         
                potential_move = move.update_move_coordinates()
                if potential_move:
                    self.possible_moves.append(potential_move)
                    x,y = potential_move.movement_coordinates
                    self.attack_board[x][y] = potential_move
                
        
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
        self.IsChecked = False
        self.add_move("North", [{"North":1}])
        self.add_move("East", [{"East":1}])
        self.add_move("South", [{"South":1}])
        self.add_move("West", [{"West":1}])
        self.add_move("NorthEast", [{"NorthEast":1}])
        self.add_move("NorthWest", [{"NorthWest":1}])
        self.add_move("SouthEast", [{"SouthEast":1}])
        self.add_move("SouthWest", [{"SouthWest":1}])
        
        if (color == "White"):
            White_King = self
        else:
            Black_King = self
        
        