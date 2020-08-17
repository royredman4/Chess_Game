try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

from Game_Initialization import Get_Piece
from Chess_Pieces import Chess_Piece

#x_let = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
#y_let = {"1":0, "2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7}
Directions = ["North","East","South","West",
              "NorthEast","SouthEast","SouthWest","NorthWest"]


# Manages anything that involves the user clicking on the Chess Board
class Toggle_Piece(Frame):
    def __init__(self, canvas):
        Frame.__init__(self)
        self.move_options = False
        self.canvas = canvas
        self.Players_Colors = ["Black", "White"]
        self.Player_One_Turn = True
        self.Movement_options = {}
        self.current_clicked_piece = None
        self.Movements_Shown = False

    '''
    If the user clicked on a chess piece, it will display the options a user could move.
    If they clicked on one of the displayed places to move, it will move the chess piece
    to the desired location. After, it will remove the displayed places to move from the
    chess board.
    '''
    def Piece_Clicked(self, x_coords, y_coords):
        current_coords = self.Coordinates_to_index(x_coords, y_coords)
        print("Current coordinates are %s" % (current_coords))
        chess_piece = Get_Piece(current_coords[0], current_coords[1])


        print ("It is player %s turn" % (self.Players_Colors[self.Player_One_Turn]))
           
        # If it's not the current chess piece, then check if it's the shown movement
        if (isinstance(chess_piece, Chess_Piece) == False or (self.Players_Colors[self.Player_One_Turn] is not chess_piece.color)):
            if self.current_clicked_piece and self.current_clicked_piece.Movements_Shown and self.current_clicked_piece.Move_Chosen(current_coords[0], current_coords[1]):
                self.current_clicked_piece.Move_Piece(current_coords[0], current_coords[1])
                self.Player_One_Turn = not self.Player_One_Turn
                self.current_clicked_piece = None
                return self.Players_Colors[self.Player_One_Turn]
                
            
            elif self.current_clicked_piece:
                self.current_clicked_piece.hide_movements()
                self.current_clicked_piece = None
                
        # If it is a chess piece, check if it's our players chess piece
        elif (self.Players_Colors[self.Player_One_Turn] is chess_piece.color):
            print("Chess piece is %s and Movement Options are %s" % (chess_piece.Piece_name, chess_piece.moves))
            if (self.current_clicked_piece):
                self.current_clicked_piece.hide_movements() 
                
            self.current_clicked_piece = chess_piece
            self.current_clicked_piece.update_moves_list()
            self.current_clicked_piece.show_movements()
        
        # If it's neither of those, hide any movements
        else:
            if (self.current_clicked_piece):
                self.current_clicked_piece.hide_movements()
                self.current_clicked_piece = None    
        
    
    
    # Converts the coordinates the user clicked, to the exact index in the Chess_Matrix
    def Coordinates_to_index(self, x_coords, y_coords):
        x_coords = x_coords/60
        y_coords = abs((y_coords/60)-7) + 1
        
        return [x_coords, y_coords-1]
    