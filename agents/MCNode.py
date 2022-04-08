
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


    def check_close_area(self):
        def _is_valid_step(chess_board, visited_map, x, y, direction):
            if direction=='l':
                if chess_board[x][y][3]:
                    return False
                x += 1  
            if direction=='r':
                if not chess_board[x][y][1]: 
                    return False
                x -= 1  
            if direction=='u':
                if not chess_board[x][y][0]: 
                    return False
                y -= 1  
            if direction=='d':
                if not chess_board[x][y][2]: 
                    return False
                y += 1  
            return visited_map[x][y]==0 and 0<=x<chess_board.shape[0] and 0<=y<chess_board.shape[1]

        def area_runner(chess_board, visited_map, x, y):
            visited_map[x][y] = 1
            area = 1
            if _is_valid_step(chess_board, visited_map, x, y, 'l'):
                area += area_runner(chess_board, visited_map, x+1, y)
            if _is_valid_step(chess_board, visited_map, x, y, 'r'):
                area += area_runner(chess_board, visited_map, x-1, y)
            if _is_valid_step(chess_board, visited_map, x, y, 'u'):
                area += area_runner(chess_board, visited_map, x, y-1)
            if _is_valid_step(chess_board, visited_map, x, y, 'd'):
                area += area_runner(chess_board, visited_map, x, y+1)
            return area

        board = self.chess_board
        x,y = self.coord
        visited_map = np.zeros([board.shape[0], board.shape[1]])    
        # if a coord is visited change it to 1
        
        area = area_runner(board, visited_map, x, y)
        # TODO: do we have to check if meet the other player? maybe not
        if area == board.shape[0] * board.shape[1]:
            return False, area
        return True, area

        