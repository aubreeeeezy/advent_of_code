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
        Return all IDs that are invalid under the old rules.

        Uses is_valid_old() to check each ID stored in self.ids.

        Returns
        -------
        list[int]
            A list of IDs that fail the old validation rules.
        """
        idStr = str(id)
        idLen = len( idStr)
        for segmentLen in range(1, 1+idLen//2):
            if idLen % segmentLen == 0:
                if len(set(__class__.tokenize_string(idStr, segmentLen))) == 1: #A little heuristic here. Not sure how optimal this is. 
                    return False
        return True
    
    @staticmethod
    def tokenize_string(s, n):
        """
        Split a string into contiguous chunks of length n and return the unique
        chunks as a set.

        Example:
            tokenize_string("ababab", 2) -> {"ab"}

        Parameters
        ----------
        s : str
            The string to tokenize.
        n : int
            The size of each chunk.

        Returns
        -------
        set[str]
            A set of unique string segments of length n.
        """
        return set([s[i:i+n] for i in range(0, len(s), n)])

    def get_invalid_ids_old(self)  -> list[int]:
        invalid_ids: list[int] = []
        for id in self.ids:
            if __class__.is_valid_old(id):
                pass
            else: 
                invalid_ids.append(id)
        return invalid_ids
    
    def get_invalid_ids(self)  -> list[int]:
        invalid_ids: list[int] = []
        for id in self.ids:
            if __class__.is_valid(id):
                pass
            else: 
                invalid_ids.append(id)
        return invalid_ids


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
                old_invalid_ids = reader.get_invalid_ids_old()
                part_1_calculation += sum(old_invalid_ids)
                invalid_ids = reader.get_invalid_ids()
                part_2_calculation += sum(invalid_ids)
        end = time.time()
        print(f"part_1_calculation: {part_1_calculation}")
        print(f"part_2_calculation: {part_2_calculation}")
        print(f"Took {end - start:.6f} seconds")    
                