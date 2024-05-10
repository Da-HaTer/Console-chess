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
        highlight= [] if highlight is None else highlight
        self.highlight=[(highlight)] if type(highlight)==tuple else highlight
        self.Draw_board(board,self.highlight)
    
    def settheme(self,theme):
        self.theme=theme
        self.d = self.piece_to_symbol() #update the dictionary
        self.Draw_board(self.board,self.highlight)
    
    def Highlight(self,highlights=None):
        highlights = [] if highlights is None else highlights
        highlights=[(highlights)] if type(highlights)==tuple else highlights
        if len(highlights)==0:
            self.highlight=[]
        else:   
            self.highlight+=highlights
        print("highlights",highlights)
        self.Draw_board(self.board,self.highlight)

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
        for i in 'ABCDEFGH':
            print(' ',i,end='')
        print('')
        print('',' __'*(8))

        for i in range(8):
            print(8-i,end='')
            print('|',end='')
            for j in range(8):
                if matrix[i,j]=='':
                    if (i,j) in highlight:
                        print(self.colored('⬜',"red"),end='|')
                    elif (i+j)%2==0:
                        print("  ",end='|')
                    else:
                        print("  ",end='|')
                else:
                    if (i,j) in highlight:
                        print(self.colored(d[matrix[i,j][0]],"red"),end='|')
                    else:
                        if matrix[i,j] in ('QRBNPK'):

                            print(self.colored(d[matrix[i,j][0]]),end='|')
                        else: 
                            print(d[matrix[i,j]],end='|')
            print()
        print('',' ‾‾'*(8))
        
    
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
    
    for i in range(8):
        display.Highlight((i,i))
    sleep(3)
    ### add highlight color to theme preferences
    display.settheme("blue")