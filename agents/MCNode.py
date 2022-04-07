
import numpy as np
from copy import deepcopy
from agents.agent import Agent
from store import register_agent

class MCNode():
    '''
    class for Monte Carlo Tree node
    '''
    def __init__(self,chess_board, state, parent=None):
            """
            Parameters
            ----------
            state: coordinate
            visit: number of visits
            """
            self.state = state
            self.chess_board = chess_board
            self.parent = parent
            self.children = []
            self.visit = 0

    def isLeaf(self):
        return (len(self.children) == 0)

    def expand(self):
        # TODO:  possible leaf to expand, if cant expand return false
        return True

    def find_area(self):
        # TODO: if cant expand(i.e. end of game), calc our area
        return 0 
    
    # def best_child(self):