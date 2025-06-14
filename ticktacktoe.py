import math
import time
import random

# Base class for players
class Player:
    def __init__(self, letter):
        self.letter = letter  # X or O

    def get_move(self, game):
        pass

# Human player class
class HumanPlayer(Player):
    def get_move(self, game):
        valid = False
        move = None
        while not valid:
            square = input(f"{self.letter}'s turn. Choose a position (0-8): ")
            try:
                move = int(square)
                if move not in game.available_moves():
                    raise ValueError
                valid = True
            except ValueError:
                print("Invalid move. Try again.")
        return move


# Computer that picks randomly
class RandomComputerPlayer(Player):
    def get_move(self, game):
        move = random.choice(game.available_moves())
        return move


# Smarter computer using Minimax
class SmartComputerPlayer(Player):
    def get_move(self, game):
        if len(game.available_moves()) == 9:
            # First move - pick random
            return random.choice(game.available_moves())
        else:
            move = self.minimax(game, self.letter)
            return move['pos']

    def minimax(self, game_state, player, alpha=-math.inf, beta=math.inf):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        # Check for previous move winning
        if game_state.current_winner == other_player:
            return {
                'pos': None,
                'score': 1 * (game_state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                    game_state.num_empty_squares() + 1)
            }

        elif not game_state.empty_squares():
            return {'pos': None, 'score': 0}  # Draw

        if player == max_player:
            best = {'pos': None, 'score': -math.inf}
        else:
            best = {'pos': None, 'score': math.inf}

        for move in game_state.available_moves():
            game_state.make_move(move, player)
            sim_score = self.minimax(game_state, other_player, alpha, beta)

            # Undo the move
            game_state.board[move] = ' '
            game_state.current_winner = None
            sim_score['pos'] = move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, sim_score['score'])
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, sim_score['score'])

            if beta <= alpha:
                break

        return best


# Game board and logic
class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Show 0-8 positions
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.check_winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        # Check row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([s == letter for s in row]):
            return True

        # Check column
        col_ind = square % 3
        col = [self.board[col_ind + i*3] for i in range(3)]
        if all([s == letter for s in col]):
            return True

        # Check diagonals
        if square % 2 == 0:
            diag1 = [self.board[i] for i in [0, 4, 8]]
            diag2 = [self.board[i] for i in [2, 4, 6]]
            if all([s == letter for s in diag1]) or all([s == letter for s in diag2]):
                return True

        return False

    def empty_squares(self):
        return ' ' in self.board

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def num_empty_squares(self):
        return self.board.count(' ')


# Game loop
def play(game, x_player, o_player, show_board=True):
    if show_board:
        game.print_board_nums()

    turn = 'X'
    while game.empty_squares():
        if turn == 'X':
            move = x_player.get_move(game)
        else:
            move = o_player.get_move(game)

        if game.make_move(move, turn):
            if show_board:
                print(f"{turn} moves to square {move}")
                game.print_board()
                print()

            if game.current_winner:
                if show_board:
                    print(f"{turn} wins!")
                return turn

            turn = 'O' if turn == 'X' else 'X'

        time.sleep(0.6)

    if show_board:
        print("It's a draw!")


# Run the game
if __name__ == '__main__':
    print("Welcome to Tic Tac Toe!")
    while True:
        x_player = SmartComputerPlayer('X')
        o_player = HumanPlayer('O')
        ttt = TicTacToe()
        play(ttt, x_player, o_player, show_board=True)

        again = input("Play again? (y/n): ").lower()
        if again != 'y':
            print("Thanks for playing!")
            break