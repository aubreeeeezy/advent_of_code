import argparse
from pathlib import Path
import time

class FoodDatabase:
    def __init__(self, ranges: list[range]) -> None:
        self.ranges = [range(start,stop) for start, stop in FoodDatabase._merge_ranges(ranges)]

    @staticmethod
    def _merge_ranges(ranges: list[range]) -> list[tuple[int, int]]:
        if not ranges:
            return []

        # Convert to (start, stop) and sort
        intervals = sorted(((r.start, r.stop) for r in ranges), key=lambda x: x[0])
        merged: list[tuple[int, int]] = [intervals[0]]

        for start, stop in intervals[1:]:
            last_start, last_stop = merged[-1]
            # Overlapping or touching
            if start <= last_stop:
                merged[-1] = (last_start, max(last_stop, stop))
            else:
                merged.append((start, stop))

        return merged

    def __repr__(self): 
        output = ""
        for range in self.ranges:
            output += f"{range}\n"
        return output
    
    def check_id(self, id ) ->  bool:
        for range in self.ranges:
            if id in range:
                return True
        return False

    def fresh_ids_count(self) -> int:
        """
        Count of distinct IDs covered by all ranges, without materializing them.
        """
        # sum of lengths of merged intervals
        return sum(stop - start for start, stop in ((r.start, r.stop) for r in self.ranges))

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dial rotation solver")

    default_file = Path(__file__).parent.parent / "sample_codes.txt"

    parser.add_argument(
        "-f", "--file",
        default=str(default_file),
        help="Path to rotation command file (default: parent directory sample file)"
    )

    args = parser.parse_args()

    part_1_calculation = 0
    part_2_calculation = 0
    banks: list[FoodDatabase] = []
    start = time.perf_counter()
    ranges:list[range] = []
    food_items:list[int] = []
    
    switched_protocol: bool = False
    with open(file=args.file, mode="r") as f:
        for line in f:
            clean_line: str = line.strip()
            if len(clean_line):
                if switched_protocol: 
                    food_items.append(int(clean_line))
                else: 
                    range_split: list[str] = clean_line.split(sep='-')
                    ranges.append(
                range(
                    int(range_split[0]), 
                    int(range_split[1]) + 1
                        )
                    )
            else: 
                switched_protocol = True
    db = FoodDatabase(ranges)
                
    for food_item in food_items:
        if db.check_id(food_item):
            part_1_calculation += 1
    print(f"part_1_calculation: {part_1_calculation}")
    part_2_calculation = db.fresh_ids_count()
    end = time.perf_counter()


    print(f"part_2_calculation: {part_2_calculation}")
    print(f"Took {end - start:.6f} seconds")    