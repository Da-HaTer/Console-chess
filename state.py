from board import Board
from piece import Piece

class State(Board,Piece):
    def __init__(self,):
        

    def add_transition(self, transition):
        self.transitions.append(transition)

    def __str__(self):
        return self.name