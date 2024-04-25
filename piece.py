import numpy as np
import regex as re
from time import sleep
from logic import Logic
from logic import IllegalMoveError, InvalidMoveError, ambigousMoveError
from draw import Display
import traceback
class ChessPiece:
    def __init__(self,color,position,type="p",enpassant=False):
        self.color = color
        #color= w, b
        self.type=type
        self.enpassant=enpassant ###temporary to be added to returned position (create new class)
        #types= p, r, n, b, q, k
        self.position = position
        #specific board position (np array)
           
    def pawn_move(self, white, position, move): #return position
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
        elif re.match(r'[a-h][x][a-h][1-7]', move):# pawn capture move: exd4, dxe4, exd4, dxe4
            j1 = ord(move[0]) - ord('a')
            j2 = ord(move[2]) - ord('a')
            i = 8 - int(move[3])
            if abs(j1-j2) != 1: #not diagonally capturing ### add custom en passant
                raise IllegalMoveError(move)
            print(i,j1,j2)
            if white:
                if new_pos[i, j2] in 'PRNBQK' and new_pos[i+1, j1] == 'p':
                    new_pos[i, j2] = 'p'
                    new_pos[i+1, j1] = ''
            else:
                if new_pos[i, j2] in 'prnbqk' and new_pos[i-1, j1] == 'P':
                    new_pos[i, j2] = 'P'
                    new_pos[i-1, j1] = ''
                else:
                    raise IllegalMoveError(move)
        elif re.match(r'[a-h][x][a-h][18][=][QRBN]', move, re.IGNORECASE): # pawn promotion move: exd8=Q, dxe1=N
            j1 = ord(move[0]) - ord('a')
            j2 = ord(move[2]) - ord('a')
            i = 8 - int(move[3])
            if abs(j1-j2) != 1:
                raise IllegalMoveError(move)
            if white:
                if new_pos[i, j2] in 'PRNBQK' and new_pos[i+1, j1] == 'p':
                    new_pos[i, j2] = move[5].lower()
                    new_pos[i+1, j1] = ''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i, j2] in 'prnbqk' and new_pos[i-1, j1] == 'P':
                    new_pos[i, j2] = move[5].upper()
                    new_pos[i-1, j1] = ''
                else:
                    raise IllegalMoveError(move)
        elif re.match(r'[a-h][18][=][QRBN]', move, re.IGNORECASE): # pawn promotion move: e8=Q, e1=N
            j = ord(move[0]) - ord('a')
            i = 8 - int(move[1])
            if white:
                if new_pos[i, j] == '' and new_pos[i+1, j] == 'p':
                    new_pos[i, j] = move[3].lower()
                    new_pos[i+1, j] = ''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i, j] == '' and new_pos[i-1, j] == 'P':
                    new_pos[i, j] = move[3].upper()
                    new_pos[i-1, j]= ''
                else:
                    raise IllegalMoveError(move)
        ### add en passant
        else:
            raise IllegalMoveError(move)
        
        return new_pos

    def knight_move(self, white, position, move):
        knight=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        
        def get_knight(pos,i,j,symbol,ambiguous='',moves=knight):
            found=0
            for move in moves:
                if 0<=i+move[0]<8 and 0<=j+move[1]<8 and pos[i+move[0],j+move[1]]==symbol: #if knight is found
                    if ambiguous:
                        if ambiguous in 'abcdefgh':
                            if chr(j+move[1]+97)==ambiguous: # if column is specified
                                coords=(i+move[0],j+move[1])
                                found+=1
                                print("flag1",coords)
                        elif ambiguous in '12345678': # if row is specified
                            if 8-(i+move[0])==int(ambiguous):
                                coords=(i+move[0],j+move[1])
                                found+=1
                                print("flag2",coords)
                    else:
                        found+=1
                        coords=(i+move[0],j+move[1])
                        print("flag3",coords)
                    if found==2: #ambiguous move without specifying row or column
                        raise ambigousMoveError(move)
            if found==1:
                return coords
            raise IllegalMoveError(move)
        
        new_pos=position.copy() #make sure to return a copy of the board and not changin the original
        if re.match(r'[n][a-h][1-8]', move,re.IGNORECASE): #simple knight move: Nf3, Nf6, Nh3, Nh6
            i=8-int(move[2])
            j=ord(move[1])-ord('a')
            if white:
                if new_pos[i,j]=='':
                    search=get_knight(new_pos,i,j,'n')
                    if search:
                        i0,j0=search
                        new_pos[i,j]='n'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i,j]=='':
                    search=get_knight(new_pos,i,j,'N')
                    if search:
                        i0,j0=search
                        new_pos[i,j]='N'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
        elif re.match(r'[n][x][a-h][1-8]', move,re.IGNORECASE): #knight capture move: Nxf3, Nxf6, Nxh3, Nxh6 
            i=8-int(move[3])
            j=ord(move[2])-ord('a')
            if white:
                if new_pos[i,j] in 'PRNBQ':
                    if get_knight(new_pos,i,j,'n'):
                        i0,j0=get_knight(new_pos,i,j,'n')
                        new_pos[i,j]='n'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i,j] in 'prnbq':
                    if get_knight(new_pos,i,j,'N'):
                        i0,j0=get_knight(new_pos,i,j,'N')
                        new_pos[i,j]='N'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
        elif re.match(r'[n][a-h1-8][a-h][1-8]', move,re.IGNORECASE): #ambiguous knight move: N2f3, Nf3, Nf3, Nf3
            i=8-int(move[3])
            j=ord(move[2])-ord('a')
            a=move[1].lower()
            if white:
                if new_pos[i,j]=='':
                    search=get_knight(new_pos,i,j,'n',a)
                    if search:
                        i0,j0=search
                        new_pos[i,j]='n'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i,j]=='':
                    search=get_knight(new_pos,i,j,'N',a)
                    if search:
                        i0,j0=search
                        new_pos[i,j]='N'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
        elif re.match(r'[n][a-h1-8][x][a-h][1-8]', move,re.IGNORECASE): #knight capture move: Nfxf3, Nfxf6, N3xh3, N2xh6
            i=8-int(move[4])
            j=ord(move[3])-ord('a')
            a=move[1].lower() #ambiguity specifier
            if white:
                if new_pos[i,j] in 'PRNBQ':
                    search=get_knight(new_pos,i,j,'n',a)
                    if search:
                        i0,j0=search
                        new_pos[i,j]='n'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i,j] in 'prnbq':
                    search=get_knight(new_pos,i,j,'N',a)
                    if search:
                        i0,j0=search
                        new_pos[i,j]='N'
                        new_pos[i0,j0]=''
                else:
                    raise IllegalMoveError(move)
        else:
            raise InvalidMoveError(move)
        return new_pos
        
    def capture(self, position):
        # Implement the logic for capturing an opponent's piece
        pass

    def promote(self, new_piece):
        # Implement the logic for promoting a pawn to a new piece
        pass

if __name__=="__main__":
    start_board= np.array([
        ['R','N','B','Q','K','B','','R'],
        ['P','P','P','P','P','P','P','P'],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','n','','','','n','',''],
        ['','','','','','','',''],
        ['p','p','p','p','p','p','p','p'],
        ['r','','b','q','k','b','','r']
    ])
old_pos=start_board
pos=np.copy(old_pos)
white=True
while True:
    board=Display(pos)
    print(f'{"white" if white else board.colored("black")} to play')
    move=input("Enter move: \n")
    if move=="q":
        break
    elif move=="back":
        pos=old_pos
        white=not white
        continue
    piece=ChessPiece('w',start_board)
    try:
        position=piece.knight_move(white,pos,move)
        board=Display(position)
        old_pos=np.copy(pos)
        pos=position
        white=not white
    # finally:
    #     pass
    except Exception as e:
        print(f"Error: {e}")
        print(traceback.format_exc())
        input("press any key to continue...")

    

