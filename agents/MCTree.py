
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

    # expansion -> in node class


    def simulate(self, node):
        def _simulate_single(node, available_x, available_y):
            success = False
            x,y,_ = self.board_area.shape

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

            # not record it to the tree by not recoding children
            next_node = MCNode(self.chess_board, (x_next,y_next), b_next, parent=node)
            return next_node

        # check if it is end of game
        reach_end, tmp =node.check_close_area()
        while not reach_end:
            available_x, available_y = tmp
            next_node = _simulate_single(node, available_x, available_y)
            node = next_node
            reach_end, tmp =node.check_close_area()

        area = tmp
        return node, area


    def backpopagation(self, tree_node):
        '''tree_node: starting node that stored in tree'''
        # TODO: this is not exactly 100% success
        node, area = self.simulate(tree_node)
        board_area = self.chess_board.shape[0] * self.chess_board.shape[1]
        while node.parent != None:
            node = node.parent
            node.add_visit()
            if area > (board_area/2):
                node.add_score(1)
            elif area == (board_area/2):
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
        # search -> node.highest_child() ???TODO
        
            

           





