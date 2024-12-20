import numpy as np
import regex as re
from time import sleep
from board import Board
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
        #move: user input
        #specier example: "a" for a1, "1" for a1, "a1" for a1
        #moves: list of possible moves
        unique=[]
        for mv in moves: ### can have issues (test if )
            if specifier in mv:
                unique.append(mv)
        if len(unique)==0:
            raise InvalidMoveError(move)
        elif len(unique)>1:
            print(f"\033[31mchoose between {' '.join(unique)}\033[0m")
            raise ambigousMoveError(move)
        return unique[0] #return move

    def c2i(self, pos): # notation to x,y coordinate
        i,j=8-int(pos[1]),ord(pos[0])-ord('a')
        return(i,j)

    def i2c(self, pos):
        i,j=pos
        return chr(j+97)+str(8-i)

    def boundries(self,i,j):
        return i>=0 and i<8 and j>=0 and j<8

    def Ranged_DFS(self,pos,i,j,symbol,moves_kernel): # returns all valid rooks that can make this
        found=[]
        debug=False
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
            debug=False
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

    def Pawn_Dfs(self,pos,i,j,white,ep=[None,None]): # returns all valid pawns that can make this move
        debug=False
        from time import sleep
        if debug:
            display=Display(pos,"green")
            display.Highlight((i,j))
        symbol="p" if white else "P"
        found=[]
        direction=1 if white else -1
        en_passant=ep[1] if white else ep[0]
        pawn_kernel=[]
        if  pos[i,j]=="": #pawn found
            pawn_kernel+=[(direction,0)]# simple move
        if (i==4 and white) or (i==3 and not white) and pos[i,j]=='' : # double move
            pawn_kernel+=[(2*direction,0)]
        if  (white and pos[i,j] in ('B','P','N','R','Q') ) or (not white and pos[i,j] in ('b','p','n','r','q')): #capture move
            pawn_kernel+=[(direction,1),(direction,-1)] # diagonal captures 
        if en_passant and pos[i,j]=="": # en passant
            # input("en passant!!")
            # print(en_passant)
            col=ord(en_passant[0]) - ord('a')
            if white and self.boundries(3,col+1) and pos[3,col+1]=="p": #pawn adjacent (right)
                # print("en passant",self.i2c((3,col+1)))
                # input("test1")
                found.append((3,col+1))
            if white and self.boundries(3,col-1) and pos[3,col-1]=="p": #pawn adjacent (left)
                # print("en passant",self.i2c((3,col-1)))
                # input("test2")
                found.append((3,col-1))
            elif not white and self.boundries(4,col+1) and pos[4,col+1]=="P": #pawn adjacent (right)
                # print("en passant",self.i2c((4,col+1)))
                # input("test3")
                found.append((4,col+1))
            elif not white and self.boundries(4,col-1) and pos[4,col-1]=="P": #pawn adjacent (left)
                # print("en passant",self.i2c((4,col-1)))
                # input("test4")
                found.append((4,col-1))
        for move in pawn_kernel:
            # sleep(0.2)
            if self.boundries(i+move[0],j+move[1]):
                if debug:
                    display.Highlight((i+move[0],j+move[1]))
                square=pos[i+move[0],j+move[1]]
                if square==symbol: #found pawn
                    found.append((i+move[0],j+move[1]))
        # if debug:
        #     display.Highlight()
        return [self.i2c(square) for square in found]

    def Reverse_Pawn_Dfs(self,pos,i,j,white,ep=[None,None],early_exit=False): # returns all moves that this pawn can make
        #i,j= position of pawn
        friends=('b','p','n','r','q') if white else ('B','P','N','R','Q')
        foes=('b','p','n','r','q') if not white else ('B','P','N','R','Q')
        symbol="p" if white else "P"
        found=[]
        direction=1 if not white else -1
        en_passant=ep[1] if white else ep[0] #pawn tha has en passant state
        if self.boundries(i+direction,j) and pos[i+direction,j]=="": # simple move
            if early_exit:
                return True
            found.append((i+direction,j))
        if self.boundries(i+direction,j+1) and pos[i+direction,j+1] in foes:#diagonal capture
            if early_exit:
                return True
            found.append((i+direction,j+1))
        if self.boundries(i+direction,j-1) and pos[i+direction,j-1] in foes:#diagonal capture
            if early_exit:
                return True
            found.append((i+direction,j-1))
        if white and i==6 and pos[i-2,j]=="" and pos[i-1,j]=="": #two square move
            if early_exit:
                return True
            found.append((i-2,j))
        if not white and i==1 and pos[i+2,j]=="" and pos[i+1,j]=="": #two square move
            if early_exit:
                return True
            found.append((i+2,j))
        if en_passant:
            if white and i==3 and self.boundries(3,j+1) and (3,j+1)==en_passant:
                if early_exit:
                    return True
                found.append((2,j+1))
            elif white and i==3 and self.boundries(3,j-1) and (3,j-1)==en_passant:
                if early_exit:
                    return True
                found.append((2,j-1))
            elif not white and i==4 and self.boundries(4,j+1) and (4,j+1)==en_passant:
                if early_exit:
                    return True
                found.append((5,j+1))
            elif not white and i==4 and self.boundries(4,j-1) and (4,j-1)==en_passant:
                if early_exit:
                    return True
                found.append((5,j-1))
        return found #return all possible moves (squares)

    def get_new_pos(self,move,position,white,symbol,ambiguous,kernel,short_range=False): #used for all pieces except pawns
        new_pos=position.copy()
        capture="x" in move

        tgt=move[-2:]
        i,j=self.c2i(tgt)
        if short_range:
            candidates=self.Instant_DFS(position,i,j,symbol,kernel)
        else:
            candidates=self.Ranged_DFS(position,i,j,symbol,kernel) # all pieces that could have made this move
        piece=self.ambiguity(move,ambiguous,candidates) #return one single move given specified ambuity constraints otherwise None

        if capture:
            # print(white,position[i,j],piece)
            if ((white and position[i,j] in ('B','P','N','R','Q')) or (not white and position[i,j] in ('b','p','n','r','q'))) and position[self.c2i(piece)]==symbol:
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

    def pawn_move(self, white, position, move): #hardcoded
        new_pos=position.copy()
        en_passant=None
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
                    en_passant=move[0]
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
                    en_passant=move[0]
                else:
                    raise IllegalMoveError(move)
        elif re.fullmatch(r'[a-h][x][a-h][1-7]', move):# pawn capture move: exd4, dxe4, exd4, dxe4
            j1 = ord(move[0]) - ord('a')
            j2 = ord(move[2]) - ord('a')
            i = 8 - int(move[3])
            if abs(j1-j2) != 1: #not diagonally capturing ### add custom en passant
                raise IllegalMoveError(move)
            if white:
                if new_pos[i, j2] in ('B','P','N','R','Q') and new_pos[i+1, j1] == 'p':
                    new_pos[i, j2] = 'p'
                    new_pos[i+1, j1] = ''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i, j2] in ('b','p','n','r','q') and new_pos[i-1, j1] == 'P':
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
                if new_pos[i, j2] in ('B','P','N','R','Q') and new_pos[i+1, j1] == 'p':
                    new_pos[i, j2] = move[5].lower()
                    new_pos[i+1, j1] = ''
                else:
                    raise IllegalMoveError(move)
            else:
                if new_pos[i, j2] in ('b','p','n','r','q') and new_pos[i-1, j1] == 'P':
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
        return (new_pos,en_passant)

    def pawn_move2(self,white,position,move,en_passant=[None,None]): ### Run Tests
        pawn_syntax= re.compile(r'^([a-h][x])?[a-h][1-8]=?[rbnq]?$',re.IGNORECASE)
        if not pawn_syntax.match(move):
            raise InvalidMoveError(move)
        square= re.search(r'[a-h][1-8]',move,re.IGNORECASE)[0]
        symbol="p" if white else "P"
        promote=re.search(r'=[QRBN]$',move,re.IGNORECASE)
        capture=re.search(r'^[a-h][x]',move,re.IGNORECASE)
        if promote:
            symbol=move[-1].lower() if white else move[-1].upper()

        i,j= self.c2i(square)

        promote=promote[0][1] if promote else ""
        capture=capture[0][0] if capture else ""
        
        if promote and not ((i==0 and white) or (i==7 and not white)):# invalid promotion square
            raise InvalidMoveError(move) #invalid promotion
        new_pos=position.copy()
        Pawns=self.Pawn_Dfs(position,i,j,white,en_passant)

        # print("Candidates: ",Pawns)
        # sleep(1)
        if len(Pawns)==0:
            raise InvalidMoveError(move)
        else:
            pawn=self.ambiguity(move,capture,Pawns)
            # print("Selected: ",pawn)
            # sleep(0.5)
            new_pos[i,j]=symbol
            new_pos[self.c2i(pawn)]=''
            if white:
                en_passant[0]=None
                if i==4 and pawn[1]=="2": #two square move
                    en_passant[0]=square
            else: #two square move
                en_passant[1]=None
                if i==3 and pawn[1]=="7":
                    en_passant[1]=square
            return (new_pos,en_passant)
        
    def rook_move(self,white,position,move):
        #interpret move 

        symbol="r" if white else "R"
        rook_syntax = re.compile(r'^([a-h]|[1-8])?x?[a-h][1-8]$') # valid Rook move syntax
        ambiguous= re.match(r"^([a-h]|[1-8])x?[a-h][1-8]$",move) #returns the ambigious part , either a letter or a number
        ambiguous=ambiguous[1] if ambiguous else ""
        kernel=[(1,0),(-1,0),(0,1),(0,-1)]
        if rook_syntax.match(move):
            return self.get_new_pos(move,position,white,symbol,ambiguous,kernel)
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
            return self.get_new_pos(move,position,white,symbol,ambiguous,kernel)
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
            return self.get_new_pos(move,position,white,symbol,ambiguous,kernel,short_range=True)
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
            return self.get_new_pos(move,position,white,symbol,ambiguous,kernel)
        else:
            raise InvalidMoveError(move)
        
    def King_move(self,white,position,move):
        #interpret move 
        symbol="k" if white else "K"
        king_syntax = re.compile(r'^x?[a-h][1-8]$')
        ambiguous= ""
        kernel=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        if king_syntax.match(move):
            return (self.get_new_pos(move,position,white,symbol,ambiguous,kernel,short_range=True),self.c2i(move[-2:])) # board and king position
        else:
            raise InvalidMoveError(move)

    def King_check(self,board,white,position=None):
        check=False
        checks=[]
        symbol="k" if white else "K"
        #attacking pieces
        knight="N" if white else "n"
        bishop="B" if white else "b"
        rook="R" if white else "r"
        queen="Q" if white else "q"
        if position is None:    
            king_pos=(-1,-1)
            for i in range(8): # find king in board
                for j in range(8):
                    if board[i,j]==symbol:
                        king_pos=(i,j)
                        break
            if king_pos==(-1,-1):
                raise Exception("King not found")
            i,j=king_pos
        else:
            i,j=position
        # pawn checks:
        if (white and ((self.boundries(i-1,j+1) and board[i-1,j+1]=="P" )or (self.boundries(i-1,j-1) and board[i-1,j-1]=="P")))\
              or (not white and((self.boundries(i+1,j+1) and  board[i+1,j+1]=="p" )or (self.boundries(i+1,j-1) and board[i+1,j-1]=="p"))): #if pawn check
            checks.append((i,j))
            # input("pawn check")
            ### red highlight ?

        rooks=self.Ranged_DFS(board,i,j,rook,[(1,0),(-1,0),(0,1),(0,-1)])
        if rooks:
            checks+=rooks
            # input("rook check")
        knights=self.Instant_DFS(board,i,j,knight,[(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)])
        if knights:
            checks+=knights
            # input("knight check")
        bishops=self.Ranged_DFS(board,i,j,bishop,[(1,1),(-1,-1),(-1,1),(1,-1)])
        if bishops:
            checks+=bishops
            # input("bishop check")
        queens=self.Ranged_DFS(board,i,j,queen,[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)])
        if queens:
            checks+=queens
            # input("queen check")
        return (checks) # all checking squares and position of the king
    
    def Castle(self,board,white,move): #if path not blocked, not in check, not gonna move through check, not gonna end up in check
        ### todo: check for king or rook moves that prevent castle
        new_pos=board.copy()
        if not white:
            if move=="O-O": 
                if new_pos[0,5]=='' and new_pos[0,6]==''and not self.King_check(new_pos,white,(0,4)) and not self.King_check(new_pos,white,(0,5)) and not self.King_check(new_pos,white,(0,6)):
                    new_pos[0,5]='R'
                    new_pos[0,6]='K'
                    new_pos[0,4]=''
                    new_pos[0,7]=''
                else:
                    raise IllegalMoveError(move)
            elif move=="O-O-O":
                if new_pos[0,1]=='' and new_pos[0,2]=='' and new_pos[0,3]=='' and not self.King_check(new_pos,white,(0,4)) and not self.King_check(new_pos,white,(0,3)) and not self.King_check(new_pos,white,(0,2)):
                    new_pos[0,3]='R'
                    new_pos[0,2]='K'
                    new_pos[0,4]=''
                    new_pos[0,0]=''
                else:
                    raise IllegalMoveError(move)
        else:
            if move=="O-O":
                if new_pos[7,5]=='' and new_pos[7,6]=='' and not self.King_check(new_pos,white,(7,4)) and not self.King_check(new_pos,white,(7,5)) and not self.King_check(new_pos,white,(7,6)):
                    new_pos[7,5]='r'
                    new_pos[7,6]='k'
                    new_pos[7,4]=''
                    new_pos[7,7]=''
                else:
                    raise IllegalMoveError(move)
            elif move=="O-O-O":
                if new_pos[7,1]=='' and new_pos[7,2]=='' and new_pos[7,3]=='' and not self.King_check(new_pos,white,(7,4)) and not self.King_check(new_pos,white,(7,3)) and not self.King_check(new_pos,white,(7,2)):
                    new_pos[7,3]='r'
                    new_pos[7,2]='k'
                    new_pos[7,4]=''
                    new_pos[7,0]=''
                else:
                    raise IllegalMoveError(move)
        return new_pos

    def Checkmate(self,board,white,draw=None,kingpos=None): #draw is a Display object
        debug=False
        Checkmate=True
        def interpolate(start,end):
            i,j=start
            k,l=end
            if i==k: #horizontal
                return [(i,m) for m in range(min(j,l),max(j,l))]
            elif j==l: #vertical
                return [(m,j) for m in range(min(i,k),min(i,k))]
            elif abs(k-i)==abs(l-j):
                return [(i+m,j+m) for m in range(1,abs(k-i))]
            else:
                return [(i+m,j+n) for m in range(1,abs(k-i)) for n in range(1,abs(l-j)) if abs(k-i)==abs(l-j) and m==n]
            
        king_kernel=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
        symbol="k" if white else "K"
        friendlies=('b','p','n','r','q') if white else ('B','P','N','R','Q')
        if kingpos is None: #get king position
            for i in range(8):
                for j in range(8):
                    if board[i,j]==symbol:
                        kingpos=(i,j)
                        break
        checks=self.King_check(board,white,kingpos)
        if not checks:
            # input("no checks")
            return False
        for move in king_kernel: #if can move
            square=(kingpos[0]+move[0],kingpos[1]+move[1])
            new_pos=board.copy()
            if not self.boundries(square[0],square[1]) or board[square[0],square[1]] in friendlies: #invalid square or capture own pieces
                if debug:
                    draw.Highlight(square)
                    pass
                continue
            new_pos[kingpos[0],kingpos[1]]=''
            new_pos[square[0],square[1]]=symbol
            if self.King_check(new_pos,white,square):#moving into check
                if debug:
                    # draw.Highlight(square)
                    # sleep(1)
                    pass
                continue
            else:
                # input("can move")
                return False
        else:
            attacker=self.c2i(checks[0])
            for square in interpolate(kingpos,attacker):
                for symbol in "brq" if white else "BRQ":
                    if symbol in ('r','R'):
                        kernel=[(1,0),(-1,0),(0,1),(0,-1)]
                    elif symbol in ('b','B'):
                        kernel=[(1,1),(-1,-1),(-1,1),(1,-1)]
                    elif symbol in ('q','Q'):
                        kernel=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(-1,1),(1,-1)]
                    piece=self.Ranged_DFS(board,square[0],square[1],symbol,kernel)
                    if piece:
                        print(piece)
                        input("piece can capture")
                        return False
                        
                symbol="n" if white else "N"
                if self.Instant_DFS(board,square[0],square[1],symbol,[(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]):
                    input("knight can capture")
                    return False
                    
                symbol="p" if white else "P"
                if self.Instant_DFS(board,square[0],square[1],symbol,[(1,1),(-1,-1),(-1,1),(1,-1)]):
                    input("pawn can capture")
                    return False
                    
        # input("checkmate")
        return Checkmate
            



        #check if king can get out check

        #check if any other piece can block the check

    def Valid_moves(self,pos,board,white,position,en_passant=None):
        symbol=pos[position]
        if symbol in ('p','P'):
            moves=self.Reverse_Pawn_Dfs(pos,position[0],position[1],white,en_passant,False) #all possible squares that this pawn can move to
            # board.Highlight(position)
            # print(moves)
            # input()
            # sleep(0.5)
            # board.Highlight(moves)
                #if valid move (no check or (illegal move ?(check)))
                    #RETURN FALSE
        elif symbol in ('n','N'):
            pass
            #if not pinned:
                #iterate 
                    #if can move
                    #RETURN FALSE
        elif symbol.lower() in ("r","b","q"): #rook, bishop, queen
            pass
            #if pinned :
                # if direction in kernel (can move within pin diagobal/ file/ rank)
                    #for move in (kernel ∩ direction)
                        #if can move
                        #Return FALSE
            #else (not pinned)
                #iterate
                    #if can move
                    #RETURN FALSE
        else: #king
            pass
            #if can move: (reuse from checkmate) - unified function ? 
                #RETURN FALSE
                    
                    

    def Stalemate(self,pos,board,white,en_passant=None):
        pieces=('b','p','n','r','q') if white else ('B','P','N','R','Q')
        for i in range(8):
            for j in range(8):
                for piece in pieces:
                    if pos[i,j]==piece:
                        moves=self.Valid_moves(pos,board,white,(i,j),en_passant)###
                        # if piece.lower()=="p":#pawn
                        if moves:
                            return False
        #check if any piece can move one by one, test en passant

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
    empty_board= np.array([
        ['','','','','K','','',''],
        ['','p','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','','','',''],
        ['','','','','k','','','']])
    pgn="1. d4 d5 2. Bg5 { D00 Queen's Pawn Game: Levitsky Attack } Nf6 3. Bxf6 gxf6 4. Nd2 e6 5. e4 c5 6. exd5 Qxd5 7. Ndf3 Nc6 8. c3 cxd4 9. cxd4 Bb4+ 10. Ke2 Qe4# { Black wins by checkmate. } 0-1"
    pgn =re.sub(r'\{.*?\}\s', '', pgn) #remove comments
    from board import Board
    pgn=Board().pgn_to_moves(pgn)
    pgn=[]
    i=0
    gui=True
    old_pos=start_board
    old_kings=[(7,4),(0,4)] #kings position
    kings=old_kings[:] # copy
    pos=np.copy(old_pos)
    white=True
    highlight=None
    en_passant=[None,None]
    old_en_passant=[None,None]
    checkmate=False
    moves=[]
    while True:
        piece=ChessPiece('w',start_board)
        board=Display(pos) if gui else None
        piece.Stalemate(pos,board,white,en_passant)
        if piece.Checkmate(pos,white,board):
            checkmate=True
            if moves:
                moves[-1]=moves[-1]+"#"
            print('moves :',moves)
            input("\033[31mCheckmate\033[0m")
        checks=(piece.King_check(pos,True),piece.King_check(pos,False))
        if white:
            en_passant[0]=None
        else:
            en_passant[1]=None
        highlight=None
        if checks[0]:
            if not checkmate:
                if moves:
                    moves[-1]=moves[-1]+"+" if moves[-1][-1]!="+" else moves[-1]
            highlight=kings[0]  
        if checks[1]:
            if not checkmate:
                if moves:
                    moves[-1]=moves[-1]+"+" if moves[-1][-1]!="+" else moves[-1]
            highlight=kings[1]
        if gui:
            board.Highlight(highlight)
        # print("white checks:", checks[0], "Black checks: ",checks[1])
        # print("enpassant:",en_passant[0],en_passant[1])
        # sleep(1)
        if i < len(pgn):
            move=pgn[i]
            i+=1
        else:
            w='\033[1m'+"white"+'\033[0m' # bold repr
            if gui:
                print(f'{ w if white else board.colored("black")} to play')
            # print("Kings pos:",f"{piece.i2c(kings[0])} {piece.i2c(kings[1])}")
            # print("Old Kings pos:",f"{piece.i2c(old_kings[0])} {piece.i2c(old_kings[1])}")
            # print("moves :",moves)
            move=input("Enter move: ( [move]|back|skip|reset|[Get/Set] FEN )\n")
        
        move=move.replace("+","") #remove check notation
        move=move.replace("#","") #remove checkmate notation
        if move=="q":
            break
        elif move=="back":
            pos=old_pos
            kings=old_kings
            en_passant=old_en_passant
            white=not white
            checkmate=False
            moves=moves[:-1]
            continue
        elif move=="skip":
            white=not white
            continue
        elif move=="reset":
            moves=[]
            pos=start_board
            kings=[(7,4),(0,4)]
            en_passant=[None,None]
            white=True
            highlight=None
            continue
        elif move.upper()=="GET FEN":
            Board().matrix_to_fen(pos,True)
            input("press any key to continue...")
            continue
        elif move.upper()=="SET FEN":
            fen=input("Enter FEN: ")
            pos=Board().fen_to_matrix(fen)
            old_pos=pos
            continue
        elif move.upper()=="GET PGN":
            print(' '.join([str(i+1)+'. '+moves[i] for i in range(len(moves))]))
            input("press any key to continue...")
            continue
        old_kings=kings[:]
        try:
            if move !="back" and move!="reset" and checkmate:
                raise IllegalMoveError("Checkmate")
            ### conflict between b pawn and bishop notation should probably be resolved with classifying by syntax instead of throwing errors right away
            ##example: bxc4 could be a pawn move or a bishop move
            ## solution: bishop: capital letter, pawn: small letter b
            if move[0] in 'abcdefgh':  
                t=piece.pawn_move2(white,pos,move,en_passant)
                position=t[0]
                en_passant=t[1]
                # i,j=piece.c2i(move[-2:])
                # piece.Pawn_Dfs(pos,i,j,white,en_passant[1] if white else en_passant[0])
            elif move[0].lower() == 'n':
                position=piece.knight_move(white,pos,move[1:])
            elif move[0] == 'B':
                position=piece.bishop_move(white,pos,move[1:])
            elif move[0].lower()=='r':
                position=piece.rook_move(white,pos,move[1:])
            elif move[0].lower()=='q':
                position=piece.queen_move(white,pos,move[1:])
            elif move[0].lower()=='k':
                king_move=piece.King_move(white,pos,move[1:])
                position=king_move[0]
                kings=[king_move[1],kings[1]] if white else [kings[0],king_move[1]] #update kings position (for optimization)
            
            elif move.lower() in ('o-o','o-o-o'):
                position=piece.Castle(pos,white,move)
            else:
                raise InvalidMoveError(move)
            checks=(piece.King_check(position,True),piece.King_check(position,False)) #check if king is in check
            if white and checks[0] or not white and checks[1]: 
                raise IllegalMoveError(f"\033[33m {move} \033[0m"+f"\n\033[31mKing is in check: {checks}\033[0m")
            
            # board=Display(position)
            old_pos=np.copy(pos)
            old_en_passant=en_passant[:]
            pos=position
            if move[0]!='B':
                moves.append((move.lower()))
            else:
                moves.append(('B'+move[1:].lower()))
            white=not white
        # finally:
        #     pass
        except Exception as e:
            # print(f"Error: {e}")
            print(traceback.format_exc())
            print("fen :",Board().matrix_to_fen(old_pos,False))
            input("press any key to continue...")
