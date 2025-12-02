from re import Pattern, compile, Match
from typing import Optional
from pathlib import Path
import argparse

ROTATION_COMMAND_RE_COMPILED: Pattern[str] = compile(pattern=r'([LR])(\d+)') #Optimizes Regex Parsing

class Dial:
    def __init__(self) -> None:
        self.position = 50
        pass 

    def _parse_rotation_command_(self, rotation_command) -> tuple[int, int]:
        """
        Parse a rotation command like "L45" or "R1200".

        Returns a tuple (relative_steps, full_rotations) where:
            - relative_steps is the signed remainder of the rotation (−99 to +99),
            - full_rotations is the number of complete 100-step turns.

        Left rotations return negative steps, right rotations return positive steps.

        Raises ValueError if the command is not valid.
        """

        match: Optional[Match[str]] = ROTATION_COMMAND_RE_COMPILED.match(string = rotation_command)
        if match: 
            total_steps = int(match[2])
            relative_steps: int = total_steps % 100
            full_rotations: int = total_steps // 100
            direction = -1 if match[1] == "L" else 1
            return (relative_steps * direction, full_rotations)
        else:
            raise ValueError(f"{rotation_command} is not a valid rotation command")


    def rotate(self, rotation_command : str) -> int:
        """
        Apply a rotation command like "L45" or "R1200" to the dial.

        The dial moves one step per click, wrapping around 0–99.
        This method returns how many times the dial points at 0 during
        this rotation, including any hits at the end of the movement.

        The rotation may include:
        - full 100-step turns (each passes zero once),
        - a remaining partial movement (which may cross or land on zero).

        Parameters
        ----------
        rotation_command : str
            Rotation command starting with 'L' or 'R' followed by digits.

        Returns
        -------
        int
            Number of times the dial pointed at 0 during this rotation.
        """
        relative_steps, times_passed_zero = self._parse_rotation_command_(rotation_command=rotation_command)
        print(f"Rotating {rotation_command}")
        initial_position = self.position
        
        raw_position = initial_position + relative_steps

        self.position = raw_position % 100 # -1 % 100 = 99

        if self.position == 0 and relative_steps: #Position is zero and has moved.
            times_passed_zero += 1 # Click at end.
        elif raw_position not in range(0,100):
            if initial_position == 0 and raw_position < 0: # if we start at 0 and go negative we have not passed zero
                pass
            else: 
                times_passed_zero += 1
        for click in range(times_passed_zero):
            print("*CLICK*")
        print(self)
        return times_passed_zero

    def __repr__(self) -> str:
        return f"Position: {self.position}"
    
    def __eq__(self, other):
        if isinstance(other, Dial):
            return self.position == other.position
        return self.position == other


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Dial rotation solver")

    default_file = Path(__file__).parent.parent / "sample_rotation_commands.txt"

    parser.add_argument(
        "-f", "--file",
        default=str(default_file),
        help="Path to rotation command file (default: parent directory sample file)"
    )

    parser.add_argument(
        "--part1",
        type=int,
        default=989,
        help="Expected Part 1 answer (default: 989)"
    )

    parser.add_argument(
        "--part2",
        type=int,
        default=5941,
        help="Expected Part 2 answer (default: 5941)"
    )

    args = parser.parse_args()

    dial = Dial()
    part_1_calculation = 0
    part_2_calculation = 0

    print(dial)

    with open(args.file, "r") as f:
        for line in f:
            rotation = line.strip()
            times_passed_zero = dial.rotate(rotation_command=rotation)
            part_2_calculation += times_passed_zero

            if dial == 0:
                part_1_calculation += 1

    assert part_1_calculation == args.part1, \
        f"Wrong part_1_calculation: got {part_1_calculation}, expected {args.part1}"

    print(f"part_1_calculation: {part_1_calculation}")

    assert part_2_calculation == args.part2, \
        f"Wrong part_2_calculation: got {part_2_calculation}, expected {args.part2}"

    print(f"part_2_calculation: {part_2_calculation}")