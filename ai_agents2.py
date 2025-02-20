import random


class RandomAgent:
    """
    A simple agent that chooses a random move from the list of valid moves.
    """
    # initialize the RandomAgent with the player identifier:
    def __init__(self, player):
        self.player = player

    def make_move(self, game):
        # get a list of valid moves for the agent:
        valid_moves = game.get_valid_moves(self.player)
        # randomly choose one of the valid moves:
        return random.choice(valid_moves)


class MediumAgent:
    """
    A medium difficulty agent that prioritizes moves that grant an extra turn.
    """
    # initialize the MediumAgent with the player identifier:
    def __init__(self, player):
        self.player = player

    def make_move(self, game):
        # get a list of valid moves for the agent:
        valid_moves = game.get_valid_moves(self.player)
        # loop through the valid moves:
        for move in valid_moves:
            # simulate the move and get the last pit where a seed was placed:
            last_pit = game.simulate_move(move)
            # if the last pit is the AI agent's Mancala/Score, choose this move:
            if last_pit == self.player:
                return move
        # if no moves result in the last seed in the Mancala/Score, choose a random valid move:
        return random.choice(valid_moves)


class MinimaxAgent:
    def __init__(self, player, depth=3):
        self.player = player
        self.depth = depth
        self.opponent = '1' if self.player == '2' else '2'

    def make_move(self, game):
        _, best_move = self.minimax(game, self.depth, float('-inf'), float('inf'), True)
        return best_move

    def evaluate(self, game):
        return game.board[self.player] - game.board[self.opponent]

    def minimax(self, game, depth, alpha, beta, maximizing_player):
        if depth == 0 or game.check_game_over():
            return self.evaluate(game), None

        best_move = None

        if maximizing_player:
            max_eval = float('-inf')
            valid_moves = game.get_valid_moves(self.player)

            for move in valid_moves:
                new_game = game.copy()
                prev_seeds = new_game.board[self.player]
                last_pit = new_game.make_move(move)
                new_game.check_capture(last_pit)
                seeds_captured = new_game.board[self.player] - prev_seeds

                extra_turn = last_pit == self.player
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, extra_turn)
                eval += seeds_captured

                if eval > max_eval:
                    max_eval = eval
                    best_move = move

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break

            return max_eval, best_move

        else:
            min_eval = float('inf')
            valid_moves = game.get_valid_moves(self.opponent)

            for move in valid_moves:
                new_game = game.copy()
                prev_seeds = new_game.board[self.opponent]
                last_pit = new_game.make_move(move)
                new_game.check_capture(last_pit)
                seeds_captured = new_game.board[self.opponent] - prev_seeds

                extra_turn = last_pit == self.opponent
                eval, _ = self.minimax(new_game, depth - 1, alpha, beta, extra_turn)
                eval -= seeds_captured

                if eval < min_eval:
                    min_eval = eval
                    best_move = move

                beta = min(beta, eval)
                if beta <= alpha:
                    break

            return min_eval, best_move
