import math
import random


class GameLogic:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
        self.current_player = self.human
        self.game_over = False
        self.ai_difficulty = 'Hard'
        self.stats = {'Human': 0, 'AI': 0, 'Tie': 0}

    def reset_board(self):
        self.board = [' ' for _ in range(9)]
        self.game_over = False
        self.current_player = self.human

    def reset_stats(self):
        self.stats = {'Human': 0, 'AI': 0, 'Tie': 0}

    def make_move(self, position, player):
        if self.game_over or self.board[position] != ' ':
            return False

        self.board[position] = player
        return True

    def get_available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def get_ai_move(self):
        available_moves = self.get_available_moves()

        if not available_moves:
            return None

        if self.ai_difficulty == 'Easy':
            if random.random() < 0.7:
                return random.choice(available_moves)
        elif self.ai_difficulty == 'Medium':
            if random.random() < 0.3:
                return random.choice(available_moves)

        return self._get_best_move()

    def _get_best_move(self):
        available_moves = self.get_available_moves()
        best_score = -math.inf
        best_move = available_moves[0]

        for move in available_moves:
            self.board[move] = self.ai
            score = self._minimax(0, False, -math.inf, math.inf)
            self.board[move] = ' '

            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def _minimax(self, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning"""
        winner = self.evaluate_board()

        if winner == self.ai:
            return 10 - depth
        elif winner == self.human:
            return depth - 10
        elif ' ' not in self.board:
            return 0

        if is_maximizing:
            max_score = -math.inf
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = self.ai
                    score = self._minimax(depth + 1, False, alpha, beta)
                    self.board[i] = ' '
                    max_score = max(score, max_score)
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
            return max_score
        else:
            min_score = math.inf
            for i in range(9):
                if self.board[i] == ' ':
                    self.board[i] = self.human
                    score = self._minimax(depth + 1, True, alpha, beta)
                    self.board[i] = ' '
                    min_score = min(score, min_score)
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
            return min_score

    def evaluate_board(self):
        """Check if there's a winner on the current board"""
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]  # diagonals
        ]

        for combo in winning_combos:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return self.board[combo[0]]

        return None

    def check_game_end(self):
        winner = self.evaluate_board()

        if winner:
            self.game_over = True
            if winner == self.human:
                self.stats['Human'] += 1
                return 'human_win'
            else:
                self.stats['AI'] += 1
                return 'ai_win'
        elif ' ' not in self.board:
            self.game_over = True
            self.stats['Tie'] += 1
            return 'tie'

        return 'continue'

    def get_winning_line(self):
        winning_combos = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]

        winner = self.evaluate_board()
        if winner:
            for combo in winning_combos:
                if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == winner:
                    return combo

        return None

    def set_difficulty(self, difficulty):
        if difficulty in ['Easy', 'Medium', 'Hard']:
            self.ai_difficulty = difficulty

    def get_formatted_stats(self):
        return (f"YOU: {self.stats['Human']}    "
                f"AI: {self.stats['AI']}    "
                f"TIES: {self.stats['Tie']}")