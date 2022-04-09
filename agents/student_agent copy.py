# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
from agents.MCNode import MCNode
from agents.MCTree import MCTree
import numpy as np

@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.autoplay = True
        #self.step_number = 0
        self.tree = None
        self.node = None
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """
        if self.tree == None:
            self.set_tree(chess_board, my_pos, adv_pos)

        _, available_pos = self.node.check_close_area(max_step=max_step, only_get_avail=True)
        if adv_pos in available_pos:
            available_pos.remove(adv_pos)
        children = self.node.children

        next = self.node.highest_child(children)
        while not (next.my_pos in available_pos) and len(children)>0:
            children.remove(next)
            next = self.node.highest_child(children)
        return next.my_pos, next.barrier


    def set_tree(self, chess_board, my_pos, adv_pos):
        root = MCNode(chess_board, my_pos, adv_pos)
        self.tree = MCTree(chess_board, root)
        self.node = self.tree.build_tree()
        
