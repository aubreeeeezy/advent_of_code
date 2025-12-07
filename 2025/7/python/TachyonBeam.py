import argparse
from pathlib import Path
import time
from functools import lru_cache

class TachyonManifold:
    def __init__(self, grid : list[list[str]]) -> None:
        self.manifoldState: list[list[str]] = grid

        self.s_row = self.s_col = -1
        for r, row in enumerate(grid):
            for c, ch in enumerate(row):
                if ch == "S":
                    self.s_row, self.s_col = r, c
                    break
            if self.s_row == -1:
                break
    
    def percolate(self) -> int:
        width : int = len(self.manifoldState[0])
        height : int = len(self.manifoldState)
        splits : int = 0 
        for i in range(height - 1):
            for j in range(width):
                if self.manifoldState[i][j] == "S":
                    self.manifoldState[i + 1][j]  = "|"
                if self.manifoldState[i][j] == "|":
                    if self.manifoldState[i + 1][j] == "^":
                        splits += 1
                        if j > 0:
                            self.manifoldState[i + 1][j-1] = "|"
                        if j < width - 1:
                            self.manifoldState[i + 1][j+1] = "|"
                    else: 
                        self.manifoldState[i + 1][j]  = "|"
        return splits
    
    def __repr__(self) -> str: 
        return "\n".join(["".join(row) for row in self.manifoldState])
    
    def percolate_quantum(self) -> int:
        width: int = len(self.manifoldState[0])
        height: int = len(self.manifoldState)

        @lru_cache(maxsize=None)
        def sub_percolation(row: int, column: int) -> int:
            if row == height - 1:
                return 1

            below = self.manifoldState[row + 1][column]

            if below == "^":
                worlds = 0
                if column == 0:
                    worlds += 1  # stepping off left edge
                else:
                    worlds += sub_percolation(row + 1, column - 1)

                if column == width - 1:
                    worlds += 1  # stepping off right edge
                else:
                    worlds += sub_percolation(row + 1, column + 1)

                return worlds
            else:
                return sub_percolation(row + 1, column)

        # Start at the S position
        return sub_percolation(self.s_row, self.s_col)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Tachyon Beams")

    default_file: Path = Path(__file__).parent.parent / "sample_beam.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to instruction file (default: sample_beam.txt)",
    )

    args = parser.parse_args()

    start: float = time.perf_counter()

    with open(file=args.file, mode="r") as f:
        lines: list[str] = f.readlines()

  
    manifold : TachyonManifold = TachyonManifold(  [list(manifoldStr.rstrip('\n')) for manifoldStr in lines])
    part_1_calculation: int = manifold.percolate()
    print(f"part_1_calculation: {part_1_calculation}")

    manifold : TachyonManifold = TachyonManifold(  [list(manifoldStr.rstrip('\n')) for manifoldStr in lines])
    part_2_calculation: int = manifold.percolate_quantum()
    print(f"part_2_calculation: {part_2_calculation}")

    end: float = time.perf_counter()
    print(f"Took {end - start:.6f} seconds")