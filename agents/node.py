import numpy as np
from copy import deepcopy
from agents.agent import Agent
from store import register_agent


class Node:
    '''
    class for monte carlo tree node
    '''
    def __init__(self, chess_board, state, move=None, parent=None):
        '''
        state: coordinate

        '''
        self.state = state
        self.chess_board = chess_board
        self.move = move
        self.parent = parent
        self.children = []
        self.visit = 0
    
    def is_leaf(self):
        return len(self.children) == 0 

    def expand(self):
        # TODO
        return 0

    def area(self):
        # TODO: calc area if end meet
        return 0
            