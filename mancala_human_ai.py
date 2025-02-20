# import required libraries:
# sys: exit the program when Player 1 inputs 'QUIT'.
# random: randomly choose the starting player.
# ai_agents: custom AI agents with different levels of difficulty to play against.
import sys
import random
from ai_agents import RandomAgent, MediumAgent, MinimaxAgent


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

    def __init__(self, ai_agent=None):
        # create a new game board and assign the current player:
        self.board = self.get_new_board()
        self.player_turn = random.choice(["1", "2"])
        self.ai_agent = ai_agent

    def get_new_board(self):
        """Create a new game board with the starting number of seeds (4) in each pit."""
        # retrieve the starting number of seeds from the class constant:
        s = self.STARTING_NUMBER_OF_SEEDS

        # return a new dictionary representing the initial game board state, with 4 seeds in each
        # pit and 0 seeds in each player's Mancala/Score (labeled '1' and '2'):
        return {'1': 0, '2': 0, 'A': s, 'B': s, 'C': s, 'D': s, 'E': s,
                'F': s, 'G': s, 'H': s, 'I': s, 'J': s, 'K': s, 'L': s}

    def display_board(self):
        """Display the current state of the game board."""
        # iterate through the pits in the specified order, get the number of seeds in each pit,
        # convert it to a string and right-justify it with a width of 2, then append it to the seed_amounts list:
        seed_amounts = []
        for pit in 'GHIJKL21ABCDEF':
            num_seeds_in_this_pit = str(self.board[pit]).rjust(2)
            seed_amounts.append(num_seeds_in_this_pit)

        # print the game board using a multiline string and string formatting to insert the seed
        # amounts at the appropriate positions in the string:
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
        and add them to the current player's Mancala/Score (unless the opposite pit is
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
        Get the list of valid moves for the current player. A move is valid
        if the pit belongs to the player and has seeds in it.

        Parameters:
        player (str): The current player ('1' or '2').

        Returns:
        list: A list of valid pit labels for the current player.
        """
        if player == '1':
            return [pit for pit in self.PLAYER_1_PITS if self.board[pit] > 0]
        else:
            return [pit for pit in self.PLAYER_2_PITS if self.board[pit] > 0]

    def simulate_move(self, pit):
        """
        Simulate a move without altering the current game state by creating
        a temporary board and distributing the seeds according to the game
        rules. This method is mainly used by AI agents to evaluate possible moves.

        Parameters:
        pit (str): The label of the pit where the move will start.

        Returns:
        str: The label of the last pit where a seed was placed.
        """
        # create a temporary copy of the board:
        temp_board = self.board.copy()
        seeds = temp_board[pit]
        temp_board[pit] = 0
        current_pit = pit

        # simulate the seed distribution:
        while seeds > 0:
            current_pit = self.NEXT_PIT[current_pit]
            if current_pit == '1' and self.player_turn == '2':
                continue
            if current_pit == '2' and self.player_turn == '1':
                continue

            temp_board[current_pit] += 1
            seeds -= 1

        # check for capture after the move:
        if temp_board[current_pit] == 1 and current_pit in self.PLAYER_1_PITS + self.PLAYER_2_PITS:
            if (self.player_turn == '1' and current_pit in self.PLAYER_1_PITS) or (
                    self.player_turn == '2' and current_pit in self.PLAYER_2_PITS):
                opposite_pit = self.OPPOSITE_PIT[current_pit]
                if temp_board[opposite_pit] > 0:
                    captured_seeds = temp_board[current_pit] + temp_board[opposite_pit]
                    temp_board[current_pit] = 0
                    temp_board[opposite_pit] = 0
                    temp_board[self.player_turn] += captured_seeds

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

    def ask_for_human_move(self):
        """
        Ask the human player (Player 1) to input their move. The move is
        considered valid if the input is a pit label from A to F and the
        pit is not empty. The player can also enter 'QUIT' to exit the game.

        Returns:
        str: The label of the chosen pit to move from.
        """
        response = None
        while not response:
            print('Player 1, choose move: A-F (or QUIT)')
            response = input('> ').upper().strip()

            if response == 'QUIT':
                print('Thanks for playing!')
                sys.exit()

            if response not in self.PLAYER_1_PITS:
                print('Invalid input, please try again.')
                response = None
                continue

            if self.board[response] == 0:
                print('You cannot move from an empty pit. Try again.')
                response = None
                continue

        return response

    def ask_for_ai_move(self):
        """
        Ask the AI agent (Player 2) to choose their move. This method assumes
        that an AI agent has been defined for Player 2.

        Returns:
        str: The label of the chosen pit to move from.

        Raises:
        ValueError: If no AI agent is defined for Player 2.
        """
        if self.ai_agent:
            move = self.ai_agent.make_move(self)
            print(f'AI Player chooses move: {move}')
            return move
        else:
            raise ValueError("AI agent is not defined for player 2.")

    def ask_for_player_move(self):
        """
        Ask the current player (Player 1 or Player 2) to choose their move,
        depending on whether the player is human or AI.

        Returns:
        str: The label of the chosen pit to move from.
        """
        if self.player_turn == '1':
            return self.ask_for_human_move()
        else:
            return self.ask_for_ai_move()

    def play_game(self):
        """
        Run the main game loop, displaying the game board, prompting the players
        for moves, performing the moves, checking for game over conditions, and
        announcing the winner or a tie.
        """
        while True:
            # display the current state of the game board:
            self.display_board()

            # get the current player's move (either human or AI):
            move = self.ask_for_player_move()

            # perform the move by distributing seeds from the chosen pit:
            last_pit = self.make_move(move)

            # check for capture conditions and update the board accordingly:
            self.check_capture(last_pit)

            # check if the game is over (no valid moves remaining for either player):
            if self.check_game_over():
                break

            # change the turn if the last pit was not the player's store:
            if last_pit != self.player_turn:
                self.change_turn()

        # display the final state of the game board:
        self.display_board()

        # announce the winner or a tie based on the final scores:
        if self.board['1'] > self.board['2']:
            print('You win!')
        elif self.board['1'] < self.board['2']:
            print('You lost...')
        else:
            print('It\'s a tie!')


if __name__ == '__main__':
    ai_agent = None

    # ask the user to select the AI difficulty level:
    while ai_agent is None:
        print("Select AI difficulty: easy, medium, or hard")
        difficulty = input('> ').lower().strip()

        # assign an AI agent based on the selected difficulty level:
        if difficulty == 'easy':
            ai_agent = RandomAgent()
        elif difficulty == 'medium':
            ai_agent = MediumAgent()
        elif difficulty == 'hard':
            ai_agent = MinimaxAgent()
        else:
            print("Invalid input. Please try again.")

    # initialize the Mancala game with the selected AI agent:
    game = Mancala(ai_agent)

    # start playing the game:
    game.play_game()
