from re import Pattern, compile, Match
from typing import Optional

ROTATION_COMMAND_RE_COMPILED: Pattern[str] = compile(pattern=r'([LR])(\d*)') #Optimizes Regex Parsing

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

        match: Optional[Match[str]] = ROTATION_COMMAND_RE_COMPILED.search(string = rotation_command)
        if match: 
            total_steps = int(match[2])
            relative_steps: int = total_steps % 100
            full_rotations: int = total_steps // 100
            if match[1] == "L":
                direction = -1
            else: 
                direction = 1
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
        print(dial)
        return times_passed_zero

    def __repr__(self) -> str:
        return f"Position: {self.position}"
    
    def __eq__(self, other):
        if isinstance(other, Dial):
            return self.position == other.position
        return self.position == other


if __name__ == "__main__":
    path = 'sample_rotation_commands.txt'
    dial = Dial()
    part_1_calculation = 0
    part_2_calculation = 0
    print(dial)
    with open(file=path, mode='r') as f:
        for line in f:
            times_passed_zero = dial.rotate(rotation_command=line.strip()) # Captures number of clicks required for part 2. 
            part_2_calculation += times_passed_zero
            if dial == 0:
                part_1_calculation += 1 # Captures number of times landed on zero required for part 1.

        PART_1_ANSWER = 989
        assert part_1_calculation == PART_1_ANSWER, f"Wrong part_1_calculation got {part_1_calculation} expected {PART_1_ANSWER}"
        print(f"part_1_calculation:{part_1_calculation}")

        PART_2_ANSWER  = 5941
        assert part_2_calculation == PART_2_ANSWER , f"Wrong part_2_calculation got {part_2_calculation} expected {PART_2_ANSWER }"
        print(f"part_2_calculation:{part_2_calculation}")
