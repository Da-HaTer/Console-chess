from board import Board
from draw import Draw_board
from time import time
from 
class ChessGame:
    def __init__(self):
        self.board = Board()
        self.turn = 0
        self.moves = []
        self.game_end = False


    def handle_user_input(self):
        ## Handle user input here
        # simple input for now
        pass

    def update_game(self):
        ## Update the game state here
        #check if the game is over
        #check if the king is in check
        #check if the move is valid
        #check if the move puts the king in check
        # self.board.randomize_board_dirty()
        pass

    def render_game(self):
        ## Render the game here
        Draw_board(self.board.board_position)

    def game_loop(self):
        # Game loop
        while not self.game_end:
            move=input('Enter move: ')
            while not valid_move(self.board.board_position,move):
                move=input('Enter valid move: ')
            
            # print(time(), end='\r')
            self.handle_user_input()
            self.update_game()
            self.render_game()

if __name__ == "__main__":
    game = ChessGame()
    game.game_loop()