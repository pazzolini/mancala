# import required libraries:
# random: used to randomly choose the starting player.
# ai_agents: custom AI agents with different levels of difficulty to play against.
import random
from ai_agents2 import RandomAgent, MediumAgent, MinimaxAgent


class Mancala:
    """A class representing the Mancala game."""
    # tuples that store labels for each player's pits:
    PLAYER_1_PITS = ('A', 'B', 'C', 'D', 'E', 'F')
    PLAYER_2_PITS = ('G', 'H', 'I', 'J', 'K', 'L')

    # a dictionary that maps a pit to its opposite pit:
    OPPOSITE_PIT = {'A': 'G', 'B': 'H', 'C': 'I', 'D': 'J', 'E': 'K',
                    'F': 'L', 'G': 'A', 'H': 'B', 'I': 'C', 'J': 'D',
                    'K': 'E', 'L': 'F'}

    # a dictionary that maps a pit to the next pit in the counterclockwise direction:
    NEXT_PIT = {'A': 'B', 'B': 'C', 'C': 'D', 'D': 'E', 'E': 'F', 'F': '1',
                '1': 'L', 'L': 'K', 'K': 'J', 'J': 'I', 'I': 'H', 'H': 'G',
                'G': '2', '2': 'A'}

    # a string containing all the pit labels, including the Mancalas/scores (1 and 2):
    PIT_LABELS = 'ABCDEF1LKJIHG2'

    # a constant representing the initial number of seeds in each pit:
    STARTING_NUMBER_OF_SEEDS = 4

    def __init__(self, ai_agent1=None, ai_agent2=None, verbose=True):
        """
        Initialize a new Mancala game.

        Args:
            ai_agent1: The AI agent for player 1.
            ai_agent2: The AI agent for player 2.
            verbose: Whether to print game state information (default: True).
        """

        # Create a new game board
        self.board = self.get_new_board()

        # Randomly choose the starting player
        self.player_turn = random.choice(["1", "2"])

        # Set the AI agent for player 1
        self.ai_agent1 = ai_agent1

        # Set the AI agent for player 2
        self.ai_agent2 = ai_agent2

        # Set the verbosity for game state information
        self.verbose = verbose

    def get_new_board(self):
        """
        Create a new game board with the starting number of seeds (4) in each pit.

        Returns:
            dict: A dictionary representing the initial game board state with pits
                  labeled A-L, and '1' and '2' for each player's Mancala/Score.
        """
        # retrieve the starting number of seeds from the class constant:
        s = self.STARTING_NUMBER_OF_SEEDS

        # return a new dictionary representing the initial game board state, with 4 seeds in each
        # pit and 0 seeds in each player's Mancala/Score (labeled '1' and '2'):
        return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
                'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}

    def display_board(self):
        """
        Display the current state of the game board.

        This method uses string formatting to create a visual representation of the
        game board, showing the seed count in each pit and the scores for both players.
        """
        # iterate through the pits in the specified order, get the number of seeds in each pit,
        # convert it to a string and right-justify it with a width of 2, then append it to the seed_amounts list:
        seed_amounts = []
        for pit in 'GHIJKL21ABCDEF':
            num_seeds_in_this_pit = str(self.board[pit]).rjust(2)
            seed_amounts.append(num_seeds_in_this_pit)

        # Print the game board using string formatting with the seed amounts
        print("""
    +------+------+--<<<<<-Player 2----+------+------+------+

    P2     |G     |H     |I     |J     |K     |L     |     P1
           |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |
    S      |      |      |      |      |      |      |      S
    C  {}  +------+------+------+------+------+------+  {}  C
    O      |A     |B     |C     |D     |E     |F     |      O
    R      |  {}  |  {}  |  {}  |  {}  |  {}  |  {}  |      R
    E      |      |      |      |      |      |      |      E

    +------+------+------+-Player 1->>>>>-----+------+------+

    """.format(*seed_amounts))

    def make_move(self, pit):
        """
        Move seeds from the selected pit and distribute them counterclockwise
        to other pits, adding one seed to each pit, until there are no more
        seeds to distribute. Skips the opponent's Mancala/Score while distributing seeds.

        Parameters:
        pit (str): The label of the pit where the move will start.

        Returns:
        str: The label of the last pit where a seed was placed.
        """
        # get the number of seeds in the selected pit, set that pit's seeds to 0,
        # and initialize the current_pit variable to the selected pit:
        seeds = self.board[pit]
        self.board[pit] = 0
        current_pit = pit

        # using the NEXT_PIT dictionary, find the next pit in the counterclockwise direction:
        while seeds > 0:
            current_pit = self.NEXT_PIT[current_pit]
            # if the current pit is the opponent's Mancala/score, skip it and continue with the next iteration.
            if current_pit == '1' and self.player_turn == '2':
                continue
            if current_pit == '2' and self.player_turn == '1':
                continue

            # add a seed to the current pit and decrease the remaining seeds:
            self.board[current_pit] += 1
            seeds -= 1

        # after all seeds have been distributed, return the label of the last pit where a seed was placed:
        return current_pit

    def check_capture(self, last_pit):
        """
        If the last seed is placed in an empty pit on the current player's
        side, capture the seeds in that pit and the seeds in the opposite pit
        and add them to the current player's store (unless the opposite pit is
        empty - in that case the seeds remain in the board).

        Parameters:
        last_pit (str): The label of the last pit where a seed was placed.
        """
        # check if the last seed was placed in an empty pit on the current player's side:
        if self.board[last_pit] == 1 and last_pit in self.PLAYER_1_PITS + self.PLAYER_2_PITS:
            # check if the current player is Player 1 and the last pit belongs to Player 1, or
            # if the current player is Player 2 and the last pit belongs to Player 2:
            if (self.player_turn == '1' and last_pit in self.PLAYER_1_PITS) or (
                    self.player_turn == '2' and last_pit in self.PLAYER_2_PITS):
                # find the opposite pit:
                opposite_pit = self.OPPOSITE_PIT[last_pit]
                # check if there are seeds in the opposite pit:
                if self.board[opposite_pit] > 0:
                    # capture the seeds from both the last pit and the opposite pit:
                    captured_seeds = self.board[last_pit] + self.board[opposite_pit]
                    self.board[last_pit] = 0
                    self.board[opposite_pit] = 0
                    # add the captured seeds to the current player's store:
                    self.board[self.player_turn] += captured_seeds

    def change_turn(self):
        """
        Switch the current player's turn to the other player. If the current player is Player 1,
        switch to Player 2, and vice versa.
        """
        self.player_turn = '1' if self.player_turn == '2' else '2'

    def check_game_over(self):
        """
        Check if the game is over (terminal state), i.e., if either player has
        no seeds left in their pits. If the game is over, add any remaining
        seeds to each player's store and return True. Otherwise, return False.
        """
        # calculate the total number of seeds in each player's pits:
        player_1_total = sum([self.board[pit] for pit in self.PLAYER_1_PITS])
        player_2_total = sum([self.board[pit] for pit in self.PLAYER_2_PITS])

        # check if either player has no seeds left in their pits:
        if player_1_total == 0 or player_2_total == 0:
            # add the remaining seeds to each player's Mancala/score:
            self.board['1'] += player_1_total
            self.board['2'] += player_2_total
            # set the number of seeds in each pit to 0, as the game is over:
            self.board.update({pit: 0 for pit in self.PLAYER_1_PITS + self.PLAYER_2_PITS})
            # return True, indicating the game is over
            return True

        return False

    def get_valid_moves(self, player):
        """
        Get the valid moves for the given player based on the current board
        state.

        Parameters:
        player (str): '1' for Player 1, '2' for Player 2.

        Returns:
        list: A list of pit labels representing valid moves for the player.
        """
        if player == '1':
            return [pit for pit in self.PLAYER_1_PITS if self.board[pit] > 0]
        elif player == '2':
            return [pit for pit in self.PLAYER_2_PITS if self.board[pit] > 0]

    def simulate_move(self, pit):
        """
        Simulate a move from the given pit and return the last pit where a
        seed was placed. This method is useful for AI agents to evaluate the
        possible outcomes of a move without changing the actual game state.

        Parameters:
        pit (str): The label of the pit where the move will start.

        Returns:
        str: The label of the last pit where a seed was placed.
        """

        # create a temporary copy of the board to simulate the move:
        temp_board = self.board.copy()
        seeds = temp_board[pit]
        temp_board[pit] = 0
        current_pit = pit

        # distribute seeds counterclockwise:
        while seeds > 0:
            current_pit = self.NEXT_PIT[current_pit]
            # Skip the opponent's score:
            if current_pit == '1' and self.player_turn == '2':
                continue
            if current_pit == '2' and self.player_turn == '1':
                continue

            # add a seed to the current pit and decrease the remaining seeds:
            temp_board[current_pit] += 1
            seeds -= 1

        # check for seed capture and update the temporary board accordingly:
        if temp_board[current_pit] == 1 and current_pit in self.PLAYER_1_PITS + self.PLAYER_2_PITS:
            if (self.player_turn == '1' and current_pit in self.PLAYER_1_PITS) or (
                    self.player_turn == '2' and current_pit in self.PLAYER_2_PITS):
                opposite_pit = self.OPPOSITE_PIT[current_pit]
                if temp_board[opposite_pit] > 0:
                    captured_seeds = temp_board[current_pit] + temp_board[opposite_pit]
                    temp_board[current_pit] = 0
                    temp_board[opposite_pit] = 0
                    temp_board[self.player_turn] += captured_seeds

        # return the last pit where a seed was placed:
        return current_pit

    def copy(self):
        """
        Create a copy of the current Mancala game instance, preserving
        the board state and player turn. This method is useful for AI agents
        to explore different game states without affecting the actual game.

        Returns:
        Mancala: A new Mancala instance with the same board state and player
                 turn as the current instance.
        """
        new_game = Mancala()
        new_game.board = self.board.copy()
        new_game.player_turn = self.player_turn
        return new_game

    def ask_for_ai_move(self):
        """
        Asks the current player's AI agent to make a move based on the current
        game state. The AI agent's `make_move` method is called with the current
        game instance as an argument.The chosen move is then printed if the verbose attribute
        is set to True, and the move is returned as a string containing the pit label.

        Returns:
        str: The chosen pit label for the AI agent's move.
        """
        if self.player_turn == '1':
            move = self.ai_agent1.make_move(self)
            if self.verbose:
                print(f'AI Player 1 chooses move: {move}')
        elif self.player_turn == '2':
            move = self.ai_agent2.make_move(self)
            if self.verbose:
                print(f'AI Player 2 chooses move: {move}')
        return move


if __name__ == '__main__':
    print("Welcome to the AI vs AI Mancala game!")
    # prompt the user to choose difficulty levels for both players:
    print("Choose the AI Agent 1: random, medium, minimax")
    difficulty1 = input().lower()

    while difficulty1 not in ['random', 'medium', 'minimax']:
        print("Invalid input. Please enter 'random', 'medium', 'minimax'")
        difficulty1 = input().lower()

    print("Choose the AI Agent 2: random, medium, minimax")
    difficulty2 = input().lower()

    while difficulty2 not in ['random', 'medium', 'minimax']:
        print("Invalid input. Please enter 'random', 'medium', 'minimax'")
        difficulty2 = input().lower()

    # assign AI agents:
    if difficulty1 == 'random':
        ai_agent1 = RandomAgent("1")
    elif difficulty1 == 'medium':
        ai_agent1 = MediumAgent("1")
    elif difficulty1 == 'minimax':
        ai_agent1 = MinimaxAgent("1")

    if difficulty2 == 'random':
        ai_agent2 = RandomAgent("2")
    elif difficulty2 == 'medium':
        ai_agent2 = MediumAgent("2")
    elif difficulty2 == 'minimax':
        ai_agent2 = MinimaxAgent("2")

    # initialize the Mancala game with the selected AI agents:
    game = Mancala(ai_agent1, ai_agent2)

    # run the main game loop:
    while not game.check_game_over():
        game.display_board()
        move = game.ask_for_ai_move()
        last_pit = game.make_move(move)
        game.check_capture(last_pit)

        if game.check_game_over():
            break

        if last_pit != game.player_turn:
            game.change_turn()

    # display the final game board and the result
    game.display_board()
    if game.board['1'] > game.board['2']:
        print('Player 1 wins!')
    elif game.board['1'] < game.board['2']:
        print('Player 2 wins!')
    else:
        print('It\'s a tie!')
