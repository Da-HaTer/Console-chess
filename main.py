from board import Board
from draw import Display
from time import sleep
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
        # Display(self.board.board_position)
        pass

    def game_loop(self):
        # Game loop
        pass

if __name__ == "__main__":
    game = ChessGame()
    game.game_loop()