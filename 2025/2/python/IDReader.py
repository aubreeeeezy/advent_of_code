from concurrent.futures import ProcessPoolExecutor
import argparse
from pathlib import Path
import time


class IDReader:
    def __init__(self, rangeStr: str) -> None:
        first, last = rangeStr.split("-")
        self.ids = range(int(first), int(last) + 1)

    @staticmethod
    def is_valid_old(id: int) -> bool:
        """
        Check whether an integer ID is considered valid under the old rules.

        An ID is invalid if:
        - It has an even number of digits, and
        - The first half of the digits is identical to the second half
            (e.g., 1212, 7777, 5050).

        Otherwise, the ID is valid.

        Parameters
        ----------
        id : int
            The numeric ID to check.

        Returns
        -------
        bool
            True if the ID is valid under the old rules, False otherwise.
        """
        idStr = str(id)
        idLen = len(idStr)
        if (idLen % 2) == 0 and idStr[0 : (idLen // 2)] == idStr[idLen // 2 :]:
            return False
        return True

    @staticmethod
    def is_valid(id: int) -> bool:
        """
        Check whether an integer ID is valid under the new rules.

        An ID is invalid if it can be written as one or more repetitions of a
        smaller digit sequence. For example:
        - 1212  (repeats "12")
        - 777777 (repeats "7")
        - 505050 (repeats "50")

        Otherwise, the ID is valid.
        """
        idStr = str(id)
        idLen = len(idStr)
        for segmentLen in range(1, 1 + idLen // 2):
            if idLen % segmentLen == 0:
                segment = idStr[:segmentLen]
                if segment * (idLen // segmentLen) == idStr:
                    return False
        return True

    @staticmethod
    def process_range(reader):
        part1 = 0
        part2 = 0
        for id in reader.ids:
            if not __class__.is_valid_old(id):
                part1 += id
            if not __class__.is_valid(id):
                part2 += id
        return part1, part2

    def __repr__(self) -> str:
        return f"{self.ids}"


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dial rotation solver")

    default_file = Path(__file__).parent.parent / "sample_ids.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to rotation command file (default: parent directory sample file)",
    )

    args = parser.parse_args()

    part_1_calculation = 0
    part_2_calculation = 0
    readers: list[IDReader] = []
    start = time.perf_counter()

    with open(args.file, "r") as f:

        for line in f:
            for rangeStr in line.split(","):
                readers.append(IDReader(rangeStr=rangeStr))
    with ProcessPoolExecutor() as executor:
        for part1, part2 in executor.map(IDReader.process_range, readers):
            part_1_calculation += part1
            part_2_calculation += part2
    end = time.perf_counter()

    print(f"part_1_calculation: {part_1_calculation}")
    print(f"part_2_calculation: {part_2_calculation}")
    print(f"Took {end - start:.6f} seconds")
