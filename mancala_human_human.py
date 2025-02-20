# import required libraries:
# sys: used to exit the program when Player 1 or PLayer 2 inputs 'QUIT'.
# random: used to randomly choose the starting player.
import sys
import random


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

    def __init__(self):
        """Initialize the Mancala game board and starting player."""
        # create a new game board with the starting number of seeds in each pit:
        self.board = self.get_new_board()

        # randomly choose the starting player (either "1" or "2"):
        self.player_turn = random.choice(["1", "2"])

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

    def ask_for_player_move(self):
        """Prompt the current player for their move."""
        response = None
        while not response:
            # prompt the human player for their move:
            if self.player_turn == '1':
                print('Player 1, choose move: A-F (or QUIT)')
            elif self.player_turn == '2':
                print('Player 2, choose move: G-L (or QUIT)')

            # read and process the player's input:
            response = input('> ').upper().strip()

            # handle the 'QUIT' command, exit the game:
            if response == 'QUIT':
                print('Thanks for playing!')
                sys.exit()

            # validate the player's move based on their player number:
            if (self.player_turn == '1' and response not in self.PLAYER_1_PITS) or \
                    (self.player_turn == '2' and response not in self.PLAYER_2_PITS):
                print('Invalid input, please try again.')
                response = None
                continue

            # check if the chosen pit is empty and ask for another move in that case:
            if self.board[response] == 0:
                print('You cannot move from an empty pit. Try again.')
                response = None
                continue

        return response

    def play_game(self):
        """
        Run the main game loop, displaying the game board, prompting the players
        for moves, performing the moves, checking for game over conditions, and
        announcing the winner or a tie.
        """
        while True:
            # display the game board:
            self.display_board()

            # ask for the player's move:
            move = self.ask_for_player_move()
            # perform the chosen move and get the last pit where a seed was placed:
            last_pit = self.make_move(move)
            # check for captures:
            self.check_capture(last_pit)

            # check if the game is over and in that case exit the game loop:
            if self.check_game_over():
                break

            # if the last seed was not placed in the current player's store, change turns:
            if last_pit != self.player_turn:
                self.change_turn()

        # display the final game board and announce the result:
        self.display_board()
        if self.board['1'] > self.board['2']:
            print('Player 1 wins!')
        elif self.board['1'] < self.board['2']:
            print('Player 2 wins!')
        else:
            print('It\'s a tie!')


if __name__ == '__main__':
    """Create a new Mancala game and run the game loop."""
    game = Mancala()
    game.play_game()
