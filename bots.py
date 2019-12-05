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

    def alpha_beta_cutoff(self, asp, cutoff_ply, eval_func):
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
            return [self.heuristic(asp), None]

        # Store the possible actions
        possible_actions = asp.get_available_actions(state)

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
        Takes in a state, returns a value indicating how good the state is
        :param state: list of lists representing the board
        :return: a single value
        """


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
