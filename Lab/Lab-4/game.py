
import time
from puzzle import Puzzle


class SlidingPuzzle:
    def __init__(self):
        self.moves = 0
        self.size = self.choose_size()
        self.puzzle = Puzzle(self.size)
        self.started = time.monotonic()

    def choose_size(self):
        while True:
            choice = input("Choose puzzle size (3, 4, or 5): ").strip()
            if choice in ("3", "4", "5"):
                return int(choice)
            print("Choose 3, 4, or 5.")

    def display(self):
        print()
        for row in self.puzzle.board:
            print(" ".join(f"{x or ' ':>2}" for x in row))
        print("Moves:", self.moves, " Time:", int(time.monotonic() - self.started), "s")

    def run(self):
        print("Sliding Puzzle — W/A/S/D moves the tile into the blank. Q quits.")
        while True:
            self.display()
            if self.puzzle.solved():
                print("Solved!")
                return

            key = input("> ").strip().lower()
            if key == "q":
                return
            if key not in "wasd":
                print("Use W/A/S/D.")
                continue
            if self.puzzle.move(key):
                self.moves += 1
                print("Moved.")
                if self.puzzle.solved():
                    self.display()
                    print("Solved!")
                    return
            else:
                print("That move is not possible.")
