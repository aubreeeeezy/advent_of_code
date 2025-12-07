from concurrent.futures import ProcessPoolExecutor
import argparse
from pathlib import Path
import time


class PowerBank:
    """
    PowerBank models a bank of batteries, represented by a sequence of digit 'jolts'.

    Attributes
    ----------
    jolts : list[int]
        The digit sequence representing the battery voltages or positions.
    """

    def __init__(self, jolts: str) -> None:
        """
        Initialize a PowerBank from a string of digits.

        Parameters
        ----------
        jolts : str
            A string of decimal digits, e.g. "123456".
        """
        self.jolts: list[int] = [int(i) for i in jolts]

    def get_positional_reading(self, num_batteries) -> list[int]:
        """
        Compute the positions of `num_batteries` digits to use for a reading.

        This uses an algorithm that scans through self.jolts and, for each
        digit to be selected, advances the position if it finds a larger digit
        that still leaves room to select the remaining digits.

        Parameters
        ----------
        num_batteries : int
            Number of digits to select from the jolts sequence.

        Returns
        -------
        list[int]
            A list of indices into self.jolts representing the chosen positions.
        """
        digit_positions: list[int] = [i for i in range(num_batteries)]
        for curr_digit in range(num_batteries):
            for battery_pos in range(
                digit_positions[curr_digit],
                len(self.jolts) - (num_batteries - curr_digit) + 1,
            ):
                if self.jolts[battery_pos] > self.jolts[digit_positions[curr_digit]]:
                    for later_digit in range(curr_digit, num_batteries):
                        digit_positions[later_digit] = (
                            battery_pos + later_digit - curr_digit
                        )
        return digit_positions

    def get_reading(self, num_batteries) -> int:
        """
        Compute an integer reading by selecting `num_batteries` digits.

        The digits chosen by get_positional_reading() are interpreted as a
        base-10 number in order.

        Parameters
        ----------
        num_batteries : int
            Number of digits to use in the reading.

        Returns
        -------
        int
            The computed reading as an integer.
        """
        reading = 0
        pos_reading = self.get_positional_reading(num_batteries)
        for i in range(num_batteries):
            reading = (reading * 10) + self.jolts[pos_reading[i]]
        return reading

    @staticmethod
    def get_reading_bank(bank) -> tuple[int, int]:
        """
        Compute both the 'old' and 'new' readings for a PowerBank.

        This is designed to be used with ProcessPoolExecutor.map as a static
        function that takes a PowerBank instance and returns a pair of results.

        Parameters
        ----------
        bank : PowerBank
            The PowerBank instance to compute readings for.

        Returns
        -------
        tuple[int, int]
            (reading_old, reading_new) where:
            - reading_old uses 2 batteries,
            - reading_new uses 12 batteries.
        """
        return bank.get_reading(2), bank.get_reading(12)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Dial rotation solver")

    default_file = Path(__file__).parent.parent / "sample_banks.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to rotation command file (default: parent directory sample file)",
    )

    args = parser.parse_args()

    part_1_calculation = 0
    part_2_calculation = 0
    banks: list[PowerBank] = []
    start = time.perf_counter()

    with open(args.file, "r") as f:
        for line in f:
            banks.append(PowerBank(line.strip()))

    with ProcessPoolExecutor() as executor:
        for part1, part2 in executor.map(PowerBank.get_reading_bank, banks):
            print(part1)
            part_1_calculation += part1
            part_2_calculation += part2
    end = time.perf_counter()

    print(f"part_1_calculation: {part_1_calculation}")
    print(f"part_2_calculation: {part_2_calculation}")
    print(f"Took {end - start:.6f} seconds")
