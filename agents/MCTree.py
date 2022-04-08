import imp
from multiprocessing import Barrier
import numpy as np
from copy import deepcopy
import time
from sympy import root
from agents.agent import Agent
from store import register_agent
from MCNode import MCNode


class MCTree():
    '''
    class for Monte Carlo Search Tree
    '''
    def __init__(self, chess_board, root):
            """
            Parameters
            ----------
            root: root node of tree
            """
            self.chess_board = chess_board
            self.root = root

    '''
    def build_tree(self, max_time):
        current_node = self.root
        end_time = time.time() + max_time
        while time.time() < end_time:
            if current_node.isLeaf():
                tmp = current_node.expand()
                if not tmp:
                    return current_node
            else:
                # TODO: above is pseudocode, add function
                # or just end before else? but runtime will exceed
                # do we have to make a guess on Area
                current_node = current_node.childrenWithMaxArea()
        return current_node

    def search(self, max_time, max_step):
        for i in range(max_step):
            current_node = root
            end_time = time.time() + max_time
            if time.time() >= end_time:
                # TODO: change break to return
                break

            while not (current_node.isLeaf()):
                # TODO: above is pseudocode, add function
                # or just end before else? but runtime will exceed
                # do we have to make a guess on Area
                current_node = current_node.childrenWithMaxArea()
            # TODO: use node.visit() to avoid revisiting same coord'''


    def set_barrier(self, x, y, b):
        # same func as node
        if not 0<=b<=3:
            return False

        if self.chess_board[x][y][b] == False:
            self.chess_board[x][y][b] = True
            # neighbor's wall
            if b == 0 :
                self.chess_board[x][y-1][2] = True
            elif b == 2 :
                self.chess_board[x][y+1][0] = True
            elif b == 1 :
                self.chess_board[x+1][y][3] = True 
            else:
                self.chess_board[x-1][y][1] = True 
            return True

        return False

    # READ THIS
    # as ppt9 p13, for current node we generate some steps with default policy, when we reach the end we record it by backpopa. 
    # mark the success trun with visited +1 and success +1. for every depth of the tree we choose highest success/visited.

    # tree policy: ?
    # default policy: random choice


    # selesction -> select root as current

    def expansion(self):
        if not self.root.expand():
            # TODO: reach end
            '''
            # above 3 lines is right but not in correct position
            player_area = self.root.area()
            board_area = self.board_area.shape[0] * self.board_area.shape[1]'''

            return 0
        
    def simulate_single(self):
        success = False
        x,y,_ = self.board_area.shape

        reach_end, tmp =self.root.check_close_area()
        if reach_end:
            return tmp  # area
        available_x, available_y = tmp

        while not success:
            other_x_next = np.random.randint(x)
            other_y_next = np.random.randint(y)
            other_b_next = np.random.randint(4)

            i = np.random.randint(len(available_x))
            x_next = available_x[i]
            y_next = available_y[i]
            b_next = np.random.randint(4)

            collision = (other_x_next==x_next) and (other_y_next==y_next)
            barrier_setted = (self.set_barrier(other_x_next,other_y_next,other_b_next)) and (self.set_barrier(x_next,y_next,b_next))
            if not collision and barrier_setted:
                success = True

    def backpopagation(self):
        return 0






