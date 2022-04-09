
import numpy as np
import time
from agents.MCNode import MCNode


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
            self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
            self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}

    def set_barrier(self, r, c, dir):
        # Set the barrier to True
        self.chess_board[r, c, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        try:
            self.chess_board[r + move[0], c + move[1], self.opposites[dir]] = True
        except IndexError:
            return None
        


    # READ THIS
    # as ppt9 p13, for current node we generate some steps with default policy, when we reach the end we record it by backpopa. 
    # mark the success trun with visited +1 and success +1. for every depth of the tree we choose highest success/visited.

    # tree policy: ?
    # default policy: random choice


    # selesction -> select root as current

    # expansion -> in node class


    def simulate(self, node):
        def _simulate_single(node, available_pos):
            success = False
            x,y,_ = self.chess_board.shape
            start_time = time.time()

            while not success:
                other_x_next = np.random.randint(x)
                other_y_next = np.random.randint(y)
                other_b_next = np.random.randint(4)

                i = np.random.randint(len(available_pos))
                x_next, y_next = available_pos[i]
                b_next = np.random.randint(4)

                collision = (other_x_next==x_next) and (other_y_next==y_next)
                barrier_setted = (self.set_barrier(other_x_next,other_y_next,other_b_next)) and (self.set_barrier(x_next,y_next,b_next))
                if not collision and barrier_setted:
                    success = True
                if time.time() > start_time+1:
                    break

            # not record it to the tree by not recoding children
            next_node = MCNode(self.chess_board, (x_next,y_next), (other_x_next,other_y_next),b_next, parent=node)
            return next_node

        # check if it is end of game
        reach_end, tmp =node.check_close_area()
        while not reach_end:
            available_pos = tmp
            next_node = _simulate_single(node, available_pos)
            node = next_node
            reach_end, tmp =node.check_close_area()

        area, adv_area = tmp
        return node, (area, adv_area)


    def backpopagation(self, tree_node):
        '''tree_node: starting node that stored in tree'''
        # TODO: this is not exactly 100% success
        node, areas = self.simulate(tree_node)
        my_area, adv_area = areas
        while node.parent != None:
            node = node.parent
            node.add_visit()
            if my_area > adv_area:
                node.add_score(1)
            elif my_area == adv_area:
                node.add_score(.5)
        # this should end at root


    def build_tree(self, max_time=30-2):
        # manage our run time
        node = self.root
        start_time = time.time()
        end_time = start_time + max_time

        while time.time() < end_time:
            if node.isLeaf():
                tmp = node.expand()
                if not tmp:
                    return self.root
                for child in node.children:
                    self.backpopagation(child)
            else:
                node = node.highest_child()

        # TODO: this is just a check
        print('tree building time: ', (time.time()-start_time))

        return self.root


    '''def search(self, max_step, max_time=2):
        end_time = time.time() + max_time
        node = self.root
        for i in range(max_step):
            if time.time() >= end_time:
                print('wuwu: search time exceeds')
                return node
            node = node.highest_child()'''
        # search -> node.highest_child() 
        
            

           





