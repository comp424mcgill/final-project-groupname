
import numpy as np
from copy import deepcopy
from agents.agent import Agent
from store import register_agent

class MCNode():
    '''
    class for Monte Carlo Tree node
    '''
    def __init__(self,chess_board, coord, barrier, parent=None):
            """
            Parameters
            ----------
            visited: number of visiting
            success: number of visiting which our palyer success
            coord: coordinates of current state
            barrier: array of boolean of lenth = 4
            """
            self.coord = coord
            self.barrier = barrier
            self.chess_board = chess_board
            self.parent = parent
            self.children = []
            self.visit = 0
            self.success = 0

    def isLeaf(self):
        return (len(self.children) == 0)

    def set_barrier(self, x, y, b):
        # b for direction of barrier
        if self.chess_board[x][y][b] == False:
            self.chess_board[x][y][b] = True
            return True
        return False


    # tree policy here
    def expand(self):
        # TODO:  possible leaf to expand, if cant expand return false
        return True

    def area(self):
        # TODO: if cant expand(i.e. end of game), calc our area
        return 0 
    
