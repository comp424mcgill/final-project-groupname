import imp
import numpy as np
from copy import deepcopy
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

    def build_tree(self, max_time):
        current_node = self.root
        end_time = time.time() + max_time
        while time.time() <= end_time:
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




