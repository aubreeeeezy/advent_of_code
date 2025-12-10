import argparse
from pathlib import Path
import time
from functools import total_ordering


@total_ordering
class Point:
    def __init__(self, coords: list[int]) -> None:
        self.coords: list[int] = coords
        self.dimensions = len(coords)
        self.parent:Point = self
        self.size: int = 1

    def __getitem__(self, key: int) -> int:
        try:
            return self.coords[key]
        except IndexError:
            raise ValueError(f"'{key}' is not a valid index in coords. Try 0-{len(self.coords) - 1}") from None
        
    def distance(self, other: "Point") -> float:
        if self.dimensions != other.dimensions:
            raise ValueError("Comparing points with different numbers of dimensions is not yet supported.")
        return sum((other[i] - self[i]) ** 2 for i in range(self.dimensions)) ** 0.5
    
    def __repr__(self) -> str:
        return f"({', '.join([str(d) for d in self.coords])})"
    
    @staticmethod
    def pairs_by_distance(points):
        pairs = ((points[i], points[j], points[i].distance(points[j]))
                for i in range(len(points))
                for j in range(i+1, len(points)))

        # sort by distance
        for p1, p2, d in sorted(pairs, key=lambda x: x[2]):
            yield (p1, p2), d

    def find(self) -> "Point":
        if self.parent is not self:
            self.parent = self.parent.find()
        return self.parent

    def union(self, other: "Point") -> None:
        root1 = self.find()
        root2 = other.find()

        if root1 is root2:
            return
        
        if root1.size < root2.size:
            root1, root2 = root2, root1

        root2.parent = root1
        root1.size += root2.size
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.coords == other.coords

    def __lt__(self, other) -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return tuple(self.coords) < tuple(other.coords)

    def __hash__(self) -> int:
        return hash(tuple(self.coords))
    
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="3d Graphing")

    default_file: Path = Path(__file__).parent.parent / "sample_coords.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to instruction file (default: sample_coords.txt)",
    )

    args = parser.parse_args()

    start: float = time.perf_counter()

    points: list[Point] = []
    with open(file=args.file, mode="r") as f:
        for line in f: 
            points.append( Point([int(d.strip()) for d in line.split(',')]))


    connections_left: int = 10
    for pair, distance in Point.pairs_by_distance(points):
        if connections_left == 0:
            break
        # print(f"Connecting {pair[0]} to {pair[1]} with a distance of {distance}")
        pair[0].union(pair[1])
        connections_left -= 1
    
    circuits : list[Point] = sorted(list(set([point.find() for point in points])), key = lambda p: p.size, reverse=True)
    circuits_to_consider = 3 
    part_1_calculation: int = circuits[0].size
    for i in range(1,circuits_to_consider):
        parent: Point = circuits[i]
        print(f"{parent} heads a circuit of {parent.size}")
        part_1_calculation *= parent.size

    print(f"part_1_calculation: {part_1_calculation}")

    points: list[Point] = []
    with open(file=args.file, mode="r") as f:
        for line in f: 
            points.append( Point([int(d.strip()) for d in line.split(',')]))

    part_2_calculation: int = 0
    for pair, distance in Point.pairs_by_distance(points):
        pair[0].union(pair[1])
        root = pair[0].find()
        if root.size == len(points):
            part_2_calculation = pair[0][0] * pair[1][0]
            break

    print(f"part_2_calculation: {part_2_calculation}")

    end: float = time.perf_counter()
    print(f"Took {end - start:.6f} seconds")   
        
