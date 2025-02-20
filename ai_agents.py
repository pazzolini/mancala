import random


class RandomAgent:
    """
    A simple agent that chooses a random move from the list of valid moves.
    """

    def make_move(self, game):
        # get a list of valid moves for Player 2:
        valid_moves = game.get_valid_moves('2')
        # randomly choose one of the valid moves:
        return random.choice(valid_moves)


class MediumAgent:
    """
    A medium difficulty agent that prioritizes moves that grant an extra turn.
    """
    def make_move(self, game):
        # get a list of valid moves for Player 2:
        valid_moves = game.get_valid_moves('2')
        # loop through the valid moves:
        for move in valid_moves:
            # simulate the move and get the last pit where a seed was placed:
            last_pit = game.simulate_move(move)
            # if the last pit is the AI agent's Mancala/Score, choose this move:
            if last_pit == '2':
                return move
        # if no moves result in the last seed in the Mancala/Score, choose a random valid move:
        return random.choice(valid_moves)


class MinimaxAgent:
    """
    An agent that uses the minimax algorithm with alpha-beta pruning to choose the best move.
    """
    # set the default search depth for the minimax algorithm:
    depth = 3

    def make_move(self, game):
        """
        Choose a move for Player 2 (AI agent) using the minimax algorithm with
        alpha-beta pruning.
        """
        # call the minimax function with the current game state, search depth, and initial alpha and beta values:
        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        # return the best move found by the minimax algorithm:
        return best_move

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.

        Parameters:
        game (Mancala): The current Mancala game instance.
        depth (int): The remaining search depth for the algorithm.
        alpha (float): The alpha value used for alpha-beta pruning.
        beta (float): The beta value used for alpha-beta pruning.
        maximizing_player (bool): True if it's the AI agent's turn, False if it's the human player's turn.

        Returns:
        float: The evaluation score of the best move.
        str: The chosen pit label for the AI agent's move.
        """
        # depth is 0 or the game is over:
        if depth == 0 or game.check_game_over():
            return game.board['2'] - game.board['1'], None

        # initialize the best_move variable to None:
        best_move = None

        # if it's the AI agent's turn (maximizing player):
        if maximizing_player:
            # initialize the max_eval variable to negative infinity:
            max_eval = float('-inf')
            # get a list of valid moves for the AI agent:
            valid_moves = game.get_valid_moves('2')

            # loop through the valid moves:
            for move in valid_moves:
                # create a copy of the game to simulate the move:
                new_game = game.copy()
                # make the move and get the last pit where a seed was placed:
                last_pit = new_game.make_move(move)
                # check for captures:
                new_game.check_capture(last_pit)

                # if the last pit is the AI agent's score, it gets an extra turn:
                extra_turn = last_pit == '2'
                # recursively call the minimax function for the next depth and player:
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, extra_turn)

                # update the max_eval and best_move if the current evaluation is better:
                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                # update the alpha value and check for pruning:
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            # return the maximum evaluation score and the best move:
            return max_eval, best_move

        # if it's the human player's turn (minimizing player):
        else:
            # initialize the min_eval variable to positive infinity:
            min_eval = float('inf')
            # get a list of valid moves for the human player:
            valid_moves = game.get_valid_moves('1')

            # loop through the valid moves:
            for move in valid_moves:
                # create a copy of the game to simulate the move
                new_game = game.copy()
                # make the move and get the last pit where a seed was placed
                last_pit = new_game.make_move(move)
                # check for captures:
                new_game.check_capture(last_pit)

                # if the last pit is the human player's score, they get an extra turn
                extra_turn = last_pit == '1'
                # recursively call the minimax function for the next depth and player
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, extra_turn)

                # update the min_eval and best_move if the current evaluation is better:
                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move
