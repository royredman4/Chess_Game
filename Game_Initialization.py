try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import os

# Indicates The amount of pieces there are for a single Chess_Piece type
Piece_count = {"Queen": 1, "King":1, "Rook":2, "Bishop":2,"Knight":2, "Pawn":8}


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
                  "Pawn":[1,0,1,0,0,0,0,0]}

Chess_Matrix = [[None for x in range(8)] for y in range(8)]

class Chess_Set(Frame):
    def __init__(self, canvas):
        Frame.__init__(self)
        self.canvas = canvas
        self.White_Pieces = Chess_Managers("White", self.canvas)
        self.Black_Pieces = Chess_Managers("Black", self.canvas)
        Print_Matrix()
	
        #self.canvas = canvas
        #print("White is \n%s" %self.White_Pieces.Chess_items)
        #print("Black is \n%s" %self.Black_Pieces.Chess_items)
        
        
class Chess_Managers():
    def __init__(self, color, canvas):
        self.Chess_color = color
        self.Chess_items = []
        self.Create_Pieces(canvas)
        
    def Create_Pieces(self, canvas):
        if (self.Chess_color is "White"):
            y_coords = "1"
            next_row = "2"
        else:
            y_coords = "8"
            next_row = "7"

        x_index = 0
        for key in ["Rook", "Knight", "Bishop", "Queen", "King", "Pawn"]:
            print("\nAdding %s" % key)
            if (key is "Pawn"):
                    y_coords = next_row
                    x_index = 0

            #Creates every chess piece
            for i in range(0, Piece_count[key], 2):
                x_coords = chr(65 + x_index)
                current_index = x_coords + y_coords
                print("current_index is %s" % current_index)
                self.Chess_items.append(Chess_Piece(key, self.Chess_color, current_index))
                Update_ChessMatrix(self.Chess_items[-1])
                Show_Piece(canvas, self.Chess_items[-1])

                '''
                If the same chess piece is also on the other side of the same row,
                then add it on the other side.
                '''
                if (key not in ["King", "Queen"]):
                    x_coords = chr(72-x_index)
                    current_index = x_coords + y_coords
                    print("Next coordinates are %s" % (current_index))
                    self.Chess_items.append(Chess_Piece(key, self.Chess_color, current_index))
                    Update_ChessMatrix(self.Chess_items[-1])
                    Show_Piece(canvas, self.Chess_items[-1])
                    
                x_index += 1
    

class Chess_Piece():
    def __init__(self, name, color,coordinates):
        self.Piece_name = name
        self.Attack_Moves = Moves_dictionary[name]
        self.color = color
        self.x_coords = coordinates[0]
        self.y_coords = coordinates[1]
        img_location = os.getcwd() + "/Chess_Pieces/%s_Pieces/%s_%s.GIF" %(color, color, name)
        self.image = PhotoImage(file=img_location)

        self.hop = False
        self.Diagonal = False
        
        if (name is "Knight"):
            self.hop = True

        elif (name is "Pawn"):
            self.diagonal = True
 

def Draw_ChessBoard(canvas):
    f = ["white", "dark gray"]
    y = 0
    p = False
    
    for z in range(0, 8):
        x = 0
        for q in range(0, 8):
            canvas.create_rectangle(x, y, x+60, y+60, fill=f[p])
            p = not p
            x += 60
        f.reverse()
        y += 60

def Update_ChessMatrix(chess_piece, old_coords= None):
    new_x = ord(chess_piece.x_coords) - 65
    new_y = ord(chess_piece.y_coords) - 49
    print("Moving chess piece to %s x %s" %(new_x, new_y))
    Chess_Matrix[new_x][new_y] = chess_piece
    if old_coords:
        old_x = ord(old_coords[0]) - 65
        old_y = ord(old_coords[1]) - 49
        Chess_Matrix[old_x][old_y] = None

def Print_Matrix():
    for y in range(8):
        for x in range(8):
            if Chess_Matrix[x][y]:
                if ((Chess_Matrix[x][y]).Piece_name is "King"):
                    piece_initial ="Ki "
                else:
                    piece_initial = (Chess_Matrix[x][y]).Piece_name[0] + "  "
                print (piece_initial),
            else:
                print ("n  "),
        print (" ")

def Get_Piece(x_coord, y_coord):
    x_letters = {0:"A", 1:"B", 2:"C",3:"D", 4:"E", 5:"F", 6:"G", 7:"H"}
    x_coord = x_coord/60
    y_coord = abs((y_coord/60)-7) +1
    print("You are at %s%s" % (x_letters[x_coord], str(y_coord)))
    return Chess_Matrix[x_coord][y_coord-1]
    
    
def Show_Piece(canvas, current_piece):
    if (current_piece is None):
        return
    x = ord(current_piece.x_coords) - 65
    y = ord(current_piece.y_coords) - 49
    #print ("X is %s, Y is %s" % (30+(x *60), 450-(y * 60)))

    #print("Image location is %s" %current_piece.image)
    canvas.create_image((30+(x *60)), 450-(y * 60), image = current_piece.image)
