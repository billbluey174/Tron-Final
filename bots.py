#!/usr/bin/python

import numpy as np
from tronproblem import *
from trontypes import CellType, PowerupType
import random, math

# Throughout this file, ASP means adversarial search problem.


class StudentBot:
    """ Write your student bot here"""

    def __init__(self):
        self.BOT_NAME = "Filthy Frank"

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}

        To get started, you can get the current
        state by calling asp.get_start_state()
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        """
        Input: None
        Output: None

        This function will be called in between
        games during grading. You can use it
        to reset any variables your bot uses during the game
        (for example, you could use this function to reset a
        turns_elapsed counter to zero). If you don't need it,
        feel free to leave it as "pass"
        """
        pass

    def heuristic(self, state):
        """
        Takes in a TronState, returns a value indicating how good the state is
        :param state: TronState
        :return: a single value
        """
        ptm = state.ptm
        player_loc = state.player_locs[ptm] # current player's location
        enemy_loc = state.player_locs[1-ptm]
        frontiers = [set(), set()]
        frontiers[ptm].add(player_loc)
        frontiers[1-ptm].add(enemy_loc)
        visited = set()
        scores = [0, 0]
        while len(frontiers[0])>0 and len(frontiers[1])>0:
            if (len(frontiers[ptm])==0):
                ptm = 1 - ptm
                continue
            
            new_frontiers = set()
            while len(frontiers[ptm])>0:
                curr = frontiers[ptm].pop()
                visited.add(curr)
                
                scores[ptm] += self.evaluate_square(state.board, curr)
                
                new_frontiers.add((player_loc[0]-1,player_loc[1]))
                new_frontiers.add((player_loc[0],player_loc[1]-1))
                new_frontiers.add((player_loc[0]+1,player_loc[1]))
                new_frontiers.add((player_loc[0],player_loc[1]+1))
                
            ptm = 1 - ptm
        
        
        
        
        return scores[state.ptm]
        '''
        score = 0
        board = state.board
        for i in range(len(board)):
            for j in range(len(board[0])):
                player_dist = abs(player_loc[0]-i) + abs(player_loc[1]-j)
                enemy_dist = abs(enemy_loc[0]-i) + abs(enemy_loc[1]-j)
                if board[i][j]==" ":
                    if (player_dist<enemy_dist):
                        score+=1
                    elif (player_dist>enemy_dist):
                        score-=1
                elif board[i][j]=="#" or board[i][j]=="x":
                    if (player_dist<enemy_dist):
                        score-=1
                    elif (player_dist>enemy_dist):
                        score+=1
                elif board[i][j]=="@":
                    if (player_dist<enemy_dist):
                        score+=10
                    elif (player_dist>enemy_dist):
                        score-=10
                elif board[i][j]=="!":
                    if (player_dist<enemy_dist):
                        score+=10
                    elif (player_dist>enemy_dist):
                        score-=10
                elif board[i][j]=="^":
                    if (player_dist<enemy_dist):
                        score+=10
                    elif (player_dist>enemy_dist):
                        score-=10
                elif board[i][j]=="*":
                    if (player_dist<enemy_dist):
                        score+=10
                    elif (player_dist>enemy_dist):
                        score-=10
                elif board[i][j]=="?":
                    if (player_dist<enemy_dist):
                        score+=10
                    elif (player_dist>enemy_dist):
                        score-=10
        return score
'''
class RandBot:
    """Moves in a random (safe) direction"""

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if possibilities:
            return random.choice(possibilities)
        return "U"

    def cleanup(self):
        pass


class WallBot:
    """Hugs the wall"""

    def __init__(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def cleanup(self):
        order = ["U", "D", "L", "R"]
        random.shuffle(order)
        self.order = order

    def decide(self, asp):
        """
        Input: asp, a TronProblem
        Output: A direction in {'U','D','L','R'}
        """
        state = asp.get_start_state()
        locs = state.player_locs
        board = state.board
        ptm = state.ptm
        loc = locs[ptm]
        possibilities = list(TronProblem.get_safe_actions(board, loc))
        if not possibilities:
            return "U"
        decision = possibilities[0]
        for move in self.order:
            if move not in possibilities:
                continue
            next_loc = TronProblem.move(loc, move)
            if len(TronProblem.get_safe_actions(board, next_loc)) < 3:
                decision = move
                break
        return decision
