from ai_agents2 import RandomAgent, MediumAgent, MinimaxAgent
from mancala_ai_ai import Mancala


def run_game(ai_agent1, ai_agent2):
    game = Mancala(ai_agent1, ai_agent2, verbose=False)  # Set verbose to False

    while not game.check_game_over():
        move = game.ask_for_ai_move()
        last_pit = game.make_move(move)
        game.check_capture(last_pit)

        if game.check_game_over():
            break

        if last_pit != game.player_turn:
            game.change_turn()

    if game.board['1'] > game.board['2']:
        return 1
    elif game.board['1'] < game.board['2']:
        return 2
    else:
        return 0


def main():
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

    print("Enter the number of games to be played:")
    num_games = int(input())

    # assign AI agents based on the chosen difficulty levels:
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

    # Run the specified number of games
    results = {'1': 0, '2': 0, '0': 0}

    for _ in range(num_games):
        result = run_game(ai_agent1, ai_agent2)
        results[str(result)] += 1

    print(f"Results after playing {num_games} games:")
    print(f"Player 1 ({difficulty1} AI) wins: {results['1']}")
    print(f"Player 2 ({difficulty2} AI) wins: {results['2']}")
    print(f"Draws: {results['0']}")
    # Calculate win percentages and draw percentage
    player1_win_percentage = (results['1'] / num_games) * 100
    player2_win_percentage = (results['2'] / num_games) * 100
    draw_percentage = (results['0'] / num_games) * 100

    # Print win percentages and draw percentage
    print(f"Player 1 ({difficulty1} AI) win percentage: {player1_win_percentage:.2f}%")
    print(f"Player 2 ({difficulty2} AI) win percentage: {player2_win_percentage:.2f}%")
    print(f"Draw percentage: {draw_percentage:.2f}%")


if __name__ == '__main__':
    main()
