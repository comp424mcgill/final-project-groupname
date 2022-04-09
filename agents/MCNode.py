

import numpy as np
from copy import deepcopy
from agents.agent import Agent
from store import register_agent

class MCNode():
    '''
    class for Monte Carlo Tree node
    '''
    def __init__(self,chess_board, my_pos, adv_pos, barrier=0, parent=None, depth=0):
        """
        Parameters
        ----------
        visited: number of visiting
        success: number of visiting which our palyer success
        my_pos: coordinates of current state
        """
        self.my_pos = my_pos
        self.adv_pos = adv_pos
        self.barrier = barrier
        self.chess_board = deepcopy(chess_board)
        self.board_size = chess_board.shape[0]    
        self.parent = parent
        self.children = []
        self.visit = 0
        self.score = 0
        self.depth = depth
        self.moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        self.opposites = {0: 2, 1: 3, 2: 0, 3: 1}

    def isLeaf(self):
        return (len(self.children) == 0)

    def add_visit(self): 
        self.visit += 1
    
    def add_score(self, add): 
        self.score += add

    '''def set_barrier(self, x, y, b):
        # same func as Tree
        if not 0<=b<=3:
            return False
        
        if self.chess_board[x][y][b] == False:
            self.chess_board[x][y][b] = True
            # neighbor's wall
            if b == 0 and y-1>0 :
                self.chess_board[x][y-1][2] = True
            elif b == 2 and y+1<len(self.chess_board[0]):
                self.chess_board[x][y+1][0] = True
            elif b == 1 and x+1<self.chess_board.shape[0]:
                self.chess_board[x+1][y][3] = True 
            elif x-1>0:
                self.chess_board[x-1][y][1] = True 
            else:
                return False
            return True
        return False'''

    def set_barrier(self, r, c, dir):
        # Set the barrier to True
        self.chess_board[r, c, dir] = True
        # Set the opposite barrier to True
        move = self.moves[dir]
        try:
            self.chess_board[r + move[0], c + move[1], self.opposites[dir]] = True
        except IndexError:
            return None

    def check_close_area(self, max_step=0, only_get_avail=False):
        '''
        if reach end, return True and area of our player get
        else, return False and available coord we can reach
        '''
        board = self.chess_board
        x,y = self.my_pos
        if max_step==0:
            max_step = board.shape[0]**2//2
        visited_map = np.zeros([board.shape[0], board.shape[1]])    
        # if a my_pos is visited change it to 1

        def _is_valid_step(visited_map, x, y, direction):
            if direction=='l':
                if not board[x][y][3]:
                    return False
                x += 1  
            if direction=='r':
                if not board[x][y][1]: 
                    return False
                x -= 1  
            if direction=='u':
                if not board[x][y][0]: 
                    return False
                y -= 1  
            if direction=='d':
                if not board[x][y][2]: 
                    return False
                y += 1  
            return  0<=x<board.shape[0] and 0<=y<board.shape[1] and visited_map[x][y]==0

        def area_runner(visited_map, x, y, step_num):
            step_num += 1
            if step_num > max_step:
                # record the steps excceed max step but still calc its area
                visited_map[x][y] = 2
            else:
                visited_map[x][y] = 1
            area = 1
            if _is_valid_step(visited_map, x, y, 'l'):
                add, visited_map = area_runner(visited_map, x+1, y, step_num)
                area += add
            if _is_valid_step(visited_map, x, y, 'r'):
                add, visited_map = area_runner(visited_map, x-1, y, step_num)
                area += add
            if _is_valid_step(visited_map, x, y, 'u'):
                add, visited_map = area_runner(visited_map, x, y-1, step_num)
                area += add
            if _is_valid_step(visited_map, x, y, 'd'):
                add, visited_map = area_runner(visited_map, x, y+1, step_num)
                area += add
            return area, visited_map

        area, visited_map = area_runner(visited_map, x, y, 0)
        available_x, available_y = np.where(visited_map==1)
        avail_pos = [(x,y) for x,y in zip(available_x, available_y)]
        
        if self.adv_pos in avail_pos or only_get_avail:
            return False, avail_pos
        else:
            adv_x, adv_y = self.adv_pos
            adv_area = area_runner(np.zeros([board.shape[0], board.shape[1]]), adv_x, adv_y, 0)[0]
            return True, (area, adv_area)


    # tree policy here, but i dont know what's that
    # so i just put default policy(random generate)
    def expand(self, num_children=20):
        # possible leaf to expand, if cant expand return false
        reach_end, tmp = self.check_close_area()
        if reach_end:
            return False
        available_pos = tmp

        for i in np.random.randint(0, len(available_pos), min(len(available_pos),num_children)):
            x,y = available_pos[i]
            if x==self.adv_pos[0] and y==self.adv_pos[1]:
                continue
            for b in range(4):
                if self.chess_board[x][y][b]==True:
                    continue
                child = MCNode(self.chess_board, (x,y), self.adv_pos, b, parent=self, depth=self.depth+1)
                self.children += [child]

        return True 

    def highest_child(self,children):
        highest_score = 0
        highest_child = self
        for child in children:
            if child.visit == 0:
                continue
            child_score = child.score/child.visit
            if child_score > highest_score:
                highest_score = child_score
                highest_child = child
        return highest_child

    ''' def sort_children(self):
        scores = []
        children = self.children
        for i in children:
            if i.visit == 0:
                scores += [0]
            else:
                score= i.score / i.visit +  np.sqrt( 2*np.log (self.visit) / i.visit)
                scores += [score]
        sorted_children = [x for _,x in sorted(zip(scores, children), reverse=True)]
        return sorted_children'''