from concurrent.futures import ProcessPoolExecutor
import argparse
from pathlib import Path
import time

class PaperStack:
    """
    Represents a 2D grid of paper rolls, where each roll is either present (`@`)
    or absent. The class computes a "heat" matrix indicating how many immediate
    neighbors each roll has, and supports iterative removal of rolls whose
    neighbor count falls below a given threshold.
    """
    NEIGHBOR_OFFSETS = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    def __init__(self, stackStrLst: list[str]) -> None:
        """
        Initialize the PaperStack from a list of string rows.

        Args:
            stackStrLst (list[str]): List of strings representing the rows
                of the stack. Each '@' denotes a present roll; any other
                character denotes empty space.

        Attributes:
            height (int): Number of rows in the grid.
            width (int): Number of columns in the grid.
            stacks (list[list[int]]): 2D array where 1 indicates a roll
                is present and 0 indicates empty.
            heat (list[list[int]]): 2D array tracking the count of neighboring
                rolls for each cell.
        """
        self.height = len(stackStrLst)
        self.width = len(stackStrLst[0].strip())
        self.stacks = [[(stackStrLst[i][j] == '@') * 1 for j in range(self.width)] for i in range(self.height)]
        self.heat = self.heat_matrix()

    def neighbors(self, i: int, j: int):
        """
        Yield valid neighboring cell positions around (i, j).

        Args:
            i (int): Row index.
            j (int): Column index.

        Yields:
            tuple[int, int]: Coordinates of a valid neighboring cell.
        """
        for di, dj in __class__.NEIGHBOR_OFFSETS:
            ni, nj = i + di, j + dj
            if 0 <= ni < self.height and 0 <= nj < self.width:
                yield ni, nj

    def heat_matrix(self) -> list[list[int]]:
        """
        Compute the heat matrix, where each cell's heat is the count of
        adjacent rolls in all 8 directions.

        Returns:
            list[list[int]]: 2D list containing neighbor counts.
        """
        matrix = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height): 
            for j in range(self.width): 
                for ni, nj in self.neighbors(i, j):
                    matrix[i][j] += self.stacks[ni][nj]
        return matrix

    def get_removable_rolls(self, threshold = 4):
        """
        Identify all rolls that are eligible for removal based on the heat matrix.

        A roll is removable if:
            - It is present.
            - Its neighbor count is below the threshold.

        Args:
            threshold (int, optional): Minimum neighbor count required for
                a roll to remain. Defaults to 4.

        Returns:
            list[tuple[int, int]]: Coordinates of rolls that can be removed.
        """
        heat_matrix = self.heat
        available_rolls = []
        for i in range(self.height):
            for j in range(self.width):
                if self.stacks[i][j] and heat_matrix[i][j] < threshold:
                    available_rolls.append((i,j))
        return available_rolls

    def remove_rolls(self,threshold = 4) -> int:
        """
        Remove all rolls that fall below the heat threshold and update the heat
        matrix accordingly.

        Each removed roll decreases the heat value of its neighbors by 1.

        Args:
            threshold (int, optional): Minimum neighbor count required to remain.
                Defaults to 4.

        Returns:
            int: Number of rolls removed during this operation.
        """
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