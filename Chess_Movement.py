try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

from Game_Initialization import Chess_Matrix, Board_Colors, Moves_dictionary, Get_Piece, Update_ChessMatrix

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
        self.Movement_options = {}

    '''
    If the user clicked on a chess piece, it will display the options a user could move.
    If they clicked on one of the displayed places to move, it will move the chess piece
    to the desired location. After, it will remove the displayed places to move from the
    chess board.
    '''
    def Piece_Clicked(self, x_coords, y_coords):
        current_coords = self.Coordinates_to_index(x_coords, y_coords)
        print("Current coordinates are %s" %(current_coords))
        chess_piece = Get_Piece(current_coords[0], current_coords[1])

        # Checks if the user clicked on the chess board after the movement options were displayed
        if self.move_options is True:
            self.move_options = False
            self.Show_Hide_Movement()

            # Checks to see if the player clicked on an actual movement option
            for key in Directions:
                for i in range(len(self.Movement_options[key])):
                    list = self.Movement_options[key][i]
                    print("Seeing if %s and %s are the same" %(list, current_coords))

                    # If the clicked coordinates and the movement coordinates are the same
                    if list == current_coords:
                        print("They are the same!! :D")
                        enemy_check = Get_Piece(current_coords[0], current_coords[1])

                        # Identifies if you are destroying an enemy piece in the process of moving
                        if (enemy_check):
                            self.Delete_Piece(current_coords[0], current_coords[1])
                            
                        self.piece.Move_Piece(current_coords[0], current_coords[1])
                        Update_ChessMatrix(self.piece, [self.x, self.y])

        else:
            # Checks if the user clicked on a chess piece or not
            if chess_piece:
                self.move_options = True
                print("%s and is %s" %(chess_piece.Piece_name, chess_piece.color))
                self.Store_Piece_Information(chess_piece)                
                self.Movement_Options()
                print("Movement options are %s" %(self.Movement_options))
                self.Show_Hide_Movement("Yellow")

    def Store_Piece_Information(self, piece):
        self.x = piece.x_coords
        self.y = piece.y_coords
        self.name = piece.Piece_name
        self.color = piece.color
        self.piece = piece
        
    
    # Identifies all the movements the chess piece could make
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
                #accept for its actual spot. Pawns cannot move backwards. Pawns can attack
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

    # Converts the coordinates the user clicked, to the exact index in the Chess_Matrix
    def Coordinates_to_index(self, x_coords, y_coords):
        x_coords = x_coords/60
        y_coords = abs((y_coords/60)-7) +1
        
        return [x_coords,y_coords-1]

    def Delete_Piece(self, x_coords, y_coords):
        del_piece = Chess_Matrix[x_coords][y_coords]
        del_piece.Remove_Piece()
        Chess_Matrix[x_coords][y_coords] = None
        print("Deleted piece is "),
        print(Chess_Matrix[x_coords][y_coords])


    '''
    Either shows a list of locations a chess piece can move on the board,
    or hides that list from the board
    '''
    def Show_Hide_Movement(self, color= None):
        if (color is None):
            Hide_options = True
        else:
            Hide_options = False
            
        for keys in Directions:
            attack_options = self.Movement_options[keys]
            for i in range(len(attack_options)):
                x = attack_options[i][0]
                y = attack_options[i][1]
                print("X is %s and Y is %s" %(x, y))
                if (Hide_options):
                    (Board_Colors[x][y]).Reset_Color()
                else:
                    (Board_Colors[x][y]).Set_Color(color)
                    
