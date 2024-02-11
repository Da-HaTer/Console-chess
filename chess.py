from os import system
from time import sleep
import numpy as np

class chess_game:
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
    def __init__(self):
        self.board = self.start_board
        self.turn = 0
        # self.winner = None
        self.moves = []
        self.symbols = self.piece_to_symbol()
        self.print_matrix_in_grid(self.board,self.symbols)
    def setboard(self,board=start_board,moves=[],turn=0):
        self.board = board
        self.turn = turn
        self.moves=moves
        self.print_matrix_in_grid(self.board,self.symbols)

    def randomize_board_dirty(self):
        arr=self.board
        arr = arr.flatten()
        np.random.shuffle(arr)
        arr = arr.reshape((8, 8))
        self.board=arr

        self.turn = 0
        self.moves = []
        self.print_matrix_in_grid(self.board,self.symbols)
    def print_matrix_in_grid(self,matrix,d):
        system('cls')
        l,c=matrix.shape
        print(' __'*(c))
        for i in range(l):
            print('|',end='')
            for j in range(c):
                if matrix[i,j]=='':
                    print('  ',end='|')
                else:
                    print(d[matrix[i,j]],end='|')
            print()
        print(' --'*(c))
    def parse_move(self,move):
        pass

    def fen_to_matrix(self,fen):
        fen = fen.split(' ')[0]
        fen = fen.split('/')
        board = np.array([['']*8 for i in range(8)])
        for i in range(8):
            j = 0
            for k in fen[i]:
                if k.isdigit():
                    j += int(k)
                else:
                    board[i,j] = k
                    j += 1
        return board

    def matrix_to_fen(self,matrix):
        fen = ''
        for i in range(8):
            j = 0
            for k in matrix[i]:
                if k == '':
                    j += 1
                else:
                    if j > 0:
                        fen += str(j)
                        j = 0
                    fen += k
            if j > 0:
                fen += str(j)
            if i < 7:
                fen += '/'
        print(fen)
        return fen

    def pgn_to_moves(self,pgn):
        pgn = pgn.split(' ')
        moves = []
        for i in pgn:
            if '.' in i:
                continue
            moves.append(i)
        return moves

    def king_in_check(self,board,turn):
        pass


    def pawn_move(self,board,move,turn):	
        pawns=['a','b','c','d','e','f','g','h']
        if move[0].low() in pawns:
            if turn==0:
                board[8-int(move[1]),pawns.index(move[0])]='P'
            else:
                board[8-int(move[1]),pawns.index(move[0])]='p'    

    def piece_to_symbol(self):
        symbols=['♔','♕','♖','♗','♘','♙','♚','♛','♜','♝','♞','♟']
        pieces=['K','Q','R','B','N','P','k','q','r','b','n','p']
        d=dict()
        for i in range(12):
            d[pieces[i]]=symbols[i]+' '
        return d

    def print_matrix_in_grid(self,matrix,d):
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
    
    def move_pawn(self,board,coordinate):
        l,c=coordinate
        if l==1:
            board[l,c]=''
            board[l+2,c]='P'
        else:
            board[l,c]=''
            board[l-2,c]='p'
        return board
    
game=chess_game()
# # fen test
# fen="q3kb1r/1p2pppp/5n2/2rp4/3Q1B2/4PN2/P1n2PPP/R3K2R w KQk - 0 14"
# board=game.fen_to_matrix(fen)

# # set board tests
# game.setboard(board)
# game.setboard()
game.randomize_board_dirty()
game.matrix_to_fen(game.board)
# print_matrix_in_grid(board,d)
# for i in range(8):
#     break
#     board=move_pawn(board,(1,i))
#     print_matrix_in_grid(board,d)
#     sleep(0.4)
#     board=move_pawn(board,(6,i))
#     print_matrix_in_grid(board,d)
#     sleep(0.4)

# # print_matrix_in_grid(board,d)
# # print(matrix_to_fen(board))
# fen="q3kb1r/1p2pppp/5n2/2rp4/3Q1B2/4PN2/P1n2PPP/R3K2R w KQk - 0 14"
# # b=(fen_to_matrix(fen))
# # print_matrix_in_grid(b,d)
# pgn="e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 O-O c3 d5 exd5 Nxd5 Nxe5 Nxe5 Rxe5 c6 d4 Bd6 Re1 Qh4 g3 Qh3 Be3 Bg4 Qd3 Rae8 Nd2 Re6 a4 Qh5 axb5 axb5 Bxd5 cxd5 Qxb5 Rb8 Qa5 Rxb2 Qd8+ Bf8 Ra8 h6 Qxf8+ Kh7 Qh8+ Kg6 Rg8 Rxe3 Qxg7+ Kf5 Qxf7#"
# print(pgn_to_moves(pgn))