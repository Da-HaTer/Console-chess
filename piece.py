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
    def ambiguity(self,move,specifier,moves):# return one single move given specified ambuity constraints otherwise None
        unique=[]
        for mv in moves:
            if specifier in mv:
                unique.append(mv)
        if len(unique)==0:
            raise InvalidMoveError(move)
        elif len(unique)>1:
            print(f"\033[31mchoose between {' '.join(unique)}\033[0m")
            raise ambigousMoveError(move)
        return unique[0] #return move


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
        elif re.fullmatch(r'[a-h][x][a-h][1-7]', move):# pawn capture move: exd4, dxe4, exd4, dxe4
            j1 = ord(move[0]) - ord('a')
            j2 = ord(move[2]) - ord('a')
            i = 8 - int(move[3])
            if abs(j1-j2) != 1: #not diagonally capturing ### add custom en passant
                raise IllegalMoveError(move)
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
        elif re.fullmatch(r'[a-h][x][a-h][18][=][QRBN]', move, re.IGNORECASE): # pawn promotion move: exd8=Q, dxe1=N
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
        elif re.fullmatch(r'[a-h][18][=][QRBN]', move, re.IGNORECASE): # pawn promotion move: e8=Q, e1=N
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

    # def knight_move(self, white, position, move):
    #     knight_moves=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        
    #     def get_knight(pos,i,j,symbol,ambiguous='',moves=knight_moves): #knight position search to check if move valid
    #         found=0
    #         for move in moves:
    #             if 0<=i+move[0]<8 and 0<=j+move[1]<8 and pos[i+move[0],j+move[1]]==symbol: #if knight is found
    #                 if ambiguous:
    #                     if len(ambiguous)==1:
    #                         if ambiguous in 'abcdefgh':
    #                             if chr(j+move[1]+97)==ambiguous: # if column is specified
    #                                 coords=(i+move[0],j+move[1])
    #                                 found+=1
    #                         elif ambiguous in '12345678': # if row is specified
    #                             if 8-(i+move[0])==int(ambiguous):
    #                                 coords=(i+move[0],j+move[1])
    #                                 found+=1
    #                     elif len(ambiguous)==2: #if both row and column are specified
    #                         if chr(j+move[1]+97)==ambiguous[0] and 8-(i+move[0])==int(ambiguous[1]):
    #                             coords=(i+move[0],j+move[1])
    #                             found+=1
    #                 else:
    #                     found+=1
    #                     coords=(i+move[0],j+move[1])
    #                 if found>1: #ambiguous move without specifying row or column
    #                     raise ambigousMoveError(move)
    #         if found==1:
    #             return coords
    #         raise IllegalMoveError(move)
        
    #     new_pos=position.copy() #make sure to return a copy of the board and not changin the original
    #     if re.fullmatch(r'[n][a-h][1-8]', move,re.IGNORECASE): #simple knight move: Nf3, Nf6, Nh3, Nh6
    #         i=8-int(move[2])
    #         j=ord(move[1])-ord('a')
    #         if white:
    #             if new_pos[i,j]=='':
    #                 search=get_knight(new_pos,i,j,'n')
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='n'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #         else:
    #             if new_pos[i,j]=='':
    #                 search=get_knight(new_pos,i,j,'N')
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='N'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #     elif re.fullmatch(r'[n][x][a-h][1-8]', move,re.IGNORECASE): #knight capture move: Nxf3, Nxf6, Nxh3, Nxh6 
    #         i=8-int(move[3])
    #         j=ord(move[2])-ord('a')
    #         if white:
    #             if new_pos[i,j] in 'PRNBQ':
    #                 if get_knight(new_pos,i,j,'n'):
    #                     i0,j0=get_knight(new_pos,i,j,'n')
    #                     new_pos[i,j]='n'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #         else:
    #             if new_pos[i,j] in 'prnbq':
    #                 if get_knight(new_pos,i,j,'N'):
    #                     i0,j0=get_knight(new_pos,i,j,'N')
    #                     new_pos[i,j]='N'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #     elif re.fullmatch(r'[n][a-h1-8][a-h][1-8]', move,re.IGNORECASE): #ambiguous knight move: N2f3, Nf3, Nf3, Nf3
    #         i=8-int(move[3])
    #         j=ord(move[2])-ord('a')
    #         a=move[1].lower()
    #         if white:
    #             if new_pos[i,j]=='':
    #                 search=get_knight(new_pos,i,j,'n',a)
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='n'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #         else:
    #             if new_pos[i,j]=='':
    #                 search=get_knight(new_pos,i,j,'N',a)
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='N'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #     elif re.fullmatch(r'[n][a-h1-8][x][a-h][1-8]', move,re.IGNORECASE): #knight capture move: Nfxf3, Nfxf6, N3xh3, N2xh6
    #         i=8-int(move[4])
    #         j=ord(move[3])-ord('a')
    #         a=move[1].lower() #ambiguity specifier
    #         if white:
    #             if new_pos[i,j] in 'PRNBQ':
    #                 search=get_knight(new_pos,i,j,'n',a)
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='n'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #         else:
    #             if new_pos[i,j] in 'prnbq':
    #                 search=get_knight(new_pos,i,j,'N',a)
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='N'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #     elif re.fullmatch(r'[n][a-h][1-8][x][a-h][1-8]', move,re.IGNORECASE): #ambiguous knight capture move: Nf5xe5, Nd3xc4, nd3xc4, Nd3xf5
    #         i0=8-int(move[2])
    #         j0=ord(move[1])-ord('a')
    #         i=8-int(move[5])
    #         j=ord(move[4])-ord('a')
    #         if white:
    #             if new_pos[i,j] in 'PRNBQ':
    #                 search=get_knight(new_pos,i,j,'n',move[1:3])
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='n'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #         else:
    #             if new_pos[i,j] in 'prnbq':
    #                 search=get_knight(new_pos,i,j,'N',move[1:3])
    #                 if search:
    #                     i0,j0=search
    #                     new_pos[i,j]='N'
    #                     new_pos[i0,j0]=''
    #             else:
    #                 raise IllegalMoveError(move)
    #     else:
    #         raise InvalidMoveError(move)
    #     return new_pos
    
    def capture(self, position):
        # Implement the logic for capturing an opponent's piece
        pass

    def promote(self, new_piece):
        # Implement the logic for promoting a pawn to a new piece
        pass

    def c2i(self, pos): # notation to x,y coordinate
        i,j=8-int(pos[1]),ord(pos[0])-ord('a')
        return(i,j)
    def i2c(self, pos):
        i,j=pos
        return chr(j+97)+str(8-i)
    def Ranged_DFS(self,pos,i,j,symbol,moves_kernel): # returns all valid rooks that can make this
        found=[]
        debug=True
        """uncomment for debug visuals:"""
        if debug:
            display=Display(pos,"green")
            display.Highlight((i,j))
        for move in moves_kernel: # for direction
            for k in range(1,8): 
                if 0<=i+k*move[0]<8 and 0<=j+k*move[1]<8: #within bounds
                    """# uncomment for debug visuals:"""
                    if debug:
                        display.Highlight((i+k*move[0],j+k*move[1]))
                    
                    square=pos[i+k*move[0],j+k*move[1]]
                    if square and square!=symbol: # obstructing piece
                        break # next direction
                    elif square==symbol: #found rook
                        found.append((i+k*move[0],j+k*move[1])) #add coords of rook to found list
                        break
                else:
                    break # out of bounds search next direction
        if debug:
            display.Highlight()
        return [self.i2c(square) for square in found]
    def Instant_DFS(self,pos,i,j,symbol,moves_kernel): # returns all valid rooks that can make this ### resuble for r,q,b
            found=[]
            debug=True
            if debug:
                display=Display(pos,"green")
                display.Highlight((i,j))
            for move in moves_kernel: # for direction
                if 0<=i+move[0]<8 and 0<=j+move[1]<8: #within bounds
                    if debug:
                        display.Highlight((i+move[0],j+move[1]))
                    
                    square=pos[i+move[0],j+move[1]]
                    if square==symbol: #found knight
                        found.append((i+move[0],j+move[1])) #add coords of knight to found list
            if debug:
                display.Highlight()
            return [self.i2c(square) for square in found]
          
    def get_new_pos(self,move,position,symbol,ambiguous,kernel,short_range=False):
        new_pos=position.copy()
        capture="x" in move

        tgt=move[-2:]
        i,j=self.c2i(tgt)
        if short_range:
            candidates=self.Instant_DFS(position,i,j,symbol,kernel)
        else:
            candidates=self.Ranged_DFS(position,i,j,symbol,kernel) # all pieces that could have made this move
        piece=self.ambiguity(move,ambiguous,candidates)

        if capture:
            print(white,position[i,j],piece)
            if ((white and position[i,j] in 'PRNBQ') or (not white and position[i,j] in 'prnbq')) and position[self.c2i(piece)]==symbol:
                new_pos[i,j]=symbol
                new_pos[self.c2i(piece)]='' 
            else:
                raise IllegalMoveError(move)
        else:
            if position[i,j]=='':
                new_pos[i,j]=symbol
                new_pos[self.c2i(piece)]=''
            else:
                raise InvalidMoveError(move)

        return new_pos
        
    def rook_move(self,white,position,move):
        #interpret move 

        symbol="r" if white else "R"
        rook_syntax = re.compile(r'^([a-h]|[1-8])?x?[a-h][1-8]$') # valid Rook move syntax
        ambiguous= re.match(r"^([a-h]|[1-8])x?[a-h][1-8]$",move) #returns the ambigious part , either a letter or a number
        ambiguous=ambiguous[1] if ambiguous else ""
        kernel=[(1,0),(-1,0),(0,1),(0,-1)]
        if rook_syntax.match(move):
            return self.get_new_pos(move,position,symbol,ambiguous,kernel)
        else:
            raise InvalidMoveError(move)

    def bishop_move(self,white,position,move):
        #interpret move 
        symbol="b" if white else "B"
        bishop_syntax = re.compile(r'^[a-h]?[1-8]?x?[a-h][1-8]$') # valid bishop move syntax
        ambiguous= re.match(r"^([a-h]|[1-8]|[a-h][1-8])x?[a-h][1-8]$",move) #returns the ambigious part , either a letter or a number
        ambiguous=ambiguous[1] if ambiguous else ""
        kernel=[(1,1),(-1,-1),(-1,1),(1,-1)]
        if bishop_syntax.match(move):
            return self.get_new_pos(move,position,symbol,ambiguous,kernel)
        else:
            raise InvalidMoveError(move)

    def knight_move(self,white,position,move):
        #interpret move 
        symbol="n" if white else "N"
        kernel=[(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]
        knight_syntax = re.compile(r'^[a-h]?[1-8]?x?[a-h][1-8]$') # valid bishop move syntax
        ambiguous= re.match(r"^([a-h]|[1-8]|[a-h][1-8])x?[a-h][1-8]$",move) #returns the ambigious part , either a letter or a number
        ambiguous=ambiguous[1] if ambiguous else ""

        if knight_syntax.match(move):
            return self.get_new_pos(move,position,symbol,ambiguous,kernel,short_range=True)
        else:
            raise InvalidMoveError(move)

    def queen_move(self,white,position,move):
        #interpret move 
        symbol="q" if white else "Q"
        queen_syntax = re.compile(r'^[a-h]?[1-8]?x?[a-h][1-8]$')
        ambiguous= re.match(r"^([a-h]|[1-8]|[a-h][1-8])x?[a-h][1-8]$",move) #returns the ambigious part , either a letter or a number
        ambiguous=ambiguous[1] if ambiguous else ""
        kernel=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        if queen_syntax.match(move):
            return self.get_new_pos(move,position,symbol,ambiguous,kernel)
        else:
            raise InvalidMoveError(move)
        
    def King_move(self,white,position,move):
        #interpret move 
        symbol="k" if white else "K"
        king_syntax = re.compile(r'^x?[a-h][1-8]$')
        ambiguous= None
        kernel=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        if king_syntax.match(move):
            return self.get_new_pos(move,position,symbol,ambiguous,kernel,short_range=True)
        else:
            raise InvalidMoveError(move)
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
old_pos=start_board
pos=np.copy(old_pos)
white=True
while True:
    board=Display(pos)
    w='\033[1m'+"white"+'\033[0m' # bold repr
    print(f'{ w if white else board.colored("black")} to play')
    move=input("Enter move: [move]|back|skip \n")
    if move=="q":
        break
    elif move=="back":
        pos=old_pos
        white=not white
        continue
    elif move=="skip":
        white=not white
        continue
    piece=ChessPiece('w',start_board)
    try:
        ### conflict between b pawn and bishop notation should probably be resolved with classifying by syntax instead of throwing errors right away
        ##example: bxc4 could be a pawn move or a bishop move
        ## solution: bishop: capital letter, pawn: small letter b
        if move[0] in 'abcdefgh':  
            position=piece.pawn_move(white,pos,move)
        elif move[0].lower() == 'n':
            position=piece.knight_move(white,pos,move[1:])
        elif move[0] == 'B':
            position=piece.bishop_move(white,pos,move[1:])
        elif move[0].lower()=='r':
            position=piece.rook_move(white,pos,move[1:])
        elif move[0].lower()=='q':
            position=piece.queen_move(white,pos,move[1:])
        elif move[0].lower()=='k':
            position=piece.King_move(white,pos,move[1:])
        else:
            raise InvalidMoveError(move)
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
