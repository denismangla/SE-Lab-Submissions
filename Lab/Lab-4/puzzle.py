
import random


class Puzzle:
    def __init__(self, size=4):
        self.size = size
        self.board = self.make_board()

    def make_board(self):
        tiles = list(range(1, self.size * self.size)) + [0]
        board = [tiles[r * self.size:(r + 1) * self.size] for r in range(self.size)]

        for _ in range(self.size * self.size * 20):
            r, c = next((r, c) for r in range(self.size) for c in range(self.size) if board[r][c] == 0)
            moves = []
            if r > 0:
                moves.append((r - 1, c))
            if r < self.size - 1:
                moves.append((r + 1, c))
            if c > 0:
                moves.append((r, c - 1))
            if c < self.size - 1:
                moves.append((r, c + 1))
            nr, nc = random.choice(moves)
            board[r][c], board[nr][nc] = board[nr][nc], board[r][c]

        return board

    def blank_pos(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return r, c

    def move(self, direction):
        r, c = self.blank_pos()
        dr, dc = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}[direction]
        nr, nc = r + dr, c + dc
        if not (0 <= nr < self.size and 0 <= nc < self.size):
            return False
        self.board[r][c], self.board[nr][nc] = self.board[nr][nc], self.board[r][c]
        return True

    def solved(self):
        return sum(self.board, []) == list(range(1, self.size * self.size)) + [0]
