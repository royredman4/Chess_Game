#!/usr/bin/python

try:
    # for Python2
    from Tkinter import *
except ImportError:
    # for Python3
    from tkinter import *

import Game_Initialization as GI
import Chess_Movement as CM

class ChessGame(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.canvas = Canvas(self, width=480, height=480)
        self.canvas.pack(side=LEFT)

        # Sets the programs window to the middle of the screen 
        Xmove = (self.winfo_screenwidth()*(1-0.3))/2
        Ymove = (self.winfo_screenheight()*(1-0.2))/2
        self.geometry("%dx%d%+d%+d" % (780, 480, Xmove, Ymove-100))

        self.New_Game()
        self.Toggle = CM.Toggle_Piece(self.canvas)
        
        self.canvas.bind("<Button-1>", self.Clicked_On_Board)

    def New_Game(self):
        GI.Draw_ChessBoard(self.canvas)
        self.Chess_Items = GI.Chess_Set(self.canvas)
        
    def Clicked_On_Board(self, event):
        print ("Hello at %s x %s" % (event.x, event.y))
        self.Toggle.Piece_Clicked(event.x,event.y)
        
        

if __name__ == "__main__":
    root = ChessGame()
    
    root.mainloop()
