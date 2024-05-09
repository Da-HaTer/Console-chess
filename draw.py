from time import sleep
from os import system
import numpy as np

class Display:
    
    def __init__(self,board=None,theme="green",highlight=None):
        if board is None:
            self.board = np.array(['']*64).reshape(8,8)
        else:
            self.board = board
        self.theme=theme
        self.d = self.piece_to_symbol() #dictionary to convert piece to symbol
        self.highlight=highlight
        self.Draw_board(board,highlight)
    
    def settheme(self,theme):
        self.theme=theme
        self.d = self.piece_to_symbol() #update the dictionary
        self.Draw_board(self.board,self.highlight)
    
    def Highlight(self,position):
        print("Highlighting",position)
        self.Draw_board(self.board,position)

    def colored(self,text,color=None):
        if color==None:
            color=self.theme
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

    def piece_to_symbol(self):
        symbols=['♔','♕','♖','♗','♘','♙',
                 '♚','♛','♜','♝','♞','♟']
        pieces=['K','Q','R','B','N','P','k','q','r','b','n','p']
        d=dict()
        for i in range(12):
            d[pieces[i]]=symbols[i]+' '
        return d
    
    def Draw_board(self,matrix=None,highlight=None):
        if matrix is None:
            matrix = self.board
        d = self.d
        sleep(0.2) # to slow down the display
        system('cls')
        l,c=matrix.shape
        for i in 'ABCDEFGH':
            print(' ',i,end='')
        print('')
        print('',' __'*(c))

        for i in range(l):
            print(8-i,end='')
            print('|',end='')
            for j in range(c):
                if matrix[i,j]=='':
                    if highlight == (i,j):
                        print(self.colored('⬜',"red"),end='|')
                    elif (i+j)%2==0:
                        print("  ",end='|')
                    else:
                        print("  ",end='|')
                else:
                    if highlight == (i,j):
                        print(self.colored(d[matrix[i,j][0]],"red"),end='|')
                    else:
                        if matrix[i,j] in ('QRBNPK'):

                            print(self.colored(d[matrix[i,j][0]]),end='|')
                        else: 
                            print(d[matrix[i,j]],end='|')
            print()
        print('',' ‾‾'*(c))
        
    
if __name__ == "__main__":
    import numpy as np
    board=np.array([
            ['R','N','B','Q','K','B','N','R'],
            ['P','P','P','P','P','P','P','P'],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['','','','','','','',''],
            ['p','p','p','p','p','p','p','p'],
            ['r','n','b','q','k','b','n','r']
        ])
    display = Display(board,"green")
    sleep(1)
    display.Highlight((4,4))
    ### add highlight color to theme preferences
    sleep(3)
    display.settheme("red")