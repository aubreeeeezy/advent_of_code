from concurrent.futures import ProcessPoolExecutor
import argparse
from pathlib import Path
import time

class PaperStack:
    NEIGHBOR_OFFSETS = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    def __init__(self, stackStrLst: list[str]) -> None:
        self.height = len(stackStrLst)
        self.width = len(stackStrLst[0].strip())
        self.stacks = [[(stackStrLst[i][j] == '@') * 1 for j in range(self.width)] for i in range(self.height)]
        self.heat = self.heat_matrix()

    def neighbors(self, i: int, j: int):
        for di, dj in __class__.NEIGHBOR_OFFSETS:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                yield ni, nj

    def heat_matrix(self) -> list[list[int]]:
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height): 
            for j in range(self.width): 
                for ni, nj in self.neighbors(i, j):
                    matrix[i][j] += self.stacks[ni][nj]
        return matrix

    def get_removable_rolls(self, threshold = 4):
        heat_matrix = self.heat
        #__class__.print_int_matrix(self.stacks)
        #__class__.print_int_matrix(heat_matrix)
        available_rolls = []
        for i in range(self.height):
            for j in range(self.width):
                if self.stacks[i][j] and heat_matrix[i][j] < threshold:
                    available_rolls.append((i,j))
        return available_rolls

    def remove_rolls(self,threshold = 4) -> int: 
        removeable_rolls = self.get_removable_rolls(threshold)
        for i, j in removeable_rolls:
            self.stacks[i][j] = 0
            for ni, nj in self.neighbors(i, j):
                self.heat[ni][nj] -= 1
        return len(removeable_rolls)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dial rotation solver")

    default_file = Path(__file__).parent.parent / "sample_stack.txt"

    parser.add_argument(
        "-f", "--file",
        default=str(default_file),
        help="Path to rotation command file (default: parent directory sample file)"
    )

    args = parser.parse_args()

    part_1_calculation = 0
    part_2_calculation = 0
    start = time.perf_counter()
    stack = None
    with open(args.file, "r") as f:
        stack = PaperStack(f.readlines())

    rolls_removed = stack.remove_rolls()  # First removal

    part_1_calculation += rolls_removed

    while rolls_removed > 0:
        part_2_calculation += rolls_removed
        rolls_removed = stack.remove_rolls()  # Fetch next removal
        
    end = time.perf_counter()

    print(f"part_1_calculation: {part_1_calculation}")
    print(f"part_2_calculation: {part_2_calculation}")
    print(f"Took {end - start:.6f} seconds")    