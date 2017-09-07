try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import os

# Indicates The amount of pieces there are for a single Chess_Piece type
Piece_count = {"Queen": 1, "King": 1, "Rook": 2, "Bishop": 2, "Knight": 2, "Pawn": 8}


'''
Organized dictionary by limited movements each piece can travel,All numbers
indicate the distance the piece can travel based on the following ordered
directions: N, E, S, W, NE, SE, SW, NW.
'''
Moves_dictionary = {"Queen":[8,8,8,8,8,8,8,8],
                    "King":[1,1,1,1,1,1,1,1],
                    "Rook":[8,8,8,8,0,0,0,0],
                    "Bishop":[0,0,0,0,8,8,8,8],
                    "Knight":[2,2,2,2,0,0,0,0],
                    "Pawn":[1,0,1,0,1,1,1,1]}

# The matrix that manages the Chess piece objects on the board
Chess_Matrix = [[None for x in range(8)] for y in range(8)]

# The matrix that manages the chessboard color objects for each piece
Board_Colors = [[None for x in range(8)] for y in range(8)]


# Manages each square of the chessboard based on its background color
class Board_Settings():
    def __init__(self, canvas, def_color, rectangle):
        self.canvas = canvas
        self.default_color = def_color
        self.rectangle_object = rectangle
        
    def Set_Color(self, color):
        self.canvas.itemconfig(self.rectangle_object, fill=color)

    def Reset_Color(self):
        self.canvas.itemconfig(self.rectangle_object, fill=self.default_color)


# The master chess class that overwatches all chess pieces
class Chess_Set(Frame):
    def __init__(self, canvas):
        Frame.__init__(self)
        self.canvas = canvas
        self.White_Pieces = Chess_Managers("White", self.canvas)
        self.Black_Pieces = Chess_Managers("Black", self.canvas)
        Print_Matrix()


# Manages every chess piece for its group ("White"/"Black" chess pieces)
class Chess_Managers():
    def __init__(self, color, canvas):
        self.Chess_color = color
        self.Chess_items = []
        self.Create_Pieces(canvas)
        
    def Create_Pieces(self, canvas):
        if (self.Chess_color is "White"):
            y_coords = 0
            next_row = 1
        else:
            y_coords = 7
            next_row = 6

        x_index = 0
        for key in ["Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]:
            print("\nAdding %s" % key)
            if (key is "Pawn"):
                    y_coords = next_row
                    x_index = 0

            # Creates every chess piece
            for i in range(0, Piece_count[key], 2):
                x_coords = x_index
                current_index = [x_coords, y_coords]
                print("current_index is %s" % current_index)
                self.Chess_items.append(Chess_Piece(key, self.Chess_color, current_index, canvas))
                Update_ChessMatrix(self.Chess_items[-1])

                '''
                If the same chess piece is also on the other side of the same row,
                then add it on the other side.
                '''
                if (key not in ["King", "Queen"]):
                    x_coords = 7 - x_index
                    current_index = [x_coords, y_coords]
                    print("Next coordinates are %s" % (current_index))
                    self.Chess_items.append(Chess_Piece(key, self.Chess_color, current_index, canvas))
                    Update_ChessMatrix(self.Chess_items[-1])
                    
                x_index += 1


# Manages a single chess pieces attributes
class Chess_Piece():
    def __init__(self, name, color, coordinates, canvas):
        self.Piece_name = name
        self.Attack_Moves = Moves_dictionary[name]
        self.color = color
        self.x_coords = coordinates[0]
        self.y_coords = coordinates[1]
        self.canvas = canvas
        self.image = None
        self.img_Obj = None
        self.Create_Piece()
            
        self.hop = False
        self.Diagonal = False
        
        if (name is "Knight"):
            self.hop = True

        elif (name is "Pawn"):
            self.diagonal = True

    def Create_Piece(self):
        x = self.x_coords
        y = self.y_coords
        img_location = os.getcwd() + "/Chess_Pieces/%s_Pieces/%s_%s.GIF" %(self.color, self.color, self.Piece_name)
        self.image = PhotoImage(file=img_location)
        self.img_Obj = self.canvas.create_image((30+(x *60)), 450-(y * 60), image = self.image)

    def Move_Piece(self, new_x, new_y):
        x = (new_x - self.x_coords) * 60
        y = (self.y_coords - new_y) * 60
        print("Moving x by %d and y by %d" % (x, y))
        self.canvas.move(self.img_Obj, x, y)

        self.x_coords = new_x
        self.y_coords = new_y

    # When this piece is destroyed in the game, then remove its image object
    def Remove_Piece(self):
        print("Deleting Piece Image")
        self.canvas.delete(self.img_Obj)


# Creates the whole ChessBoard from scratch
def Draw_ChessBoard(canvas):
    f = ["dark gray", "white"]
    y = 0
    p = False
    
    for z in range(0, 8):
        x = 0
        for q in range(0, 8):
            temp = canvas.create_rectangle(x, 480-y, x+60, 480-(y+60), fill=f[p])
            Board_Colors[q][z] = Board_Settings(canvas, f[p], temp)

            print("x:%d y:%d is %s" % (q, z, f[p]))
            p = not p
            x += 60
        f.reverse()
        y += 60


# Updates the matrix, to reflect a chess piece moving
def Update_ChessMatrix(chess_piece, old_coords=None):
    new_x = chess_piece.x_coords
    new_y = chess_piece.y_coords
    print("Moving chess piece to %s x %s" % (new_x, new_y))
    Chess_Matrix[new_x][new_y] = chess_piece
    if old_coords:
        old_x = old_coords[0]
        old_y = old_coords[1]
        Chess_Matrix[old_x][old_y] = None
        print("Old Coordinates were %s and the new coordinates are %s" % ([old_x, old_y], [new_x, new_y]))
        (Board_Colors[old_x][old_y]).Reset_Color()


# Outputs all the chess pieces neatly onto the console (for debugging purposes)
def Print_Matrix():
    for y in range(8):
        for x in range(8):
            if Chess_Matrix[x][y]:
                if ((Chess_Matrix[x][y]).Piece_name is "King"):
                    piece_initial = "Ki "
                else:
                    piece_initial = (Chess_Matrix[x][y]).Piece_name[0] + "  "
                print (piece_initial),
            else:
                print ("   "),
        print (" ")


# Returns either the chess piece at the coordinates, or None if nothing is there
def Get_Piece(x_coord, y_coord):
    return Chess_Matrix[x_coord][y_coord]
