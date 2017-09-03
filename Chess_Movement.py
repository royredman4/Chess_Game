try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *
    
from Game_Initialization import Chess_Matrix, Moves_dictionary, Show_Piece 

x_let = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7}
y_let = {"1":0, "2":1, "3":2, "4":3, "5":4, "6":5, "7":6, "8":7}
Directions = ["North","East","South","West",
              "NorthEast","SouthEast","SouthWest","NorthWest"]

class Toggle_Piece(Frame):
    def __init__(self, canvas):
        Frame.__init__(self)
        self.move_options = False
        self.canvas = canvas
        self.Movement_options = {}
        
    def Piece_Clicked(self, chess_piece):
        if self.move_options is True:
            pass
            # need to check all the options for a possible option 

        else:
            if chess_piece:
                print("%s and is %s" %(chess_piece.Piece_name, chess_piece.color))
                self.x = x_let[chess_piece.x_coords]
                self.y = y_let[chess_piece.y_coords]
                self.name = chess_piece.Piece_name
                self.color = chess_piece.color
                self.piece = chess_piece
                self.Movement_Options()
                print("Movement options are %s" %(self.Movement_options))
                self.Show_Hide_Movement("Yellow")


    def Movement_Options(self):
        # This will go for how many directions there are (8)
        for i in range(len(Directions)):
            current_coordinates = [self.x, self.y]
            acceptable_moves = []
            
            # This indicates how many possible moves the piece can make
            # In that specific direction
            for j in range(Moves_dictionary[self.name][i]):

                ################################################################
                #STILL NEED TO CHECK FOR SPECIAL CASES: Is it a pawn? their first move
                #As a pawn (two moves). A knight ignores all things that are in its way
                #accept for its actual spot. Pawns cannot move backwards. Paws can attack
                #diagonally only if an enemy is one diagonal move from itself
                #################################################################
                
                if (Directions[i] in ["North", "NorthEast", "NorthWest"]):
                    if (current_coordinates[1] is 7):
                        break
                    else:
                        current_coordinates[1] += 1
                if (Directions[i] in ["East", "NorthEast", "SouthEast"]):
                    if (current_coordinates[0] is 7):
                        break
                    else:
                        current_coordinates[0] += 1
                if (Directions[i] in ["South", "SouthEast", "SouthWest"]):
                    if (current_coordinates[1] is 0):
                        break
                    else:
                        current_coordinates[1] -= 1

                if (Directions[i] in ["West", "SouthWest", "NorthWest"]):
                    if (current_coordinates[0] is 0):
                        break
                    else:
                        current_coordinates[0] -= 1

                temp_piece = Chess_Matrix[current_coordinates[0]][current_coordinates[1]]
                if ((temp_piece is None) or (temp_piece.color is not self.color)):
                    acceptable_moves.append([current_coordinates[0], current_coordinates[1]])
                if (temp_piece is not None):
                    break

            self.Movement_options[Directions[i]] = acceptable_moves


    def Show_Hide_Movement(self, color):
        for keys in Directions:
            attack_options = self.Movement_options[keys]
            for i in range(len(attack_options)):
                x = attack_options[i][0] * 60
                y = (7 - attack_options[i][1]) * 60
                print("X is %s and Y is %s" %(x, y))
                self.canvas.create_rectangle(x,y,x+60,y+60,fill=color)
                Show_Piece(self.canvas, Chess_Matrix[attack_options[i][0]][attack_options[i][1]])
                
                
    
