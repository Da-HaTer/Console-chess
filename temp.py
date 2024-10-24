import numpy as np


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

matrix=np.ndarray((8,8),dtype=str)

#Loop

def mat(d:dict):
    return ' '.join([str(v)+k for k,v in d.items()])
        
def get_flag(matrix:np.ndarray)->tuple[str,tuple[int,int]]: #check for checkmate, stalemate and insufficient material returns flag and coordinates if needed
    bp=('B','P','N','R','Q') # black pieces
    wp=('b','p','n','r','q') # white pieces
    w_d=dict()
    b_d=dict()
    stalemate=True
    white=True
    for i in range(8):
        for j in range(8):

            #Update material dictionary (for material count)
            if matrix[i,j] in wp:
                if matrix[i,j] not in w_d:
                    w_d[matrix[i,j]]=1
                else:
                    w_d[matrix[i,j]]+=1
            elif matrix[i,j] in bp:
                if matrix[i,j] not in b_d:
                    b_d[matrix[i,j]]=1
                else:
                    b_d[matrix[i,j]]+=1

            #check for check & checkmate:
            if matrix[i,j].upper()=='K':
                if check(i,j,white,matrix):
                    if checkmate(i,j,white,matrix):
                        return("Checkmate",(i,j))
                    else:
                        return("Check",(i,j)) #can't be stalemate
            if matrix[i,j]!="":# a piece
                if all_moves(i,j,white,matrix)!=[]: ##all possible moves of this piece
                    stalemate=False
    if stalemate:
        return("Stalemate",None)
    mat_w,mat_b=mat(w_d),mat(b_d)
    insufficient_material= mat_w in ('','1b','1n','2n') and mat_b in ('','1B','1N','2N')
    if insufficient_material:
        return("Insufficient material")
    return (None,None)

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
            

while True:
    break
    # piece=Piece('w',start_board)
    # board=Display(pos) if gui else None
    flag=get_flag(matrix)
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
        print("fen :",Board().matrix_to_fen(old_pos,False))
        input("press any key to continue...")

if __name__=="__main__":
    start=4,4
    end=4,4
    print(interpolate(start,end))