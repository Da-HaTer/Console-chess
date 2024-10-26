import numpy as np
from board import State

def check(*a):
    return True

def checkmate(*a):
    return True

def all_moves(*a):
    return [1]

start_board= np.array([
['','','','','','','B',''],
['','','','','','','',''],
['','','','','','','',''],
['','','','','','','',''],
['','','','','','','',''],
['','','','','','','',''],
['','','','','n','n','',''],
['','','','','k','','K','']])

board=np.ndarray((8,8),dtype=str)

#Loop

boundries=lambda i,j: 0<=i<8 and 0<=j<8
c2i=lambda c: (8-int(c[1]),ord(c[0])-97)
i2c=lambda i,j: chr(j+97)+str(8-i)
def mat(d:dict)->str:
    """
    Convert matieral count dictionary to string (for insufficient material check)"""
    return ' '.join([str(v)+k for k,v in d.items()])

def can_move(board:State,frm:tuple[int,int],to:tuple[int,int],ep=None)->bool:
    """Check if a move is legal (doesn't walk into check or stay in check) , doesn't check for invalid moves (format ) """
    new_pos=np.copy(board[:])
    new_pos[to]=new_pos[frm]
    new_pos[frm]=''
    if ep:
        new_pos[ep]=''
    new_state=State(new_pos,board.white,board.castle,'-',0,board.fullmove_count+1,board.kings_pos)#white kept to check if check persists
    if check(new_state):
        return False
    return True

def LOOP(board:State): #check for checkmate, stalemate and insufficient material returns flag and coordinates if needed
    bp=('B','P','N','R','Q') # black pieces
    wp=('b','p','n','r','q') # white pieces
    w_d=dict()
    b_d=dict()
    stalemate=True
    white=True
    for i in range(8):
        for j in range(8):
            #Update material dictionary (for material count)
            if board[i,j] in wp:
                if board[i,j] not in w_d:
                    w_d[board[i,j]]=1
                else:
                    w_d[board[i,j]]+=1
            elif board[i,j] in bp:
                if board[i,j] not in b_d:
                    b_d[board[i,j]]=1
                else:
                    b_d[board[i,j]]+=1
            #check for check & checkmate:
            if board[i,j].upper()=='K':
                pos=(i,j)
                checks=check(board,pos)
                if checks:###to be implemented (returns many)
                    if checkmate(board,pos,checks):###to be implemented
                        return("Checkmate")
                    else:
                        return("Check") #can't be stalemate
            
            if board[i,j]!="":# a piece
                pos=i,j
                moves=all_moves(board,pos,early_exit=True)
                if moves!=[]: ##all possible moves of this piece
                    stalemate=False
    if stalemate:
        return("Stalemate")
    mat_w,mat_b=mat(w_d),mat(b_d)
    insufficient_material= mat_w in ('','1b','1n','2n') and mat_b in ('','1B','1N','2N')
    if insufficient_material:
        return("Insufficient material")
    return (None)

def Pawn_DFS(self,board:State,pos:tuple[int,int],early_exit=False)->list[tuple[int,int]]:
        """ Returns all possible valid moves of a pawn on the board
        """
        white=board.white
        i,j=pos
        friends,foes=('b','p','n','r','q','k'),('B','P','N','R','Q','K')
        friends,foes=(friends,foes) if white else (foes,friends)
        ep=c2i(board.en_passant) if board.en_passant!="-" else None# en passant pawn coordinates
        found=[]
        direction=1 if not white else -1
        if boundries(i+direction,j) and board[i+direction,j]=="": # simple move
            if can_move(board,pos,(i+direction,j)):
                if early_exit:
                    return True
                found.append((i+direction,j))

        for k in (-1,1): #diagonal capture 
            if boundries(i+direction,j+k) and board[i+direction,j+k] in foes:#diagonal capture
                if can_move(board,pos,(i+direction,j+k)):
                    if early_exit:
                        return True
                    found.append((i+direction,j+k))

        if i==1 and white or i==6 and not white:
            if board[i+direction,j]=="" and board[i+2*direction,j]=="":
                if can_move(board,pos,(i+2*direction,j)):
                    if early_exit:
                        return True
                    found.append((i+2*direction,j))

        if ep and ep[0]==i: #en passant
            for r in (3,4):#row 
                for c in (1,-1):#column offset
                    if (i%2)==white and boundries(r,j+c) and (r,j+c)==ep:
                        if can_move(board,pos,(r+direction,j+c),ep):
                            if early_exit:
                                return True
                            found.append((r,c))
        #### TO BE TESTED
        return found #return all possible moves (squares)
    
def Ranged_DFS(board:State,pos:tuple[int,int],early_exit=False)->list[tuple[int,int]]:
    """Returns all possible moves of a ranged piece on the board
    Rook, Bishop, Queen
    """
    i,j=pos
    piece=board[i,j]
    if piece.lower()=='r':
        moves_kernel=[(0,1),(1,0),(0,-1),(-1,0)]
    elif piece.lower()=='b':
        moves_kernel=[(1,1),(-1,-1),(1,-1),(-1,1)]
    elif piece.lower()=='q':
        moves_kernel=[(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]

    friends,foes=('b','p','n','r','q','k'),('B','P','N','R','Q','K')
    friends,foes=(friends,foes) if board.white else (foes,friends)
    found=[]
    for move in moves_kernel: # for direction
        for k in range(1,8): 
            if 0<=i+k*move[0]<8 and 0<=j+k*move[1]<8: #within bounds
                square=board[i+k*move[0],j+k*move[1]]
                if square in friends:
                    break # next direction
                elif square in foes or square =="": #can move or capture
                    if can_move(board,pos,(i+k*move[0],j+k*move[1])):
                        if early_exit:
                            return True
                        found.append((i+k*move[0],j+k*move[1]))
                    break
            else:
                break # out of bounds search next direction

    return [square for square in found]

def Instant_DFS(board:State,pos:tuple[int,int],early_exit=False)->list[any]:
    """Returns all possible moves of an instant piece on the board
    Knight, King
    """
    i,j=pos
    piece=board[i,j]
    if piece.lower()=='n':
        moves_kernel=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    elif piece.lower()=='k':
        moves_kernel=[(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]

    friends,foes=('b','p','n','r','q','k'),('B','P','N','R','Q','K')
    friends,foes=(friends,foes) if board.white else (foes,friends)
    found=[]
    for move in moves_kernel: # for direction
        if 0<=i+move[0]<8 and 0<=j+move[1]<8: #within bounds
            square=board[i+move[0],j+move[1]]
            if square in friends:
                break # next direction
            elif square in foes or square =="": #can move or capture
                if can_move(board,pos,(i+move[0],j+move[1])):
                    if early_exit:
                        return True
                    found.append((i+move[0],j+move[1]))
    return [square for square in found] 
   
def piece_moves(board:State,pos:tuple[int,int],early_exit:bool=False)->list[any]:
    """Returns all possible moves of a piece on the board
        use early_exit to check if a piece can make at least one move
    """
    i,j=pos
    piece=board[i,j]
    moves=[]
    if piece.lower == 'p':
        moves=Pawn_DFS(board,pos,early_exit)
    elif piece.lower in ('r','q','b'):
        moves=Ranged_DFS(board,pos,early_exit)
    elif piece.lower in ('n','k'):
        moves=Instant_DFS(board,pos,early_exit)
    return moves

def reverse_Ranged_DFS(board:State,pos:tuple[int,int],early_exit:bool=False)->list[any]:
    """searches for ranged pieces that can attack the given position
    """
    found=[]
    bishop_kernel=[(1,1),(-1,-1),(1,-1),(-1,1)]
    bishop_attackers=('B','Q') if board.white else ('b','q')
    rook_attackers=('R','Q') if board.white else ('r','q')
    friendlies=('b','p','n','r','q','k') if board.white else ('B','P','N','R','Q','K')
    rook_kernel=[(0,1),(1,0),(0,-1),(-1,0)]
    for kernel in (rook_kernel,bishop_kernel):
        attackers=rook_attackers if kernel==rook_kernel else bishop_attackers
        for move in bishop_kernel:
            for k in range(1,8):
                i,j=pos[0]+k*move[0],pos[1]+k*move[1]
                if boundries(i,j):
                    square=board[i,j]
                    if square in attackers:
                        if early_exit:
                            return True
                        found.append((i,j))
                    elif square in friendlies:
                        break
                else:
                    break
    return [square for square in found]
            
def reverse_Instant_DFS(board:State,pos:tuple[int,int],early_exit:bool=False)->list[any]:
    """searches for instant pieces that can attack the given position
    """
    found=[]
    knight_kernel=[(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
    king_kernel=[(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
    knight_attackers=('N') if board.white else ('n')
    king_attackers=('K') if board.white else ('k')
    friendlies=('b','p','n','r','q','k') if board.white else ('B','P','N','R','Q','K')
    for kernel in (knight_kernel,king_kernel):
        attackers=knight_attackers if kernel==knight_kernel else king_attackers
        for move in kernel:
            i,j=pos[0]+move[0],pos[1]+move[1]
            if boundries(i,j):
                square=board[i,j]
                if square in attackers:
                    if early_exit:
                        return True
                    found.append((i,j))

    return [square for square in found]

def reverse_Pawn_DFS(board:State,pos:tuple[int,int],early_exit:bool=False)->list[any]:
    """searches for pawns that can attack the given position
    """
    ### Test with en passant position
    found=[]
    i,j=pos
    attacker='P' if board.white else 'p'
    direction=-1 if board.white else 1
    en_passant=c2i(board.en_passant) if board.en_passant!="-" else None
    for k in (-1,1): #diagonal capture 
        if boundries(i+direction,j+k): #diagonal capture
            square=board[i+direction,j+k]
            if square ==attacker:
                if early_exit:
                    return True
                found.append((i+direction,j+k))
        elif en_passant and boundries(i,j+k) and board[i,j+k]==attacker and en_passant==(i,j+k):
            if early_exit:
                return True
            found.append((i,j+k))

    return [square for square in found]

def move_candidates(board:State,pos:tuple[int,int],early_exit:bool=False)->list[any]:
    """Returns all possible pieces that can move to pos (current player's pieces)
        use early_exit if you want to check if at least one piece can move to pos
    """
    i,j=pos
    moves=[]
    St=State(board[:],not board.white,board.castle,board.en_passant,board.halfmove_count,board.fullmove_count,board.kings_pos)
    #change turn to get friendly pieces instead of attackers
    dfs=reverse_Instant_DFS(St,pos,early_exit)
    if dfs:
        if early_exit:
            return True
        moves.append(dfs)
    dfs=reverse_Ranged_DFS(St,pos,early_exit)
    if dfs:
        if early_exit:
            return True
        moves.append(dfs)
    dfs=reverse_Pawn_DFS(St,pos,early_exit) ### en passant problem ?
    if dfs:
        if early_exit:
            return True
        moves.append(dfs)
    return moves

def interpolate(start:tuple[int,int],end:tuple[int,int]) ->list[tuple[int,int]]:
    """Returns all squares between two points on the board (exclusive)
    """
    i,j=start
    k,l=end
    dy,dx=k-i,l-j
    if i==k: #horizontal
        rg=range(j+1,l) if dx>0 else range(j-1,l,-1)
        return[(i,m) for m in rg]
    elif j==l: #vertical
        rg=range(i+1,k) if dy>0 else range(i-1,k,-1)
        return [(m,j) for m in rg]
    elif dy==dx: #diagonal with solpe=1
        rg=range(1,abs(k-i)) 
        dir=1 if dy>0 else -1
        return [(i+m*dir,j+m*dir) for m in rg]
    
    elif dy==-dx: #diagonal with slope=-1
        rg=range(1,abs(k-i)) 
        dir=1 if dy>0 else -1
        return [(i+m*dir,j-m*dir) for m in rg]
    return []

def check(board:State)->bool:
    """Returns weether the current player's king is in check
    searches in all directions for enemy pieces
    """
    i,j=board.kings_pos[0,1] if board.white else board.kings_pos[2,3]
    if reverse_Instant_DFS(board,(i,j),early_exit=True): #if a knight is attacking the king ###also searches for kings (prevents illegal king moves)
        return True
    elif reverse_Ranged_DFS(board,(i,j),early_exit=True): #if a ranged piece is attacking the king
        return True
    elif reverse_Pawn_DFS(board,(i,j),early_exit=True): #if a pawn is attacking the king
        return True
    return False    

def checkmate(board:State)->bool:
    """Returns weether the current player's king is in checkmate
    """
    i,j=board.kings_pos[0,1] if board.white else board.kings_pos[2,3]
    king_kernel=[(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
    for move in king_kernel:# can move out of check
        if boundries(i+move[0],j+move[1]) and can_move(board,(i,j),(i+move[0],j+move[1])):
            return False
    attackers=reverse_Ranged_DFS(board,(i,j))
    if len(attackers)>2:#can't block 
        return True
    for attacker in attackers:
        path=interpolate(i,j,attacker)
        for square in path:
            if move_candidates(board,square,early_exit=True):
                return False
    return True
            
def stalemate(board:State)->bool:
    """Returns weether the current player's king is in stalemate
    """
    pieces= ['b','p','n','r','q','k'] if board.white else ['B','P','N','R','Q','K']
    if check(board):
        return False
    for i in range(8):
        for j in range(8):
            if board[i,j] in pieces:
                if piece_moves(board,(i,j),early_exit=True):
                    return False            
    return True

while True:
    break
    # piece=Piece('w',start_board)
    # board=Display(pos) if gui else None
    flag=get_flag(board)
    if flag[0]=="checkmate":
        pass
        ##update moves
        # checkmate=True
        # if moves:
        #     moves[-1]=moves[-1]+"#"
        # print('moves :',moves)
        ##print stuff
        # print("\033[31mCheckmate\033[0m")
        # print("FEN :",Board().matrix_to_fen(pos,True))
        # print("PGN :", Board().Moves_to_Pgn(moves))
        # break
    elif flag[0]=="check":
        checks=(piece.King_check(pos,True),piece.King_check(pos,False)) ##checking pieces
    #reset en passant on each turn ### should move to piece 
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
    if i < len(premoves):
        move=premoves[i]
        i+=1
    else:
        w='\033[1m'+"white"+'\033[0m' # bold repr
        if gui:
            print(f'{ w if white else board.colored("black")} to play')
        # print("Kings pos:",f"{piece.i2c(kings[0])} {piece.i2c(kings[1])}")
        # print("Old Kings pos:",f"{piece.i2c(old_kings[0])} {piece.i2c(old_kings[1])}")
        # print("moves :",moves)
        move=input("Enter move: ( [move]|back|skip|reset|[Get/Set] FEN|Get PGN )\n")

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
        State().matrix_to_fen(pos,True)
        input("press any key to continue...")
        continue
    elif move.upper()=="SET FEN":
        fen=input("Enter FEN: ")
        pos=State().fen_to_matrix(fen)
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
        if move[0]!="B" or move[0] not in ("N","R","Q","K"):
            moves.append((move[0]+move[1:].lower()))
        else:
            moves.append((move[0].upper()+move[1:].lower()))
        white=not white
    # finally:
    #     pass
    except Exception as e:
        # print(f"Error: {e}")
        print(traceback.format_exc())
        print("fen :",State().matrix_to_fen(old_pos,False))
        input("press any key to continue...")

if __name__=="__main__":
    start=4,4
    end=4,4
    print(interpolate(start,end))
    mat()