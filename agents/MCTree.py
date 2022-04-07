import imp
import numpy as np
from copy import deepcopy

from sympy import root
from agents.agent import Agent
from store import register_agent
from MCNode import MCNode
import time

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

    # READ THIS
    # as ppt9 p13, for current node we generate some steps with default policy, when we reach the end we record it by backpopa. 
    # #mark the success trun with visited +1 and success +1. for every depth of the tree we choose highest success/visited.

    # tree policy: ?
    # default policy: random choice

    def selection(self):
        return 0
    
    def expansion(self):
        return 0
    
    def simulation(self):
        return 0

    def backpopagation(self):
        return 0






