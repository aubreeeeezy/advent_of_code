import argparse
from pathlib import Path
import time
from functools import total_ordering
from collections import deque


@total_ordering
class Point:
    def __init__(self, coords: list[int]) -> None:
        self.coords: list[int] = coords
        self.dimensions = len(coords)
        self.parent: "Point" = self
        self.size: int = 1

    def __getitem__(self, key: int) -> int:
        try:
            return self.coords[key]
        except IndexError:
            raise ValueError(
                f"'{key}' is not a valid index in coords. "
                f"Try 0-{len(self.coords) - 1}"
            ) from None

    def distance_sq(self, other: "Point") -> int:
        if self.dimensions != other.dimensions:
            raise ValueError(
                "Comparing points with different numbers of dimensions "
                "is not yet supported."
            )
        return sum((other[i] - self[i]) ** 2 for i in range(self.dimensions))

    def __repr__(self) -> str:
        return f"({', '.join(str(d) for d in self.coords)})"

    @staticmethod
    def pairs(points):
        # Just generate all unique pairs; no sort by distance necessary for area
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                yield points[i], points[j]

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


class NormalEdge:
    def __init__(self, point_a: Point, point_b: Point):
        # Ensure deterministic ordering
        if point_b < point_a:
            point_a, point_b = point_b, point_a

        x1, y1 = point_a[0], point_a[1]
        x2, y2 = point_b[0], point_b[1]

        if x1 == x2:
            # Vertical edge
            self.alignment = "V"
            self.x = x1
            self.y1 = min(y1, y2)
            self.y2 = max(y1, y2)
        elif y1 == y2:
            # Horizontal edge
            self.alignment = "H"
            self.y = y1
            self.x1 = min(x1, x2)
            self.x2 = max(x1, x2)
        else:
            raise ValueError("Expected points to be vertically or horizontally aligned.")


class Rectangle:
    def __init__(self, point_a: Point, point_b: Point) -> None:
        x1, y1 = point_a[0], point_a[1]
        x2, y2 = point_b[0], point_b[1]

        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

    def area(self) -> int:
        return (self.x2 - self.x1 + 1) * (self.y2 - self.y1 + 1)


def build_edges(points: list[Point]) -> list[NormalEdge]:
    edges: list[NormalEdge] = []
    n = len(points)
    for i in range(n):
        a = points[i]
        b = points[(i + 1) % n]
        edges.append(NormalEdge(a, b))
    return edges


def build_compressed_coords(points: list[Point]):
    xs_set = set()
    ys_set = set()

    for p in points:
        x, y = p[0], p[1]
        xs_set.add(x - 1)
        xs_set.add(x)
        xs_set.add(x + 1)
        ys_set.add(y - 1)
        ys_set.add(y)
        ys_set.add(y + 1)

    xs = sorted(xs_set)
    ys = sorted(ys_set)

    x_index = {x: i for i, x in enumerate(xs)}
    y_index = {y: i for i, y in enumerate(ys)}

    return xs, ys, x_index, y_index


def mark_boundary_on_compressed_grid(
    edges: list[NormalEdge],
    xs: list[int],
    ys: list[int],
    x_index: dict[int, int],
    y_index: dict[int, int],
):
    """
    Create a grid marking which compressed cells are on the polygon boundary.
    Grid is boolean [len(xs)][len(ys)].
    """
    W = len(xs)
    H = len(ys)
    boundary = [[False] * H for _ in range(W)]

    for e in edges:
        if e.alignment == "H":
            y = e.y
            iy = y_index[y]
            ix1 = x_index[e.x1]
            ix2 = x_index[e.x2]
            for ix in range(ix1, ix2 + 1):
                boundary[ix][iy] = True
        else:  # Vertical
            x = e.x
            ix = x_index[x]
            iy1 = y_index[e.y1]
            iy2 = y_index[e.y2]
            for iy in range(iy1, iy2 + 1):
                boundary[ix][iy] = True

    return boundary


def flood_outside(boundary, W: int, H: int):
    """
    Flood fill in compressed grid to mark which cells are outside.
    boundary[ix][iy] == True means the cell is part of the polygon boundary.
    Returns a 2D boolean array 'outside'.
    """
    outside = [[False] * H for _ in range(W)]
    q: deque[tuple[int, int]] = deque()

    # We consider the outer border as starting outside locations.
    # We'll start from all boundary cells of the compressed grid that are NOT polygon boundary.
    for ix in range(W):
        for iy in (0, H - 1):
            if not boundary[ix][iy] and not outside[ix][iy]:
                outside[ix][iy] = True
                q.append((ix, iy))
    for iy in range(H):
        for ix in (0, W - 1):
            if not boundary[ix][iy] and not outside[ix][iy]:
                outside[ix][iy] = True
                q.append((ix, iy))

    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while q:
        x, y = q.popleft()
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if not (0 <= nx < W and 0 <= ny < H):
                continue
            if outside[nx][ny]:
                continue
            if boundary[nx][ny]:
                continue
            outside[nx][ny] = True
            q.append((nx, ny))

    return outside


def build_allowed_mask(boundary, outside, W: int, H: int):
    """
    allowed[ix][iy] is True if the cell is either boundary or interior (not outside).
    """
    allowed = [[False] * H for _ in range(W)]
    for ix in range(W):
        for iy in range(H):
            if boundary[ix][iy]:
                allowed[ix][iy] = True
            elif not outside[ix][iy]:
                # interior
                allowed[ix][iy] = True
    return allowed


def rectangle_fully_allowed(
    rect: Rectangle,
    xs: list[int],
    ys: list[int],
    x_index: dict[int, int],
    y_index: dict[int, int],
    allowed,
) -> bool:
    """
    Check if the rectangle is fully within the allowed region, using compressed grid.

    We look at all compressed cells whose coordinates fall within
    [rect.x1 .. rect.x2] x [rect.y1 .. rect.y2] and require all to be allowed.
    """
    # Find compressed index ranges that fall within the rect’s coordinate range.
    # Because xs, ys contain x-1, x, x+1 for each original x, every change
    # of inside/outside status is captured on these integer coordinates.

    # We select indices where xs[ix] is between [x1, x2], similarly for y.
    # This ensures every relevant tile-center position is checked.
    x_indices = [ix for ix, x in enumerate(xs) if rect.x1 <= x <= rect.x2]
    y_indices = [iy for iy, y in enumerate(ys) if rect.y1 <= y <= rect.y2]

    if not x_indices or not y_indices:
        return False

    for ix in x_indices:
        for iy in y_indices:
            if not allowed[ix][iy]:
                return False
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Largest rectangle with red corners and only red/green tiles inside"
    )

    default_file: Path = Path(__file__).parent / "sample_coords.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to coordinate file",
    )

    args = parser.parse_args()

    start: float = time.perf_counter()

    # Read points
    points: list[Point] = []
    with open(file=args.file, mode="r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            coords = [int(d.strip()) for d in line.split(",")]
            points.append(Point(coords))

    # Part 1: largest area rectangle between any two red tiles (no color constraint)
    part_1_calculation: int = 0

    # Build edges from red tiles
    edges = build_edges(points)

    # Coordinate compression
    xs, ys, x_index, y_index = build_compressed_coords(points)
    W, H = len(xs), len(ys)

    # Mark polygon boundary on compressed grid
    boundary = mark_boundary_on_compressed_grid(edges, xs, ys, x_index, y_index)

    # Flood fill outside region
    outside = flood_outside(boundary, W, H)

    # Allowed = boundary + interior
    allowed = build_allowed_mask(boundary, outside, W, H)

    # Pre-map each red point to compressed indices if needed later
    # (we only really need their original coords for area)
    part_2_calculation: int = 0

    # Iterate over all pairs of red points
    for p1, p2 in Point.pairs(points):
        # Their rectangle must be axis-aligned & corners opposite
        rect = Rectangle(p1, p2)
        area = rect.area()

        # Part 1: largest area using any red corners
        if area > part_1_calculation:
            part_1_calculation = area

        # Part 2: rectangle must be fully allowed
        if area > part_2_calculation:
            if rectangle_fully_allowed(rect, xs, ys, x_index, y_index, allowed):
                part_2_calculation = area

    print(f"part_1_calculation: {part_1_calculation}")
    print(f"part_2_calculation: {part_2_calculation}")

    end: float = time.perf_counter()
    print(f"Took {end - start:.6f} seconds")
