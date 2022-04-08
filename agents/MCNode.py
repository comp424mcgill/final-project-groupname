

import numpy as np
from copy import deepcopy
from agents.agent import Agent
from store import register_agent

class MCNode():
    '''
    class for Monte Carlo Tree node
    '''
    def __init__(self,chess_board, my_pos, adv_pos, barrier='u', parent=None, depth=0):
        """
        Parameters
        ----------
        visited: number of visiting
        success: number of visiting which our palyer success
        my_pos: coordinates of current state
        barrier: array of boolean of lenth = 4
        """
        self.my_pos = my_pos
        self.adv_pos = adv_pos
        self.barrier = barrier
        self.chess_board = chess_board
        self.parent = parent
        self.children = []
        self.visit = 0
        self.success = 0
        self.depth = depth

    def isLeaf(self):
        return (len(self.children) == 0)

    def add_visit(self): 
        self.visit += 1
    
    def add_score(self, score): 
        self.success += score

    def set_barrier(self, x, y, b):
        # same func as Tree
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
                add, visited_map += area_runner(visited_map, x, y+1, step_num)
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
    def expand(self, num_children=30):
        # possible leaf to expand, if cant expand return false
        reach_end, tmp = self.check_close_area()
        if reach_end:
            return False
        available_pos = tmp

        for i in np.random.randint(0, len(available_pos), min(len(available_pos),num_children)):
            x,y = available_pos[i]
            if x==self.adv_pos[0] and y==self.adv_pos[1]:
                continue
            b = 0
            while not self.set_barrier(x, y, b) and b<4:
                b += 1
            #TODO: adv_pos
            child = MCNode(self.chess_board, (x,y), self.adv_pos, b, parent=self, depth=self.depth+1)
            self.children += [child]

        return True 

    def highest_child(self):
        highest_score = 0
        highest_child = self
        for child in self.children:
            if child.visit == 0:
                continue
            child_score = child.success/child.visit
            if child_score > highest_score:
                highest_score = child.score
                highest_child = child
        return highest_child

    def sort_children(self):
        scores = []
        for i in self.children:
            score=i.success / i.visit +  np.sqrt( 2*np.log (self.visit) / i.visit)
            scores += score
        sorted_children = [x for _,x in sorted(zip(scores, self.children), reverse=True)]
        return sorted_children