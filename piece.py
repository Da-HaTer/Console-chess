import numpy as np

from time import sleep
from logic import Logic
from logic import IllegalMoveError, InvalidMoveError
from draw import Display
class ChessPiece:
    def __init__(self,color,position,type="p"):
        self.color = color
        #color= w, b
        self.type=type
        #types= p, r, n, b, q, k
        self.position = position
        #specific board position (np array)
           
    def move_pawn(self, white, position, move): #return position
        new_pos=position.copy()
        if len(move) == 2: # simple pawn move: e4, d4, e5, d5
            j = ord(move[0]) - ord('a') #col
            i = 8 - int(move[1]) #row
            if white: #white pawn move
                if move[1] in '128': #illegal for white
                    raise IllegalMoveError(move)
                if new_pos[i, j] == '' and new_pos[i+1, j] == 'p': # 1 square move
                    new_pos[i, j] = 'p'
                    new_pos[i+1, j] = ''
                elif i==4 and new_pos[i, j] == '' and new_pos[i+2, j] == 'p': # 2 square move
                    new_pos[i, j] = 'p'
                    new_pos[i+2, j] = ''
                else:
                    raise IllegalMoveError(move)
            else: #black pawn move
                if move[1] in '178':
                    raise IllegalMoveError(move)
                if new_pos[i, j] == '' and new_pos[i-1, j] == 'P': # 1 square move
                    new_pos[i, j] = 'P'
                    new_pos[i-1, j] = ''
                elif i==3 and new_pos[i, j] == '' and new_pos[i-2, j] == 'P': # 2 square move
                    new_pos[i, j] = 'P'
                    new_pos[i-2, j] = ''
                else:
                    raise IllegalMoveError(move)
        return new_pos

    def capture(self, position):
        # Implement the logic for capturing an opponent's piece
        pass

    def promote(self, new_piece):
        # Implement the logic for promoting a pawn to a new piece
        pass

if __name__=="__main__":
    start_board= np.array([
        ['R','N','B','Q','K','B','N','R'],
        ['P','P','P','P','P','P','P','P'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['p','p','p','p','p','p','p','p'],
        ['r','n','b','q','k','b','n','r']
    ])
pos=start_board
white=True
while True:
    board=Display(pos)
    move=input("Enter move: ")
    if move=="q":
        break
    
    piece=ChessPiece('w',start_board)
    try:
        position=piece.move_pawn(white,pos,move)
        board=Display(position)
        pos=position
        white=not white
    except Exception as e:
        print(e)
        input("press any key to continue...")

    

