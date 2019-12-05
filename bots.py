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
        # state = asp.get_start_state()
        # locs = state.player_locs
        # board = state.board
        # ptm = state.ptm
        # loc = locs[ptm]
        # possibilities = list(TronProblem.get_safe_actions(board, loc))
        # if possibilities:
        #     return random.choice(possibilities)
        choice = self.alpha_beta_cutoff(asp, 5)
        #print(choice)
        #print(self.heuristic(asp.get_start_state()))
        return choice

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

    def get_safe_moves(self,board, loc):
        #print(loc)
        safe = set()
        
        curr = (loc[0]-1,loc[1])
        spot = board[curr[0]][curr[1]]
        
        if spot == "#" or spot == "x" or spot == "1" or spot == "2":
            pass
        else:
            safe.add(U)
            
        curr = (loc[0]+1,loc[1])
        spot = board[curr[0]][curr[1]]
        
        if spot == "#" or spot == "x" or spot == "1" or spot == "2":
            pass
        else:
            safe.add(D)
        
        curr = (loc[0],loc[1]-1)
        spot = board[curr[0]][curr[1]]
        
        if spot == "#" or spot == "x" or spot == "1" or spot == "2":
            pass
        else:
            safe.add(L)
        
        curr = (loc[0],loc[1]+1)
        spot = board[curr[0]][curr[1]]
        
        if spot == "#" or spot == "x" or spot == "1" or spot == "2":
            pass
        else:
            safe.add(R)
        
        
        return safe

    def alpha_beta_cutoff(self, asp, cutoff_ply):
        """
        This function should:
        - search through the asp using alpha-beta pruning
        - cut off the search after cutoff_ply moves have been made.

        Inputs:
            asp - an AdversarialSearchProblem
            cutoff_ply- an Integer that determines when to cutoff the search
                and use eval_func.
                For example, when cutoff_ply = 1, use eval_func to evaluate
                states that result from your first move. When cutoff_ply = 2, use
                eval_func to evaluate states that result from your opponent's
                first move. When cutoff_ply = 3 use eval_func to evaluate the
                states that result from your second move.
                You may assume that cutoff_ply > 0.
            eval_func - a function that takes in a GameState and outputs
                a real number indicating how good that state is for the
                player who is using alpha_beta_cutoff to choose their action.
                You do not need to implement this function, as it should be provided by
                whomever is calling alpha_beta_cutoff, however you are welcome to write
                evaluation functions to test your implementation. The eval_func we provide
                does not handle terminal states, so evaluate terminal states the
                same way you evaluated them in the previous algorithms.

        Output: an action(an element of asp.get_available_actions(asp.get_start_state()))
        """

        return self.alpha_beta_cutoff_helper(asp.get_start_state(), True, asp, float("-inf"), float("inf"), cutoff_ply)[1]

    def alpha_beta_cutoff_helper(self, state, max_player, asp, alpha, beta, depth):
        """
        This helper is the recursive helper of alpha_beta. It takes in a state and asp, then
        returns an action.
        """

        # If the node is terminal, return its value
        if asp.is_terminal_state(state):
            return [asp.evaluate_state(state)[asp.get_start_state().player_to_move()], None]

        if depth == 0:
            return [self.heuristic(state), None]

        # Store the possible actions
        possible_actions = self.get_safe_moves(state.board, state.player_locs[state.ptm])
        #print(possible_actions)
        # If this is the player we want to maximize
        if max_player:

            # Create a value which represents the max value of the states below
            value = float("-inf")

            action = None

            # Loop through every possible action
            for x in possible_actions:

                # Find the value of every state below
                temp = self.alpha_beta_cutoff_helper(asp.transition(state, x), False, asp, alpha, beta, depth - 1)[0]

                # Change value's value if the temp is greater than value
                if value < temp:
                    value = temp
                    action = x

                if alpha < value:
                    alpha = value

                if alpha >= beta:
                    return [beta, None]

            # Return this value
            return [value, action]

        # If this is the player we want to minimize
        else:

            # Create a value which represents the max value of the states below
            value = float("inf")

            action = None

            # Loop through every possible action
            for x in possible_actions:

                # Find the value of every state below
                temp = self.alpha_beta_cutoff_helper(asp.transition(state, x), True, asp, alpha, beta, depth - 1)[0]

                # Change value's value if the temp is greater than value
                if value > temp:
                    value = temp
                    action = x

                if beta > value:
                    beta = value

                if alpha >= beta:
                    return [alpha, None]

            # Return this value
            return [value, action]

    def heuristic(self, state):
        """
        Takes in a TronState, returns a value indicating how good the state is
        :param state: TronState
        :return: a single value
        """
        ptm = 0
        player_loc = state.player_locs[ptm]
        enemy_loc = state.player_locs[1-ptm]
        frontiers = [set(), set()]
        frontiers[ptm].add(player_loc)
        frontiers[1-ptm].add(enemy_loc)
        visited = set()
        scores = [0, 0]
        walls = set()
        while len(frontiers[0]) > 0 or len(frontiers[1]) > 0:
            if len(frontiers[ptm]) == 0:
                ptm = 1 - ptm
                continue
            
            new_frontiers = set()
            while len(frontiers[ptm]) > 0:
                curr = frontiers[ptm].pop()
                visited.add(curr)
                
                value = self.evaluate_square(state.board,curr)
                
                scores[ptm] += value
                if value == 0:
                    walls.add(curr)
                
                new_states = [(curr[0]-1, curr[1]),
                              (curr[0], curr[1]-1),
                              (curr[0]+1, curr[1]),
                              (curr[0], curr[1]+1)]
                
                for s in new_states:
                    if s not in visited and s not in walls and self.check_square(state.board, s):
                        new_frontiers.add(s)

            frontiers[ptm] = new_frontiers
            ptm = 1 - ptm
        
        return scores[0]-scores[1]
    
    def check_square(self, board, curr):
        spot = board[curr[0]][curr[1]]
        if spot == "#" or spot == "x" or spot == "1" or spot == "2":
            return False
        else:
            return True
        
        
    

    def evaluate_square(self, board, curr):
        spot = board[curr[0]][curr[1]]

        if spot == " ":
            return 1
        elif spot == "#" or spot == "x":
            return 0
        elif spot == "@":
            return 10
        elif spot == "!":
            return 10
        elif spot == "^":
            return 10
        elif spot == "*":
            return 10
        elif spot == "?":
            return 10
        else:
            return 0


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
