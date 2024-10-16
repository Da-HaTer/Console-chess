from board import Board
from draw import Display
from time import sleep
import numpy as np
# import re
from piece import ChessPiece
from board import Board
from logic import Logic
from logic import IllegalMoveError, InvalidMoveError, ambigousMoveError
from draw import Display
import traceback
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.white = True
        self.moves = []
        self.positions=[self.board.matrix_to_fen(self.board.start_board,False)]
        self.game_end = False


    def handle_user_input(self): #unused for now
        ## Handle user input here
        # simple input for now
        pass

    def update_game(self,piece,pos,white,board,moves,checkmate): #unused for now
        ## Update the game state here
        if piece.Checkmate(pos,white,board):
                checkmate=True
                if moves:
                    moves[-1]=moves[-1]+"#"
                # print('moves :',moves)
                print("\033[31mCheckmate\033[0m")
                print("FEN :",Board().matrix_to_fen(pos,True))
                print("PGN :", Board().Moves_to_Pgn(moves))
                return checkmate
        #check if the game is over
        #check if the king is in check
        #check if the move is valid
        #check if the move puts the king in check
        # self.board.randomize_board_dirty()
        pass

    def render_game(self):
        ## Render the game here
        # Display(self.board.board_position)
        pass

    def game_loop(self):
        # Game loop       
        start_board=self.board.start_board 
        pgn="1. d4 d5 2. Bg5 { D00 Queen's Pawn Game: Levitsky Attack } Nf6 3. Bxf6 gxf6 4. Nd2 e6 5. e4 c5 6. exd5 Qxd5 7. Ndf3 Nc6 8. c3 cxd4 9. cxd4 Bb4+ 10. Ke2 Qe4# { Black wins by checkmate. } 0-1"
        # pgn =re.sub(r'\{.*?\}\s', '', pgn) #remove comments
        premoves=self.board.pgn_to_moves(pgn) #Autoplay moves (faster without gui)
        premoves=[]
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
            if piece.Checkmate(pos,white,board):
                checkmate=True
                if moves:
                    moves[-1]=moves[-1]+"#"
                # print('moves :',moves)
                print("\033[31mCheckmate\033[0m")
                print("FEN :",Board().matrix_to_fen(pos,True))
                print("PGN :", Board().Moves_to_Pgn(moves))
                break
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
                if move=="":
                    continue
                if move.lower() == "exit":
                    break
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
                
                old_pos=np.copy(pos)
                old_en_passant=en_passant[:]
                pos=position
                if move[0]!="B" or move[0] not in ("N","R","Q","K"):
                    moves.append((move[0]+move[1:].lower()))
                else:
                    moves.append((move[0].upper()+move[1:].lower()))
                white=not white
            except Exception as e:
                print(traceback.format_exc())
                print("fen :",Board().matrix_to_fen(old_pos,False))
                input("press any key to continue...")


if __name__ == "__main__":
    game = ChessGame()
    game.game_loop()