from time import sleep
from os import system

class Draw_board:
    def __init__(self,board=None):
        if board is None:
            self.board = np.array(['']*64).reshape(8,8)
        else:
            self.board = board
        self.piece_to_symbol = self.piece_to_symbol() #dictionary to convert piece to symbol
        self.Draw_board()

    def piece_to_symbol(self):
        symbols=['♔','♕','♖','♗','♘','♙','♚','♛','♜','♝','♞','♟']
        pieces=['K','Q','R','B','N','P','k','q','r','b','n','p']
        d=dict()
        for i in range(12):
            d[pieces[i]]=symbols[i]+' '
        return d
    
    def Draw_board(self,matrix=None,d=None):
        # default paramter is attribute
        if matrix is None:
            matrix = self.board
        if d is None: 
            d = self.piece_to_symbol
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
                    print('  ',end='|')
                else:
                    print(d[matrix[i,j]],end='|')
            print()
        print('',' --'*(c))
    
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
    chess = Draw_board(board)
    chess.Draw_board()
