import argparse
from pathlib import Path
import time
import math
from concurrent.futures import ProcessPoolExecutor


class MathProblem:
    """
    Represents a simple arithmetic problem consisting of an operator
    (`+` or `*`) and a list of integer numerals.

    Attributes
    ----------
    MULTIPLICATION_OPERATOR : str
        The multiplication operator symbol ("*").
    ADDITION_OPERATOR : str
        The addition operator symbol ("+").
    VALID_OPERATORS : list[str]
        The set of valid operators for a MathProblem.
    numerals : list[int]
        A list of integers that will be combined using the operator.
    operator : str
        A string representing the operation (+ or *).
    """

    MULTIPLICATION_OPERATOR = "*"
    ADDITION_OPERATOR = "+"
    VALID_OPERATORS: list[str] = [MULTIPLICATION_OPERATOR, ADDITION_OPERATOR]

    def __init__(self, operator, numerals=[]) -> None:
        """
        Initialize a MathProblem instance.

        Parameters
        ----------
        operator : str
            The arithmetic operator ("+" or "*").
        numerals : list[int]
            The list of integers to be used in the computation.
        """
        self.numerals = numerals
        self.operator = operator

    def solve(self) -> int:
        """
        Compute the value of this math problem based on its operator.

        Returns
        -------
        int
            The result of summing or multiplying the numerals.
        """
        if self.operator == "*":
            return math.prod(self.numerals)
        elif self.operator == "+":
            return sum(self.numerals)
        else:
            raise ValueError(
                f"Invalid operator '{self.operator}' expected value in {self.VALID_OPERATORS}"
            )

    def __repr__(self) -> str:
        """Return a readable string representation of the math problem."""
        return f"{self.operator} {' '.join([str(i) for i in self.numerals])}"

    @staticmethod
    def solve_problem(problem) -> int:
        """
        Solve a single MathProblem. Used for parallel processing.

        Parameters
        ----------
        problem : MathProblem
            The math problem to solve.

        Returns
        -------
        int
            Result of the computation.
        """
        return problem.solve()

    @staticmethod
    def solve_problems(problems: list) -> int:
        """
        Solve many MathProblems concurrently using a process pool.

        Parameters
        ----------
        problems : list[MathProblem]
            A list of math problems to compute.

        Returns
        -------
        int
            The sum of the results of all problems.
        """
        solution: int = 0
        with ProcessPoolExecutor() as executor:
            for ans in executor.map(MathProblem.solve_problem, problems):
                solution += ans
        return solution


def get_operator_positions(
    operator_line: str, operators=MathProblem.VALID_OPERATORS
) -> list[int]:
    """
    Return the indices in a string where arithmetic operator characters appear.

    Parameters
    ----------
    operator_line : str
        The line containing operator characters.
    operators : list[str]
        A list of valid operator characters.

    Returns
    -------
    list[int]
        Index positions where operators occur.
    """
    return [i for i in range(len(operator_line)) if operator_line[i] in operators]


def get_problem_chunks(lines: list[str]):
    """
    Split homework text lines into problem chunks based on operator positions.

    Each operator in the final line defines a vertical slice (column interval)
    of the problem.

    Parameters
    ----------
    lines : list[str]
        The full input lines including numerals and the operator line.

    Yields
    ------
    list[str]
        A problem chunk: corresponding vertical slices across all lines.
    """
    operator_indexes: list[int] = get_operator_positions(lines[-1])
    operator_count: int = len(operator_indexes)

    for i, val in enumerate(iterable=operator_indexes):
        if i == operator_count - 1:
            yield [line[val:] for line in lines]
        else:
            next_val: int = operator_indexes[i + 1]
            yield [line[val:next_val] for line in lines]


def get_problem(problem_chunk: list[str]) -> MathProblem:
    """
    Convert a vertical chunk of text into a MathProblem (normal orientation).

    Parameters
    ----------
    problem_chunk : list[str]
        A slice of input lines containing integers followed by an operator.

    Returns
    -------
    MathProblem
        The constructed math problem.
    """
    numerals: list[int] = [int(line.strip()) for line in problem_chunk[0:-1]]
    operator: str = problem_chunk[-1].strip()
    return MathProblem(operator=operator, numerals=numerals)


def get_cephalid_problem(problem_chunk: list[str]) -> MathProblem:
    """
    Convert a text chunk into a MathProblem using "cephalid" column interpretation.

    This version reads numbers vertically: each column forms one numeral.

    Parameters
    ----------
    problem_chunk : list[str]
        The text block representing a vertically-stacked problem.

    Returns
    -------
    MathProblem
        The math problem with column-based numeral extraction.
    """
    width: int = len(problem_chunk[0])
    columns: list[str] = [
        "".join([line[column] for line in problem_chunk[0:-1]])
        for column in range(width)
    ]
    numerals: list[int] = [
        int(column.strip()) for column in columns if len(column.strip())
    ]
    operator: str = problem_chunk[-1].strip()
    return MathProblem(operator=operator, numerals=numerals)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Homework solver")

    default_file = Path(__file__).parent.parent / "sample_homework.txt"

    parser.add_argument(
        "-f",
        "--file",
        default=str(default_file),
        help="Path to instruction file (default: sample_homework.txt)",
    )

    args = parser.parse_args()

    start: float = time.perf_counter()

    with open(file=args.file, mode="r") as f:
        lines: list[str] = f.readlines()

    problems: list[MathProblem] = []
    problems_cepahlid: list[MathProblem] = []

    for problem_chunk in get_problem_chunks(lines=lines):
        problems.append(get_problem(problem_chunk=problem_chunk))
        problems_cepahlid.append(get_cephalid_problem(problem_chunk=problem_chunk))

    part_1_calculation: int = MathProblem.solve_problems(problems=problems)
    print(f"part_1_calculation: {part_1_calculation}")

    part_2_calculation = MathProblem.solve_problems(problems=problems_cepahlid)
    print(f"part_2_calculation: {part_2_calculation}")

    end: float = time.perf_counter()
    print(f"Took {end - start:.6f} seconds")
