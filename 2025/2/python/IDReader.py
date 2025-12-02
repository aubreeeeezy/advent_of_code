import argparse
from pathlib import Path
import time
class IDReader:
    def __init__(self, rangeStr:str) -> None:
        first,last = rangeStr.split('-')
        self.ids = range(int(first), int(last) + 1)

    @staticmethod
    def is_valid_old(id:int) -> bool:
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
        idLen = len( idStr)
        if(idLen % 2) == 0 and idStr[0:(idLen//2)] == idStr[idLen//2:]:
            return False
        return True
    
    @staticmethod
    def is_valid(id:int) -> bool:
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
        idLen = len( idStr)
        for segmentLen in range(1, 1+idLen//2):
            if idLen % segmentLen == 0:
                segment = idStr[:segmentLen]
                if segment * (idLen // segmentLen) == idStr:
                    return False
        return True

    def __repr__(self) -> str:
        return f"{self.ids}"
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dial rotation solver")

    default_file = Path(__file__).parent.parent / "sample_ids.txt"

    parser.add_argument(
        "-f", "--file",
        default=str(default_file),
        help="Path to rotation command file (default: parent directory sample file)"
    )

    args = parser.parse_args()

    part_1_calculation = 0
    part_2_calculation = 0


    with open(args.file, "r") as f:
        start = time.time()
        for line in f:
            for rangeStr in line.split(','):
                reader = IDReader(rangeStr=rangeStr)
                part_1_calculation += sum(id for id in reader.ids if not IDReader.is_valid_old(id))
                part_2_calculation += sum(id for id in reader.ids if not IDReader.is_valid(id))
        end = time.time()
        print(f"part_1_calculation: {part_1_calculation}")
        print(f"part_2_calculation: {part_2_calculation}")
        print(f"Took {end - start:.6f} seconds")    
                