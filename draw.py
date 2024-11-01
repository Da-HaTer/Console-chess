from time import sleep
import os
from board import State
import numpy as np


def colored(text,color=None):
    if color==None:
        color="red"
    if text=='⬜':
        if color=='red':
            return '🟥'
        elif color=='green':
            return '🟩'
        elif color=='blue':
            return '🟦'
        elif color=='yellow':
            return '🟨'
        elif color=='purple':
            return '🟪'
    if color=='red':
        return '\033[31m'+text+'\033[0m'
    elif color=='green':
        return '\033[32m'+text+'\033[0m'
    elif color=='blue':
        return '\033[34m'+text+'\033[0m'
    elif color=='yellow':
        return '\033[33m'+text+'\033[0m'
    elif color=='purple':
        return '\033[35m'+text+'\033[0m'
class Display():
    
    def __init__(self,board:State=None,last_move:tuple[tuple[int]]=None, checks:tuple[bool,bool]=None ,highlights:tuple[any]=None,theme:dict={"main":"green","check":"red","last_move":"yellow","highlight":"blue"}):
        self.board=board if board is not None else State()
        self.theme=theme #main,check,last_move,highlight colors
        self.d = self.piece_to_symbol() #dictionary to convert piece to symbol
        
        self.last_move= [] if last_move is None else last_move #last move (from to squares) #yellow
        self.highlights= [] if highlights is None else highlights #manual highlights squares #blue
        self.check = []
        self.update_checks(checks) #check squares #red
        ###
        # self.highlights=[(highlights)] if type(highlights)==tuple else self.highlights
        # self.last_move=[(last_move)] if type(last_move)==tuple else self.last_move
        # self.check=[(checks)] if type(checks)==tuple else self.check


    def update_checks(self,checks:tuple[bool,bool])->None:
        if checks[0]:
            self.check=[self.board.kings_pos[0:2]]
        if checks[1]:
            self.check=[self.board.kings_pos[2:]]
        self.Draw_board()
        

    def piece_to_symbol(self) -> dict:
        """Returns a dictionary to convert piece characters to chess symbols for display on the board
        """
        symbols=['♔','♕','♖','♗','♘','♙',
                 '♚','♛','♜','♝','♞','♟']
        pieces=['K','Q','R','B','N','P','k','q','r','b','n','p']
        d=dict()
        for i in range(12):
            d[pieces[i]]=symbols[i]+' ' ###To test on linux and other kernels
        return d
    def settheme(self,theme:dict={"main":"green","check":"red","last_move":"yellow","highlight":"blue"}) -> None:
        self.theme=theme
        self.d = self.piece_to_symbol() #update the dictionary ###what happens if we don't
        self.Draw_board()
    
    def Highlight(self,highlights:list=None)->None:
        # highlights = [] if highlights is None else highlights
        # highlights=[(highlights)] if type(highlights)==tuple else highlights
        if highlights is None or len(highlights)==0:
            self.highlights=[] 
        else:
            highlights= tuple(highlights)
            self.highlights+=(highlights,)
        # print("highlights",highlights)
        self.Draw_board()

    def Draw_board(self,matrix=None):
        if matrix is None:
            matrix = self.board[:]
        d = self.d

        ### sleep(0.2) # to slow down the display
        os.system('cls' if os.name == 'nt' else 'clear')
        for i in 'ABCDEFGH':
            print(' ',i,end='')
        print('')
        print('',' __'*(8))

        for i in range(8):
            print(8-i,end='')
            print('|',end='')
            for j in range(8):
                if matrix[i,j]=='': # empty square

                    if (i,j) in self.highlights:
                        print(colored('⬜',self.theme["highlight"]),end='|')
                    elif (i,j) in self.last_move:
                        print(colored('⬜',self.theme["last_move"]),end='|')
                    elif (i+j)%2==0:
                        print("  ",end='|')
                    else:
                        print("  ",end='|')
                else: #piece

                    if self.highlights and (i,j) in self.highlights:
                        print(colored(d[matrix[i,j][0]],self.theme["highlight"]),end='|')
                    elif (i,j) in self.check:
                        print(colored(d[matrix[i,j][0]],self.theme["check"]),end='|')
                    elif (i,j) in self.last_move:
                        print(colored(d[matrix[i,j][0]],self.theme["last_move"]),end='|')
                    else:
                        if matrix[i,j] in ('QRBNPK'):
                            print(colored(d[matrix[i,j][0]],self.theme["main"]),end='|')
                        else: 
                            print(d[matrix[i,j]],end='|')
            print()
        print('',' ‾‾'*(8))
        
    
if __name__ == "__main__":
    import numpy as np
    board=State()
    checks=(False,True)
    last_move=((2,1),(3,1))
    highlights=((2,3),(3,4),(4,5),(5,6))
    display=Display(board,last_move,checks,highlights)
    # display = Display(board,"green")
    for i in range(8):
        display.update_checks((i%2==0,i%2==1))
        display.Highlight((i,i))
        sleep(2)
    sleep(3)
    ### add highlight color to theme preferences
    theme={"main":"purple","check":"red","last_move":"yellow","highlight":"green"}
    display.Highlight()
    display.settheme(theme)
